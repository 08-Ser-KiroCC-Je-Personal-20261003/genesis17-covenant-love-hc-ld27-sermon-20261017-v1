# 引文与内容校验：CCI 原文逐字、经文逐字、背诵分行、孤儿/近似引文、data.js 格式、CITED 覆盖、内容禁则、CSS 溢出规则
# 用法：python tools/cci/verify.py [--strict] [site_dir]
import html, io, json, os, re, sys
from html.parser import HTMLParser

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
from build_cci import render  # noqa: E402

PAGES = ["index.html", "creeds.html", "confessions.html"]
EXT_DOMAINS = ["ccreformed.org", "reformedbeginner.net", "canrc.org", "urcna.org", "heritagereformed.com", "prca.org",
               "opc.org", "canadianreformedseminary.ca", "wts.edu", "crts.edu"]
TOP_KEYS = ["CARDS", "DISCUSS", "PLACES", "MAP_SHAPES", "ROUTE", "TIMELINE", "APOS", "NIC_SPLIT", "BIBLE_REFS", "CITED"]
ALLOWED_TAGS = {"q": {"data-cite", "data-bible", "data-p"}, "b": set(), "strong": set(), "em": set(), "br": set(), "span": {"class"}}
VOID = {"br", "img", "hr", "meta", "link", "input", "source", "wbr", "area", "base", "col", "embed", "param", "track"}
SKIP_ORPHAN = {"script", "style", "title"}
BLOCK = {"p", "li", "div", "h1", "h2", "h3", "h4", "td", "th", "tr", "section", "figure", "figcaption", "details", "summary",
         "text", "dt", "dd", "header", "footer", "nav", "aside", "article", "ol", "ul", "table", "noscript", "button"}
QUOTE_RE = re.compile(r'“([^”\x00]+)”|「([^」\x00]+)」|‘([^’\x00]+)’')
CJK = re.compile(r'[\u3400-\u9fff]')
nosup = lambda s: re.sub(r'<sup>.*?</sup>', '', s, flags=re.S)
norm = lambda s: re.sub(r'[\W_]+', '', s)


class Doc(HTMLParser):
    """记录元素（标签、属性、行号、内部文字）与用于孤儿扫描的扁平文本。"""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.elems, self.flat, self.flat_lines = [], [], [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        el = {"tag": tag, "attrs": a, "line": self.getpos()[0], "text": [], "ids": [e["attrs"].get("id") for e in self.stack]}
        self.elems.append(el)
        if tag not in VOID:
            self.stack.append(el)
        if tag in BLOCK or self._excluded():
            self._sep()

    def handle_startendtag(self, tag, attrs):
        self.elems.append({"tag": tag, "attrs": dict(attrs), "line": self.getpos()[0], "text": [], "ids": []})

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]["tag"] == tag:
                was = self._excluded()
                del self.stack[i:]
                if was or tag in BLOCK:
                    self._sep()
                return

    def _excluded(self):
        for e in self.stack:
            if e["tag"] in SKIP_ORPHAN:
                return True
            if e["tag"] == "q" and ("data-cite" in e["attrs"] or "data-bible" in e["attrs"] or "ext" in e["attrs"].get("class", "").split()):
                return True
        return False

    def _sep(self):
        self.flat.append("\x00")
        self.flat_lines.append(self.getpos()[0])

    def handle_data(self, data):
        for e in self.stack:
            e["text"].append(data)
        if not self._excluded():
            self.flat.append(data)
            self.flat_lines.append(self.getpos()[0])


def parse(src):
    p = Doc()
    p.feed(src)
    p.close()
    return p


def load_g17(path):
    s = open(path, encoding="utf-8").read().strip()
    pre = "window.G17 = "
    if not (s.startswith(pre) and s.endswith(";")):
        raise ValueError("data.js 不是 window.G17 = <JSON>; 格式")
    return json.loads(s[len(pre):-1])


