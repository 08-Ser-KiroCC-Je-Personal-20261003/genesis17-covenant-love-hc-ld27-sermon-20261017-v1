# 设计评审 · 创世记17章讲章网站（design.md v2）

评审日期：2026-10-17 ｜ 结论：**CHANGES_REQUESTED**（HIGH 1 / MEDIUM 6 / NIT 6）

总体评价：v2 已把上一轮 20 条意见基本落实。四要点、HC 72–74、四重闭环、三信经背诵版与对比、SVG 地图、思维导图、流程图、闪卡、10 道讨论题都有具体落点；仓库名、Pages、surge 路径清楚。剩下的阻塞问题集中在两处：一是"改一个字也能查出"的孤儿引文算法对短片段失效，且有几条绕过路径；二是仪文数据结构、livecheck 覆盖面、布局自检的误报/漏报规则、凭据在多次独立命令中的使用方式还不够具体。

---

## 发现列表

### 1. [HIGH] 孤儿引文"改一字"检测对短片段失效，与验收 2c 冲突（§14 第12步 (b)、§4 验收2c）

问题：规则 (b) 要求 8-gram 预筛命中，且最长公共子串 L ≥ 8、L/len(f) ≥ 0.6。验收 2b 的下限是 ≥6 个 CJK 字。对 6–15 字的片段，在中间改一个字后，两侧剩下的连续段都 < 8：
- 例：BC 34 原文"这一切不是洗礼之水所带来的功效"（15 字），改成"这一切不是洗礼之水所带出的功效"，最长公共子串为"这一切不是洗礼之水所带"（11 字），能命中；但改第 8 个字时两侧为 7/7，L=7 < 8，漏检。
- 例：10 字片段"割礼已被洗礼所取代了"类，改第 5 字，L ≤ 5，8-gram 预筛直接不命中。

结果是"在裸引号片段中改一个字 → 构建失败"（验收 2c）对常见长度的短引文不成立。这正是用户"一字不差"要求的核心防线。

修复：把 (b) 换成"等长窗口编辑距离"规则，保留 LCS 规则只作为长片段补充：

```python
# 预筛：3-gram（短片段也能命中）
def grams(s, n=3): return {s[i:i+n] for i in range(len(s)-n+1)}
def near_match(f, entry):
    n = len(f)
    best = n
    for w in (n-1, n, n+1):                 # 允许增删一字
        for i in range(0, max(1, len(entry)-w+1)):
            best = min(best, levenshtein(f, entry[i:i+w]))
            if best == 0: return 0
    return best
# 判定：len(f) >= 6 且与某条语料共享 >= 2 个 3-gram，
#      且 near_match(f, entry) <= max(1, len(f)//8) 且 > 0  → FAIL "疑似被改动的CCI引文"
# 另：len(f) >= 20 时保留原 LCS 规则（L>=8 且 L/len(f)>=0.6）作补充
```

`levenshtein` 用标准库自写的 O(n·m) DP（片段 ≤ 200 字，语料按 3-gram 预筛后只剩少量条目，性能可接受）。经文 (c) 同样增加 `near_match <= max(1, len(f)//8)` → FAIL"疑似被改动的经文"。§19 增加用例：6 字片段改 1 字、10 字片段改中间 1 字、15 字片段改第 8 字，均须 FAIL。

### 2. [MEDIUM] 逐字校验存在三条绕过路径（§13.5、§13.6、§14 第12步）

问题：
- (a) `q.ext` 白名单包含 ccifellowship.org。用 `<q class="ext" data-ext="https://ccifellowship.org/…">` 写 CCI 原文时，只检查字数，不做逐字比对；同时 `<q>` 内文字被孤儿扫描排除。
- (b) 孤儿扫描排除全部 `<blockquote>`。设计只规定 `blockquote.bible[data-ref]` 运行时填充，没有禁止在 HTML 中写死 blockquote 文字，任何 blockquote 内的 CCI 原文都不会被检查。
- (c) `.cq[data-src]` 只检查键与 data-p，没有要求 HTML 中容器为空；写死在 `.cq` 内的文字会被运行时覆盖，但无 JS 时显示的就是未校验文字。

