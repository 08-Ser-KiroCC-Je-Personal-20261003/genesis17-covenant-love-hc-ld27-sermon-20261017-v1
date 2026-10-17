# 创世记17章讲章网站 · 需求与技术设计（v3 · 2026-10-17）

> 题目：主与我们建立爱的关系 ｜ 读经：创世记 17 章 ｜ 要理：海德堡要理问答 主日27（问72–74）
> 项目目录：`genesis17-covenant-love-hc-ld27-sermon-20261017-v1/`
> 版本说明：v3 为第二轮评审修订版，逐条回应 `.agents/tasks/design-review.json`（v2 评审：CHANGES_REQUESTED，HIGH 1 / MEDIUM 6 / NIT 6，共 13 条），回应见 §24。第一轮 20 条意见的回应保留在 §23。

---

## 第一部分 · 需求

### 1. 摘要

制作一个欧陆改革宗（Continental Reformed）讲章学习网站。经文为创世记17章，教义锚点为海德堡要理问答主日27，按讲章四要点展开："这圣约：出于神／由宝血印证／包括我们的儿女／呼召我们凭信心回应"。内容包括：真实历史背景、在整本圣经中的位置、逐节解经、多视角解读、四重闭环（救赎历史／圣约神学／圣经神学／罪—救赎—感恩）、讨论题与答案分析、拓展与总结、记忆模块，以及三大普世信经背诵版与深度对比。所有信经、三项联合信条及 CCI 仪文原文逐字取自 ccifellowship.org。构建时自动核对：已标注的引文要逐字相符，未标注的"孤儿引文"也会被查出。站点为纯静态多页、响应式、毛玻璃高级 UI，托管于新建 GitHub 公开仓库，部署到 GitHub Pages 与 surge.sh，README 列出 3 个链接。

### 2. 功能需求

**FR-1 讲章正文（index.html）**
- FR-1.1 礼拜程序面板：按用户给出的次序展示 5 首诗歌：圣诗第19首、韵诗第25篇1–5节、韵诗第30篇、韵诗第1篇、圣诗第9首。每首只显示编号；韵诗另加"对应圣经：诗N"和一行作者撰写的主题关联说明；圣诗只写"礼拜位置：…"的礼拜功能说明，不写主题。不出现歌词、曲名、出处说法或外链（§9.1）。
- FR-1.1b 海德堡要理问答主日27 集中呈现：在 `core` 后设 `#ld27` 小节，连续展示问72、73、74 三张逐字卡片与问答逻辑流程图（§9.3a）。
- FR-1.2 历史背景：作者（摩西）；原受众（旷野中的以色列）；年代（约主前2000年，注明早期/晚期年代学的不确定性）；处境（亚伯兰99岁、以实玛利出生后13年）；上下文（创12–22亚伯拉罕叙事循环，关联创12、15、16、18、21、22）；为何而写；古近东立约背景。
- FR-1.3 本质核心一句话，以及整本圣经中的位置：创3:15→挪亚→亚伯拉罕→西奈→大卫→耶31新约→基督→罗4/加3/西2:11–12/徒2:39/林前7:14/来9→启21:3。另附类似经文核心对照表。
- FR-1.4 先看整体（结构图、关键词频），再看局部（逐段解经）。关键词：我是全能的神、立约、永远的约、作你和你后裔的神、记号、割礼、剪除。
- FR-1.5 四要点，每点固定四块：释经／教义／信条锚点（HC/BC/CoD 逐字引用，要点三另含 CCI《婴儿洗礼仪文》）／应用。
- FR-1.6 多视角：救赎历史、圣约神学、圣经神学、系统神学、教牧家庭、礼拜仪式。
- FR-1.7 四重闭环可视化。其中罪—救赎—感恩闭环对应海德堡三部分。
- FR-1.8 ≥8 道讨论题（数据在 `G17.DISCUSS`），每题含详细答案分析，可折叠。
- FR-1.9 拓展：婴儿洗礼争议、割礼与洗礼对照、圣约与拣选关系。
- FR-1.10 总结列表与总结表格。
- FR-1.11 记忆模块：助记口诀、翻转闪卡（动画）、关键经文背诵卡、一页速记（可打印）。

**FR-2 三信经页（creeds.html）**
- FR-2.1 使徒信经、尼西亚信经、亚他那修信经的干净阅读/背诵版。正文只由 app.js 从数据渲染，HTML 中不写死任何信经正文。
- FR-2.2 背诵模式：全文／首字提示／遮盖自测（点击逐行显隐）／逐行显示／字号切换（小中大）／打印／朗读。
- FR-2.3 深度对比：异同、各自解决的历史问题、为何需要三份而非一份，配对比表与图示，并关联讲章主题（三一神的圣约信实）。

**FR-3 信条原文页（confessions.html）**：本站引用的全部 HC/BC/CoD/仪文条目与 CCI 简介，以全文卡片呈现（问、答、经文出处、CCI 原文链接），分组展示并提供页内搜索。

**FR-4 共享 UI**：可隐藏的详细目录（桌面侧栏／移动抽屉）、scrollspy 高亮、阅读进度条、返回顶部、明暗主题、跨页顶部导航、重点/难点配色图例。

**FR-5 可视化与多媒体**
- 亚伯拉罕行程内联 SVG 地图：主图共 9 个 `.place` 标记，即 8 个地点（吾珥、哈兰、示剑、伯特利、埃及/孟菲斯、希伯仑/幔利、别是巴、摩利亚）加 1 个区域标记"迦南"。下方始终显示 HTML 图例 `ol.map-legend`。
- 另有表格、内联 SVG/emoji 图标、流程图、思维导图、时间线、动态图（SVG/CSS 动画）、闭环环形图。
- 多媒体＝浏览器 speechSynthesis（zh-CN）朗读，覆盖三信经背诵行与关键经文背诵卡。无 zh-CN 语音时隐藏按钮。不引入音视频文件。

**FR-6 来源与校验**：CCI 引文必须逐字，且每条带可点击的来源 URL。CCI 原文只能用 `<q data-cite>` 或空的 `.cq[data-src]` 占位书写；裸引号、`q.ext`、`blockquote` 或写死在 `.cq` 内的 CCI 原文都按构建失败处理。其他网站只释义并加链接，单处逐字短引按 §13.5 字数限制。威斯敏斯特准则作为长老会改革宗补充，必须显式标注。构建时自动校验，不符则失败；部署前联网复核本站实际引用的全部 CCI 条目（§14a）。

**FR-7 布局校验**：三页面分别在 360/768/1024/1440 px 四种宽度下校验，要求无横向溢出、无重叠、无裁切、SVG 文字不过小。

**FR-8 仓库与部署**：新建公开仓库 `08-Ser-KiroCC-Je-Personal-20261003/genesis17-covenant-love-hc-ld27-sermon-20261017-v1`，默认分支 `main`；部署到 GitHub Pages；surge.sh 域名 `genesis17-covenant-love-hc-ld27-sermon-20261017-v1.surge.sh`；README 列出 2 个部署链接和 1 个仓库链接。仓库中不得出现任何密码、令牌或 surge 账号邮箱。

### 3. 非功能需求

- NFR-1 性能：不依赖任何第三方 CDN 脚本或字体。三页面的 HTML+CSS+JS 合计 < 400 KB（不含 cci.js、bible.js）。首屏无阻塞外链。
- NFR-2 流畅：动画只用 transform/opacity。滚动监听用 rAF 节流加 IntersectionObserver。`prefers-reduced-motion: reduce` 时关闭全部非必要动画与平滑滚动。
- NFR-3 可访问性：
  - 每页只有一个 h1，h2/h3 不跳级；
  - SVG 带 `role="img"` 与 `<title>`/`aria-label`；
  - 目录可键盘操作（Tab/Enter/Esc），焦点可见；
  - 明暗两主题下正文对比度均 ≥ 4.5:1，由自检 `lowContrast` 计数校验（§13.10），layoutcheck 明暗各跑一次。
  - 注：完整的 WCAG 合规需要用辅助技术做人工测试并经专家审查，本项目只做自动检查加人工抽查。
- NFR-4 兼容：最新两版 Chrome/Edge/Safari/Firefox，iOS Safari 15+。不支持 backdrop-filter 时降级为半透明纯色。
- NFR-5 安全：无表单、无后端。data.js 字符串只允许白名单标签（§13.5）。凭据不写入任何文件或提交记录。

### 4. 验收标准

1. 仓库根目录存在 `index.html`、`creeds.html`、`confessions.html`，三页共享 `assets/style.css`、`assets/app.js`、`assets/cci.js`、`assets/data.js`、`assets/bible.js`。
2. `python tools/build.py` 退出码为 0。以下任一人为改动都会使退出码非 0，并打印出错文件、位置与片段：
   - (a) 任一 `<q data-cite>` 中改一个字；
   - (b) 在正文或 data.js 中用裸引号写一段 ≥6 个 CJK 字的 CCI 原文；
   - (c) 在 (b) 的裸引号片段中改一个字；
   - (d) 用裸引号写一段已收录的经文；
   - (e) 在 creeds.html 背诵容器内写死文字。
3. `?check=1` 自检输出 `citeNoLink=0`：index.html 中每个 `<q data-cite>` 与 `.cq[data-src]` 都显示可点击的 ccifellowship.org 来源链接。
4. 诗歌面板恰好 5 项，次序与用户给出的一致。页面中不出现歌词，也不出现"日内瓦""圣诗部分""待核实"字样（verify 第10步检查）。
5. 四要点各含"释经/教义/信条锚点/应用"四个子块（自检 `points=4 blocks=16`）。
6. 要点二含 `hc:72`、`hc:73`、`bc:34`（data-p=1）卡片。要点三含 `hc:74`、`cd:section1:17`、`bc:34`（data-p=4）卡片，以及至少 1 张 `lf:1` 卡片（降级条件见 Q9）。
7. 讨论题 ≥ 8 道，由 `G17.DISCUSS` 渲染，每道有可展开的答案分析（自检 `discuss>=8`）。
8. 四个闭环 SVG 都存在，且末段路径带 `data-closes`，终点与起点节点中心距离 ≤ 6 单位（自检 `loops=4 loopsClosed=4`）。
9. 地图主图含 9 个 `.place`（8 个地点加 1 个区域，插图副本不计）。图例 `ol.map-legend` 有 9 项。点击或聚焦任一标记、图例项，信息面板显示对应经文出处（自检 `mapMarkers=9 legend=9`）。
10. verify 输出 `APOS/NIC/ATH == CCI: True`；creeds 页自检 `reciteMatch=1`。
11. 背诵页的全部模式与操作可用，字号切换在刷新后保留。
12. `python tools/layoutcheck.py` 覆盖 3 页 × 4 宽度共 12 种组合，全部满足 `vw == W`、`docW <= vw`、`issues=0`（issues 含 OVERFLOW/OVERLAP/FLIPCLIP/CLIP/SVGTEXT），并生成 12 张截图。style.css 中 html/body 不含 `overflow-x:hidden|clip`（verify 检查）。
13. 目录在桌面可隐藏/恢复；在 ≤ 960 px 时为抽屉，按 Esc 关闭，焦点回到目录按钮。
14. 开启系统"减少动态效果"后，页面没有自动循环动画。
15. GitHub Pages 与 surge.sh 两个公开链接返回 200，三页面均可访问；README 含 3 个链接，不含邮箱。
16. 凭据扫描：`[bool]($h.Contains($pw))` 输出 False，且 `ghp_|github_pat_|gho_|SURGE_TOKEN=` 在全历史中无匹配（§18）。
17. `python -m unittest discover tools/tests` 全部通过。

