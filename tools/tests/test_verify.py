# verify.py 单元测试：python -m unittest discover tools/tests
import json, os, shutil, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "cci"))
sys.path.insert(0, os.path.join(HERE, "..", "bible"))
import verify  # noqa: E402
from build_cci import render  # noqa: E402
from fetch_bible import normalize  # noqa: E402

ATH_ITEMS = [{"n": i, "t": "第%d点。" % i} for i in range(1, 43)]
CCI = {
    "creeds": {
        "apos": {"intro": "使徒信经简介文字。", "body": ["我信神，全能的父。", "我信圣灵。"], "url": "/a"},
        "nic": {"intro": "尼西亚信经简介文字。", "body": ["我们信独一的神。"], "url": "/n"},
        "ath": {"intro": "亚他那修信经简介文字。", "body": ["%d) %s" % (i["n"], i["t"]) for i in ATH_ITEMS], "url": "/t", "items": ATH_ITEMS},
        "index": []},
    "hc": {"72": {"n": 72, "ld": 27, "q": "外在的水洗能除去罪吗？", "a": ["答：不能。唯有耶稣基督的宝血和圣灵才能洗去我们一切的罪<sup>1</sup>。"], "refs": [], "url": "/h"},
           "74": {"n": 74, "ld": 27, "q": "婴孩也要受洗吗？", "a": ["答：是的，因为他们与父母同属于神的圣约和教会。在新约时代，割礼已被洗礼所取代。"], "refs": [], "url": "/h"}},
    "bc": {"34": {"title": "第三十四条 论圣洗礼", "paras": ["他废除了与血有关的割礼，并设立圣洗礼取代了它。", "这一切不是洗礼之水所带来的功效。"], "refs": [], "url": "/b"}},
    "cd": {"section1": {"title": "第一项教义", "arts": {"17": {"title": "第十七条", "paras": ["信徒的儿女是圣洁的，不是因为他们的本性圣洁。"], "refs": [], "url": "/c"}}}},
    "home": {"intro": [], "arts": [], "end": [], "url": "/"},
    "intros": {"hc": ["海德堡简介。"], "bc": ["比利时简介。"], "cd": ["多特简介。"], "forms": []},
    "forms": {"1": {"title": "婴儿洗礼仪文", "paras": ["第一段仪文文字。", "第二段仪文文字。"], "refs": [], "url": "/f"}},
}
BIBLE = {"创17:7": {"raw": "我要与你并你世世代代的后裔坚立我的约，作永远的约，是要作你和你后裔的神。",
                    "text": "我要与你并你世世代代的后裔坚立我的约，作永远的约，是要作你和你后裔的神。", "verified": True}}
G17 = {"CARDS": [{"q": "问", "a": "答", "ref": "r"}] * 16,
       "DISCUSS": [{"id": "d%d" % i, "q": "题", "a": {"points": ["点"], "verses": [], "creeds": [], "misread": "", "oneLine": ""}} for i in range(8)],
       "PLACES": [{"id": "p%d" % n, "n": n} for n in range(1, 10)], "MAP_SHAPES": [], "ROUTE": [], "TIMELINE": {},
       "APOS": [{"t": "我信神，全能的父。", "c": "father"}, {"t": "我信圣灵。", "c": "spirit"}],
       "NIC_SPLIT": [{"t": "我们信独一的神。", "c": "father"}], "BIBLE_REFS": ["创17:7"],
       "CITED": ["hc:72", "hc:74", "bc:34", "cd:section1:17", "lf:1"]}
PAGE = '<!doctype html><html><body><main>%s</main></body></html>'


