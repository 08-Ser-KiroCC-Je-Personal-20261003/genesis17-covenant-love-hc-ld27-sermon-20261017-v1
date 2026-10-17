from site_lib import creed, link, page, write

NAMES = [('apos', '使徒信经', '🕊', '约主后2–4世纪成形，罗马洗礼信经'), ('nic', '尼西亚信经', '🔥', '主后325尼西亚 / 381君士坦丁堡'),
         ('ath', '亚他那修信经', '👑', '约主后5–6世纪，西方教会')]


def clean(k, nm):
    c = creed(k)
    lines = ''.join(f'<p class="ln" data-src="creed:{k}">{p}</p>' for p in c['body'])
    return (f'<div class="pane{" on" if k == "apos" else ""}" id="c-{k}"><div class="creed">{lines}</div>'
            f'<details><summary>📖 历史简介（ccifellowship.org）</summary><p>{c["intro"]}</p></details>'
            f'<div class="src" style="font-size:13px;color:var(--mut)">原文出处 {link(c["url"])}</div></div>')


tabs = ''.join(f'<button class="btn{" on" if k == "apos" else ""}" data-p="c-{k}">{i} {n}</button>' for k, n, i, _ in NAMES)
panes = ''.join(clean(k, n) for k, n, _, _ in NAMES)

body = f'''
<section id="hero" class="card hero"><h1>三大普世信经 · 背诵版与深度对比</h1>
<div class="chips"><span class="chip">🕊 使徒信经</span><span class="chip">🔥 尼西亚信经</span><span class="chip">👑 亚他那修信经</span></div>
<p>三份信经都是“一信”的不同层次：<span class="key">使徒信经</span>讲信仰的骨架，<span class="key">尼西亚信经</span>守护子的神性，<span class="key">亚他那修信经</span>精确界定三一与二性。</p></section>

<section id="read" class="card"><h2>📖 干净阅读版 / 背诵模式</h2>
<div class="tabs">{tabs}</div>
<p><button class="btn" id="reciteBtn">🙈 背诵模式</button> <button class="btn" id="fMinus">A−</button> <button class="btn" id="fPlus">A＋</button>
<span style="font-size:13px;color:var(--mut)">背诵模式下逐句模糊，点击某一句即可显示。</span></p>
{panes}</section>

<section id="cmp" class="card"><h2>⚖ 深度对比</h2><div class="tw"><table>
<tr><th>项目</th><th>🕊 使徒信经</th><th>🔥 尼西亚信经</th><th>👑 亚他那修信经</th></tr>
<tr><td>成形</td><td>源于罗马洗礼信经（约主后200年），今文约主后400年后定型</td><td>325年尼西亚会议，381年君士坦丁堡会议扩充</td><td>约5–6世纪西方教会，托名亚他那修</td></tr>
<tr><td>处境</td><td>洗礼认信、教导慕道者</td><td>阿里乌主张“子是受造的”；后有否认圣灵神性者</td><td>需要精确表述三一论与基督论，抵挡撒伯流、阿里乌、聂斯脱利、欧迪奇等错谬</td></tr>
<tr><td>核心焦点</td><td>三一架构下的救赎历史叙事</td><td><span class="key">子与父同质</span>，圣灵是主、赐生命的</td><td><span class="key">一体三位、三位一体</span>；基督<span class="hard">一位二性</span></td></tr>
<tr><td>文体</td><td>简洁叙述、十二条</td><td>礼仪性认信，“我们信”</td><td>教义性定义，带“警告条款”</td></tr>
<tr><td>功能</td><td>信仰入门与崇拜认信</td><td>护教与合一的标准</td><td>教导与界线（神学“栅栏”）</td></tr>
<tr><td>与圣约的关系</td><td>“我信圣而公之教会……罪得赦免”——圣约群体</td><td>“为我们人类……降世”——救赎出于三一神</td><td>“凡愿意得救的”——圣约要求真信心</td></tr>
</table></div>
<h3>🔗 共同点</h3><ul><li>都是三一结构：父—子—圣灵。</li><li>都以基督的位格与工作为中心。</li><li>都被欧陆改革宗明确接纳：比利时信条第九条明言乐意接受这三大信经。</li></ul>
<h3>❓ 为什么需要三份而不是一份？</h3>
<div class="flow"><span class="n">异端提出新问题</span><span class="a">→</span><span class="n">教会回到圣经</span><span class="a">→</span><span class="n">用更精确的话认信</span><span class="a">→</span><span class="n hl">旧信经不废，新信经加深</span></div>
<p>三份信经不是互相取代，而是<span class="key">层层加固</span>：使徒信经像房屋的框架，尼西亚信经加固“子是真神”这根梁，亚他那修信经再把三一论与基督论的每个接点焊牢。一份太简会被曲解，一份太繁不便敬拜；三份并用，既可背诵敬拜，又可守护真道。</p>
<div class="box h"><b class="hard">难点</b>：亚他那修信经“除非……必永远灭亡”并非“靠背条文得救”，而是说否认真神就是离弃唯一的救主（参约17:3；约壹2:23）。</div>
<h3>🧠 记忆口诀</h3><div class="grid">
<div class="fc"><div class="in"><div class="f">🕊 使徒 = 骨架</div><div class="b">父创造 · 子救赎 · 灵成圣 · 教会与永生</div></div></div>
<div class="fc"><div class="in"><div class="f">🔥 尼西亚 = 同质</div><div class="b">出于真神而为真神；受生而非被造；与父一体</div></div></div>
<div class="fc"><div class="in"><div class="f">👑 亚他那修 = 界线</div><div class="b">不混淆位格，不分割本质；一位基督，二性不混</div></div></div></div></section>

<section id="time" class="card"><h2>🗓 时间线</h2><div class="flow">
<span class="n">~200 罗马洗礼信经</span><span class="a">→</span><span class="n hl">325 尼西亚</span><span class="a">→</span><span class="n">381 君士坦丁堡</span><span class="a">→</span><span class="n">451 迦克墩</span><span class="a">→</span><span class="n hl">~500 亚他那修信经</span><span class="a">→</span><span class="n">1561 比利时信条第九条接纳</span></div></section>
'''
TOC = [('hero', '✝ 概览', ''), ('read', '📖 背诵版', ''), ('cmp', '⚖ 深度对比', ''), ('time', '🗓 时间线', '')]
write('creeds.html', page('三大普世信经 · 背诵与对比', TOC, body))