### 5. 范围外

- 不提供诗歌歌词、乐谱、曲名、音频或诗歌出处说明（版权与准确性无法核实）。
- 不提供圣经全文阅读器，只引用创17及讲章用到的关键经节。
- 不做后端、评论、登录、统计埋点。
- 不做 Netlify 部署（用户只要求两个平台）。
- 全站只用简体中文，不提供其他语言。

---

## 第二部分 · 技术设计

### 6. 总览

站点沿用上一项目 `three-ecumenical-creeds-reformed-study-20261014-v2` 已验证的架构：纯静态 HTML，加一份手写 CSS 和一份原生 JS。CCI 原文由 `tools/cci/build_cci.py` 从 `cci.json` 生成 `assets/cci.js`，页面用 `data-src="hc:74"` 占位，由脚本渲染逐字卡片；正文短引文用 `<q data-cite>` 书写，由 `verify.py` 核对。

与上一项目相比，有以下变化：
- 拆为三页，共享资源。
- 去掉 Leaflet 与 Mermaid 两个 CDN 依赖，地图、流程图、思维导图改为内联 SVG 与 CSS 绘制。
- data.js 改为严格 JSON，信经背诵正文与讨论题全部由数据渲染。
- 引文校验收紧：已标注引文必须出现在所标注的那一条目中，并新增孤儿引文检测，用来发现未标注或被改动的 CCI 原文与经文。
- 新增 CCI《婴儿洗礼仪文》数据（`lf:*` 键）。
- 新增 Chrome 无头布局校验，检测溢出、裁切和 SVG 小字。
- 由 `tools/build.py` 统一入口。

### 7. 技术栈（锁定）

| 层 | 选择 | 说明 |
|---|---|---|
| 页面 | 手写 HTML5，`lang="zh-CN"` | 三页：index / creeds / confessions |
| 样式 | 单文件 CSS（自定义属性、Grid/Flex、`clamp()`、`backdrop-filter`、`@supports`、`@media (prefers-reduced-motion)`、`@media print`） | 从上一项目 style.css 迁移变量与组件，但删除 html/body 上的 `overflow-x:hidden`（§13.1） |
| 脚本 | 原生 ES2017 JS（IIFE，无框架、无打包） | app.js 按 `document.body.dataset.page` 启用模块 |
| 数据 | `assets/data.js` = `window.G17 = <严格 JSON>;`（单行赋值） | §8.1 |
| 图形 | 内联 SVG + CSS 动画 | 地图、闭环、Hero 圣约之环、时间线；思维导图用嵌套列表 + CSS；流程图用 HTML 盒子 |
| 多媒体 | Web Speech API `speechSynthesis` | 无音视频文件 |
| 字体 | 系统字体栈（沿用上一项目 `--font`/`--serif`） | 不加载网络字体 |
| 工具 | Python 3.11 标准库（`json`、`html.parser`、`difflib`、`urllib`、`subprocess`、`unittest`） | build / verify / layoutcheck / fetch_bible / add_forms / 测试 |
| 布局校验 | 本机 Chrome（`C:\Program Files\Google\Chrome\Application\chrome.exe`，已确认存在），`--headless=new --dump-dom` / `--screenshot` | 不新增 npm/pip 依赖。唯一例外：Q4 触发时允许本机 `pip install playwright==1.47.0`，只用于校验，不写入任何仓库依赖文件 |
| 部署 | `gh` CLI 2.88.1（已确认）、`npx --yes surge@0.23.1`（npm 上已确认存在） | GitHub Pages 从 `main` 根目录发布 |

### 8. 文件结构

```
genesis17-covenant-love-hc-ld27-sermon-20261017-v1/
├─ index.html            讲章（主页面）
├─ creeds.html           三信经背诵 + 深度对比（正文由 JS 渲染）
├─ confessions.html      本站引用的 HC/BC/CoD/仪文/简介 全文卡片
├─ README.md             3 个链接 + 构建/校验/部署说明
├─ .nojekyll  .gitignore  .surgeignore
├─ assets/
│  ├─ style.css          共享样式
│  ├─ app.js             共享交互（按页面启用模块）
│  ├─ cci.js             生成文件，勿手改（build_cci.py）
│  ├─ bible.js           生成文件，勿手改（fetch_bible.py）
│  └─ data.js            window.G17 = <严格JSON>;
└─ tools/
   ├─ build.py           统一入口：build_cci → verify → (可选 --layout) layoutcheck
   ├─ layoutcheck.py     Chrome 无头多宽度校验 + 截图
   ├─ cci/
   │  ├─ ccilib.py       新增：content/clean/paras/refs/page_title 公共函数（从 compile.py 抽出）
   │  ├─ compile.py      改为 import ccilib（行为不变）
   │  ├─ add_forms.py    新增：抓取仪文 1、2 并合并进 cci.json["forms"]
   │  ├─ build_cci.py    重构为 render(d)->str；__main__ 写文件
   │  ├─ verify.py       改写（§14），逻辑在 run(site_dir)->(fails,warns)
   │  ├─ fetch.py crawl.py livecheck.py（livecheck 加仪文）  cci.json  FETCH_NOTES.md
   ├─ bible/fetch_bible.py, bible.json
   └─ tests/test_verify.py, tests/fixtures/…
```

`.gitignore` 追加以下条目：`tools/layout/`（截图输出）、`.agents/`、`.env`、`*.token`、`tools/bible/*.raw.json`、`tools/cci/*.html`、`tools/cci/*.txt`、`__pycache__/`。

`.surgeignore` 使用唯一一份固定清单，§20 同此：

```
tools/
.agents/
.git/
.gitignore
.surgeignore
README.md
```

#### 8.1 data.js 格式（严格 JSON）

- 文件只有一条语句：`window.G17 = {...};`，其中 `{...}` 必须是 `json.loads` 可解析的严格 JSON：双引号、无尾逗号、无注释。注释写在 README 中。
- verify 的解析方式：读文件 → 去首尾空白 → 检查前缀 `window.G17 = ` 与末尾 `;` → 截取中间部分 → `json.loads`。任何一步失败 → FAIL `data.js 不是 window.G17 = <JSON>; 格式`。

顶层键（全部必需）：

| 键 | 结构 | 用途 |
|---|---|---|
| `CARDS` | `[{q, a, ref}]`，16 项 | 翻转闪卡 |
| `DISCUSS` | `[{id, q, a:{points:[..], verses:[..], creeds:[..], misread, oneLine}}]`，≥8 项 | 讨论题，由 app.js 渲染为 `<details>` |
| `PLACES` | `[{id, n, name, lat, lon, kind:"point"|"region", refs, event, inset:bool}]`，9 项 | 地图与图例 |
| `MAP_SHAPES` | `[{id, d, cls}]` | 底图路径 |
| `ROUTE` | `["ur","harran","shechem","bethel","egypt","bethel","hebron","beersheba","moriah"]` | 行程顺序 |
| `TIMELINE` | `{covenant:[..], abraham:[..]}` | 两条时间线 |
| `APOS` | `[{t, c}]`，c ∈ `father|son|spirit|church` | 使徒信经背诵分行 |
| `NIC_SPLIT` | `[{t, c}]` | 尼西亚信经背诵分行 |
| `BIBLE_REFS` | `["创17:1-27","罗4:9-12",…]` | fetch_bible 的抓取清单 |
| `CITED` | `["hc:1",…,"lf:1","intro:hc",…]` | 信条页渲染清单与覆盖校验 |

字符串叶子允许的内联标签白名单：`q`（只允许 `data-cite`/`data-bible`/`data-p` 属性）、`b`、`strong`、`em`、`br`、`span`（只允许 `class`）。出现其他标签或属性 → verify FAIL。app.js 渲染时用 `innerHTML`，因为数据是作者可控、并且经 verify 白名单检查过的内容。

APOS/NIC_SPLIT 迁移：从上一项目 data.js 取各行 `t`，按 `p` 字段映射色类（`f→father`、`s→son`、`h→spirit`、其余→`church`），只保留 `{t, c}`。上一项目的 `k`（注释）字段不迁移，因为其中含裸引号短语。迁移后由新 verify 第 6 步重新证明拼接相等，不沿用上一项目的结论。

### 9. 讲章内容设计（index.html）

讲章采用欧陆改革宗"经文—教义—信条—应用"形式，以海德堡要理问答第2问的三段（罪／救赎／感恩）作为全篇闭环框架：
- 罪：引言揭示"人想自己成全应许"（创16）的罪与无能；
- 救赎：四要点展开神在恩典之约中的救赎；
- 感恩：结论落在"在我面前作完全人"（17:1）的感恩生活。

经文短语一律写成 `<q data-bible="创17:1">`，下同。章节与锚点 id 固定如下（目录、scrollspy、校验都依赖这些 id）：

| # | id | 标题 | 主要内容 |
|---|---|---|---|
| 0 | `hero` | 主与我们建立爱的关系 | 题目、经文、主日27、四要点徽章、一句话核心、Hero 圣约之环 SVG（§10.6） |
| 1 | `liturgy` | 礼拜程序 | §9.1 |
| 2 | `background` | 真实背景 | §9.2 + 地图 |
| 3 | `core` | 本质核心 | §9.3 |
| 4 | `canon` | 在整本圣经中的位置 | §9.4 时间线 + 圣约公式表 |
| 5 | `parallels` | 类似经文核心对照 | 表格 |
| 6 | `overview` | 跳出框架看整体 | 结构图、关键词频、交错结构、思维导图 |
| 7 | `exegesis` | 逐段解经 | 6 段 + 关键词卡 |
| 8–11 | `p1`…`p4` | 四要点 | §9.6 |
| 12 | `angles` | 多视角解读 | §9.7 |
| 13 | `loops` | 四重闭环 | §10.4 |
| 14 | `discuss` | 讨论题与答案分析 | §9.8 |
| 15 | `extend` | 拓展 | §9.9 |
| 16 | `summary` | 总结列表与表格 | §9.10 |
| 17 | `memory` | 记忆模块 | §9.11 |
| 18 | `sources` | 出处与参考 | 全部来源 URL 静态列表 |

