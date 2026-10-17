"""Shared helpers: every confession/creed quote is pulled verbatim from tools/cci/cci.json
(cached from https://ccifellowship.org), so the site never hand-types confessional text."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, 'tools', 'cci', 'cci.json'), encoding='utf-8'))
BASE = 'https://ccifellowship.org'


def link(url):
    u = url if url.startswith('http') else BASE + url
    return f'<a href="{u}" target="_blank" rel="noopener">ccifellowship.org ↗</a>'


def hc(n):
    x = D['hc'][str(n)]
    a = ''.join(f'<p>{p}</p>' for p in x['a'])
    return (f'<blockquote class="cq" data-src="hc:{n}"><div class="qq">海德堡要理问答 第{n}问（主日{x["ld"]}）：{x["q"]}</div>'
            f'{a}<div class="src">经文：{"；".join(x.get("refs", []))}　· 原文出处 {link(x["url"])}</div></blockquote>')


def bc(n, idx=None):
    x = D['bc'][str(n)]
    ps = x['paras'] if idx is None else [x['paras'][i] for i in idx]
    body = ''.join(f'<p>{p}</p>' for p in ps)
    return (f'<blockquote class="cq" data-src="bc:{n}"><div class="qq">比利时信条 {x["title"]}</div>{body}'
            f'<div class="src">原文出处 {link(x["url"])}</div></blockquote>')


def cd(sec, art):
    x = D['cd'][sec]['arts'][str(art)]
    t = D['cd'][sec]['title']
    body = ''.join(f'<p>{p}</p>' for p in x['paras'])
    return (f'<blockquote class="cq" data-src="cd:{sec}:{art}"><div class="qq">多特信经 {t} · {x["title"]}</div>{body}'
            f'<div class="src">原文出处 {link(x["url"])}</div></blockquote>')


def creed(k):
    return D['creeds'][k]


def page(title, toc, body, extra_btns=''):
    toc_html = ''.join(f'<a href="#{i}" class="{c}">{t}</a>' for i, t, c in toc)
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title>
<meta name="description" content="欧陆改革宗讲章：创世记17章 · 海德堡要理问答主日27 · 主与我们建立爱的关系">
<link rel="stylesheet" href="assets/site.css"></head><body>
<div id="bar"></div>
<header class="top"><button class="btn" id="tocBtn" aria-label="显示或隐藏目录">☰ 目录</button>
<div class="t">📜 {title}</div>
<a class="btn" href="index.html">🕊 讲章</a><a class="btn" href="creeds.html">✝ 三大信经</a>{extra_btns}
<button class="btn" id="themeBtn" aria-label="切换明暗主题">🌓</button></header>
<nav id="toc" aria-label="目录">{toc_html}</nav>
<main>{body}</main>
<footer>信经与信条原文均逐字引自 <a href="https://ccifellowship.org" target="_blank" rel="noopener">ccifellowship.org</a>（构建脚本 tools/build_site.py 直接读取缓存原文，tools/cci/livecheck.py 在线比对）。经文引自和合本。<br>
参考：<a href="https://www.ccreformed.org">恩约教会</a> · <a href="https://www.reformedbeginner.net">改革宗初学者</a> · <a href="https://canrc.org">CanRC</a> · <a href="https://www.urcna.org">URCNA</a> · <a href="https://heritagereformed.com">HRC</a> · <a href="https://www.prca.org">PRCA</a> · <a href="https://opc.org">OPC</a> · <a href="https://canadianreformedseminary.ca">CRTS</a> · <a href="https://www.wts.edu">WTS</a></footer>
<a href="#" id="totop" class="btn" aria-label="回到顶部">⬆</a>
<script src="assets/site.js"></script></body></html>'''


def write(name, html):
    open(os.path.join(ROOT, name), 'w', encoding='utf-8', newline='\n').write(html)
    print('wrote', name, len(html))