修复（写入 §13.5 与 §14）：
- ext 白名单移除 ccifellowship.org；`data-ext` 域名为 ccifellowship.org → FAIL"CCI 原文请用 data-cite"。
- 只允许 `blockquote.bible[data-ref]`，且 HTML 中内容必须为空（只允许空白）；其他 blockquote → FAIL。
- `.cq[data-src]` 在 HTML 与 data.js 中内容必须为空 → 否则 FAIL。
- 孤儿扫描排除范围收窄为：`q[data-cite]`、`q[data-bible]` 内部（已逐字校验）、`script`、`style`、`title`。`q.ext` 内部仍跑 (a)(b)，命中 CCI 语料即 FAIL。
- §19 增加三条对应用例。

### 3. [MEDIUM] 仪文 `lf:*` 的数据结构与生成链路未定义（§6、§8、§13.5、§23 #10）

问题：设计只说"add_forms.py 合并进 cci.json["forms"]""build_cci、verify 同步支持"，但：
- 未给出 `forms` 条目的字段结构，`text(lf:n)` 依赖的 `paras` 从何而来没写明。
- 现有 cci.json 的 `intros` 下已有键 `forms`（空列表），与新顶层键 `forms` 同名，易混淆。
- 现有 build_cci.py 用白名单字典逐键输出（creeds/home/intros/hc/bc/cd/hcParts），不会自动带上 `forms`；`render(d)` 必须显式加入。
- 已实测 `/books/book-of-praise/liturgical-forms/1` 标题为"婴儿洗礼仪文"，内容区有 23 个 `<p>`，父母誓约三问与"任何约均包括两部分，即应许和义务"都在 `<p>` 中；另有 4 个标题、1 个 `ol.reference-list`（脚注经文）、"__________"施洗占位。设计未说明标题与脚注如何处理。

修复：在 §8 固定如下：

```json
"forms": {
  "1": {"title": "婴儿洗礼仪文",
        "paras": ["主耶稣基督所爱的众弟兄姊妹，圣洗礼的教义总结如下：", "..."],
        "refs": ["...ol.reference-list 中每个 li 的文本..."],
        "url": "/books/book-of-praise/liturgical-forms/1"}
}
```

- `paras` = `ccilib.paras(ccilib.content(html))`，只取 `<p>`，标题不入 paras，`<sup>` 按现有 clean() 保留；"__________"原样保留。
- `render(d)` 增加 `"forms": d.get("forms", {})`；`intros.forms` 不动，也不作为任何键。
- `text(lf:n) = "\n".join(forms[str(n)]["paras"])`，带 data-p 时取 `paras[p-1]`。
- add_forms.py 打印 `序号 | 前 30 字`，实现者据此在 §9.6 要点三与要点四里写死所选 data-p（建议要点三选"第一/第二/第三，你们是否承认/承诺"三段之一，要点四选"任何约均包括两部分"段）。

### 4. [MEDIUM] livecheck 覆盖面不足，且不是真正"联网"（§16、§18、A1）

问题：现有 livecheck.py 读取本地 `.html`（需先 fetch.py），只比对 BC 15/33/34、CD 1.17、HC LD27、三信经。本站 CITED 中的 hc:1/2/19/21/54/60/61/66/69/86、bc:9/14/17/22、cd 1.7/1.8/2.8、intro:* 从未在本项目重抓核对。§18 称"cci.json 的真实性由 livecheck 负责"，§16 把 livecheck 的失败写成"网络失败"，都与现状不符。用户要求原文一字不差来自 ccifellowship.org，部署前应覆盖全部实际引用。

修复：新增 `tools/cci/livecheck_cited.py`（或改写 livecheck.py）：
- 读取 `assets/data.js` 的 `CITED`；对每个键取 cci.json 中该条目的 `url`（intro:* 取对应简介页 url，creed:* 取信经 url），用 `fetch.get` 联网抓取（超时 60 s、重试 3 次）。
- 用 ccilib 解析后与 cci.json 逐字比较：hc 比 `q` 与 `a`；bc/cd/lf 比 `paras`；creed 比 `body`；intro 比原文。
- 每键输出一行 `KEY True/False`；任一 False → 退出码 1；网络不可用 → 退出码 3。
- 部署流程（§20 第1步）规定：退出码 0 才可部署；退出码 3 时停止并报告，不跳过。FETCH_NOTES 记录运行日期与结果。

### 5. [MEDIUM] 布局自检规则会误报抽屉/aurora，且漏检 SVG 内文字重叠（§13.1、§13.10、§10.4）

