#!/usr/bin/env node
/**
 * Run one real command, keep the raw transcript, and render it as a terminal
 * card HTML that html2png.py can turn into a screenshot.
 *
 *   node capture_cli.cjs <label> --out <shotsDir> [--id 03] [--cwd <dir>]
 *        [--timeout 120000] [--max-lines 90] [--python python] [--png] -- <command>
 */
'use strict';

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const ANSI = /[\u001B\u009B][[\]()#;?]*(?:\d{1,4}(?:;\d{1,4})*)?[\dA-PR-TZcf-nq-uy=><~]/g;

function parse(argv) {
  const dash = argv.indexOf('--');
  if (dash === -1) throw new Error('缺少 `-- <命令>`，例如 -- node -v');
  const opts = {
    id: null,
    cwd: process.cwd(),
    timeout: 120_000,
    maxLines: 90,
    png: false,
    python: 'python',
    encoding: 'auto',
    out: null,
    label: null,
    cmd: argv.slice(dash + 1).join(' ').trim(),
  };
  const head = argv.slice(0, dash);
  if (head.length === 0) throw new Error('缺少 <label>（这张截图讲什么）');
  opts.label = head.shift();
  for (let i = 0; i < head.length; i++) {
    const k = head[i];
    const next = () => {
      if (i + 1 >= head.length) throw new Error(`${k} 缺少参数`);
      return head[++i];
    };
    if (k === '--id') opts.id = next();
    else if (k === '--out') opts.out = next();
    else if (k === '--cwd') opts.cwd = next();
    else if (k === '--timeout') opts.timeout = Number(next());
    else if (k === '--max-lines') opts.maxLines = Number(next());
    else if (k === '--python') opts.python = next();
    else if (k === '--encoding') opts.encoding = next();
    else if (k === '--png') opts.png = true;
    else throw new Error(`未知参数 ${k}`);
  }
  if (!opts.cmd) throw new Error('`--` 之后是空命令');
  if (!opts.out) throw new Error('缺少 --out <shots 目录>');
  return opts;
}

const slug = (s) =>
  s
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 48);

const esc = (s) =>
  s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

// Piped child stdout on zh-CN Windows is cp936, not UTF-8: strict-utf8 first,
// then fall back so Chinese CLI output does not become mojibake in the shot.
function decode(buf, forced) {
  if (!buf || buf.length === 0) return { text: '', codec: 'none' };
  if (forced && forced !== 'auto') {
    return { text: new TextDecoder(forced).decode(buf), codec: forced };
  }
  try {
    return { text: new TextDecoder('utf-8', { fatal: true }).decode(buf), codec: 'utf-8' };
  } catch {
    return { text: new TextDecoder('gbk').decode(buf), codec: 'gbk' };
  }
}

function clip(lines, max) {
  if (lines.length <= max) return { body: lines, omitted: 0 };
  const head = Math.ceil(max * 0.6);
  const tail = max - head;
  return {
    body: [
      ...lines.slice(0, head),
      `… 省略 ${lines.length - max} 行，完整输出见同名 .txt …`,
      ...lines.slice(-tail),
    ],
    omitted: lines.length - max,
  };
}

