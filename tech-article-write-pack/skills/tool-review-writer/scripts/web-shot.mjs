// Web UI 截图驱动：headless Chrome + CDP，导航、可选注入会话 cookie、可选执行 JS（点页签/按钮/滚动）、截图。
// 绕开「应用内浏览器无视口」的死路：自带 --user-data-dir 与调试端口，视口由 Emulation 指定。
//
// usage: node web-shot.mjs <url> <out.png> [waitMs]
// env:
//   SHOT_SESS         会话 cookie 值（可选；目标 UI 需要登录时才设）。取法：先 curl 登录接口
//                     -c cookies.txt，再从 cookies.txt 读会话 cookie。
//                     密码由用户当次提供，不落盘、不进记忆（项目记忆有明确授权的除外）。
//   SHOT_COOKIE_NAME  cookie 名，设了 SHOT_SESS 时必填
//   SHOT_ORIGIN       cookie domain，默认 localhost
//   SHOT_EVAL         加载后执行的 JS（awaitPromise:true，可写 async 串起「点页签→等→点按钮→等→滚动」）
//   SHOT_EVAL_WAIT    eval 之后等待毫秒，默认 2500
//   SHOT_CLIP         只截该 CSS 选择器对应的元素（如 ".ant-drawer-body"），默认整视口
//   SHOT_PORT         Chrome 调试端口，默认 9333
//   SHOT_W / SHOT_H   视口，默认 1440x900（deviceScaleFactor 固定 2）
//   CHROME            Chrome 二进制路径覆盖
//
// 点击选择器经验（antd 系 UI 通用）：页签用 `.ant-tabs-tab` 按文本匹配；按钮/链接用 `button,a`
// 按文本匹配且要求 offsetParent 非空；宽泛的 `div,span` 文本匹配会命中外层容器（如 .ant-card-extra）
// 而点不动。抽屉/弹窗正文在 `.ant-drawer-body` / `.ant-modal-body`，滚动容器通常是它。
// 返回值会打印为 EVAL>，用来确认点没点中，别盲截。

import { writeFileSync } from 'node:fs';
import { spawn } from 'node:child_process';

const [url, out, waitArg] = process.argv.slice(2);
if (!url || !out) {
  console.error('usage: node web-shot.mjs <url> <out.png> [waitMs]');
  process.exit(2);
}
if (process.env.SHOT_SESS && !process.env.SHOT_COOKIE_NAME) {
  console.error('SHOT_COOKIE_NAME is required when SHOT_SESS is set');
  process.exit(2);
}

const waitMs = parseInt(waitArg || '4000', 10);
const CHROME = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PORT = process.env.SHOT_PORT || '9333';
const W = parseInt(process.env.SHOT_W || '1440', 10);
const H = parseInt(process.env.SHOT_H || '900', 10);

const chrome = spawn(CHROME, [
  '--headless=new', '--disable-gpu', '--hide-scrollbars',
  '--no-first-run', '--no-default-browser-check',
  `--user-data-dir=/tmp/console-shot-profile-${PORT}`,
  `--remote-debugging-port=${PORT}`,
  `--window-size=${W},${H}`,
  'about:blank',
], { stdio: ['ignore', 'pipe', 'pipe'] });

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function targets() {
  for (let i = 0; i < 40; i++) {
    try {
      const r = await fetch(`http://127.0.0.1:${PORT}/json/list`);
      const t = await r.json();
      if (t.length) return t;
    } catch {}
    await sleep(250);
  }
  throw new Error('chrome debug port never came up');
}

let nextId = 1;
function cdp(ws) {
  const pending = new Map();
  ws.addEventListener('message', (ev) => {
    const m = JSON.parse(ev.data);
    if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); }
  });
  return (method, params = {}) => new Promise((res, rej) => {
    const id = nextId++;
    pending.set(id, (m) => (m.error ? rej(new Error(JSON.stringify(m.error))) : res(m.result)));
    ws.send(JSON.stringify({ id, method, params }));
  });
}

const list = await targets();
const page = list.find((t) => t.type === 'page');
const ws = new WebSocket(page.webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener('open', r, { once: true }));
const send = cdp(ws);

await send('Network.enable');
if (process.env.SHOT_SESS) {
  await send('Network.setCookie', {
    name: process.env.SHOT_COOKIE_NAME,
    value: process.env.SHOT_SESS,
    domain: process.env.SHOT_ORIGIN || 'localhost',
    path: '/',
    httpOnly: true,
  });
}
await send('Page.enable');
await send('Emulation.setDeviceMetricsOverride', { width: W, height: H, deviceScaleFactor: 2, mobile: false });
await send('Page.navigate', { url });
await sleep(waitMs);

if (process.env.SHOT_EVAL) {
  const r = await send('Runtime.evaluate', {
    expression: process.env.SHOT_EVAL, awaitPromise: true, returnByValue: true,
  });
  console.log('EVAL>', JSON.stringify(r.result && r.result.value));
  await sleep(parseInt(process.env.SHOT_EVAL_WAIT || '2500', 10));
}

const shotParams = { format: 'png' };
if (process.env.SHOT_CLIP) {
  const r = await send('Runtime.evaluate', {
    expression: `(()=>{const e=document.querySelector(${JSON.stringify(process.env.SHOT_CLIP)});
      if(!e) return null; const b=e.getBoundingClientRect();
      return JSON.stringify({x:b.x,y:b.y,width:b.width,height:b.height});})()`,
    returnByValue: true,
  });
  const v = r.result && r.result.value;
  if (!v) throw new Error('SHOT_CLIP matched no element: ' + process.env.SHOT_CLIP);
  const b = JSON.parse(v);
  // 元素高于视口时先滚到顶部，配合 captureBeyondViewport 截全
  await send('Runtime.evaluate', { expression: 'window.scrollTo(0,0)' });
  await sleep(300);
  shotParams.clip = { x: Math.floor(b.x), y: Math.floor(b.y), width: Math.ceil(b.width), height: Math.ceil(b.height), scale: 1 };
  shotParams.captureBeyondViewport = true;
  console.log('CLIP>', JSON.stringify(shotParams.clip));
}

const { data } = await send('Page.captureScreenshot', shotParams);
writeFileSync(out, Buffer.from(data, 'base64'));
console.log('saved', out);
ws.close();
chrome.kill('SIGTERM');
process.exit(0);