问题：
- 360/768 px 下目录为抽屉。若关闭时用 `transform:translateX(-100%)`，其子元素 `r.left < -1`，按 OVERFLOW 规则（只在遇到 auto/scroll 祖先时停止）会报错。排除条件只有 display:none、≤1px、.sr-only。
- aurora 光斑在 `overflow:hidden` 的 aurora 层内超出视口时，OVERFLOW 同样会报（data-clip-ok 只豁免 CLIP）。
- 上一项目 style.css 第204行 `.diagram{overflow-x:auto}`，若迁移过来会让图内溢出被当作"可滚动容器"而跳过，与"表格是唯一允许内部横向滚动的组件"矛盾，且没有检查项阻止。
- OVERLAP 只检查列出的网格容器的直接子元素。闭环 SVG 每个节点标签最长 7 字 × 16 单位 ≈ 112 单位，半径 140 环上 6 个节点相邻弧长约 147 单位，左右两端标签离 viewBox 边界仅约 4 单位，标签之间或标签与箭头相交不会被任何检查发现。

修复：
- 抽屉关闭时规定为 `visibility:hidden` + `inert`（打开时移除）；自检排除 computed `visibility:hidden` 的元素及 `[inert]` 子树。
- OVERFLOW 祖先链遇到"`overflow` 为 hidden|clip 且带 `data-clip-ok`"的祖先也停止。
- verify 第11步增加：style.css 中 `overflow(-x)?\s*:\s*(auto|scroll)` 只允许出现在 `.table-wrap`、`.map-zoom`（dialog 平移容器）、`.sidebar`/`.toc`（纵向滚动）规则块中，其他 → FAIL。
- 新增 `SVGOVERLAP`：每个可见 svg（地图主图除外，插图内仍检查）内，`text` 元素两两 `getBoundingClientRect()` 相交 > 1 px，或 text 超出所在 svg 矩形 > 1 px → 计入 issues。layoutcheck 断言不变（issues=0 已覆盖）。

### 6. [MEDIUM] 凭据在"每条命令独立进程"下的使用与提交前扫描不可执行（§18、§20 第5步、验收16）

问题：
- 设计假设"凭据只存在于当前 PowerShell 进程的变量中"，并在 §18、§20、验收16 多处使用 `$pw`、`$email`，但没说明它们在哪里赋值。代理每次调用命令都是新进程，变量不跨调用保留，多处检查会因 `$pw` 为空而失效：`"…".Contains($null)` 会抛错，或改为空串时恒为 True。
- "提交前"扫描用 `git log -p --all`，看不到暂存区内容，只能靠人工 `git diff --cached`。
- README 不含邮箱只在验收中提到，没有自动检查。

修复（§18 替换为）：
- 规则：任何需要凭据的操作，都在单条命令内完成赋值、使用与清除，例如 `$pw='…'; $email='…'; <操作>; Remove-Variable pw,email`；不写入脚本文件。
- 提交前自动检查（同一条命令内）：

```powershell
$pw='…'; $email='…'
$staged = git diff --cached | Out-String
$tree = git ls-files -co --exclude-standard | ForEach-Object { Get-Content -Raw -LiteralPath $_ -ErrorAction SilentlyContinue } | Out-String
"staged:" + ($staged.Contains($pw) -or $staged.Contains($email))
"tree:"   + ($tree.Contains($pw)   -or $tree.Contains($email))
Remove-Variable pw,email
```

  两项都必须为 False 才可提交。
- 推送后检查改为 `(git log -p --all | Out-String)` 同时检查 `$pw` 与 `$email`，以及令牌模式。
- 输出只打印布尔值，不打印内容。

### 7. [MEDIUM] `BIBLE_REFS` 未列全，经文校验与孤儿检测会悄悄漏掉（§8.1、§9、§14 第9/12步）

问题：(c) 规则只能检测 bible.json 已收录的经节，而 `BIBLE_REFS` 只写了 `["创17:1-27","罗4:9-12",…]`。设计正文本身就有多处 ≥6 字的经文短语需要标注：
- "耶和华岂有难成的事"（创18:14）
- "神必自己预备"（创22:8）
- 圣约公式各节（出6:7、利26:12、耶31:33、结37:27、林后6:16、启21:3）
- 诗25:10、14

这些节若未列入清单，裸写也不会被发现，写成 `<q data-bible>` 时则会因节不存在而 FAIL。另外 FHL API 一次只接受单个连续范围，"加3:7–9、16、29"这类非连续引用的抓取与键名也未定义。