#### 9.1 礼拜程序面板（只列编号，不写歌词，不写出处说法）

礼拜次序标题为"欧陆改革宗主日礼拜次序（示意）"，下面写一行说明："各教会次序不尽相同，此为示意"。不把这一次序归属于任何特定宗派网站。实现者如果在 canrc.org/urcna.org 找到并实际阅读了礼拜次序页面，可以加"参考"链接；找不到就不加。

次序：宣召与问安 → 🎵 圣诗第19首 → 十诫 → 认罪与赦罪宣告 → 🎵 韵诗第25篇 1–5节 → 祷告 → 读经：创世记17章；要理：海德堡主日27 → 🎵 韵诗第30篇 → 讲道 → 🎵 韵诗第1篇（回应）→ 奉献、代祷 → 🎵 圣诗第9首 → 祝福。

诗歌卡片字段：

| 显示 | 圣诗第19首 | 韵诗第25篇 1–5节 | 韵诗第30篇 | 韵诗第1篇 | 圣诗第9首 |
|---|---|---|---|---|---|
| 对应圣经 | — | 诗25 | 诗30 | 诗1 | — |
| 关联说明（作者撰写） | 开启敬拜：神召聚他立约的子民 | 立约之慈爱与"亲密"——爱的关系（诗25:10、14 用 `<q data-bible>` 时需列入 BIBLE_REFS） | 从哀哭到喜乐的感恩 | 两条路：守约蒙福／违约灭亡，对应17:14"剪除" | 差遣：带着约的应许回到生活 |

诗歌卡片不显示曲名、"日内瓦""《敬拜手册》圣诗部分""待核实"等字样，也不加外链。

#### 9.2 真实背景

用一组"六问卡"（作者／受众／年代／处境／上下文／为何而写）加一张时间轴呈现：

- 作者：摩西（传统与改革宗立场，依据：出17:14；24:4；约5:46；路24:27）。另设一张"难点"卡，说明现代批判学的底本说，并给出改革宗回应要点（释义，如有实际读过的 wts.edu / crts.edu 文章则加链接）。
- 原受众：出埃及后在旷野、即将进入迦南的以色列。他们要从创17得知：自己为何受割礼、为何是神的子民、迦南为何是"永远的产业"（17:8）。
- 年代：约主前2000年前后。按王上6:1 与出埃及早期年代（约主前1446年）推算，亚伯拉罕约生于主前2166年，99岁约在主前2067年。若采用晚期出埃及年代，整体后移约150–200年。页面明确标注"约数，学界未定"。
- 处境：
  - 亚伯兰86岁生以实玛利（16:16），99岁蒙神显现（17:1），中间13年圣经沉默；
  - 以实玛利此时13岁（17:25），撒莱约89岁（参17:17"九十岁"）；
  - 人用夏甲的办法"帮神成就应许"失败之后，神亲自显现。
- 上下文：用一张交错结构图呈现创12–22 亚伯拉罕叙事循环：
  - 12 呼召与应许（地、后裔、福）
  - 15 以血立约（劈开的牲畜、神独自经过）
  - 16 夏甲与以实玛利（人的办法）
  - **17 立约记号、改名、以撒之应许**
  - 18 幔利三客、"耶和华岂有难成的事"
  - 21 以撒出生
  - 22 摩利亚献以撒（"神必自己预备"）
- 为何而写：
  1. 向以色列宣告神约的主动与信实；
  2. 解释割礼记号的来源与意义；
  3. 以"剪除"警告背约；
  4. 预备西奈之约与应许之地。
- 古近东立约背景：用对照表比较两种模型，即赫人宗主—附庸条约（序言自称、历史回顾、条款、见证、祝福与咒诅）与"王室赐地之约"。
  - 创15 更接近赐地之约：宗主自我咒诅，参耶34:18。
  - 创17 加入了对附庸的要求（"作完全人""遵守我的约"）与记号。
  - 割礼在埃及等地也有，但创17 赋予它全新意义：第八日行、全家都受（含买来的）、作为属神之约的记号。
- 地图：§10.1。

#### 9.3 本质核心

一句话核心（金句卡，金色底纹，作者语句，不加引号）：全能的神主动与罪人立永远的约，以流血的记号印证"我要作你的神"，把信徒的儿女一并纳入，并呼召我们凭信心行在他面前。

辅以"约的四个W"：
- 谁立：神（17:2）；
- 凭什么印证：记号，从割礼到洗礼，指向基督的血；
- 包括谁：你和你的后裔（17:7）；
- 要什么回应：行在我面前（17:1、9）。

#### 9.4 在整本圣经中的位置

横向时间线（移动端改纵向）。每个节点注明经文、立约对象、记号、应许，以及与创17的关系：

1. 创3:15 原始福音
2. 创9 挪亚之约（虹）
3. 创12/15/17/22 亚伯拉罕之约（割礼）
4. 出19–24 西奈之约（出24:8 立约的血）
5. 撒下7 大卫之约
6. 耶31:31–34 新约应许
7. 路22:20 用我血所立的新约
8. 罗4:9–12 割礼是因信称义的印证
9. 加3:7–9、16、29
10. 西2:11–12 基督的割礼与洗礼
11. 徒2:38–39 应许归你们和你们的儿女
12. 林前7:14 儿女是圣洁的
13. 来9:15–22 无血不得赦免
14. 启21:3 神要亲自与他们同在

另配一张"圣约公式"表，列出创17:7–8、出6:7、利26:12、耶31:33、结37:27、林后6:16、启21:3，显示"我要作你们的神，你们要作我的子民"从创17 贯穿到启21，形成经文闭环。本节嵌入 `hc:19`、`bc:17` 卡片。

#### 9.5 跳出框架看整体，再逐段解经

**整体（overview）**
- 结构图（六段）：
  - 1–2 显现与呼召
  - 3–8 应许：多国之父、改名、永远的约、作你神、迦南地
  - 9–14 记号：割礼、第八日、剪除
  - 15–16 撒莱改名撒拉
  - 17–22 亚伯拉罕的笑、以撒之名、以实玛利的福
  - 23–27 "正当那日"全家受割礼
- 关键词频条形图：数值由构建时对 bible.json 创17 `text` 自动统计。评审已实测"约"出现 13 次，"血"出现 0 次。
- 交错结构提示：神的话（1–21）包着人的顺服（23–27）。

**逐段（exegesis）**：每段卡片固定五个字段：经文（`blockquote.bible[data-ref]`，运行时填充）／原文要点／释义／"字字珠玑"金句（作者语句）／一个思考问题。

关键词卡（翻转式小卡）：
- 我是全能的神（El Shaddai，17:1；参出6:3；罗4:19）。
- 立约：17:2 用 natan（赐下），17:7 用 heqim（坚立）；17:14 的"剪除"（karat）与"切约"同根，形成文字对照。
- 永远的约（17:7、13、19）。
- 作你和你后裔的神（17:7–8）：约的心脏是关系，即"爱的关系"。
- 记号（17:11，和合本作"证据"），对照罗4:11"印证"。
- 割礼：第八日、男丁、家里生的和买来的。
- 剪除（17:14）：难点卡列出三种解释（处死／被逐出群体／由神亲自施行），取"被逐出约民、在神面前担罪"的主流理解，并说明理由。
- 改名：亚伯兰→亚伯拉罕（多国之父，17:5）；撒莱→撒拉（17:15）。

#### 9.6 四要点（每点固定四块：📖释经 ／ 🧭教义 ／ 🛡信条锚点 ／ 🌱应用）

信条锚点块一律用 `.cq[data-src]` 渲染逐字卡片。正文中需要点出关键短语时用 `<q data-cite>`，不得用裸引号。

**要点一 · 这圣约出于神（`p1`，`--p1` 金）**
- 释经：把17:1–8 中以神为主语的动作（显现、说、立、使、赐、作）逐一标亮；17:3 亚伯兰"俯伏在地"，说明约不是谈判。对照创15 神独自经过肉块之间。
- 教义：恩典之约在起源上是"单方设立"：起源、内容、成全都出于神。拣选是约的根基（`<q data-cite="cd:section1:8">` 摘取其中"旧约之下还是在新约之下"一句）。三一神的约：父定意、子作中保、圣灵施行（连到三信经页）。
- 信条锚点：`bc:17`、`hc:19`、`cd:section1:7`、`cd:section1:8`、`hc:54`。
- 应用：安慰在于神抓住我们，不在于我们抓住神。面对"13年的沉默"与人自己的"夏甲方案"，要回到神的话。

**要点二 · 这圣约由宝血印证（`p2`，`--p2` 红）**
- 释经（诚实标注）：创17 经文本身没有"血"字（已实测）。"血"的连接来自正典整体：创15 劈开的牲畜、出4:24–26、出24:8、来9:18–22。割礼是流血的记号，指向必须除去的污秽（申10:16；30:6）。
- 教义：
  - 圣礼是可见的记号与印证（`hc:66`、`bc:33`）；
  - 线索：割礼之血 → 基督宝血 → 洗礼；
  - 基督成全并终止了流血的礼仪（`bc:34` 首段）；
  - CoD 第二项教义第8条讲十字架上的宝血坚立新约，用 `<q data-cite="cd:section2:8">` 引用；
  - 外在的水不能洗罪（`hc:72`），神藉记号使我们确信（`hc:73`）。
- 信条锚点：`hc:72`、`hc:73`、`hc:66`、`hc:69`、`bc:33`、`bc:34`（data-p="1"）、`cd:section2:8`。
- 流程图（§10.3）："血的线索"：创15 → 创17 → 逾越节 → 西奈 → 路22:20 → 西2:11–12 → 圣餐。
- 应用：受洗者的确据不在水，也不在自己的感受，而在基督已流的血。

**要点三 · 这圣约包括我们的儿女（`p3`，`--p3` 青）**
- 释经：
  - 17:7 你和你世世代代的后裔；
  - 17:12 第八日行割礼：婴孩不能表达信心，却受约的记号；
  - 17:13 约的施行范围是家；
  - 17:20–21 以实玛利蒙福，但约立于以撒：在约中不等于自动得救（罗9:6–8）。
