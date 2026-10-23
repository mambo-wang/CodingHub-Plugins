#!/usr/bin/env node
/**
 * Lint a review draft: structure, image refs, evidence ledger, claim strength,
 * and optional public-account (wechat) layout limits.
 *
 *   node lint_article.cjs <draft.md> [--track a|b] [--facts <facts.md>] [--wechat]
 *
 * Exit 0 = clean or warnings only. Exit 1 = at least one FAIL.
 */
'use strict';

const fs = require('fs');
const path = require('path');
const { TRACKS, detectTrack } = require('./tracks.cjs');

const STRENGTHS = new Set(['measured', 'read-code', 'author-claim', 'inferred']);
const HEDGE = /声称|自称|标称|号称|README|官方文档|文档里写|文档说|按它的说法|作者自述|官网写/;
const STRONG =
  /最快|最好|最强|最省|完全|彻底|从不|永不|100%|无一例外|所有|全部|必然|一定能|稳定可靠|无缝|显著|大幅|质的飞跃|颠覆|开箱即用无脑|零成本/;
const METRIC =
  /\d+(?:\.\d+)?\s*(?:%|倍|ms|s|秒|分钟|小时|行|个|条|篇|次|万|MB|GB|KiB|MiB|tokens|字)|\d+\s*(?:核|路|并发)/;

function parse(argv) {
  const o = { wechat: false, facts: null, track: null };
  const args = argv.slice(2);
  if (!args.length || args[0].startsWith('--')) {
    console.log('用法: node lint_article.cjs <draft.md> [--track a|b] [--facts facts.md] [--wechat]');
    process.exit(2);
  }
  o.md = args.shift();
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--facts') o.facts = args[++i];
    else if (args[i] === '--track') o.track = args[++i];
    else if (args[i] === '--wechat') o.wechat = true;
    else throw new Error(`未知参数 ${args[i]}`);
  }
  if (o.track && !TRACKS[o.track]) throw new Error('--track 只能是 a 或 b');
  return o;
}