修复：在 §8.1 写出完整清单，并规定语法：

```
"BIBLE_REFS": ["创3:15","创9:12-13","创12:1-7","创13:18","创15:9-18","创16:16","创17:1-27",
 "创18:1","创18:14","创21:5","创21:31-33","创22:2","创22:8","创25:7","出4:24-26","出6:7","出24:8",
 "利26:12","申10:16","申30:6","撒下7:12-16","诗25:10","诗25:14","耶31:31-34","结37:27","路22:20",
 "罗4:9-12","罗9:6-8","罗11:20-22","加3:7-9","加3:16","加3:27-29","西2:11-12","徒2:38-39",
 "徒16:15","徒16:33","林前7:14","林后6:16","来9:15-22","来10:28-29","启21:3"]
```

- 每项必须是"书卷+章:节"或"书卷+章:起-止"的单一连续范围，非连续引用拆成多项；verify 用正则 `^[\u4e00-\u9fff]{1,3}\d+:\d+(-\d+)?$` 校验格式。
- 页面中出现的每个 `data-bible` / `data-ref` 都必须落在某项范围内，否则 FAIL（已有）。
- 实现者新增经文引用时同步追加。

### 8. [NIT] `creed:<k>` 键与 CITED/信条页渲染未衔接（§11 与 §12 冲突）

问题：§11 新增 `creed:apos|nic|ath` 键用于 data-cite；§12 的覆盖规则要求所有使用的键都在 CITED 中，但 CITED 分组与 confessions.html 渲染都没有 creed 组，getItem 对 creed 的卡片渲染方式也未定义。

修复：CITED 允许 creed:*；confessions.html 增加"三大信经"组，每项渲染为标题 + CCI 链接 + "全文背诵版见 creeds.html#recite"，不重复全文；`.cq[data-src^="creed:"]` 在三页中禁止使用，只允许 `q[data-cite]`。

### 9. [NIT] `q[data-cite]` 的空白处理未定义（§13.5）

问题：data-bible 规则会去空白，data-cite 规则不去。HTML 源码里 q 内换行或缩进会导致误 FAIL；CCI 原文里又确有空格（如"西2: 11-13"），不能简单全部去除。

修复：规定 `q[data-cite]` 文本中的 `\s*\n\s*` 视为源码换行并删除，其余空白原样比对；不得跨段落引用，跨段用 `……` 分段。

### 10. [NIT] 诗歌"关联说明"可能被读成诗歌内容（§9.1）

问题：圣诗第19首、第9首的内容未核实（CCI 网站无诗歌页面，`/books/book-of-praise/hymns/19` 实测 404）。"神召聚他立约的子民""带着约的应许回到生活"会被读者理解为这两首诗歌的主题。

修复：圣诗两项的说明改为礼拜功能，并加前缀"礼拜位置："，例如"礼拜位置：宣召后开启敬拜""礼拜位置：祝福前差遣"。韵诗三项因对应诗篇明确，保留主题说明。

### 11. [NIT] 主日27 缺少集中呈现（§9 结构表）

问题：Q72–74 分散在要点二、要点三与流程图中，没有一处让读者连续读完整个主日27，不利于记忆。

修复：在 `core` 后加 h3 `#ld27`"海德堡要理问答 主日27（问72–74）"，放三张 `.cq[data-src="hc:72|73|74"]` 卡片与 §10.3 的问答逻辑流程图；要点二、三中的同名卡片改为 `<a href="#ld27">` 加关键短语 `q[data-cite]`，避免重复长卡片。验收6 改为检查 `#ld27` 内三张卡片。

### 12. [NIT] 对比度要求没有校验手段（NFR-3）

问题："明暗两主题下正文对比度 ≥ 4.5:1"没有对应的自动或人工检查步骤。

修复：自检增加 `lowContrast` 计数：对 `p, li, td, .callout *, .cq` 文本元素，取 computed `color` 与最近非透明背景色计算 WCAG 对比度，< 4.5 计数。layoutcheck 在每个宽度下以 `?check=1&theme=dark` 与 `&theme=light` 各跑一次（`theme` 参数只在 check 模式生效），断言 `lowContrast=0`。毛玻璃半透明底按 `--panel` 叠加在 `--bg` 上的合成色计算。

### 13. [NIT] BC 34 篇幅描述有误（§21）

问题："BC 34 约 1200 字"不准确，实测 4 段，去 `<sup>` 后约 827 字。