- 教义：
  - 婴儿洗礼的根据是约的统一性：同一个恩典之约，施行方式不同；
  - 割礼已被洗礼取代（`<q data-cite="hc:74">` 摘末句）；
  - CoD 1.17 论死于婴幼期的信徒儿女；
  - 驳重洗派（`bc:34` 第4段）。
- 信条锚点：
  - `hc:74`、`cd:section1:17`、`bc:34`（data-p="4"）、`bc:15`；
  - CCI《婴儿洗礼仪文》：`lf:1` 卡片 1–2 张。段落由实现者在 add_forms.py 打印的段落清单中选取，优先选父母誓约问题段与"约的两个部分"段，用 `data-p` 指定。
  - 威斯敏斯特补充框（`.callout.wsm`，标"长老会改革宗补充"）：WCF 28.4、WSC 95、WLC 166，释义并加 opc.org 链接。
- 应用（教牧家庭）：父母在洗礼中的誓约（对照仪文卡片）、家庭敬拜、要理问答教导、教会全体的责任，以及对未信主子女的盼望与呼召。

**要点四 · 这圣约呼召我们凭信心回应（`p4`，`--p4` 绿）**
- 释经：
  - 17:1 你当在我面前作完全人；
  - 17:9 遵守我的约；
  - 17:14 违约剪除；
  - 17:23 正当那日；
  - 罗4:11：信心在先，记号印证。
- 教义：
  - 恩典之约在施行上是"双方施行"：约有神的应许与我们的义务两个部分。若仪文中有对应段落，可用 `<q data-cite="lf:1">` 摘引。
  - 信心是领受的工具（`bc:22`、`hc:21`、`hc:60–61`）。
  - 违约警告是真实的（来10:28–29；罗11:20–22），但人不是靠行为得救。
  - 欧陆改革宗内部表述不同：CanRC/URCNA 多讲约的应许与要求；PRCA 强调约是神与选民之间无条件的友谊之约。两种表述只释义、并列呈现，撰写前须实际访问 prca.org 等页面。
- 信条锚点：`hc:21`、`hc:60`、`hc:61`、`bc:22`、`hc:86`、`hc:1`。
- 应用：从17:17 的"笑"到17:23 的"正当那日"；以诗篇1篇的两条路作自省清单（只保存在本地状态，不存储）。

#### 9.7 多视角解读（`angles`）

六张视角卡：桌面端用 tab 切换（`role="tablist"`，方向键切换），移动端为手风琴。每张卡回答四项：核心问题／创17的答案／关键经文／信条连接。

1. 救赎历史：承接创15，开启出19 与加3。
2. 圣约神学：
   - 行为之约（创2；BC 14 释义；WCF 7.2 补充）与恩典之约；
   - 恩典之约"单方设立、双方施行"；
   - 约是统一的，施行方式多样（割礼／洗礼）；
   - 注明：HC/BC 不使用"行为之约"一词，WCF 明确使用，PRCA 不接受这一表述，作为改革宗内部差异说明。
3. 圣经神学：两条主题线："记号"（虹→割礼→安息日→洗礼/圣餐→新天新地），"后裔"（创3:15→以撒→大卫→基督→教会）。
4. 系统神学：神论、圣礼论（记号与所表之事的圣礼联合）、教会论、救恩论。
5. 教牧家庭：父母、教会、儿女三方的约的责任。
6. 礼拜仪式：主日礼拜中的洗礼仪式。用 `lf:1` 说明仪文如何在会众面前重申创17 的应许，包括仪文中的认罪、祝福等环节。

#### 9.8 讨论题（`discuss`，10 题，数据在 `G17.DISCUSS`）

由 app.js 渲染为 `<details>`。答案分析固定五段：要点 → 经文 → 信条 → 常见误解 → 一句话结论。HTML 中只有容器 `<div id="discuss-list" data-render="discuss">` 与 `<noscript>`（提示需开启 JS，并附 confessions.html 链接）。答案中凡涉及 CCI 原文，一律写 `<q data-cite>`。例如第3题的"与血有关的割礼"写成 `<q data-cite="bc:34">与血有关的割礼</q>`。

1. 为什么神在亚伯兰99岁、以实玛利13岁时才显现立约？
2. 创15 与创17 是两个约还是一个约？
3. 创17 没有"血"字，凭什么说"由宝血印证"？
4. 外在的水能洗罪吗？圣经为何称洗礼为"重生的洗"？（HC 72–73）
5. 婴孩没有信心，为何能受洗？重洗派最强的反对是什么？（HC 74；BC 34；徒16:15、33）
6. 割礼只给男丁，洗礼为何男女都受？（加3:27–28）
7. 以实玛利受了割礼却不承受约的应许，这说明什么？
8. 死于婴幼期的信徒儿女得救吗？依据是什么？（CoD 1.17）
9. "凭信心回应"是否让圣约变成有条件的交易？
10. 三一神如何在圣约中显出信实？三大信经与本章有何关系？

#### 9.9 拓展（`extend`）

- 婴儿洗礼争议：用四栏对照表比较改革宗、浸信会、罗马天主教（事效论）、路德宗。改革宗的区分点用 `<q data-cite="hc:72">` 与 `<q data-cite="bc:34">这一切不是洗礼之水所带来的功效</q>`。
- 割礼与洗礼对照表：设立者、时间、对象、是否流血、所表之事、经文。
- 圣约与拣选的关系：用同心圆图表示（HTML/CSS 嵌套圆，非 SVG 文字）。外圈为约的施行，内圈为拣选（`cd:section1:7`）；CoD 1.17 位于二者交汇处。

#### 9.10 总结（`summary`）

- 总结列表：四要点各一句，加一处 HC 关键短语（`<q data-cite>`）。
- 总结表：行为四要点，列为 {经文 / 教义 / 信条 / 罪 / 救赎 / 感恩} 六项。
- 思维导图（§10.5）。

#### 9.11 记忆模块（`memory`）

- 助记口诀（作者语句）：
  - 四要点：神立 · 血印 · 儿承 · 信应；
  - 数字口诀：99 · 13 · 8 · 1；
  - 主日27 三问：水不能、灵要确、儿也洗。
- 翻转闪卡：16 张（`G17.CARDS`），3D 翻转。reduced-motion 时改为淡入切换。键盘 Enter/Space 翻转。
- 关键经文背诵卡：创17:1、17:7、17:10–11、罗4:11、西2:11–12、徒2:39、启21:3。文本取自 bible.js，可遮盖/显示，带朗读按钮。
- 一页速记：A4 打印版（`@media print` 时只打印 `#memory`）。

### 10. 可视化设计

**总则（SVG 可读性）**
- 所有 SVG 都用 `viewBox` 加 `width:100%; height:auto`。
- 闭环图、Hero 圣约之环等非地图 SVG：viewBox 宽 ≤ 400，正文文字 ≥ 14 单位。在 360 px 视口下容器约 336 px，14 单位约等于 11.8 px。
- 流程图、思维导图、同心圆图用 HTML/CSS 实现，不用 SVG 文字。
- 自检 `SVGTEXT`：可见 `svg text` 的 `getBoundingClientRect().height < 10` 且所在 svg 没有 `data-small-ok` 时，计入 issues。只有地图主图带 `data-small-ok`，因为它的全部文字在 HTML 图例中都有等价内容。

**10.1 亚伯拉罕行程地图（`#map`，位于 `background`）**
- 投影：等距圆柱投影，经度 30–48°E、纬度 28–38°N 映射到 viewBox `0 0 900 500`，换算为 x = (lon−30)×50，y = (38−lat)×50。
- 底图为简化轮廓：地中海、红海北端、波斯湾北端、两河、尼罗河三角洲、约旦河/死海。路径数据在 `G17.MAP_SHAPES`。图注写"示意图，非精确测绘"。
- 主图共 9 个 `.place`（`<g class="place" tabindex="0" role="button" aria-label="…">`），图例编号与之对应：

  | n | id | 地名 | 坐标 | kind | 主图呈现 |
  |---|---|---|---|---|---|
  | 1 | ur | 吾珥 | 30.96N 46.10E | point | 编号圆点 r=16、数字 30 单位 + 地名 |
  | 2 | harran | 哈兰 | 36.87 39.03 | point | 同上 |
  | 3 | canaan | 迦南（区域） | 33.0 35.6 | region | 虚线椭圆 + 编号 + "迦南"；信息面板：创12:5–7、17:8 |
  | 4 | shechem | 示剑 | 32.21 35.28 | point | 小点 r=5（无数字），插图中有编号副本 |
  | 5 | bethel | 伯特利 | 31.93 35.22 | point | 同上 |
  | 6 | egypt | 埃及（孟菲斯） | 29.85 31.25 | point | 编号圆点 + 地名 |
  | 7 | hebron | 希伯仑/幔利 | 31.53 35.10 | point | 小点，插图中有编号副本；面板注"创17 可能发生于此一带（参13:18；18:1），经文未明说" |
  | 8 | beersheba | 别是巴 | 31.25 34.79 | point | 小点，插图中有编号副本 |
  | 9 | moriah | 摩利亚（耶路撒冷） | 31.78 35.23 | point | 小点，插图中有编号副本 |

- 迦南放大插图：放在左上角地中海区域，viewBox 内 x 10–185、y 10–310，放大 5×（250 单位/度），覆盖 lon 34.7–35.4、lat 31.15–32.35。
  - 已核算：插图范围内没有主图地点，Bethel→Egypt 路线在 x=185 处 y≈343，也不经过插图。
  - 5× 时相邻点最小间距约 37.5 单位（伯特利—摩利亚），r=16 的编号圆点不会重叠。评审提出的 3× 放大会让间距只有 22.5 单位，圆点重叠，所以改为 5×。
  - 插图有不透明底与边框，并用细线连到区域标记 3。
  - 插图内副本带 `aria-hidden="true"`，不带 tabindex，不计入 mapMarkers。鼠标点击副本时转发到主图对应 `.place`。
- 路线按 `G17.ROUTE` 绘制：吾珥→哈兰（创11:31）→示剑（12:6）→伯特利（12:8）→埃及（12:10）→伯特利（13:3）→希伯仑幔利（13:18）→别是巴（21:31–33）→摩利亚（22:2）。用 `stroke-dasharray`/`stroke-dashoffset` 分段动画，"播放行程"按钮依次高亮各段。reduced-motion 下直接显示完整路线。
- 图例 `<ol class="map-legend">`：始终显示（任何宽度），9 项，每项为 `<button>`，内容为编号、地名、经文、事件。与主图标记双向联动，点击或聚焦任一方都会高亮另一方并更新信息面板（`aria-live="polite"`）。
- ≤ 600 px 时，用 CSS 隐藏 SVG 内的 `.place-name` 地名文字（`display:none`，自检时因尺寸为 0 被排除），只保留编号。
- "放大查看"：`<dialog>` 内用 `<div style="overflow:auto">` 包住宽 200% 的同一 SVG 克隆，可横向平移。