const stripInline = (s) =>
  s
    .replace(/!\[[^\]]*\]\([^)]*\)/g, '')
    .replace(/\[([^\]]*)\]\([^)]*\)/g, '$1')
    .replace(/`[^`]*`/g, '');

function readFacts(file) {
  const facts = new Map();
  if (!fs.existsSync(file)) return { facts, error: `台账不存在：${file}` };
  const lines = fs.readFileSync(file, 'utf8').split(/\r?\n/);
  let cur = null;
  lines.forEach((line, i) => {
    const id = line.match(/^##\s+(E\d+)\s*$/);
    if (id) {
      cur = { id: id[1], line: i + 1, fields: {} };
      facts.set(cur.id, cur);
      return;
    }
    if (/^##\s/.test(line)) {
      cur = null;
      return;
    }
    const f = cur && line.match(/^-\s*(claim|source|observed|strength)\s*[:：]\s*(.*)$/);
    if (f) cur.fields[f[1]] = f[2].trim();
  });
  return { facts, error: null };
}

function main() {
  const o = parse(process.argv);
  const mdPath = path.resolve(o.md);
  const base = path.dirname(mdPath);
  const src = fs.readFileSync(mdPath, 'utf8');
  const lines = src.split(/\r?\n/);
  const rel = (n) => `${path.basename(mdPath)}:${n}`;
  const fails = [];
  const warns = [];
  const push = (arr, line, msg) => arr.push(`${rel(line)} ${msg}`);

  const fence = [];
  let open = null;
  lines.forEach((l, i) => {
    const t = l.match(/^\s*(```|~~~)/);
    if (!open && t) open = { mark: t[1], start: i };
    else if (open && new RegExp(`^\\s*${open.mark}`).test(l)) {
      fence.push([open.start + 1, i + 1]);
      open = null;
    }
  });
  const inFence = (n) => fence.some(([a, b]) => n >= a && n <= b);

  const headings = [];
  lines.forEach((l, i) => {
    const h = l.match(/^##\s+(.+)$/);
    if (h && !inFence(i + 1)) headings.push({ title: h[1].trim(), line: i + 1 });
  });

  // 1. structure
  const track = o.track || detectTrack(headings.map((h) => h.title));
  const spec = TRACKS[track];
  for (const [title] of spec.sections) {
    const want = title.replace(/^\d+\.\s*/, '');
    if (!headings.some((h) => h.title.includes(want)))
      fails.push(`${path.basename(mdPath)} [${spec.name}] 缺章节「${title}」`);
  }

  // 2. ledger
  const factsFile = o.facts ? path.resolve(o.facts) : path.join(base, 'facts.md');
  const { facts, error } = readFacts(factsFile);
  if (error) fails.push(error);
  const cited = new Set();

  const prose = [];
  lines.forEach((l, i) => {
    const n = i + 1;
    if (inFence(n) || /^\s*[>#|]/.test(l) || !l.trim()) return;
    prose.push({ line: l, n });
  });

  for (const { line, n } of prose) {
    for (const m of line.matchAll(/\[(E\d{2,})\]/g)) cited.add(m[1]);
    const bare = stripInline(line);
    const judged = STRONG.test(bare) || METRIC.test(bare);
    if (judged && !/\[E\d{2,}\]/.test(line)) {
      if (STRONG.test(bare))
        push(warns, n, `判断句没有挂 [E##]：${bare.trim().slice(0, 46)}`);
      else push(warns, n, `带数字但没有 [E##]：${bare.trim().slice(0, 46)}`);
    }
    for (const m of line.matchAll(/!\[([^\]]*)\]\(([^)]+)\)/g)) {
      const target = m[2].split(/\s+/)[0];
      if (/^https?:/.test(target)) continue;
      const p = path.resolve(base, target);
      if (!fs.existsSync(p)) push(fails, n, `图片不存在：${target}`);
      else if (p.endsWith('.html')) push(fails, n, `正文要引 PNG，不是 HTML：${target}`);
      if (!m[1].trim()) push(fails, n, '图片缺少 alt 文本');
    }
  }

  for (const id of cited) {
    if (!facts.has(id)) push(fails, lines.findIndex((l) => l.includes(`[${id}]`)) + 1, `台账里没有 ${id}`);
  }
  for (const [id, f] of facts) {
    const missing = ['claim', 'source', 'observed', 'strength'].filter((k) => !f.fields[k]);
    if (missing.length)
      fails.push(`facts.md:${f.line} ${id} 缺字段 ${missing.join('、')}`);
    else if (!STRENGTHS.has(f.fields.strength))
      fails.push(`facts.md:${f.line} ${id} strength 非法：${f.fields.strength}`);
    else if (f.fields.strength === 'inferred' && !/可能|大概|推测|估计|尚未|不确定/.test(f.fields.claim))
      warns.push(`facts.md:${f.line} ${id} 是 inferred，正文必须写成推测语气`);
    if (f.fields.strength === 'author-claim' && cited.has(id)) {
      const users = prose.filter((p) => p.line.includes(`[${id}]`));
      const unhedged = users.filter((p) => !HEDGE.test(p.line));
      for (const u of unhedged)
        push(warns, u.n, `[${id}] 是 author-claim，这句话没写「声称/README 说」之类归因`);
    }
    if (!cited.has(id) && f.fields.claim && !/^一句话结论$/.test(f.fields.claim))
      warns.push(`facts.md:${f.line} ${id} 正文里没引用（删掉或在用到时挂上）`);
  }

  // 3. leftovers
  lines.forEach((l, i) => {
    const n = i + 1;
    if (inFence(n)) return;
    if (/待填。|TODO:|\[To be written\]/.test(l)) push(fails, n, '仍有占位内容');
  });

  // 4. wechat layout limits
  if (o.wechat) {
    fence.forEach(([a, b]) => {
      for (let n = a + 1; n < b; n++) {
        const w = [...lines[n - 1]].length;
        if (w > 48) warns.push(`${rel(n)} 代码行 ${w} 字符，手机上会折行（≤48）`);
      }
    });
    let prevCols = 0;
    lines.forEach((l, i) => {
      const n = i + 1;
      if (inFence(n) || !/^\s*\|/.test(l)) {
        prevCols = 0;
        return;
      }
      if (/^\s*\|[\s:-]+\|/.test(l)) return;
      const cols = l.split(/(?<!\\)\|/).filter((c) => c.trim() !== '').length;
      if (cols > 4 && cols !== prevCols)
        warns.push(`${rel(n)} 表格 ${cols} 列，手机上放不下（≤4）`);
      prevCols = cols;
    });
  }

  console.log(`track=${track}（${spec.name}）  章节 ${headings.length}  台账 ${facts.size}  引用 ${cited.size}`);
  for (const f of fails) console.log(`FAIL  ${f}`);
  for (const w of warns) console.log(`WARN  ${w}`);
  console.log(`${fails.length} FAIL, ${warns.length} WARN`);
  process.exit(fails.length ? 1 : 0);
}

try {
  main();
} catch (e) {
  console.error(String(e.message || e));
  process.exit(2);
}