修复：改为"约 830 字"。折叠策略不变。

---

## 已核实的假设

- cci.json 顶层键为 source/creeds/hc/bc/cd/home/intros。hc 共 129 条，字段为 `n, ld, q, a[], refs, url`；bc 共 37 条，字段为 `title, paras, refs, url`；cd 四个 section，`arts` 为以字符串编号为键的字典。
- ATH：`items` 共 42 项，`n == 1..42`；`re.sub(r'\s*\d+\)\s*','',''.join(body)) == ''.join(t)` 结果为 True。ATH 简介中写的是"第1-28点 / 第29-43点"，与 42 项不一致，设计 §11 加作者注的处理恰当。
- hc:74 答案含"割礼已被洗礼所取代"；hc:72、73 均为 ld 27。
- bc:34 共 4 段：第1段含"他废除了与血有关的割礼"；第3段含"这一切不是洗礼之水所带来的功效"；第4段含"我们弃绝重洗派的错谬"。设计 §9.6 与 §9.9 的引用和 data-p 正确。
- cd section1/8 含"无论是在旧约之下还是在新约之下"；cd section2/8 含"十字架上所流的宝血坚立新约"；cd section1/17 存在。
- intros 只有 bc/hc/cd/forms（forms 为空列表）；三信经简介在 `creeds[k].intro`，与 §13.5 的 intro 取值定义一致。
- 现有 build_cci.py 已生成 `hcParts`（3–11 / 12–85 / 86–129），与 §10.4 一致；该脚本目前是模块级直接写文件，需按设计重构为 `render(d)`。
- `/books/book-of-praise/liturgical-forms/1` 实测 200，标题为"婴儿洗礼仪文"，含 `block-tulip-content`，有 23 个 `<p>`，父母誓约三问与"任何约均包括两部分，即应许和义务"均在其中。
- FHL API `qb.php?chineses=创&chap=17&sec=1-2&version=unv&gb=1` 实测返回 `status:"success"`、`record_count`、`record[].bible_text`；文本中"全能的　神"含 U+3000，§13.4 的规范化规则针对的就是这个。
- 本地分支为 `master`（§20 第2步需改名）。
- Chrome 路径存在；gh 2.88.1；Python 3.11.9。
- 上一项目 data.js 的 APOS/NIC_SPLIT 行带 `p` 字段（f/s/h/c），可按 §8.1 映射；上一项目 style.css 第25行 body 有 `overflow-x:hidden`，迁移时须删除（设计已注明）。
- 地图插图几何：5×（250 单位/度）时插图宽 175、高 300，与 x10–185、y10–310 吻合；5 个迦南地点都在 lon 34.7–35.4、lat 31.15–32.35 内；埃及 (62.5, 407.5) 与迦南区域 (280, 250) 都不在插图内；伯特利→埃及路线在 x=185 处 y≈343，不穿过插图；伯特利—摩利亚插图内间距 37.5 单位。
- CCI 网站没有诗歌页面（hymns/19 实测 404），设计不引诗歌出处是对的。

## 未核实或有误的假设

- **有误**：§18/§16 认为 livecheck 负责 cci.json 真实性、会因"网络失败"出错。实际上现有 livecheck.py 只读本地 HTML，且只覆盖少数条目（见发现 4）。
- **有误**：§14 第12步 (b) 能查出"改一个字"的裸引号片段（验收 2c）。6–15 字片段大多漏检（见发现 1）。
- **有误**：§21 中"BC 34 约 1200 字"，实际约 827 字。
- **有误/缺失**：build_cci "同步支持" lf，现有脚本是白名单输出，不会自动包含 forms（见发现 3）。
- **未核实**：Q4，即无头 Chrome `--window-size=360,…` 是否会被钳制。设计已有 Playwright 兜底，可接受。
- **未核实**：Q10，即 `https://surge.surge.sh/token` 能否用 Basic 认证换取令牌。设计有方案 B 兜底，可接受。
- **未核实**：`surge@0.23.1` 在 npm 上存在。本次未联网查询 npm，沿用设计的说法。
- **未核实**：组织 `08-Ser-KiroCC-Je-Personal-20261003` 是否允许启用 Pages、当前 gh 账号是否有建库权限。设计已规定失败时停止并报告。
- **未核实**：各外站（prca.org、canrc.org 等）页面的具体主张。设计已要求撰写前实际访问，可接受。