**10.2 时间线**：两条时间线，桌面横向、≤ 768 px 纵向，用 CSS Grid 实现。
- 圣约时间线：§9.4。
- 亚伯拉罕生平：75岁（12:4）→ 86岁（16:16）→ 99岁（创17）→ 100岁（21:5）→ 175岁（25:7）。

**10.3 流程图**：HTML 盒子加 CSS 箭头，用 flex-wrap，窄屏自动转为竖排。
- 要点二"血的线索"。
- 主日27 问答逻辑：72 水不能 → 73 为何称重生之洗 → 74 婴孩也受。

**10.4 四重闭环（`loops`）**
- 每个闭环是一个 `<figure>`，内含 SVG（viewBox `0 0 400 400`，环半径 140）。节点为 `<circle id="L{k}n{i}">` 加 ≤ 7 个 CJK 字的标签（16 单位），节点之间是带箭头的弧形 `<path>`。
- 最后一段弧带 `data-closes="L{k}n1"`。自检用 `getPointAtLength(getTotalLength())` 取终点，与起点圆心比较，距离 ≤ 6 单位计为闭合。
- `<figcaption>` 为 HTML，长文字与信条引文都放在这里，不放在 SVG 内。

1. 救赎历史闭环：伊甸同在 → 堕落 → 应许 3:15 → 创17 立约 → 基督成全 → 启21:3 同在 → 回到起点。
2. 圣约神学闭环：神单方设立 → 作你的神 → 记号印证 → 信心领受 → 顺服回应 → 神信守更新 → 回到起点。
3. 经文圣经神学闭环：创17:7 → 出6:7 → 耶31:33 → 林后6:16 → 启21:3 → 回到起点。
4. 罪—救赎—感恩闭环：对应 HC 三部分（hcParts 3–11 / 12–85 / 86–129），罪 → 救赎 → 感恩 → 回到起点。环心写作者短语"唯一的安慰"。figcaption 中放 `<q data-cite="hc:2">` 与 `hc:86` 链接。

**10.5 思维导图**：`overview` 与 `summary` 各一个，用嵌套 `<ul class="mind">`。
- ≥ 1024 px：左右展开的树形（CSS Grid 加伪元素连线）。
- < 1024 px：可折叠的缩进树。

**10.6 动态图**
- Hero 区"圣约之环"SVG（viewBox `0 0 400 400`）：四色弧依次点亮，中央是 `<text>` 两行"我要作" / "你的神"（各 4 个 CJK 字以内，不触发孤儿引文规则）。
- 关键词频条形图：进入视口时生长。
- 数字口诀计数器滚动。
- 以上均为 CSS 动画，reduced-motion 时显示静态终态。不使用 canvas，删除上一版 §13.8 提到的星光 canvas。

**10.7 配色与图例（全站统一，页首有可折叠的图例条）**

| 用途 | 样式 | 变量/类 |
|---|---|---|
| 🔑 重点 | 金色左边框 + 浅金底纹 | `.callout.key` / `--gold` |
| 🧩 难点 | 紫色左边框 + 浅紫底纹 | `.callout.hard` / `--purple` |
| ⚠ 警告/误解 | 红 | `.callout.warn` / `--red` |
| 🌱 应用 | 绿 | `.callout.apply` / `--green` |
| 🛡 改革宗信条 | 蓝 | `.callout.reformed` / `--blue` |
| 🧠 记忆 | 粉 | `.callout.memo` / `--pink` |
| 🏛 威斯敏斯特补充 | 灰蓝虚线边框 + 角标"长老会改革宗补充" | `.callout.wsm` |
| 📜 仪文 | 琥珀边框 | `.cq.lf` |
| 罪／救赎／感恩 | 暗红 / 金 / 绿 标签 | `.tag.sin/.redeem/.thanks` |
| 四要点 | 金 / 红 / 青 / 绿 | `--p1..--p4` |

所有配色在明暗两主题下都要定义，文字与底纹对比度 ≥ 4.5:1。

### 11. 三信经页（creeds.html）

**结构**：`hero` → `recite`（背诵版）→ `compare`（深度对比）→ `why3`（为何需要三份）→ `link`（与讲章主题的关联）→ `sources`。

**背诵正文只由 JS 渲染**
- HTML 中有三个空容器：`<div class="recite-body" data-recite="apos|nic|ath"></div>`，模式与字号控件放在容器外的 `.recite-controls` 中。
- 容器外放一个 `<noscript>`，内容为三份信经的 CCI 原文链接。
- verify 检查：每个 `[data-recite]` 元素在 HTML 中不含任何非空白文本节点（验收2e）。
- 数据来源：使徒信经用 `G17.APOS`，尼西亚信经用 `G17.NIC_SPLIT`，亚他那修信经用 `CCI.creeds.ath.items`（42 点，显示网站自带编号）。每行带色条：父/子/圣灵/教会与盼望。

**模式**
- `full` 全文；
- `hint` 首字提示：每个分句只显示首字，其余用"□"占位；
- `blur` 遮盖自测：点击行显隐；
- `step` 逐行显示：上一行/下一行/重置按钮，键盘 ← →；
- 字号 `A− A A+`（16/19/23 px，存 localStorage `g17-recite-size`）；
- 打印：干净无色版；
- 朗读：speechSynthesis。

**reciteMatch 自检**：先切换到 `full` 模式，把每份信经渲染后各行的 textContent 依次拼接，再与 `CCI.creeds.<k>.body.join("")` 比较。亚他那修信经比较前先用 `/\s*\d+\)\s*/g` 去掉编号，渲染侧也不含编号节点（编号放在 `::before`，内容取自 `data-n`）。三份都相等时 `reciteMatch=1`。

**深度对比表**
- 维度：形成年代与会议、东西方使用、文体（我信／我们信／大公信仰是）、主要针对的问题、结构、核心句、在三项联合信条中的位置（BC 第9条；HC 第23问）。
- "据 CCI"的事实句一律用 `<q data-cite="intro:apos">` 等逐字短引：使徒信经以罗马信经为基础；尼西亚 325 年驳亚流，381 年扩充圣灵部分；亚他那修信经约出现于6世纪、作者不详。
- 亚他那修信经的 CCI 简介照原文逐字引用。其后附作者注："CCI 正文编号共 42 点，简介所述分段编号按原文保留"，不改动原文。

**图示**
- 三环递进图（HTML/CSS）：故事／身份／规则。
- 三栏"异同"图。

**为何三份而非一份**
1. 场合不同：洗礼认信、会议定义、教导护栏。
2. 不同时代的异端各自逼出更精确的表述。
3. 三份相互印证，后者不改前者，而是保护前者。
4. 改革宗以 BC 第9条接受三信经，表明宗教改革是归回大公信仰。

**与讲章关联**：三一神的圣约信实——父设立、子立约之血、圣灵施行。亚他那修信经中关于位格与本质的语句，用 `<q data-cite="intro:ath">` 或直接引自 `creeds.ath` 的 `<q data-cite>` 引用。为此，键格式增加 `creed:<apos|nic|ath>`（§13.5）。

### 12. 信条原文页（confessions.html）

渲染 `G17.CITED` 中每个键为完整 `.cq` 卡片（不折叠），分组如下：
- 海德堡：1、2、19、21、54、60、61、66、69、72、73、74、86
- 比利时信条：9、14、15、17、22、33、34
- 多特信经：1.7、1.8、1.17、2.8
- 仪文：`lf:1`（如抓取成功，另加 `lf:2` 成人洗礼仪文）
- 简介：`intro:apos|nic|ath|hc|bc|cd`

顶部提供搜索框，在已渲染卡片的文本内过滤并高亮；另有"主日27"快速跳转。

CITED 覆盖规则：三页中出现的每个 `data-src`/`data-cite` 键都必须在 `CITED` 中，`CITED` 中的每个键也必须在 cci.js 中存在。

### 13. UI、交互与内容机制

**13.1 布局与溢出规则**
- 沿用上一项目的 `.topbar` + `.layout`（`.sidebar` + `.main`）+ `.scrim` 结构与 CSS 变量。
- `.main` 内容最大宽度为 `min(100%, 1180px)`，左右内边距 `clamp(12px, 3vw, 40px)`。
- 表格包在 `.table-wrap{overflow-x:auto}` 中，表格是唯一允许内部横向滚动的组件。
- 断点：≤ 600、≤ 960（目录变抽屉）、≥ 1440。
- 全局设置 `img,svg{max-width:100%}`、`overflow-wrap:anywhere`。
- 禁止在 `html`/`body` 上设置 `overflow-x:hidden|clip`，否则 `docW` 断言会失效。
- aurora 背景层自身设 `position:fixed; inset:0; overflow:hidden; pointer-events:none`，并带 `data-clip-ok`。
- 目录项允许换行，不使用 `text-overflow:ellipsis`，因为省略号也算裁切。
- 主动折叠的长卡片 `.cq.collapsed` 带 `data-clip-ok`，自检时先全部展开。

**13.2 毛玻璃**
- `.topbar`、`.sidebar`、`.sec` 卡片、弹窗使用 `background: var(--panel); backdrop-filter: blur(14px) saturate(140%)`。
- `@supports not (backdrop-filter: blur(1px))` 时降级为不透明度 0.92 的纯色。
- 背景为 aurora 渐变光斑，transform 漂移动画。

**13.3 目录**
- 生成：脚本扫描 `main h2[id], main h3[id]`，生成两级目录。
- 桌面：`body.toc-hidden` 控制隐藏，状态存 localStorage `g17-toc`。
- ≤ 960 px：抽屉（`body.toc-open`），带 scrim，按 Esc 关闭；打开时焦点移到搜索框，关闭时焦点回到按钮。
- 目录内可搜索过滤。
- scrollspy：IntersectionObserver，`rootMargin: "-20% 0px -70% 0px"`。
- 跨页导航：topbar 三个链接（📖 讲章 / 📜 三信经 / 📚 信条原文），当前页加 `aria-current="page"`。

**13.4 经文文本**
- 来源：和合本（神版）简体。`tools/bible/fetch_bible.py` 调用 `https://bible.fhl.net/json/qb.php?chineses=<书卷>&chap=<章>&sec=<节范围>&version=unv&gb=1`，抓取 `G17.BIBLE_REFS` 中的全部经节，包括创17:1–27。该 API 已由评审实测可用。
- bible.json 每节存 `{"raw": 原文, "text": 规范化文本, "verified": true}`。规范化规则依次为：
  1. 删除 `【…】` 小注；
  2. `「」` 转 `“”`，`『』` 转 `‘’`；
  3. 删除 U+3000 全角空格；
  4. 去首尾空白。
