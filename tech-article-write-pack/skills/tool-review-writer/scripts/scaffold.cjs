#!/usr/bin/env node
/* Scaffold a tool-review article: draft outline + evidence ledger + asset dirs. */
const fs = require('fs');
const path = require('path');

const { TRACKS } = require('./tracks.cjs');

function parse(argv) {
  const out = { track: 'a', force: false };
  const args = argv.slice(2);
  if (!args.length) {
    console.log('用法: node scaffold.cjs <slug> --track a|b --out <父目录> [--title 标题] [--force]');
    process.exit(2);
  }
  out.slug = args.shift();
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--track') out.track = args[++i];
    else if (args[i] === '--out') out.out = args[++i];
    else if (args[i] === '--title') out.title = args[++i];
    else if (args[i] === '--force') out.force = true;
  }
  if (!TRACKS[out.track]) throw new Error(`--track 只能是 a 或 b（收到 ${out.track}）`);
  if (!out.out) throw new Error('缺少 --out <父目录>');
  return out;
}

const { slug, track, out: parent, title, force } = parse(process.argv);
const dir = path.join(parent, slug);
const spec = TRACKS[track];
const draftPath = path.join(dir, 'draft.md');

if (fs.existsSync(draftPath) && !force) {
  console.error(`已存在 ${draftPath}（要覆盖加 --force）`);
  process.exit(1);
}

fs.mkdirSync(path.join(dir, 'shots'), { recursive: true });
fs.mkdirSync(path.join(dir, 'diagrams'), { recursive: true });

const fm = [
  '---',
  `title: "${title || `待填：${slug} 评测`}"`,
  'version: "0.1 草稿"',
  `date: "${new Date().toISOString().slice(0, 10)}"`,
  `tool: "${title || slug}"`,
  `track: "${spec.name}"`,
  'status: Draft',
  '---',
  '',
].join('\n');

const body = spec.sections
  .map(([h, hint]) => `## ${h}\n\n> ${hint}\n\n待填。判断句末尾用 [E01] 指向 facts.md。\n`)
  .join('\n---\n\n');

fs.writeFileSync(draftPath, `${fm}# ${title || slug}\n\n${body}`, 'utf8');

fs.writeFileSync(
  path.join(dir, 'facts.md'),
  [
    '# 事实台账',
    '',
    '每条事实一个编号，正文用 [E01] 引用。strength 只有四种：',
    '`measured`（本机跑出来的）· `read-code`（读源码得到的）· `author-claim`（对方 README/官网自称）· `inferred`（推断，正文必须写成推测）。',
    '',
    '## E01',
    '- claim: 一句话结论',
    '- source: `file:<绝对路径>:<起-止行>` 或 `command: <命令> (exit 0)` 或 `url: <链接>`',
    '- observed: 实际看到什么（贴原文，不要转述成形容词）',
    '- strength: measured',
    '',
  ].join('\n'),
  'utf8'
);

console.log(`创建 ${spec.name}`);
console.log(dir);
console.log(`  draft.md   ${spec.sections.length} 节骨架`);
console.log('  facts.md   台账模板');
console.log('  shots/     CLI 实操取证');
console.log('  diagrams/  架构图与流程图');
