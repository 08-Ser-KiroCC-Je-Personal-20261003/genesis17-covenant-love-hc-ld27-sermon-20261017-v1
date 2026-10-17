from site_lib import hc, bc, cd, page, write

MAP = '''<svg viewBox="0 0 640 400" role="img" aria-label="亚伯拉罕行程地图：吾珥→哈兰→示剑→伯特利→埃及→希伯仑→别是巴">
<defs><linearGradient id="sea" x1="0" x2="1"><stop offset="0" stop-color="#2b6cb0" stop-opacity=".55"/><stop offset="1" stop-color="#2b6cb0" stop-opacity=".1"/></linearGradient></defs>
<rect x="0" y="0" width="640" height="400" rx="18" fill="rgba(255,255,255,.04)"/>
<path d="M0 120 C60 140 90 190 120 230 L120 400 L0 400Z" fill="url(#sea)"/><text x="18" y="200" fill="#9cc7ff" font-size="13">大海（地中海）</text>
<path d="M360 40 C420 120 470 220 560 330" stroke="#6fb6ff" stroke-width="3" fill="none" opacity=".7"/><text x="452" y="170" fill="#9cc7ff" font-size="12">幼发拉底河</text>
<path d="M395 30 C450 110 520 200 600 300" stroke="#6fb6ff" stroke-width="2" fill="none" opacity=".45"/>
<path class="route" d="M565 340 C520 230 450 120 380 55 C320 90 260 150 222 196 L214 222 C190 260 140 310 100 345 C150 300 190 255 214 222 L206 258 L196 292" stroke="#f5c76a" stroke-width="3" fill="none"/>
<g font-size="13" fill="#e8ecf8">
<circle cx="565" cy="340" r="7" fill="#ff7a8a"/><text x="520" y="368">吾珥 Ur</text>
<circle cx="380" cy="55" r="7" fill="#ff7a8a"/><text x="392" y="52">哈兰 Haran（创11:31）</text>
<circle cx="222" cy="196" r="6" fill="#5fe0a8"/><text x="232" y="192">示剑（创12:6）</text>
<circle cx="214" cy="222" r="6" fill="#5fe0a8"/><text x="226" y="226">伯特利（创12:8）</text>
<circle cx="206" cy="258" r="8" fill="#f5c76a"/><text x="220" y="262">希伯仑/幔利（创13:18；17章背景）</text>
<circle cx="196" cy="292" r="6" fill="#5fe0a8"/><text x="208" y="300">别是巴（创21:33）</text>
<circle cx="100" cy="345" r="7" fill="#b99bff"/><text x="40" y="378">埃及（创12:10）</text></g>
<text x="420" y="390" font-size="11" fill="#a9b3d1">示意图，非比例尺</text></svg>'''

MIND = '''<svg viewBox="0 0 700 380" role="img" aria-label="思维导图：创世记17章圣约四要点">
<g stroke-width="2" fill="none"><path d="M350 190 L150 80" stroke="#6fb6ff"/><path d="M350 190 L550 80" stroke="#ff7a8a"/><path d="M350 190 L150 300" stroke="#5fe0a8"/><path d="M350 190 L550 300" stroke="#b99bff"/></g>
<g font-size="14" text-anchor="middle" fill="#fff">
<rect x="255" y="160" width="190" height="60" rx="30" fill="#c08a1e"/><text x="350" y="186">创17 恩典之约</text><text x="350" y="206" font-size="12">主与我们建立爱的关系</text>
<rect x="40" y="50" width="220" height="62" rx="16" fill="#1f64c8"/><text x="150" y="76">①出于神</text><text x="150" y="96" font-size="12">全能的神 · 我与你立约 · 改名</text>
<rect x="440" y="50" width="220" height="62" rx="16" fill="#c2264a"/><text x="550" y="76">②由宝血印证</text><text x="550" y="96" font-size="12">割礼流血 → 基督宝血 → 洗礼</text>
<rect x="40" y="270" width="220" height="62" rx="16" fill="#0b8a5b"/><text x="150" y="296">③包括儿女</text><text x="150" y="316" font-size="12">你和你后裔 · 生下第八日</text>
<rect x="440" y="270" width="220" height="62" rx="16" fill="#6a3fd1"/><text x="550" y="296">④凭信回应</text><text x="550" y="316" font-size="12">行在我面前 · 当日受割礼</text></g></svg>'''