- 生成 `assets/bible.js`（`window.BIBLE = {"创17:1": "…", …}`，只含 text）。
- 页面显示与比对都使用 `text`。sources 区注明："经文取自信望爱站（FHL）和合本，已去除神版空格与小注"。
- `verified:false` 只在 fetch 重试失败、手工录入时使用。普通构建时为 WARN；`build.py --layout`（部署前）时为 FAIL。

**13.5 引文标记约定（verify 依据）**

| 标记 | 含义 | 规则 |
|---|---|---|
| `<div class="cq" data-src="KEY" [data-p="n"]>` | CCI 全文/指定段卡片 | 运行时从 cci.js 渲染；键必须存在；`data-p` 从 1 开始，不超过段落数（仅 bc/cd/lf 支持） |
| `<q data-cite="KEY">…</q>` | CCI 短引文 | 去标签、`html.unescape` 后按 `……` 拆段，各段须按顺序为 `text(KEY)`（去 `<sup>…</sup>`）的子串 |
| `<q data-bible="创17:7">…</q>` / `"创17:10-11"` | 经文短引 | 去掉所有空白与引号字符（`“”‘’「」『』"'`）后，须为对应节 text 拼接（同样处理）的子串 |
| `<q class="ext" data-ext="https://…">…</q>` | 其他网站逐字短引 | 域名须在白名单。片段含任一 CJK 字时，去标点后 CJK 字数 ≤ 45；否则按空白分词 ≤ 30 词 |
| 无属性的 `<q>` | 禁止 | FAIL |
| 裸引号 `“…”` `「…」` `‘…’` 中的 CCI 原文或经文 | 禁止 | 孤儿引文检测（§14 第12步）FAIL |

- 键格式：`hc:<1–129>`、`bc:<1–37>`、`cd:<section1|section2|section3-4|section5>:<n>`、`lf:<n>`、`intro:<apos|nic|ath|hc|bc|cd>`、`creed:<apos|nic|ath>`。
- `text(KEY)` 的定义：
  - hc：`q + "\n" + "\n".join(a)`；
  - bc/cd/lf：`"\n".join(paras)`，带 `data-p` 的 `.cq` 只取该段；
  - intro：`creeds[k].intro` 或 `"\n".join(intros[k])`；
  - creed：`"".join(creeds[k].body)`。
- 上一项目在 data.js 中用 `x:"…“…”"` 隐式引号表示引文，该约定已废弃。闪卡、讨论题中的 CCI 原文统一写 `<q data-cite>`。
- app.js 会在每个 `q[data-cite]` 之后插入 `<a class="cite-link" href="https://ccifellowship.org<url>" target="_blank" rel="noopener" aria-label="CCI 原文：…">↗</a>`。`sources` 区另有静态 URL 列表，不开 JS 也能看到出处。

**13.6 外站内容规则**
- 以下 10 个外站只作释义，写成"参考：xxx"并加链接：ccreformed.org、reformedbeginner.net、canrc.org、urcna.org、heritagereformed.com、prca.org、opc.org、canadianreformedseminary.ca、wts.edu、crts.edu。
- 白名单为这 10 个域名加 ccifellowship.org。
- 实现者撰写释义前，必须实际访问相应页面；无法访问时只链接站点首页，不写具体主张的归属。
- 威斯敏斯特准则（WCF 7、28；WSC 94–95；WLC 165–167）一律放在 `.callout.wsm` 中。

**13.7 主题与偏好**：`data-theme="dark|light"`。初值读 localStorage `g17-theme`，没有时跟随 `prefers-color-scheme`。head 内联脚本在首绘前设置，避免闪烁。

**13.8 动效**
- `.reveal` 进入视口时淡入上移（IntersectionObserver，只触发一次）。
- `scroll-behavior:smooth`，reduced-motion 下改为 `auto`。
- 闪卡翻转 0.6 s。
- 所有 `@keyframes` 都包在 `@media (prefers-reduced-motion: no-preference)` 中。
- 不使用 canvas。

**13.9 app.js 模块**：`common`、`sermon`、`creeds`、`confessions` 四个模块，按 `body[data-page]` 启用。
- `common`：主题、目录、scrollspy、进度条、返回顶部、reveal、cite-link、cq 渲染（含 lf）、bible 填充、朗读、自检。
- `sermon`：地图与图例、闭环、闪卡、讨论题渲染、经文背诵卡、速记打印。
- `creeds`：背诵模式与 reciteMatch。
- `confessions`：卡片与搜索。
- 上一项目的 `esc/rich/plain/getItem/cardHtml/fillCard` 迁移过来，`getItem` 增加 `lf`、`creed` 键。`rich()` 先整体转义，再只还原 `<sup>`。

**13.10 自检（`?check=1`）**
- 准备：展开全部 details 与 `.cq.collapsed`，强制显示 reveal，creeds 页切换到 full 模式，等待 1500 ms。
- 输出：在 body 顶部插入 `<pre id="__check">`，输出 `vw docW issues points blocks loops loopsClosed mapMarkers legend cq missingCQ citeNoLink recite reciteMatch cards discuss`，并列出最多 40 条明细。
- 判定规则（遍历所有可见元素；`display:none`、宽或高 ≤ 1 px、`.sr-only` 不计）：
  - `vw = document.documentElement.clientWidth`；`docW = document.documentElement.scrollWidth`。由于 html/body 不再设 overflow-x:hidden，`docW` 能真实反映溢出。
  - OVERFLOW：沿祖先链向上查找，遇到 `overflow-x` 为 `auto|scroll` 的祖先就停止（视为可滚动容器，不报告）。若未遇到这样的祖先，且元素 `r.right > vw + 1` 或 `r.left < -1`，记 OVERFLOW。
  - CLIP：上述祖先链中，遇到 `overflow`/`overflow-x`/`overflow-y` 为 `hidden|clip` 的祖先 A 时，若元素矩形超出 A 的矩形 > 1 px，记 CLIP。若元素本身，或元素与 A 之间（含 A）的任一祖先带 `data-clip-ok`，则豁免。
  - OVERLAP：同一网格容器（`.grid,.cards,.timeline,.chips,.mind,.points,.liturgy,.map-legend`）中，可见子元素矩形相交 > 1 px。
  - FLIPCLIP：闪卡背面 scrollHeight > clientHeight + 1。
  - SVGTEXT：见 §10 总则。
  - 计数项：`loopsClosed` 见 §10.4；`reciteMatch` 见 §11；`mapMarkers` 统计 `#map svg.main .place`；`legend` 统计 `.map-legend li`。

### 14. 引文自动校验（改写 tools/cci/verify.py）

`verify.py` 暴露 `run(site_dir) -> (fails: list[str], warns: list[str])`，`__main__` 负责打印并以 `sys.exit(1 if fails else 0)` 退出。

- 解析器：所有 HTML 解析用同一个 `html.parser.HTMLParser` 子类，记录每个文本节点的行号、祖先标签栈与属性。
- 输入：
  - 三页 HTML；
  - `assets/data.js`（按 §8.1 方式 json.loads，递归遍历所有字符串叶子，每个叶子作为 HTML 片段用同一个解析器处理）；
  - `assets/cci.js`、`assets/style.css`、`tools/cci/cci.json`、`tools/bible/bible.json`。

**步骤**（每一步都可能产生 FAIL 或 WARN）：

1. cci.js 同步：`from build_cci import render`，若 `render(json.load(cci.json)) != 磁盘上的 cci.js` → FAIL"请运行 build_cci.py"。
2. 条目文本表：按 §13.5 定义计算 `text(KEY)`，全部先去掉 `<sup>…</sup>`。再生成 CCI 语料列表：所有条目（含 home、forms、creeds.index），去 sup 后每条一个字符串。
3. `q[data-cite]`：键必须存在；各段文字须按顺序为 `text(KEY)` 的子串 → 否则 FAIL，打印 `文件:行号 KEY 片段`。
4. `.cq[data-src]`：键必须存在，`data-p` 不越界。
5. 无属性的 `<q>` → FAIL。`q.ext` 的域名白名单与字数规则（§13.5）不满足 → FAIL。
6. 背诵分行：
   - `"".join(x["t"] for x in APOS) == "".join(creeds.apos.body)`；
   - NIC 同理；
   - ATH：`re.sub(r'\s*\d+\)\s*', '', ''.join(body)) == ''.join(i['t'] for i in items)`，且 `[i['n'] for i in items] == list(range(1, 43))`（评审已实测为 True）。
   - 不满足 → FAIL，并打印首个差异位置的前后 20 字。成功时输出 `APOS/NIC/ATH == CCI: True`。
7. data.js 校验：
   - 格式（§8.1）、顶层键齐全、标签与属性白名单；
   - 叶子中的 `q[data-cite]`/`q[data-bible]` 按第 3、9 步检查；
   - `DISCUSS` 长度 ≥ 8，`PLACES` 为 9 项且 `n` 为 1..9。
8. CITED 覆盖：三页与 data.js 中出现的所有键 ⊆ `CITED` ⊆ cci.js 已有键。
9. 经文：`q[data-bible]` 按 §13.5 规则比对；`blockquote.bible[data-ref]` 的引用必须在 bible.json 中存在。条目 `verified:false` 时，普通模式 WARN，`--strict`（由 `build.py --layout` 传入）时 FAIL。bible.json 缺失时，普通模式 WARN，`--strict` 时 FAIL。
10. 内容禁则：
    - 出现 `class="lyrics"` → FAIL；
    - index.html 的 `#liturgy` 中出现"日内瓦""圣诗部分""待核实" → FAIL；
    - 用字提示（上帝、阿里乌、腓特烈 等）→ WARN。
11. CSS 与背诵容器：
    - style.css 中选择器列表含独立的 `html` 或 `body`（正则 `(^|[,}\s])(html|body)\s*(,|\{)`）的规则块，若出现 `overflow(-x)?\s*:\s*(hidden|clip)` → FAIL；
    - creeds.html 的 `[data-recite]` 内有非空白文本 → FAIL。
