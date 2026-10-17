# 抓取讲章引用的和合本经文（信望爱站 FHL API），生成 tools/bible/bible.json 与 assets/bible.js
# 用法：python fetch_bible.py            联网抓取 G17.BIBLE_REFS 中全部经节并生成 bible.js
#       python fetch_bible.py --build-js-only   仅从 bible.json 重新生成 bible.js（不联网）
import json, os, re, sys, time, io, urllib.request, urllib.parse
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
D = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.normpath(os.path.join(D, "..", ".."))
BJ = os.path.join(D, "bible.json")
JS = os.path.join(SITE, "assets", "bible.js")
API = "https://bible.fhl.net/json/qb.php?"
REF_RE = re.compile(r'^([\u4e00-\u9fff]{1,3})(\d+):(\d+)(?:-(\d+))?$')


def normalize(raw):
    """删除【…】小注；「」→“”，『』→‘’；删除全角空格；去首尾空白。"""
    s = re.sub(r'【[^】]*】', '', raw)
    s = s.replace("「", "“").replace("」", "”").replace("『", "‘").replace("』", "’")
    s = s.replace("\u3000", "")
    return s.strip()


def parse_ref(ref):
    m = REF_RE.match(ref)
    if not m:
        raise ValueError("经文引用格式错误：" + ref)
    book, chap, a, b = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4)
    return book, chap, a, int(b) if b else a


def fetch(ref):
    book, chap, a, b = parse_ref(ref)
    q = urllib.parse.urlencode({"chineses": book, "chap": chap, "sec": "%d-%d" % (a, b) if b > a else str(a), "version": "unv", "gb": 1})
    last = None
    for _ in range(3):
        try:
            req = urllib.request.Request(API + q, headers={"User-Agent": "Mozilla/5.0 (g17-sermon fetch_bible)"})
            with urllib.request.urlopen(req, timeout=30) as r:
                if r.status != 200:
                    raise IOError("HTTP %s" % r.status)
                j = json.loads(r.read().decode("utf-8"))
            if j.get("status") != "success" or len(j.get("record", [])) != b - a + 1:
                raise IOError("FHL 返回异常：%s" % ref)
            out = {}
            for rec in j["record"]:
                if "bible_text" not in rec:
                    raise IOError("缺 bible_text")
                raw = rec["bible_text"]
                out["%s%d:%d" % (book, rec["chap"], rec["sec"])] = {"raw": raw, "text": normalize(raw), "verified": True}
            return out
        except Exception as e:  # 重试
            last = e
            time.sleep(3)
    raise last


def load_refs():
    s = open(os.path.join(SITE, "assets", "data.js"), encoding="utf-8").read().strip()
    return json.loads(s[len("window.G17 = "):-1])["BIBLE_REFS"]


def build_js(bj):
    js = "/* 本文件由 tools/bible/fetch_bible.py 生成，勿手改：经文取自信望爱站（FHL）和合本，已去除神版空格与小注 */\nwindow.BIBLE = " + \
        json.dumps({k: v["text"] for k, v in bj.items()}, ensure_ascii=False, separators=(",", ":")) + ";\n"
    open(JS, "w", encoding="utf-8", newline="\n").write(js)
    print("written", JS, len(bj), "verses")


if __name__ == "__main__":
    if "--build-js-only" in sys.argv:
        build_js(json.load(open(BJ, encoding="utf-8")))
        sys.exit(0)
    bj = {}
    try:
        for ref in load_refs():
            bj.update(fetch(ref))
    except Exception as e:
        print("抓取失败，未覆盖 bible.json：", e, file=sys.stderr)
        sys.exit(1)
    json.dump(bj, open(BJ, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
    build_js(bj)
