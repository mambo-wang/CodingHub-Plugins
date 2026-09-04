#!/usr/bin/env node
/**
 * codebuddy-hook.js — CodeBuddy 钩子适配器（ponytail-caveman-pack）
 *
 * 上游 ponytail / caveman 的钩子脚本按 Claude Code（以及 Copilot / Codex）的
 * 约定输出：SessionStart 时向 stdout 输出纯文本规则、或输出带 hookSpecificOutput 的
 * JSON。CodeBuddy 的统一契约是：
 *
 *   { "continue": true,
 *     "hookSpecificOutput": { "hookEventName": "<Event>", "additionalContext": "<text>" } }
 *
 * 本适配器负责：
 *   1. 读取 stdin 上的钩子负载（JSON），归一化 prompt 字段形态；
 *   2. 用子进程运行对应的上游脚本（同一 Node），透传负载并注入
 *      CLAUDE_PLUGIN_ROOT / CLAUDE_CONFIG_DIR（隔离到 ~/.codebuddy）；
 *   3. 把上游 stdout 归一化为 CodeBuddy 契约 JSON：
 *      - 纯文本  -> hookSpecificOutput.additionalContext（SessionStart / UserPromptSubmit）
 *      - 已是 JSON -> 补 continue:true、补齐 hookEventName、剥离 statusline 提示块；
 *   4. 超时兜底（8s）与 stdin 兜底（1.5s），保证钩子不阻塞会话。
 *
 * 用法：node codebuddy-hook.js <EventName> <relative/path/to/script.js>
 * 事件：SessionStart | UserPromptSubmit | SubagentStart
 */
'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawn } = require('child_process');

const eventName = process.argv[2];
const relScript = process.argv[3];

const hookDir = __dirname;                  // <plugin>/hooks
const pluginRoot = path.dirname(hookDir);   // <plugin>
const scriptPath = relScript ? path.resolve(hookDir, relScript) : '';

const STATUSLINE_MARK = '\n\nSTATUSLINE SETUP NEEDED:';
const CHILD_TIMEOUT_MS = 8000;
const STDIN_FALLBACK_MS = 1500;

function emitJson(obj) {
  process.stdout.write(JSON.stringify(obj));
}

/** 去掉上游附加的 “STATUSLINE SETUP NEEDED: …”（CodeBuddy 无 Claude 状态栏，属于噪音）。 */
function stripStatusline(text) {
  const idx = text.indexOf(STATUSLINE_MARK);
  if (idx !== -1) text = text.slice(0, idx);
  return text.replace(/[\s\uFEFF]+$/, '');
}

/**
 * 归一化输出并打印。
 * base 形如 { continue: true }。
 */
function emit(base, raw) {
  const text = String(raw || '').replace(/^\uFEFF/, '').trim();
  if (!text || text === 'OK') { emitJson(Object.assign({}, base)); return; }

  if (text.startsWith('{')) {
    try {
      const parsed = JSON.parse(text);
      const out = Object.assign({}, base, parsed);
      if (typeof out.continue !== 'boolean') out.continue = true;

      const hso = out.hookSpecificOutput;
      if (hso && typeof hso === 'object') {
        hso.hookEventName = eventName;
        if (typeof hso.additionalContext === 'string') {
          hso.additionalContext = stripStatusline(hso.additionalContext);
        }
      } else if (typeof out.additionalContext === 'string') {
        out.hookSpecificOutput = {
          hookEventName: eventName,
          additionalContext: stripStatusline(out.additionalContext)
        };
        delete out.additionalContext;
      }
      emitJson(out);
      return;
    } catch (e) { /* 非 JSON 纯文本，按下方逻辑包装 */ }
  }

  const context = stripStatusline(text);
  if (!context) { emitJson(Object.assign({}, base)); return; }
  emitJson(Object.assign({}, base, {
    hookSpecificOutput: { hookEventName: eventName, additionalContext: context }
  }));
}

/** 运行上游脚本并归一化输出。 */
function run(payload) {
  if (!eventName || !scriptPath || !fs.existsSync(scriptPath)) {
    emitJson({ continue: true });
    return;
  }

  const env = Object.assign({}, process.env, {
    CLAUDE_PLUGIN_ROOT: pluginRoot
  });
  if (!process.env.CLAUDE_CONFIG_DIR) {
    // 模式状态、nudge 标记等落到 ~/.codebuddy，避免污染 ~/.claude
    env.CLAUDE_CONFIG_DIR = path.join(os.homedir(), '.codebuddy');
  }

  // 负载归一化：不同宿主会把 prompt 传成字符串 / {content} / user_prompt；
  // SubagentStart 的代理名可能在 agent.name。尽量转成上游脚本认识的形态。
  if (payload) {
    try {
      const data = JSON.parse(payload);
      let changed = false;
      let p = data.prompt;
      if (p && typeof p === 'object' && !Array.isArray(p)) { p = p.content; changed = true; }
      if (typeof p !== 'string') { p = data.user_prompt; }
      if (typeof p === 'string') { data.prompt = p; changed = true; }
      if (!data.agent_type && data.agent && typeof data.agent === 'object' && typeof data.agent.name === 'string') {
        data.agent_type = data.agent.name;
        changed = true;
      }
      if (changed) payload = JSON.stringify(data);
    } catch (e) { /* 保留原始 payload */ }
  }

  const child = spawn(process.execPath, [scriptPath], {
    env: env,
    stdio: ['pipe', 'pipe', 'pipe']
  });

  const MAX_OUT = 256 * 1024;
  let stdout = '';
  let stderr = '';
  let settled = false;

  child.stdout.on('data', (d) => { if (stdout.length < MAX_OUT) stdout += d; });
  child.stderr.on('data', (d) => { if (stderr.length < 64 * 1024) stderr += d; });

  const killTimer = setTimeout(() => {
    try { child.kill(); } catch (e) { /* ignore */ }
  }, CHILD_TIMEOUT_MS);

  child.on('error', () => {
    clearTimeout(killTimer);
    if (settled) return;
    settled = true;
    emitJson({ continue: true });
  });

  child.on('close', () => {
    clearTimeout(killTimer);
    if (settled) return;
    settled = true;
    emit({ continue: true }, stdout);
  });

  try {
    if (payload) child.stdin.write(payload);
    child.stdin.end();
  } catch (e) { /* ignore */ }
}

// —— 读 stdin（兜底计时防止管道永不关闭） ——
let input = '';
let started = false;
function go() {
  if (started) return;
  started = true;
  run(input.trim());
}
process.stdin.setEncoding('utf8');
process.stdin.on('data', (c) => { input += c; });
process.stdin.on('end', go);
process.stdin.on('error', go);
setTimeout(go, STDIN_FALLBACK_MS).unref();