def loop(title, c, items, back):
    li = ''.join(f'<li>{i}</li>' for i in items)
    return f'<div class="loop" style="--c:{c}"><h3>{title}</h3><ol>{li}</ol><div style="text-align:center"><span class="back">↺ {back}</span></div></div>'


QA = [
 ('神为何在亚伯兰99岁、以实玛利13岁时才显现立约？', '创16章亚伯兰听从撒莱，用夏甲“帮神成就应许”，此后经文沉默13年。神等到人的力量完全枯竭（罗4:19“身体如同已死”），才宣告“我是全能的神”。<span class="key">恩典之约的起点不是人的能力，而是神的全能</span>。这也预表从死里复活的福音（罗4:17）。'),
 ('“立约”既是单方面的又是双方面的，如何理解？', '<span class="key">起源上单方</span>：神主动、神定条款、神担保（创15章唯神经过肉块）。<span class="key">施行上双方</span>：有应许也有要求（“你要作完全人”“你要守我的约”）。海德堡要理问答把这表达为：神应许，我们以信心和顺服回应——但连回应的信心也是圣灵所赐（HC 65）。'),
 ('割礼为何是“流血”的记号？与宝血何关？', '割礼是切除、流血、在后裔的源头上作记号：表明人本性污秽须被“割除”（申10:16；30:6），也预示那位从亚伯拉罕后裔而出的基督要被“剪除”（赛53:8），以自己的血成就约（太26:28）。西2:11-12称洗礼为“基督的割礼”。'),
 ('洗礼的水本身能洗净罪吗？', '不能。HC 72答：唯有耶稣基督的宝血和圣灵洗净我们一切的罪。记号指向实体，印证实体，却不等于实体。<span class="hard">难点</span>：既不能贬低圣礼为“仅仅象征”，也不能把恩典绑在水上；圣礼是神“印证”应许的工具（HC 66）。'),
 ('婴孩没有信心，为什么要受洗？', 'HC 74：他们与父母同属于神的圣约和教会；应许也是给他们的（徒2:39）。旧约第八日的婴孩同样不能表达信心，却由神命令受割礼（创17:12）。新约的恩典不会比旧约更窄。比利时信条第34条明确驳斥重洗派。'),
 ('“剪除”（创17:14）警告什么？今天还适用吗？', '轻看圣约记号就是轻看立约的神。圣约中有祝福也有咒诅（来10:28-29）。在教会中即是对不悔改者施行教会劝惩（HC 85）。<span class="key">圣约儿女不是自动得救，而是被呼召悔改相信</span>。'),
 ('以撒与以实玛利的分别对我们有何意义？', '神听了亚伯拉罕为以实玛利的祷告并赐福他（17:20），但约立在以撒身上（17:21）。加4章：凭应许生的与按血气生的。得救的根基是神主权的拣选（多特信经第一项教义），不是人的努力。'),
 ('“我要作你和你后裔的神”在整本圣经如何展开？', '这是圣约公式：出6:7、利26:12、耶31:33、结37:27、林后6:16，直到启21:3“神要亲自与他们同在，作他们的神”。<span class="key">圣约的终点是同在：神住在他百姓中间</span>。'),
 ('不在基督徒家庭长大的人如何进入这约？', '创17:12-13外邦买来的仆人也受割礼；加3:29“你们既属乎基督，就是亚伯拉罕的后裔”。信而受洗（徒2:41）。圣约的门向万国敞开——亚伯拉罕是“多国的父”（17:5）。'),
 ('“作完全人”是否要求无罪完美？', '不是。原文意为“全心、正直、没有二心”（参申18:13）。这是感恩的生活方向：在神面前（coram Deo）行走。我们的完全在基督里（HC 60），我们的成圣是一生的悔改（HC 88-90）。'),
]