12. 孤儿引文检测：
    - 扫描范围：三页 HTML 中不在 `<q>`、`<blockquote>`、`<script>`、`<style>`、`<title>` 内的文本节点（SVG `<text>` 与 `<noscript>` 也在扫描范围内），以及 data.js 字符串叶子中同样不在 `<q>` 内的文本。
    - 片段提取：用正则 `“([^”]+)”|「([^」]+)」|‘([^’]+)’` 提取引号内片段。
    - 规范化：删除全部标点、空白、引号，得到 `f`；`f` 中 CJK 字数 < 6 的片段跳过。CCI 语料与 bible text 做同样规范化。
    - 判定（依次进行，命中即 FAIL）：
      - (a) `f` 是某条 CCI 语料的子串 → FAIL"未标注的CCI引文，请改用 `<q data-cite>`"；
      - (b) 预筛：用语料的 8 字 n-gram 索引找出与 `f` 共享至少一个 8-gram 的条目；对这些条目用 `difflib.SequenceMatcher(None, f, entry, autojunk=False).find_longest_match` 求最长公共子串 L；若 L ≥ 8 且 L/len(f) ≥ 0.6 → FAIL"疑似被改动的CCI引文"；
      - (c) `f` 是 bible.json 任一节 text（或相邻节拼接）的子串 → FAIL"未标注的经文引文，请改用 `<q data-bible>`"。
    - 局限（写入 README）：只能检测引号包裹的片段，以及 bible.json 已收录的经节。不用引号的整段照抄要靠人工审阅，实现与审稿时须遵守 §13.5 的书写规则。
13. 汇总输出 `quotes checked / cards / orphan fragments scanned / mismatches / warnings`。

`tools/build.py`：依次运行 `build_cci.py`、`fetch_bible.py --build-js-only`（从 bible.json 重新生成 bible.js，不联网）、`verify.py`。带 `--layout` 时，verify 以 `--strict` 运行，之后再运行 `layoutcheck.py`。任一步骤退出码非 0，build.py 立即以该码退出。

### 15. 布局校验（tools/layoutcheck.py）

1. 在空闲端口（`socket.bind(("127.0.0.1",0))`）以子进程启动 `python -m http.server`。
2. 按以下顺序查找浏览器：环境变量 `CHROME_PATH` → `C:\Program Files\Google\Chrome\Application\chrome.exe` → `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`。都找不到时退出码 2。
3. 对 3 页 × {360, 768, 1024, 1440} 逐一运行：
   - 命令：`--headless=new --disable-gpu --hide-scrollbars --user-data-dir=<临时目录> --window-size=W,900 --virtual-time-budget=15000 --dump-dom "http://127.0.0.1:P/<page>?check=1"`，然后解析 `#__check`。
   - 通用断言：`vw == W`、`docW <= vw`、`issues == 0`、`missingCQ == 0`、`citeNoLink == 0`。
   - index 额外断言：`points=4 blocks=16 loops=4 loopsClosed=4 mapMarkers=9 legend=9 discuss>=8 cards=16`。
   - creeds 额外断言：`recite>0 reciteMatch=1`。
   - 截图：`--screenshot=tools/layout/<page>-<W>.png --window-size=W,2400`。
4. 每次 Chrome 调用超时 60 s。结束时终止 http.server，删除临时目录。
5. 打印 12 行结果表。任一项失败，退出码 1。

Q4 应对：如果 `vw != W`（无头 Chrome 钳制了窗口宽度），改用 Playwright（`pip install playwright==1.47.0`，`channel="chrome"`，复用本机 Chrome，不下载浏览器）的 `viewport={"width":W,"height":900}`，断言集不变。见 §7 的唯一例外说明。

### 16. 错误处理

| 操作 | 失败条件 | 可恢复? | 调用方得到 | 日志 |
|---|---|---|---|---|
| build_cci.py | cci.json 缺失或损坏 | 否 | 退出码 1，异常栈 | stderr |
| add_forms.py | 网络超时（60 s）/ HTTP 非 200 / 缺 `block-tulip-content` / 段落数为 0 | 是（重试 3 次，间隔 5 s） | 仍失败时退出码 1，不改动 cci.json，按 Q9 降级 | stderr |
| verify.py | 任一 FAIL | 否（须修改内容） | 退出码 1，加明细 | stdout，每项一行 `✗` |
| verify.py | bible.json 缺失或 verified:false | 普通模式可恢复，--strict 不可 | WARN / FAIL | stdout `⚠`/`✗` |
| fetch_bible.py | 超时 30 s / 非 200 / `status!="success"` / record 数 ≠ 请求节数 / 缺 `bible_text` | 是（重试 2 次，间隔 3 s） | 仍失败时退出码 1，不覆盖已有 bible.json | stderr |
| livecheck（CCI） | 网络失败 | 是 | 退出码 1，保留现有 cci.json | stderr |
| layoutcheck.py | 无浏览器 | 否 | 退出码 2 | stderr |
| layoutcheck.py | 单项超时或断言失败 | 否 | 该行 FAIL，最终退出码 1 | stdout 表格 |
| 运行时：cq 键不存在 | cci.js 中无该条 | 是 | 卡片显示"（未找到原文：KEY）" | console.warn；计入 missingCQ |
| 运行时：cci.js/bible.js/data.js 未加载 | 路径或网络错误 | 是 | 卡片与经文位置显示 CCI/FHL 原文链接；讨论题与背诵区显示 noscript 同款提示 | console.error |
| 运行时：localStorage 不可用 | 隐私模式 | 是 | 偏好不持久化 | 无 |
| 运行时：speechSynthesis 无 zh-CN 语音 / IntersectionObserver 缺失 | 旧浏览器 | 是 | 隐藏朗读按钮；reveal 直接显示，scrollspy 关闭 | 无 |
| gh repo create | 未登录 / 无权限 | 否 | 停止并报告 | 终端 |
| gh repo create | 仓库已存在 | 否 | 停止并询问用户，不覆盖、不强推 | 终端 |
| 启用 Pages | 409（已启用） | 是 | 视为成功 | 终端 |
| 启用 Pages | 422（分支不存在） | 否 | 停止并报告（说明 main 未推送） | 终端 |
| surge token 端点 | 非 200 | 是 | 转方案 B（§20） | 终端，只打印状态码 |
| surge 发布 | 认证失败 / 域名被占用 | 否 | 停止并报告；域名被占用时询问用户备选域名 | 终端，不回显凭据 |

### 17. 外部输入校验

| 输入 | 必填 | 类型/限制 | 失败行为 |
|---|---|---|---|
| URL `?check=1` | 否 | 精确匹配 `/[?&]check=1(&|$)/` | 不匹配则忽略 |
| localStorage `g17-theme` | 否 | `dark|light` | 非法值忽略并删除 |
| localStorage `g17-toc` | 否 | `open|hidden` | 同上 |
| localStorage `g17-recite-size` | 否 | `s|m|l` | 同上，默认 `m` |
| 目录/信条页搜索框 | 否 | 截断 50 字；高亮前转义 HTML 与正则元字符 | 空串时显示全部 |
| HTML/data.js 中的 data-src/data-cite/data-bible/data-p | 是（作者输入） | 格式见 §13.5 | 构建时 FAIL；运行时显示"未找到" |
| data.js 整体 | 是 | §8.1 严格 JSON + 标签白名单 | 构建时 FAIL |
| CCI 抓取 HTML | — | 必须含 `id="block-tulip-content"` 且段落数 > 0 | 不写出 |
| FHL API JSON | — | 见 §16 | 不写出 |

### 18. 不变量与归属

- CCI 原文逐字（已标注的引文）：由 verify 第 3/4/6 步负责（构建层）。运行时无法判断文字是否被改，只有构建期能对照 cci.json。cci.json 本身的真实性由 livecheck.py 负责，部署前在网络可用时运行一次。
- CCI 原文不得裸写：由 verify 第 12 步负责。片段只要带引号就能自动检测；无引号的整段照抄靠作者遵守 §13.5，并由人工审阅把关。
- 信经背诵正文只来自数据：由 verify 第 6、11 步与运行时 reciteMatch 共同负责。
- cci.js 只由生成器产生：由 verify 第 1 步负责。
- 讲章所有引用在信条页可查：由 verify 第 8 步负责。
- 页面不含歌词及未核实的诗歌出处：由 verify 第 10 步加人工审阅负责。
- 无溢出、裁切、重叠：由 layoutcheck（集成层）负责，前提是 verify 第 11 步保证 html/body 不隐藏溢出。
- 无凭据入库：由部署步骤负责。
  - 凭据只存在于当前 PowerShell 进程的变量中，不写文件，README 中也不写邮箱。
  - 提交前与推送后各扫描一次：

    ```powershell
    $h = git log -p --all | Out-String; [bool]($h.Contains($pw))
    git log -p --all | Select-String -Pattern 'ghp_|github_pat_|gho_|SURGE_TOKEN='
    ```

    第一行只输出 True/False，第二行必须无结果；同时用 `git diff --cached` 做人工检查。
- HTML 注入安全：cci.js 内容由 `rich()` 负责（只还原 `<sup>`）；data.js 内容由 verify 第 7 步的白名单负责。

### 19. 可测试性

- 单元测试：`python -m unittest discover tools/tests`。
  - 夹具：最小 cci.json（两条 HC、一条 BC、一个 lf、apos/nic/ath 各一段）、最小 bible.json、data.js 与一页 HTML。
  - 用例：
    1. 正确引文通过；
    2. 改一字失败；
    3. 无属性 `<q>` 失败；
    4. 不存在的键失败；
    5. `……` 分段乱序失败；
    6. ext 超长失败（中文 46 字 / 英文 31 词各一例）；
    7. 背诵分行少一字失败；
    8. ATH 漏一点失败；
    9. 裸引号 CCI 原文失败；
    10. 裸引号改一字失败（触发 LCS 规则）；
    11. 裸引号经文失败；
    12. data.js 非严格 JSON 失败；
    13. data.js 含 `<img>` 失败；
    14. style.css 中 `body{overflow-x:hidden}` 失败；
    15. `[data-recite]` 中写死文字失败；
    16. `lf:1` 的 `data-p` 越界失败。
  - fetch_bible 的规范化函数 `normalize(raw)` 单独测试：小注、「」、U+3000 各一例。
- 集成测试：layoutcheck.py（12 种组合）加 `?check=1` 计数。
- 人工测试清单（写进 README）：
  - 键盘走查目录、地图、图例、闪卡、tab；
  - 用 NVDA/VoiceOver 抽查标题与 SVG 名称；
  - 开启"减少动态效果"后检查；
  - 打印预览；
  - iOS Safari 抽查毛玻璃；
  - 通读全文，确认没有无引号照抄的 CCI 段落。

### 20. 仓库与部署计划（概述，执行在后续步骤）

1. 构建与提交：
   - `python tools/build.py --layout` 通过；
   - `git add index.html creeds.html confessions.html README.md .nojekyll .gitignore .surgeignore assets tools`（`.gitignore` 已排除 `tools/layout/`、`tools/cci/*.html` 等）；
   - 运行 §18 凭据扫描，然后提交。
