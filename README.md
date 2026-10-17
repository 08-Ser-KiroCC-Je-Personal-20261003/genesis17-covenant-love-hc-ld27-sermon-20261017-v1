# 主与我们建立爱的关系 · 创世记17章 · 海德堡要理问答主日27

欧陆改革宗讲章网站（v1，2026-10-17）。

## 链接

- GitHub Pages: https://08-ser-kirocc-je-personal-20261003.github.io/genesis17-covenant-love-hc-ld27-sermon-20261017-v1/
- Surge: https://genesis17-covenant-love-hc-ld27-sermon-20261017-v1.surge.sh
- 仓库: https://github.com/08-Ser-KiroCC-Je-Personal-20261003/genesis17-covenant-love-hc-ld27-sermon-20261017-v1

## 结构

- `index.html` 讲章：背景、地图、四要点、主日27、四重闭环、思维导图、讨论题、记忆卡
- `creeds.html` 三大普世信经背诵版（背诵模式、字号）与深度对比
- `assets/site.css`、`assets/site.js` 样式与交互（无外部依赖）
- `tools/cci/cci.json` 自 https://ccifellowship.org 抓取的信经/信条原文缓存

## 构建

```
python tools/build_sermon.py
python tools/build_creeds.py
```

页面里的信经和信条引文，都由构建脚本直接从 `cci.json` 读取，不手工录入，所以与 ccifellowship.org 原文逐字一致。如需重新与网站在线比对，运行 `tools/cci/livecheck.py`。