body = f'''
<section id="hero" class="card hero"><div class="chips"><span class="chip">🇳🇱 欧陆改革宗讲章</span><span class="chip">📖 创世记 17 章</span><span class="chip">📘 海德堡要理问答 主日 27</span></div>
<h1>主与我们建立爱的关系</h1>
<p style="font-size:1.1em">“我要与你并你世世代代的后裔坚定我的约，作永远的约，是要作你和你后裔的神。”<br><small>——创世记 17:7（和合本）</small></p>
<div class="grid" style="text-align:left;margin-top:16px">
<div class="card pt p1"><span class="num">1</span><b>出于神</b><br><small>全能的神主动立约</small></div>
<div class="card pt p2"><span class="num">2</span><b>由宝血印证</b><br><small>割礼 → 十架 → 洗礼</small></div>
<div class="card pt p3"><span class="num">3</span><b>包括我们的儿女</b><br><small>你和你的后裔</small></div>
<div class="card pt p4"><span class="num">4</span><b>呼召我们凭信心回应</b><br><small>行在我面前</small></div></div>
<p class="legend" style="justify-content:center;margin-top:14px"><span class="key">重点</span><span class="hard">难点</span><span style="border-left:4px solid var(--gold);padding-left:6px">信条原文</span><span style="border-left:4px solid var(--blue);padding-left:6px">圣经经文</span></p></section>

<section id="liturgy" class="card"><h2>🎵 崇拜程序</h2><div class="tw"><table><tr><th>环节</th><th>内容</th></tr>
<tr><td>🎶 开始诗歌</td><td>圣诗第19首</td></tr><tr><td>🎶 认罪前</td><td>韵诗第25篇 1–5 节（“耶和华啊，我的心仰望你”）</td></tr>
<tr><td>🎶 读经前</td><td>韵诗第30篇</td></tr><tr><td>📖 读经</td><td>创世记 17 章</td></tr><tr><td>📘 教理</td><td>海德堡要理问答 主日27（第72–74问）</td></tr>
<tr><td>🎶 讲道后</td><td>韵诗第1篇（“不从恶人的计谋……这人便为有福”）</td></tr><tr><td>🎶 结束诗歌</td><td>圣诗第9首</td></tr></table></div>
<p style="font-size:13px;color:var(--mut)">诗歌仅列篇目；歌词请依所在教会《赞美诗集》（Book of Praise）。韵诗25与30：仰望立约之神的怜悯；韵诗1：圣约子民在神律法中喜乐——正是“感恩”的回应。</p></section>

<section id="bg" class="card"><h2>🏺 真实历史背景</h2><div class="tw"><table>
<tr><th>维度</th><th>内容</th></tr>
<tr><td>✍ 作者</td><td>摩西（犹太与教会传统，参路24:27；约5:46）</td></tr>
<tr><td>👥 原始受众</td><td>出埃及后在旷野、即将进迦南的以色列人：他们本身就是“受割礼的约民”，要知道自己从何而来、为何受割礼。</td></tr>
<tr><td>📅 事件年代</td><td>约主前2000年代（中青铜时代；确切年份学者有不同计算）。亚伯兰99岁，离开哈兰（75岁）已24年，以实玛利13岁。</td></tr>
<tr><td>📍 处境</td><td>住在迦南如同客旅（希伯仑幔利一带），无地可业，无子嗣继承；刚经历创16章“夏甲事件”的失败与13年沉默。</td></tr>
<tr><td>🧭 上下文</td><td>创12（呼召与应许）→ 创15（以血立约，唯神经过肉块）→ 创16（人的办法）→ <b>创17（立约记号与改名）</b>→ 创18–21（以撒应许与出生）→ 创22（献以撒，“耶和华以勒”）</td></tr>
<tr><td>🎯 为何写</td><td>向以色列显明：①你们的存在出于神的信实；②割礼不是民族习俗而是神的约印；③约包括后裔，所以要教导儿女；④约要求信靠与顺服，背约就被剪除。</td></tr>
<tr><td>🌍 古近东背景</td><td>当时宗主条约有“序言—历史—条款—记号—祝福/咒诅”。神俯就人的文化形式，却颠覆它：是<span class="key">大君王自己起誓、自己担保</span>。</td></tr></table></div>
<h3>🗺 亚伯拉罕行程图</h3>{MAP}</section>

<section id="whole" class="card"><h2>🔭 跳出框架看整体：创17在整本圣经中的位置</h2>
<div class="flow"><span class="n">创3:15 女人后裔</span><span class="a">→</span><span class="n">挪亚之约（虹）</span><span class="a">→</span><span class="n hl">亚伯拉罕之约（割礼）</span><span class="a">→</span><span class="n">西奈之约（逾越节/律法）</span><span class="a">→</span><span class="n">大卫之约（宝座）</span><span class="a">→</span><span class="n">耶31 新约</span><span class="a">→</span><span class="n hl">基督的血立新约（洗礼/圣餐）</span><span class="a">→</span><span class="n">启21:3 神与人同住</span></div>
<p>整本圣经是一条<span class="key">恩典之约</span>的长河：不同时代施行方式不同，实质只有一个——“我要作你们的神，你们要作我的子民”，中保始终是基督（加3:16“这后裔就是基督”）。</p>
<h3>📚 类似经文核心对照</h3><div class="tw"><table><tr><th>经文</th><th>核心</th><th>与创17的关联</th></tr>
<tr><td>创15:6–18</td><td>以血立约，唯神经过</td><td>约的单方面起源</td></tr>
<tr><td>申30:6</td><td>神要给你心行割礼</td><td>记号指向内心实体</td></tr>
<tr><td>耶31:31–34</td><td>新约：律法写在心上</td><td>约的成全与内化</td></tr>
<tr><td>罗4:9–12</td><td>割礼是因信称义的印证</td><td>记号与信心的关系</td></tr>
<tr><td>加3:6–29</td><td>属基督就是亚伯拉罕后裔</td><td>约扩展到万国</td></tr>
<tr><td>西2:11–12</td><td>基督的割礼，与他一同埋葬于洗礼</td><td>割礼—洗礼的连续</td></tr>
<tr><td>徒2:38–39</td><td>应许是给你们和你们的儿女</td><td>儿女仍在约中</td></tr>
<tr><td>启21:3</td><td>神的帐幕在人间</td><td>约的终极目标</td></tr></table></div></section>

<section id="text" class="card"><h2>🔍 再看局部：创世记17章结构与字词</h2><div class="tw"><table>
<tr><th>段落</th><th>主题</th><th>关键字词</th></tr>
<tr><td>1–2</td><td>神显现自我介绍</td><td><span class="key">“我是全能的神”</span>（El Shaddai）；“你当在我面前作完全人”</td></tr>
<tr><td>3–8</td><td>神的应许</td><td>“多国的父”、改名亚伯拉罕、“永远的约”、“作你和你后裔的神”、迦南地为永业</td></tr>
<tr><td>9–14</td><td>约的记号</td><td>割礼、“生下来第八日”、“我的约就立在你们肉体上”、<span class="hard">“剪除”</span></td></tr>
<tr><td>15–21</td><td>撒拉与以撒</td><td>改名撒拉、亚伯拉罕笑、“我的约是与以撒坚定的”</td></tr>
<tr><td>22–27</td><td>立即顺服</td><td>“正当那日”亚伯拉罕和全家受割礼</td></tr></table></div>
<div class="bible">“我是全能的神，你当在我面前作完全人，我就与你立约，使你的后裔极其繁多。”（创17:1–2）</div>
<p>全章“约”字出现十三次——几乎每一节都在说：<span class="key">这是“我的”约</span>。主语是神：“我与你立约”“我必使你”“我要作你的神”。</p></section>

<section id="p1" class="card pt p1"><h2><span class="num">1</span>这圣约出于神</h2>
<h3>📖 释经</h3><p>神先介绍自己，再提出要求。亚伯兰俯伏在地（17:3），神却说话不停——立约全是神的主动。改名“亚伯拉罕”（多国之父）是神在宣告一个尚未看见的现实，正如“使无变为有”（罗4:17）。</p>
<h3>💡 教义</h3><p>恩典之约起源于神白白的爱与拣选，而非人的配得。人在亚当里背约而堕落，<span class="key">是神来寻找人</span>。</p>
{bc(17)}{cd('section1', 7)}
<h3>🙏 应用</h3><ul><li>你的信仰不是你“选择宗教”，而是神先爱你（约壹4:19）。</li><li>当你像亚伯兰一样“自己想办法”失败后，神仍以“全能的神”的名再来。</li></ul></section>

<section id="p2" class="card pt p2"><h2><span class="num">2</span>这圣约由宝血印证</h2>
<h3>📖 释经</h3><p>创15章约以动物的血立定；创17章约的记号刻在人身上，带着血。割礼说：人的本性需要被切除，生命源头需要洁净。这一切指向那位真正被“剪除”的后裔——基督（赛53:8），他的血是“立约的血”（太26:28）。</p>
<h3>💡 教义</h3><p>圣礼是神设立的<span class="key">记号与印证</span>：记号指向基督，印证神的应许。洗礼取代割礼，<span class="hard">水不能洗罪，唯有基督的宝血和圣灵</span>。</p>
{hc(66)}{hc(72)}{hc(73)}
<h3>🙏 应用</h3><ul><li>怀疑得救时，回到你的洗礼：神用看得见的记号向你起誓。</li><li>不要信靠记号本身，要信靠记号所指的基督。</li></ul></section>

<section id="p3" class="card pt p3"><h2><span class="num">3</span>这圣约包括我们的儿女</h2>
<h3>📖 释经</h3><p>“你和你的后裔”在全章反复出现。第八日的男婴受割礼——他没有选择，却被神放在约中。新约里彼得说：“这应许是给你们和你们的儿女”（徒2:39）。</p>
<h3>💡 教义</h3><p>信徒的儿女是“圣洁的”（林前7:14），即属乎约、被分别出来。因此改革宗教会为婴孩施洗，并以教导、要理问答培养他们。</p>
{hc(74)}{bc(34)}{cd('section1', 17)}
<div class="box h"><b class="hard">难点</b>：婴儿洗礼不等于“自动得救”。约中有以撒也有以扫（罗9:6–13）。所以父母要祷告、教导，儿女长大要公开认信。</div>
<h3>🙏 应用</h3><ul><li>父母：在受洗时所作的誓约，就是每天的家庭敬拜与教导（申6:6–7）。</li><li>儿女：你不是“将来”才属神，你现在就被呼召以信心拥抱这约。</li></ul></section>

<section id="p4" class="card pt p4"><h2><span class="num">4</span>这圣约呼召我们凭信心回应</h2>
<h3>📖 释经</h3><p>“你当在我面前作完全人”（17:1）、“你要守我的约”（17:9）。亚伯拉罕的回应是“正当那日”（17:26）立即顺服。罗4:11：割礼是他“因信称义的印证”——信心在先，记号印证。</p>
<h3>💡 教义</h3><p>约有两部分：<span class="key">应许与要求</span>。我们的回应是信心与新的顺服；而这信心本身也是圣灵藉福音所赐，藉圣礼坚固。</p>
{hc(65)}{hc(86)}
<h3>🙏 应用</h3><ul><li>今天就回应：不拖延的顺服（“正当那日”）。</li><li>感恩的生活：主日敬拜、圣餐、家庭、职场都在“神面前”。</li></ul></section>

<section id="ld27" class="card"><h2>📘 海德堡要理问答 主日27 全文</h2>{hc(72)}{hc(73)}{hc(74)}
<div class="box k"><b class="key">记忆</b>：72 水不洗罪 → 73 但称为“重生的洗”，因为它表明并保证 → 74 婴孩同在约中，割礼由洗礼取代。</div></section>

<section id="loops" class="card"><h2>♾ 四重闭环</h2><div class="grid">
{loop('救赎历史闭环', 'var(--blue)', ['伊甸：神与人同在', '堕落：人离开神', '亚伯拉罕之约：应许后裔', '基督：真后裔成就约', '新天新地：神与人同住'], '回到“神与人同在”')}
{loop('圣约神学闭环', 'var(--red)', ['工作之约在亚当里破碎', '恩典之约出于神（要点1）', '以血印证（要点2）', '传给儿女（要点3）', '信心回应（要点4）'], '回应中再次领受应许')}
{loop('经文圣经神学闭环', 'var(--green)', ['创17 割礼', '申30 心的割礼', '耶31 新约', '西2 基督的割礼', '启21 我要作他们的神'], '同一句圣约公式贯穿')}
{loop('罪—救赎—感恩', 'var(--violet)', ['罪：亚伯兰靠血气（创16）', '救赎：全能神立约、宝血印证', '感恩：在神面前行走、守约', '儿女承接，世代相传'], 'HC第2问：三件事')}
</div>{hc(2)}</section>

<section id="views" class="card"><h2>🎭 多角度解读</h2><div class="grid">
<div class="card"><h3>⏳ 救赎历史</h3><p>创17是应许到成全的关键节点：后裔、土地、同在三大应许在此被立约印证。</p></div>
<div class="card"><h3>📜 圣约神学</h3><p>单方面起源、双方面施行；记号与实体；约中的祝福与咒诅。</p></div>
<div class="card"><h3>📚 系统神学</h3><p>圣礼论：记号、印证、施行者、对象；与称义（罗4）的关系。</p></div>
<div class="card"><h3>🏠 教牧/家庭</h3><p>婴儿洗礼、家庭敬拜、要理问答教导、公开认信。</p></div>
<div class="card"><h3>⛪ 礼拜仪式</h3><p>洗礼仪文中父母誓约、会众代祷：圣约群体共同承担。</p></div>
<div class="card"><h3>🌍 宣教</h3><p>“多国的父”：圣约的门向万民敞开，加3:29。</p></div></div></section>

<section id="mind" class="card"><h2>🧠 思维导图</h2>{MIND}</section>

<section id="ext" class="card"><h2>🧩 拓展</h2><h3>割礼与洗礼对照</h3><div class="tw"><table>
<tr><th>项目</th><th>割礼（旧约）</th><th>洗礼（新约）</th></tr>
<tr><td>设立者</td><td>神（创17）</td><td>基督（太28:19）</td></tr><tr><td>方式</td><td>流血</td><td>不流血（基督的血已流）</td></tr>
<tr><td>对象</td><td>亚伯拉罕家中男子、第八日婴孩</td><td>信徒及其儿女，男女皆可（加3:28）</td></tr>
<tr><td>意义</td><td>除去罪污、归属神、因信称义的印证</td><td>与基督同死同复活、罪得洗净、归入教会</td></tr>
<tr><td>警告</td><td>不受割礼者被剪除</td><td>藐视圣约者受更重刑罚（来10:29）</td></tr></table></div>
<h3>改革宗 vs 重洗派</h3><div class="tw"><table><tr><th>议题</th><th>改革宗</th><th>重洗派/浸信会</th></tr>
<tr><td>新旧约关系</td><td>同一恩典之约的不同施行</td><td>强调断裂</td></tr><tr><td>洗礼前提</td><td>神的应许（徒2:39）</td><td>个人信心表白</td></tr>
<tr><td>儿女身份</td><td>约中成员，需回应</td><td>约外，待信后加入</td></tr></table></div>
<p style="font-size:13px;color:var(--mut)">长老会改革宗的威斯敏斯特信条第7章（论神与人所立的约）、第28章（论洗礼）与上述欧陆信条一致，可作补充参考（见 <a href="https://opc.org" target="_blank" rel="noopener">opc.org</a>）。</p></section>

<section id="qa" class="card"><h2>💬 讨论题与答案分析</h2>
{''.join(f'<details><summary>Q{i+1}. {q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(QA))}</section>

<section id="sum" class="card"><h2>📋 总结与记忆</h2><div class="tw"><table>
<tr><th>要点</th><th>关键经文</th><th>信条锚点</th><th>一句话</th></tr>
<tr><td>①出于神</td><td>创17:1,7</td><td>BC 17；CD I.7</td><td>不是我找神，是神找我</td></tr>
<tr><td>②宝血印证</td><td>创17:10–11；西2:11–12</td><td>HC 66, 72–73</td><td>记号指向基督的血</td></tr>
<tr><td>③包括儿女</td><td>创17:7,12；徒2:39</td><td>HC 74；BC 34；CD I.17</td><td>应许给你们和你们的儿女</td></tr>
<tr><td>④信心回应</td><td>创17:1,9,26；罗4:11</td><td>HC 65, 86</td><td>正当那日，就顺服</td></tr></table></div>
<div class="box k"><b>🔑 口诀：「神起 · 血印 · 儿承 · 信应」</b>——神发起、血印证、儿女承受、信心回应。</div>
<div class="grid">
<div class="fc"><div class="in"><div class="f">🃏 El Shaddai 是什么意思？</div><div class="b">“全能的神”——在人力已尽时显现（创17:1）</div></div></div>
<div class="fc"><div class="in"><div class="f">🃏 HC 72 核心？</div><div class="b">外在的洗不能洗罪，唯有基督的宝血与圣灵</div></div></div>
<div class="fc"><div class="in"><div class="f">🃏 HC 74 为何婴孩受洗？</div><div class="b">同属圣约与教会；割礼已被洗礼取代</div></div></div>
<div class="fc"><div class="in"><div class="f">🃏 圣约公式？</div><div class="b">“我要作你们的神，你们要作我的子民”</div></div></div>
<div class="fc"><div class="in"><div class="f">🃏 罗4:11？</div><div class="b">割礼是因信称义的印证</div></div></div>
<div class="fc"><div class="in"><div class="f">🃏 西2:11–12？</div><div class="b">基督的割礼 = 与他同埋于洗礼</div></div></div></div>
<p style="text-align:center;margin-top:16px">🙌 <b>结语</b>：全能的神以宝血为印，把我们和儿女一同写进他爱的约中；我们以信心和感恩回答：“主啊，你是我们的神。”</p></section>
'''

TOC = [('hero', '🕊 题目与要点', ''), ('liturgy', '🎵 崇拜程序', ''), ('bg', '🏺 历史背景与地图', ''), ('whole', '🔭 整本圣经中的位置', ''),
       ('text', '🔍 经文结构', ''), ('p1', '① 出于神', 'sub'), ('p2', '② 由宝血印证', 'sub'), ('p3', '③ 包括我们的儿女', 'sub'),
       ('p4', '④ 凭信心回应', 'sub'), ('ld27', '📘 主日27 全文', ''), ('loops', '♾ 四重闭环', ''), ('views', '🎭 多角度解读', ''),
       ('mind', '🧠 思维导图', ''), ('ext', '🧩 拓展', ''), ('qa', '💬 讨论题', ''), ('sum', '📋 总结与记忆卡', '')]
write('index.html', page('主与我们建立爱的关系 · 创世记17章', TOC, body))
