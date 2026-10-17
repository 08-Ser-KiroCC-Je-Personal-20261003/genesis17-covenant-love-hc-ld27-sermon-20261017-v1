# CCI 原文来源与复现记录

所有信经/信条文字逐字取自 https://ccifellowship.org/books/book-of-praise （敬拜手册）。
`cci.json` 复用自 `three-ecumenical-creeds-reformed-study-20261014-v2/tools/cci/cci.json`（全站抓取：HC 1–129、BC 1–37、CD 全部要点、三大信经、首页、简介页），并于 2026-10-17 对本讲章重点段落实时重抓并逐字比对，全部一致（`livecheck.py` 输出均为 True）。

## 重点段落来源 URL

| 内容 | URL |
|---|---|
| 使徒信经 | https://ccifellowship.org/books/book-of-praise/creeds/apostles-creed |
| 尼西亚信经 | https://ccifellowship.org/books/book-of-praise/creeds/nicene-creed |
| 亚他那修信经 | https://ccifellowship.org/books/book-of-praise/creeds/athanasian-creed |
| 海德堡要理问答 主日27（问答72/73/74） | https://ccifellowship.org/books/book-of-praise/confessions/heidelberg-catechism/section2/part5/lord-day-27 |
| 海德堡其他主日 | 见 cci.json 中 `hc[n].url`（格式 `/books/book-of-praise/confessions/heidelberg-catechism/sectionX/partY/lord-day-N`） |
| 比利时信条 第15/33/34条 | https://ccifellowship.org/books/book-of-praise/confessions/the-belgic-confession/15 （/33、/34 同理；其余条 1–37） |
| 多特信经 第一要点第17条 | https://ccifellowship.org/books/book-of-praise/confessions/canons-of-dort/section1/17 |
| 多特信经其余条款 | `/books/book-of-praise/confessions/canons-of-dort/{section1,section2,section3-4,section5}/{n}` |

## 命令（PowerShell，在 tools/cci 下）

```powershell
$env:PYTHONIOENCODING="utf-8"
# 实时重抓重点页面并与 cci.json 逐字比对
$p="/books/book-of-praise/confessions/heidelberg-catechism/section2/part5/lord-day-27","/books/book-of-praise/confessions/the-belgic-confession/15","/books/book-of-praise/confessions/the-belgic-confession/33","/books/book-of-praise/confessions/the-belgic-confession/34","/books/book-of-praise/confessions/canons-of-dort/section1/17","/books/book-of-praise/creeds/apostles-creed","/books/book-of-praise/creeds/nicene-creed","/books/book-of-praise/creeds/athanasian-creed"
python fetch.py @p
python livecheck.py
Remove-Item *.html,*.txt
# 生成站点数据 assets/cci.js
python build_cci.py
```

完整重建（如需）：`python crawl.py /books/book-of-praise` 抓取全部页面（另需保存首页为 `home.html`），再 `python compile.py` 生成 cci.json，然后 `python build_cci.py`。
网页引用核对：`python verify.py`（检查 index.html 中引用与 cci.js 逐字一致）。