2. 改分支名：`git branch -M main`（当前本地分支为 `master`，已实测）。
3. 建库并推送：`gh repo create 08-Ser-KiroCC-Je-Personal-20261003/genesis17-covenant-love-hc-ld27-sermon-20261017-v1 --public --source . --remote origin --push`。仓库已存在时停止并询问用户。
4. 启用 GitHub Pages：
   - `gh api -X POST repos/08-Ser-KiroCC-Je-Personal-20261003/genesis17-covenant-love-hc-ld27-sermon-20261017-v1/pages -f "source[branch]=main" -f "source[path]=/"`；返回 409 视为成功，返回 422 时停止。
   - 轮询 `gh api …/pages/builds/latest`，直到状态为 `built`。
   - 预期链接：`https://08-ser-kirocc-je-personal-20261003.github.io/genesis17-covenant-love-hc-ld27-sermon-20261017-v1/`。
5. surge.sh：
   - 先写入 §8 中的固定 `.surgeignore` 清单。
   - 方案 A（首选），在同一个 PowerShell 进程内执行：

     ```powershell
     $b=[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("$email`:$pw"))
     $r=Invoke-WebRequest -Method Post -Uri https://surge.surge.sh/token -Headers @{Authorization="Basic $b"}
     $env:SURGE_TOKEN=($r.Content|ConvertFrom-Json).token; $env:SURGE_LOGIN=$email
     npx --yes surge@0.23.1 . genesis17-covenant-love-hc-ld27-sermon-20261017-v1.surge.sh
     Remove-Item Env:SURGE_TOKEN
     ```

     不打印 `$r` 及其中的令牌，非 200 时只打印状态码。注意：该端点未经验证。
   - 方案 B：方案 A 失败时，用 send_message(warning) 请用户在本机执行 `npx --yes surge@0.23.1 login`，完成后继续；代理不接触密码。
   - 发布后提醒用户：密码曾在对话中以明文出现，建议更改。
6. README（中文）：
   - 内容：项目简介、3 个链接（Pages、surge、仓库 `https://github.com/08-Ser-KiroCC-Je-Personal-20261003/genesis17-covenant-love-hc-ld27-sermon-20261017-v1`）、文件说明、data.js 字段说明、来源规则与孤儿引文检测的局限、构建/校验/重新发布命令、人工测试清单。
   - 不写邮箱和任何凭据。
   - 更新 README 后再次提交、推送，并重新发布 surge。
7. 发布后用 `Invoke-WebRequest` 检查两个站点的三页均返回 200，并再运行一次 §18 扫描。

### 21. 边缘情况

- 窄屏 360 px：
  - 四要点四块纵向堆叠；
  - 表格在 `.table-wrap` 内横向滚动，并提示"← 左右滑动 →"；
  - 地图隐藏地名、保留编号，HTML 图例承载全部文字；
  - 思维导图变为缩进树；
  - 闭环图单列，SVG 文字约 11.8 px。
- 超宽屏 ≥ 1920 px：限制内容最大宽度，背景铺满。
- 长引文卡片（BC 34 约 1200 字、仪文段落）：讲章页默认折叠（`.cq.collapsed[data-clip-ok]`），信条页不折叠；自检时先展开。
- 闪卡背面文字超出：卡片高度取正反面中较高者，FLIPCLIP 检测。
- 打印：隐藏 topbar、侧栏、aurora 与动画，强制明色，链接后附 URL。
- 无 JS：正文、表格、SVG、静态出处列表仍可读；cq 卡片、讨论题、背诵区显示 noscript 提示与原文链接。
- 主题切换：SVG 用 `currentColor` 与 CSS 变量，无需重绘。
- 锚点跳转：设 `scroll-margin-top: calc(var(--topbar-h) + 12px)`，避免被 topbar 遮挡。
- `<q>` 引号：用 CSS `quotes` 生成，verify 只比对 q 内部文字。
- 原文格式：CCI 原文中的"西2: 11-13"等写法原样保留。
- 作者语句：只要包含 ≥6 字的裸引号片段并与 CCI/经文高度重合，就会被 FAIL，作者需改写措辞或改用正式标注。

### 22. 开放问题与未验证假设

- Q1（已关闭）：诗歌只显示编号、对应诗篇与关联说明（§9.1），不再寻找出处。
- Q2：诗歌在礼拜中的位置，假设按用户列出的顺序；礼拜次序标注为"示意"。用户若另有程序，只需替换次序。
- Q3（已关闭）：FHL API 已由评审实测可用，规范化规则见 §13.4。
- Q4：Chrome 无头模式下 `--window-size=360,…` 是否会被钳制，尚未验证；替代方案见 §15。
- Q5：年代学采用早期出埃及年代（约主前2067年为创17），页面同时说明晚期年代并标"约数"。
- Q6：`.agents/` 不提交、不上传。
- Q7（已关闭）：npm 上 `surge@0.23.1` 已确认存在。
- Q8：改革宗内部差异（行为之约术语、约的条件性、PRCA 立场）一律释义并列呈现，撰写前须实际访问外站核实。
- Q9：仪文页的可抓取性。评审实测 `/books/book-of-praise/liturgical-forms/1` 存在。本次设计时再次直连 ccifellowship.org 超时（90 s），未能复核段落结构。若实现时 add_forms.py 重试 3 次仍失败：
  - 移除 `lf:*` 卡片与 CITED 中的 lf 键；
  - 要点三与礼拜视角改用纯链接"参见 CCI《婴儿洗礼仪文》"，不加引文；
  - 在最终报告中说明验收6 中 lf 部分未满足。
  - 其余验收不受影响。
- Q10：surge token 端点 `https://surge.surge.sh/token` 能否用 Basic 认证换取令牌，尚未验证；方案 B 兜底。
- 假设 A1：FETCH_NOTES 所记 2026-10-17 livecheck 全部 True 有效；部署前若网络可用再运行一次（含仪文 URL）。
- 假设 A2：讲章为供阅读学习的书面讲章网站。
- 假设 A3：compile.py 依赖的原始抓取 HTML 已删除，无法完整重跑。因此仪文通过独立的 add_forms.py 合并进 cci.json，只新增 `forms` 键，不触碰其他键。两者共用 ccilib.py 的解析函数，保证解析规则一致。

### 23. 评审意见回应（design-review.json，20 条）

| # | 级别 | 处理 | 落点与说明 |
|---|---|---|---|
| 1 | HIGH | 已解决 | §13.5 增加书写规则；§14 第12步加入孤儿引文检测（子串 / 8-gram 预筛 + difflib LCS≥8 且 ≥60% / 经文）；§19 用例 9–11；废弃 `x:"…“…”"` 约定；§9.8/§9.9 中原先的裸引号已改为 `<q data-cite>`；验收2b–d |
| 2 | MEDIUM | 已解决 | §8.1：`window.G17 = <严格JSON>;`，用 json.loads 解析并遍历所有字符串叶子，加标签白名单；讨论题移入 `G17.DISCUSS` 由 app.js 渲染（§9.8）；APOS/NIC 迁移为 `[{t,c}]` 并重新校验 |
| 3 | MEDIUM | 已解决 | §14 第6步采用评审给出的 ATH 规则；§11 背诵容器为空、只由 JS 渲染；§14 第11步加入容器检查；reciteMatch 自检（§11、§15） |
| 4 | MEDIUM | 已解决 | §13.4 bible.json 存 `{raw,text,verified}` 及规范化规则；§13.5 比对前去掉空白与引号；`--strict` 下 verified:false 为 FAIL；Q3 关闭 |
| 5 | MEDIUM | 已解决 | §13.1 禁止 html/body 隐藏溢出；§14 第11步 CSS 检查；§13.10 加 CLIP（`data-clip-ok` 豁免）与 `left<-1`；溢出算法改为遇到 auto/scroll 才停止 |
| 6 | MEDIUM | 已解决 | §10 总则：非地图 SVG 的 viewBox 宽 ≤ 400、文字 ≥ 14 单位；地图用编号标记，HTML 图例始终显示，≤600px 隐藏地名；SVGTEXT 自检；放大 dialog 可横向平移 |
| 7 | MEDIUM | 已解决（有调整） | 9 个 `.place` = 8 个点 + 迦南区域标记 (33.0N, 35.6E)，插图副本 aria-hidden 不计数；插图移到左上角地中海。调整：插图放大倍数从 3× 改为 5×，范围为 x10–185、y10–310，因为 3× 时伯特利与摩利亚相距只有 22.5 单位，编号圆点会重叠；已核算新范围不遮挡任何地点与路线 |
| 8 | MEDIUM | 已解决 | §20 第5步：方案 A 用 token 端点（未验证，Q10），方案 B 用 warning 请用户自行登录；§18 用 `Contains` 布尔扫描与令牌模式检索；README 不写邮箱 |
| 9 | MEDIUM | 已解决 | §20 第2步 `git branch -M main`；§16 增加 Pages 422 → 停止 |
| 10 | MEDIUM | 已解决（实现方式调整） | 新增 `lf:<n>` 键（支持 data-p），verify、build_cci、livecheck 同步支持；要点三与礼拜视角使用 1–2 张卡片；confessions.html 增加仪文分组。调整：原始 HTML 已删除，compile.py 无法重跑，改由 add_forms.py 合并 forms，与 compile.py 共用 ccilib.py（A3）。抓取失败时的降级见 Q9 |
| 11 | MEDIUM | 已解决 | §9.1 只显示编号、对应诗篇与关联说明，不写日内瓦、出处或外链；礼拜次序标"示意"，不归属任何网站；verify 第10步检查禁用词；Q1 关闭 |
| 12 | NIT | 已解决 | §8 中统一使用唯一的 `.surgeignore` 清单，§20 引用该清单 |
| 13 | NIT | 已解决 | §7 注明唯一例外 |
| 14 | NIT | 已解决 | §13.5：含 CJK 时按去标点 CJK 字数 ≤ 45，否则按空白分词 ≤ 30 词；§19 用例 6 |
| 15 | NIT | 已解决 | build_cci 重构为 `render(d)`，verify 第1步直接 import |
| 16 | NIT | 已解决 | §11 照原文引用 CCI 简介，并加作者注 |
| 17 | NIT | 已解决 | 删除 canvas（§10.6、§13.8） |
| 18 | NIT | 已解决 | FR-5 明确多媒体为 speechSynthesis，覆盖背诵行与关键经文卡 |
| 19 | NIT | 已解决 | §10.4 加 `data-closes` 与终点距离 ≤ 6；自检输出 `loopsClosed=4` |
| 20 | NIT | 已解决 | §12 CITED 纳入 `intro:*`（以及 `lf:*`），confessions.html 增加简介分组 |