class VerifyTest(unittest.TestCase):
    def setUp(self):
        self.site = tempfile.mkdtemp()
        for p in ("assets", "tools/cci", "tools/bible"):
            os.makedirs(os.path.join(self.site, p))
        self.w("tools/cci/cci.json", json.dumps(CCI, ensure_ascii=False))
        self.w("assets/cci.js", render(CCI))
        self.w("tools/bible/bible.json", json.dumps(BIBLE, ensure_ascii=False))
        self.w("assets/style.css", "body{margin:0}")
        self.data(G17)
        self.page("<p>正文</p>")

    def tearDown(self):
        shutil.rmtree(self.site)

    def w(self, rel, s):
        with open(os.path.join(self.site, rel), "w", encoding="utf-8") as fh:
            fh.write(s)

    def data(self, g):
        self.w("assets/data.js", "window.G17 = " + json.dumps(g, ensure_ascii=False) + ";")

    def page(self, body, creeds="<p>x</p>"):
        self.w("index.html", PAGE % body)
        self.w("creeds.html", PAGE % creeds)
        self.w("confessions.html", PAGE % "<p>y</p>")

    def fails(self):
        return verify.run(self.site)[0]

    def assertFail(self, body, needle=None, **kw):
        self.page(body, **kw)
        f = self.fails()
        self.assertTrue(f, "预期 FAIL")
        if needle:
            self.assertTrue(any(needle in x for x in f), f)

    def test_01_ok(self):
        self.page('<q data-cite="hc:72">唯有耶稣基督的宝血和圣灵才能洗去我们一切的罪</q><q data-bible="创17:7">作永远的约</q>'
                  '<div class="cq" data-src="lf:1" data-p="2"></div>')
        self.assertEqual(self.fails(), [])

    def test_02_cite_changed(self):
        self.assertFail('<q data-cite="hc:72">唯有耶稣基督的宝血和圣灵才能洗去我一切的罪</q>', "不符")

    def test_03_bare_q(self):
        self.assertFail('<q>你好</q>', "无属性")

    def test_04_missing_key(self):
        self.assertFail('<q data-cite="hc:99">什么</q>', "不存在")

    def test_05_order(self):
        self.assertFail('<q data-cite="bc:34">这一切不是洗礼之水……他废除了与血有关的割礼</q>', "不符")

    def test_06_ext_long(self):
        self.assertFail('<q class="ext" data-ext="https://opc.org/x">%s</q>' % ("字" * 46), "45")
        self.assertFail('<q class="ext" data-ext="https://opc.org/x">%s</q>' % " ".join(["w"] * 31), "30")
        self.assertFail('<q class="ext" data-ext="https://ccifellowship.org/x">短</q>', "白名单")

    def test_07_recite_line(self):
        g = dict(G17, APOS=[{"t": "我信神，全能父。", "c": "father"}, {"t": "我信圣灵。", "c": "spirit"}])
        self.data(g)
        self.assertTrue(any("APOS" in x for x in self.fails()))

    def test_08_ath_missing(self):
        c = json.loads(json.dumps(CCI))
        c["creeds"]["ath"]["items"] = c["creeds"]["ath"]["items"][:-1]
        self.w("tools/cci/cci.json", json.dumps(c, ensure_ascii=False))
        self.w("assets/cci.js", render(c))
        self.assertTrue(any("ATH" in x for x in self.fails()))

    def test_09_orphan_exact(self):
        self.assertFail('<p>“他废除了与血有关的割礼”</p>', "未标注的CCI")

    def test_10_orphan_changed_long(self):
        self.assertFail('<p>“他废除了与血相关的割礼，并设立圣洗礼取代了它”</p>', "疑似")

    def test_10b_orphan_changed_6_10_15(self):
        # 6 字、10 字、15 字片段各改一字
        cases = {"信徒的儿男是圣": 7, "这一切不是洗理之水所带": 11, "唯有耶稣基督的宝血和圣灵才可洗去": 16}
        for frag in cases:
            self.page("<p>“%s”</p>" % frag)
            f = self.fails()
            self.assertTrue(any("疑似" in x for x in f), (frag, f))
        self.page("<p>“信徒儿女是圣洁”</p>")  # 6 CJK：删去一字
        self.assertTrue(any("疑似" in x for x in self.fails()))

    def test_10c_unrelated_quote_passes(self):
        self.page("<p>“神的迟延不是缺席而是预备”</p>")
        self.assertEqual(self.fails(), [])

    def test_11_orphan_bible(self):
        self.assertFail('<p>“作你和你后裔的神”</p>', "经文")
        self.assertFail('<p>“作你和你后代的神”</p>', "经文")

    def test_12_data_not_json(self):
        self.w("assets/data.js", "window.G17 = {CARDS:[]};")
        self.assertTrue(any("data.js" in x for x in self.fails()))

    def test_13_data_img(self):
        g = json.loads(json.dumps(G17))
        g["CARDS"][0] = {"q": "<img src=x>", "a": "a", "ref": "r"}
        self.data(g)
        self.assertTrue(any("白名单" in x for x in self.fails()))

    def test_14_css_body_overflow(self):
        self.w("assets/style.css", "body{overflow-x:hidden}")
        self.assertTrue(any("overflow" in x for x in self.fails()))

    def test_15_recite_hardcoded(self):
        self.assertFail("<p>x</p>", "data-recite", creeds='<div class="recite-body" data-recite="apos">我信神</div>')

    def test_16_lf_p_out_of_range(self):
        self.assertFail('<div class="cq" data-src="lf:1" data-p="3"></div>', "越界")

    def test_17_cq_hardcoded(self):
        self.assertFail('<div class="cq" data-src="hc:72">写死</div>', "写死")

    def test_normalize(self):
        self.assertEqual(normalize("【注】起初　神「说」『话』 "), "起初神“说”‘话’")


if __name__ == "__main__":
    unittest.main()