def leaves(o, path="G17"):
    if isinstance(o, str):
        yield path, o
    elif isinstance(o, dict):
        for k, v in o.items():
            yield from leaves(v, path + "." + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from leaves(v, "%s[%d]" % (path, i))


def sellers(pat, text):
    """pat 与 text 中任一子串的最小编辑距离（近似子串匹配）。"""
    m = len(pat)
    prev = list(range(m + 1))
    best = m
    for ch in text:
        cur = [0] * (m + 1)
        for j in range(1, m + 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (pat[j - 1] != ch))
        best = min(best, cur[m])
        prev = cur
    return best


class Corpus:
    def __init__(self, entries):
        self.entries = [norm(e) for e in entries if norm(e)]
        self.g3, self.g8 = {}, {}
        for i, e in enumerate(self.entries):
            for k in range(len(e) - 2):
                self.g3.setdefault(e[k:k + 3], set()).add((i, k))
            for k in range(len(e) - 7):
                self.g8.setdefault(e[k:k + 8], set()).add(i)

    def exact(self, f):
        return any(f in e for e in self.entries)

    def near(self, f):
        """近似匹配：3-gram 预筛后在命中位置附近求编辑距离；返回 (距离, 片段) 或 None。"""
        thr = max(1, len(f) // 8)
        cnt = {}
        for k in range(len(f) - 2):
            for i, pos in self.g3.get(f[k:k + 3], ()):
                cnt[(i, pos - k)] = cnt.get((i, pos - k), 0) + 1
        # 每处编辑至多破坏 3 个 3-gram；插入/删除使起点偏移 ≤ thr
        need = max(1, len(f) - 2 - 3 * thr)
        for (i, s) in sorted(cnt):
            if sum(cnt.get((i, s + dd), 0) for dd in range(-thr, thr + 1)) < need:
                continue
            e = self.entries[i]
            lo, hi = max(0, s - thr - 1), min(len(e), s + len(f) + thr + 1)
            d = sellers(f, e[lo:hi])
            if 0 < d <= thr:
                return d, e[lo:hi]
        return None

    def lcs(self, f):
        from difflib import SequenceMatcher
        cand = set()
        for k in range(len(f) - 7):
            cand |= self.g8.get(f[k:k + 8], set())
        for i in cand:
            m = SequenceMatcher(None, f, self.entries[i], autojunk=False).find_longest_match(0, len(f), 0, len(self.entries[i]))
            if m.size >= 8 and m.size / len(f) >= 0.6:
                return self.entries[i][m.b:m.b + m.size]
        return None


def run(site, strict=False):
    fails, warns, stat = [], [], {"quotes": 0, "cards": 0, "orphans": 0}
    F = lambda m: fails.append(m)
    cci = json.load(open(os.path.join(site, "tools", "cci", "cci.json"), encoding="utf-8"))
    # 1. cci.js 同步
    disk = open(os.path.join(site, "assets", "cci.js"), encoding="utf-8").read().replace("\r\n", "\n")
    if render(cci) != disk:
        F("cci.js 与 cci.json 不同步：请运行 build_cci.py")
    # 2. 条目文本表
    T = {}
    for n, h in cci["hc"].items():
        T["hc:" + n] = [nosup(h["q"] + "\n" + "\n".join(h["a"]))]
    for n, b in cci["bc"].items():
        T["bc:" + n] = [nosup(p) for p in b["paras"]]
    for sec, s in cci["cd"].items():
        for n, a in s["arts"].items():
            T["cd:%s:%s" % (sec, n)] = [nosup(p) for p in a["paras"]]
    for k in ("apos", "nic", "ath"):
        T["intro:" + k] = [nosup(cci["creeds"][k]["intro"])]
        T["creed:" + k] = [nosup("".join(cci["creeds"][k]["body"]))]
    for k in ("hc", "bc", "cd"):
        T["intro:" + k] = [nosup("\n".join(cci["intros"][k]))]
    for n, f in cci.get("forms", {}).items():
        T["lf:" + n] = [nosup(p) for p in f["paras"]]
    corpus_entries = ["\n".join(v) for v in T.values()]
    corpus_entries += [nosup(x) for _, x in leaves(cci["home"])] + [nosup(x) for _, x in leaves(cci["creeds"].get("index", []))]
    cc = Corpus(corpus_entries)
    # 经文
    bpath = os.path.join(site, "tools", "bible", "bible.json")
    bible = {}
    if os.path.exists(bpath):
        bible = json.load(open(bpath, encoding="utf-8"))
        for k, v in bible.items():
            if not v.get("verified"):
                (F if strict else warns.append)("经文未核实（verified:false）：" + k)
    else:
        (F if strict else warns.append)("bible.json 缺失")
    chap = {}
    for k, v in bible.items():
        m = re.match(r'^(.+?)(\d+):(\d+)$', k)
        chap.setdefault(m.group(1) + m.group(2), []).append((int(m.group(3)), v["text"]))
    bc_ = Corpus(["".join(t for _, t in sorted(vs)) for vs in chap.values()])

    def verses(ref):
        m = re.match(r'^(.+?)(\d+):(\d+)(?:-(\d+))?$', ref)
        if not m:
            return None
        a, b = int(m.group(3)), int(m.group(4) or m.group(3))
        out = [bible.get("%s%s:%d" % (m.group(1), m.group(2), v)) for v in range(a, b + 1)]
        return None if None in out else "".join(o["text"] for o in out)

    used = set()
    qstrip = lambda s: re.sub(r'[\s“”‘’「」『』"\']', '', s)

    def check_q(el, where):
        a, raw = el["attrs"], "".join(el["text"])
        txt = re.sub(r'\s*\n\s*', '', html.unescape(raw))
        stat["quotes"] += 1
        if "data-cite" in a:
            key = a["data-cite"]
            used.add(key)
            if key not in T:
                F("%s q 键不存在：%s" % (where, key))
                return
            body = "\n".join(T[key])
            pos = 0
            for seg in txt.split("……"):
                i = body.find(seg, pos)
                if not seg or i < 0:
                    F("%s 引文与 CCI 不符 %s：%s" % (where, key, seg[:40]))
                    return
                pos = i + len(seg)
        elif "data-bible" in a:
            ref = a["data-bible"]
            vt = verses(ref)
            if vt is None:
                F("%s 经文未收录：%s" % (where, ref))
                return
            for seg in txt.split("……"):
                if qstrip(seg) not in qstrip(vt):
                    F("%s 经文与和合本不符 %s：%s" % (where, ref, seg[:40]))
                    return
        elif "ext" in a.get("class", "").split():
            url = a.get("data-ext", "")
            dom = re.sub(r'^https://(www\.)?', '', url).split("/")[0]
            if dom not in EXT_DOMAINS:
                F("%s q.ext 域名不在白名单：%s" % (where, url))
            if CJK.search(txt):
                if len(CJK.findall(txt)) > 45:
                    F("%s q.ext 中文超过 45 字" % where)
            elif len(txt.split()) > 30:
                F("%s q.ext 超过 30 词" % where)
        else:
            F("%s 无属性的 <q>：%s" % (where, txt[:30]))

    def orphan_scan(doc, name):
        flat = "".join(doc.flat)
        offs, acc = [], 0
        for piece, ln in zip(doc.flat, doc.flat_lines):
            offs.append((acc, ln))
            acc += len(piece)
        for m in QUOTE_RE.finditer(flat):
            frag = next(g for g in m.groups() if g is not None)
            f = norm(frag)
            if len(CJK.findall(f)) < 6:
                continue
            stat["orphans"] += 1
            ln = max((l for o, l in offs if o <= m.start()), default=0)
            where = "%s:%s" % (name, ln)
            if cc.exact(f):
                F("%s 未标注的CCI引文，请改用 <q data-cite>：%s" % (where, frag[:40]))
                continue
            r = cc.near(f)
            if r:
                F("%s 疑似被改动的CCI引文（编辑距离 %d）：%s ≈ %s" % (where, r[0], frag[:40], r[1][:40]))
                continue
            if len(f) >= 20 and cc.lcs(f):
                F("%s 疑似被改动的CCI引文（LCS）：%s" % (where, frag[:40]))
                continue
            if bc_.exact(f):
                F("%s 未标注的经文引文，请改用 <q data-bible>：%s" % (where, frag[:40]))
                continue
            r = bc_.near(f)
            if r:
                F("%s 疑似被改动的经文引文（编辑距离 %d）：%s ≈ %s" % (where, r[0], frag[:40], r[1][:40]))

    def check_doc(doc, name, page=None):
        for el in doc.elems:
            where = "%s:%d" % (name, el["line"])
            a, cls = el["attrs"], el["attrs"].get("class", "").split()
            if el["tag"] == "q":
                check_q(el, where)
            if "data-src" in a and "cq" in cls:
                stat["cards"] += 1
                key = a["data-src"]
                used.add(key)
                if key.startswith("creed:") or key not in T:
                    F("%s .cq 键无效：%s" % (where, key))
                elif "data-p" in a:
                    p = a["data-p"]
                    if not p.isdigit() or not (1 <= int(p) <= len(T[key])) or not key.startswith(("bc:", "cd:", "lf:")):
                        F("%s data-p 越界或不支持：%s p=%s" % (where, key, p))
                if "".join(el["text"]).strip():
                    F("%s .cq[data-src] 内不得写死文字" % where)
            if el["tag"] == "blockquote":
                if not ("bible" in cls and "data-ref" in a) or "".join(el["text"]).strip():
                    F("%s blockquote 只允许空的 blockquote.bible[data-ref]" % where)
                elif verses(a["data-ref"]) is None:
                    F("%s 经文未收录：%s" % (where, a["data-ref"]))
            if page == "creeds.html" and "data-recite" in a and "".join(el["text"]).strip():
                F("%s [data-recite] 内不得写死文字" % where)
            if a.get("class") and "lyrics" in cls:
                F("%s 出现 class=lyrics" % where)
        orphan_scan(doc, name)

    pages = {}
    for pg in PAGES:
        path = os.path.join(site, pg)
        if not os.path.exists(path):
            F("缺少页面：" + pg)
            continue
        src = open(path, encoding="utf-8").read()
        pages[pg] = src
        doc = parse(src)
        check_doc(doc, pg, pg)
        if pg == "index.html":
            lit = "".join(t for el in doc.elems if el["attrs"].get("id") == "liturgy" for t in el["text"])
            for w in ("日内瓦", "圣诗部分", "待核实"):
                if w in lit:
                    F("index.html #liturgy 出现禁用词：" + w)
    # 7. data.js
    g = None
    try:
        g = load_g17(os.path.join(site, "assets", "data.js"))
    except Exception as e:
        F("data.js 不是 window.G17 = <JSON>; 格式：%s" % e)
    if g is not None:
        for k in TOP_KEYS:
            if k not in g:
                F("data.js 缺少顶层键：" + k)
        for path, s in leaves(g):
            doc = parse(s)
            for el in doc.elems:
                if el["tag"] not in ALLOWED_TAGS or set(el["attrs"]) - ALLOWED_TAGS[el["tag"]]:
                    F("data.js %s 标签/属性不在白名单：<%s %s>" % (path, el["tag"], " ".join(el["attrs"])))
            check_doc(doc, "data.js " + path)
        if len(g.get("DISCUSS", [])) < 8:
            F("DISCUSS 少于 8 道")
        if [p.get("n") for p in g.get("PLACES", [])] != list(range(1, 10)):
            F("PLACES 须为 9 项且 n=1..9")
        if len(g.get("CARDS", [])) != 16:
            F("CARDS 须为 16 张")
        for r in g.get("BIBLE_REFS", []):
            if not re.match(r'^[\u4e00-\u9fff]{1,3}\d+:\d+(-\d+)?$', r):
                F("BIBLE_REFS 格式错误：" + r)
        # 6. 背诵分行
        ok = True
        for k, arr in (("apos", "APOS"), ("nic", "NIC_SPLIT")):
            a, b = "".join(x["t"] for x in g.get(arr, [])), "".join(cci["creeds"][k]["body"])
            if a != b:
                ok = False
                i = next((i for i in range(min(len(a), len(b))) if a[i] != b[i]), min(len(a), len(b)))
                F("%s 背诵分行与 CCI 不符 @%d：%r / %r" % (arr, i, a[max(0, i - 20):i + 20], b[max(0, i - 20):i + 20]))
        ath = cci["creeds"]["ath"]
        if re.sub(r'\s*\d+\)\s*', '', "".join(ath["body"])) != "".join(i["t"] for i in ath["items"]) or [i["n"] for i in ath["items"]] != list(range(1, 43)):
            ok = False
            F("ATH items 与 CCI 正文不符")
        if ok:
            stat["recite"] = True
        # 8. CITED 覆盖
        cited = set(g.get("CITED", []))
        for k in sorted(used - cited):
            F("引用键未列入 CITED：" + k)
        for k in sorted(cited - set(T)):
            F("CITED 键在 cci.js 中不存在：" + k)
    # 10. 用字提示
    for w in ("上帝", "阿里乌", "腓特烈"):
        n = sum(s.count(w) for s in pages.values())
        if n:
            warns.append("用字提示：%s ×%d" % (w, n))
    # 11. CSS
    css_path = os.path.join(site, "assets", "style.css")
    if os.path.exists(css_path):
        css = re.sub(r'/\*.*?\*/', '', open(css_path, encoding="utf-8").read(), flags=re.S)
        for m in re.finditer(r'([^{}]+)\{([^{}]*)\}', css):
            sels = [s.strip() for s in m.group(1).split(",")]
            if any(s in ("html", "body") for s in sels) and re.search(r'overflow(-x)?\s*:\s*(hidden|clip)', m.group(2)):
                F("style.css：html/body 不得设置 overflow-x:hidden|clip")
    stat["mismatches"] = len(fails)
    return fails, warns, stat


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    site = os.path.abspath(args[0] if args else os.path.join(D, "..", ".."))
    fails, warns, stat = run(site, "--strict" in sys.argv)
    for w in warns:
        print("  ⚠", w)
    for f in fails:
        print("  ✗", f)
    print("quotes checked: %(quotes)d / cards: %(cards)d / orphan fragments scanned: %(orphans)d / mismatches: %(mismatches)d" % stat,
          "/ warnings: %d" % len(warns))
    if stat.get("recite"):
        print("APOS/NIC/ATH == CCI: True")
    print("PASS" if not fails else "FAIL")
    sys.exit(1 if fails else 0)
