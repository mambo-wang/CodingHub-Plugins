#!/usr/bin/env python3
"""Markdown -> WeChat-paste-friendly HTML with inline styles.

WeChat's editor strips <style> blocks and class attributes, so every rule has to
be inline. Layout avoids flex/grid (unreliable after sanitising); tables use
border-collapse + per-cell styles.

Usage:
    python3 wechatify.py <article.md> [more.md ...]
"""
import re
import sys
from pathlib import Path

import markdown

BODY = ("font-family:-apple-system,BlinkMacSystemFont,'PingFang SC',"
        "'Hiragino Sans GB','Microsoft YaHei',sans-serif;"
        "font-size:16px;line-height:1.8;letter-spacing:.4px;color:#3f3f3f;"
        "max-width:677px;margin:0 auto;padding:20px 16px 40px")

S = {
    'h1': "font-size:22px;font-weight:700;color:#0d0d0d;line-height:1.5;"
          "margin:8px 0 26px;letter-spacing:-.2px",
    'h2': "font-size:19px;font-weight:700;color:#0d0d0d;line-height:1.5;"
          "margin:44px 0 22px;padding-left:11px;border-left:4px solid #1f6feb",
    'h3': "font-size:17px;font-weight:700;color:#0d0d0d;margin:30px 0 16px",
    'p': "margin:0 0 20px;line-height:1.8",
    'blockquote': "margin:0 0 24px;padding:14px 18px;background:#f7f8fa;"
                  "border-left:3px solid #c3ccd9;color:#5a6478;font-size:15px;"
                  "line-height:1.8;border-radius:0 6px 6px 0",
    'pre': "margin:0 0 22px;padding:16px 18px;background:#282c34;color:#abb2bf;"
           "border-radius:8px;font-size:13px;line-height:1.68;overflow-x:auto;"
           "font-family:ui-monospace,'SF Mono',Menlo,Consolas,monospace;"
           "white-space:pre-wrap;word-break:break-all",
    'ul': "margin:0 0 20px;padding-left:26px",
    'ol': "margin:0 0 20px;padding-left:26px",
    'li': "margin:0 0 9px;line-height:1.8",
    'hr': "border:0;border-top:1px dashed #dfe3ea;margin:38px 0",
    'table': "border-collapse:collapse;width:100%;margin:0 0 24px;font-size:14.5px",
    'th': "border:1px solid #dfe3ea;padding:9px 11px;background:#f2f5f9;"
          "color:#0d0d0d;font-weight:700;text-align:left;line-height:1.6",
    'td': "border:1px solid #dfe3ea;padding:9px 11px;line-height:1.7;"
          "vertical-align:top;color:#3f3f3f",
    'code': "font-family:ui-monospace,'SF Mono',Menlo,Consolas,monospace;"
            "font-size:13.5px;background:#f2f4f7;color:#b03050;"
            "padding:2px 5px;border-radius:4px;word-break:break-all",
    'strong': "color:#0d0d0d;font-weight:700",
    'em': "color:#6b7689;font-style:normal",
    'img': "max-width:100%;height:auto;display:block;margin:6px auto 10px;"
           "border-radius:8px;border:1px solid #eceff3",
}


def style(html: str) -> str:
    # <pre><code> blocks: the outer <pre> owns the styling, drop inner code tags
    def fix_pre(m):
        inner = re.sub(r'</?code[^>]*>', '', m.group(1))
        return f'<pre style="{S["pre"]}">{inner.strip()}</pre>'
    html = re.sub(r'<pre><code[^>]*>(.*?)</code></pre>', fix_pre, html, flags=re.S)

    for tag, css in S.items():
        if tag == 'pre':
            continue
        # Keep the original attribute group -- dropping it would strip <img src>.
        html = re.sub(rf'<{tag}(?![\w-])((?:\s[^>]*?)?)>',
                      lambda m, t=tag, c=css: '<%s style="%s"%s>' % (t, c, m.group(1)),
                      html)
    # Image-only paragraphs -> centred block with a caption gap below.
    html = re.sub(r'<p style="[^"]*">(\s*<img [^>]*/?>\s*)</p>',
                  r'<section style="text-align:center;margin:0 0 26px">\1</section>',
                  html)
    return html


def convert(src: Path) -> Path:
    text = src.read_text(encoding='utf-8')

    # Pull the H1 out as the article title; keep it in the body but drop its rule.
    body_md = text
    title = re.search(r'^#\s+(.+)$', text, flags=re.M)
    title = title.group(1).strip() if title else src.stem
    body_md = re.sub(r'^#\s+.+$\n+', '', body_md, count=1, flags=re.M)

    inner = markdown.markdown(body_md, extensions=['tables', 'fenced_code', 'sane_lists'])
    inner = style(inner)

    out = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title></head>
<body style="{BODY}">
<section style="{BODY}">
<h1 style="{S['h1']}">{title}</h1>
{inner}
</section>
</body></html>
"""
    dst = src.with_suffix('.wechat.html')
    dst.write_text(out, encoding='utf-8')
    return dst


def resolve(arg: str) -> Path:
    p = Path(arg)
    if p.is_absolute():
        return p
    cand = Path.cwd() / p
    if cand.exists():
        return cand
    return Path(__file__).resolve().parent / p


if __name__ == '__main__':
    if not sys.argv[1:]:
        sys.exit("usage: python3 wechatify.py <article.md> [more.md ...]")
    for arg in sys.argv[1:]:
        p = resolve(arg)
        d = convert(p)
        n = len(re.findall(r'<img ', d.read_text(encoding='utf-8')))
        print(f"{p.name} -> {d.name}  ({d.stat().st_size//1024} KB, {n} images)")
