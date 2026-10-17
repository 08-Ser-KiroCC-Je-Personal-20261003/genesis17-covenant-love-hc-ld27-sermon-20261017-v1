# 将实时抓取的页面与 cci.json 逐字比对（先运行 fetch.py 抓取下列页面）
import json, re, os, io, sys, html as H
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
D = os.path.dirname(os.path.abspath(__file__))
def content(h):
    i = h.find('id="block-tulip-content"'); j = h.find('<nav role="navigation"', i)
    return h[i:j if j > 0 else len(h)]
def clean(s):
    s = re.sub(r'<sup[^>]*>', '\x01', s); s = s.replace('</sup>', '\x02')
    s = re.sub(r'(?i)<br\s*/?>', '\n', s); s = re.sub(r'<[^>]+>', '', s)
    s = H.unescape(s).replace('\xa0', ' ').strip()
    return s.replace('\x01', '<sup>').replace('\x02', '</sup>')
def paras(c): return [clean(p) for p in re.findall(r'<p[^>]*>(.*?)</p>', c, re.S) if clean(p)]
def P(f): return paras(content(open(os.path.join(D, f + '.html'), encoding='utf-8').read()))
d = json.load(open(os.path.join(D, 'cci.json'), encoding='utf-8')); b = 'books__book-of-praise__'
for n in ['15', '33', '34']:
    print('BC', n, P(b + 'confessions__the-belgic-confession__' + n) == d['bc'][n]['paras'])
print('CD1.17', P(b + 'confessions__canons-of-dort__section1__17') == d['cd']['section1']['arts']['17']['paras'])
c = P(b + 'confessions__heidelberg-catechism__section2__part5__lord-day-27')
print('HC LD27', all(a in c for n in ['72', '73', '74'] for a in d['hc'][n]['a']))
for k, s in [('apos', 'apostles-creed'), ('nic', 'nicene-creed'), ('ath', 'athanasian-creed')]:
    print(k, P(b + 'creeds__' + s)[1:] == d['creeds'][k]['body'])