function card({ label, cmd, body, code, signal, ms, key }) {
  const mono = "'Cascadia Mono','JetBrains Mono',Consolas,'Noto Sans Mono','Courier New',monospace";
  const sans = "'Noto Sans SC','PingFang SC','Microsoft YaHei',system-ui,sans-serif";
  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>${esc(label)}</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: #f5f5f5; padding: 28px; font-family: ${sans}; }
  .shot-card { width: 1000px; background: #ffffff; border: 1px solid rgba(45,49,66,0.35);
               border-radius: 6px; overflow: hidden; }
  .bar { display: flex; align-items: center; gap: 10px; padding: 10px 16px;
         background: #2d3142; color: #f5f5f5; }
  .dots { display: flex; gap: 6px; }
  .dots i { width: 10px; height: 10px; border-radius: 50%; background: rgba(245,245,245,0.35); }
  .bar .title { font-size: 12px; font-weight: 500; letter-spacing: 0.02em; }
  .bar .id { margin-left: auto; font-family: ${mono}; font-size: 10px;
             color: rgba(245,245,245,0.6); }
  pre { padding: 16px 18px; font-family: ${mono}; font-size: 12.5px; line-height: 1.62;
        color: #2d3142; background: #ffffff; white-space: pre-wrap; word-break: break-all;
        max-width: 100%; }
  .cmd { color: #bf4520; }
  .prompt { color: #4f5d75; user-select: none; }
  .foot { padding: 9px 18px; border-top: 1px solid rgba(45,49,66,0.12);
          font-family: ${mono}; font-size: 10.5px; color: #4f5d75; background: #fafafa; }
  .zero { color: #2f7d4f; } .nonzero { color: #bf4520; }
</style>
</head>
<body>
<div class="shot-card">
  <div class="bar">
    <span class="dots"><i></i><i></i><i></i></span>
    <span class="title">${esc(label)}</span>
    <span class="id">${esc(key)}</span>
  </div>
  <pre><span class="cmd"><span class="prompt">$ </span>${esc(cmd)}</span>
${body.map((l) => esc(l) || '&nbsp;').join('\n')}</pre>
  <div class="foot">exit <span class="${code === 0 ? 'zero' : 'nonzero'}">${code}${
    signal ? ' · signal ' + esc(signal) : ''
  }</span> · ${(ms / 1000).toFixed(1)}s${
    body.some((l) => l.startsWith('… 省略')) ? ` · 输出已截断` : ''
  }</div>
</div>
</body>
</html>
`;
}

function main() {
  const o = parse(process.argv.slice(2));
  const dir = path.resolve(o.out);
  fs.mkdirSync(dir, { recursive: true });

  const started = Date.now();
  const r = spawnSync(o.cmd, {
    shell: true,
    cwd: o.cwd,
    timeout: o.timeout,
    maxBuffer: 64 * 1024 * 1024,
    encoding: 'buffer',
  });
  const ms = Date.now() - started;

  if (r.error && r.status === null) {
    console.error(`命令未能启动：${r.error.message}`);
    process.exit(2);
  }

  const so = decode(r.stdout, o.encoding);
  const se = decode(r.stderr, o.encoding);
  const codec =
    [...new Set([so, se].filter((x) => x.codec !== 'none').map((x) => x.codec))].join('+') ||
    'utf-8';
  const raw = `${so.text}${se.text}`.replace(/\r/g, '');
  const clean = raw.replace(ANSI, '');
  const allLines = clean.split('\n');
  if (allLines.length > 1 && allLines[allLines.length - 1] === '') allLines.pop();
  const clipped = clip(allLines, o.maxLines);
  const code = r.status === null ? -1 : r.status;
  const key = slug(o.label) || slug(o.cmd) || 'shot';
  const base = `${o.id ? o.id + '-' : ''}${key}`;

  const txt = path.join(dir, `${base}.txt`);
  fs.writeFileSync(
    txt,
    [`$ ${o.cmd}`, `# cwd: ${o.cwd}`, `# exit: ${code}  duration_ms: ${ms}  codec: ${codec}`, '', clean].join('\n'),
    'utf8',
  );

  const html = path.join(dir, `${base}.html`);
  fs.writeFileSync(
    html,
    card({
      label: o.label,
      cmd: o.cmd,
      code,
      signal: r.signal,
      ms,
      key: o.id ? `${o.id} · ${key}` : key,
      body: clipped.body,
    }),
    'utf8',
  );

  const head = clipped.body.slice(0, 4).join('\n');
  console.log(
    [
      `exit=${code}  ${ms}ms  codec=${codec}  输出 ${allLines.length} 行${clipped.omitted ? `（图内省略 ${clipped.omitted} 行，全文见 .txt）` : ''}`,
      `txt  ${txt}`,
      `html ${html}`,
      head ? '--- 开头 ---\n' + head : '（无输出）',
    ].join('\n'),
  );

  if (o.png) {
    const png = path.join(dir, `${base}.png`);
    const py = spawnSync(o.python, [path.join(__dirname, 'html2png.py'), html, png, '2'], {
      encoding: 'utf8',
      shell: true,
      env: { ...process.env, PYTHONIOENCODING: 'utf-8' },
    });
    const outLine = `${py.stdout || ''}${py.stderr || ''}`.trim();
    if (py.status !== 0) {
      console.error(`png 失败（exit ${py.status}）：\n${outLine}`);
      process.exit(3);
    }
    console.log(`png  ${png}\n     ${outLine}`);
  }
}

try {
  main();
} catch (e) {
  console.error(String(e.message || e));
  process.exit(1);
}
