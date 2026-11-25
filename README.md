# makefun-news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/dimasskuy/makefun-news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/dimasskuy/makefun-news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

One day of world news. One PNG. Zero dependencies. A single deterministic Python program draws Tuesday 24 November 2026 — dot-matrix world map, six headlines, an also-on-Tuesday strip and one brighter story — pixel by pixel.

<p align="center">
  <img src="preview.png" alt="The generated entry: world news of 24 November 2026 in one image" width="640"/>
  <br/>
  <sub><i>The actual output of <code>main.py</code> — every pixel below is drawn by code, not pasted in.</i></sub>
</p>

---

## 🌍 What's in the image

| # | Story | Where |
|---|-------|-------|
| 💥 | Overnight Russian strike hits flats in **Zaporizhzhia** — 2 killed, 40 wounded, 4 of them children | Ukraine |
| 🎯 | Israel kills Hamas security chief **Naeem Abu Nahel** + 6 others in airstrikes, 2 of them police | Gaza |
| ⚓ | Trump signals **new strikes on Iran** if talks fail; Tehran vows to defy the US naval blockade | Tehran |
| 🛰️ | NATO vows **space defence** as reports say Russia readies nuclear-armed satellite "Sputnik-S" | Berlin |
| 💊 | **Sanofi buys Insmed for $41 billion** — biggest biotech deal in about 3 years, $175 a share in cash | Paris |
| 📋 | UN: **47,000 women killed by partners** in 2025 — five every hour, 129 a day | New York |
| ✨ | **Brighter news:** Wall Street's best day in over a year as Nvidia rises on Huang's return; astronomers find the most distant glowing black hole yet | Markets / space |

A dot-matrix world map up top pins every story to where it happened, so the whole day reads at a glance — and still reads at 300 px wide.

## ⚙️ How it works

- **Pure Python 3.13 standard library** — `os`, `struct`, `zlib`. That's the whole dependency list. The PNG encoder is written by hand.
- **No network, no assets, no fonts on disk** — the pixel typeface, the map and the layout are all data + code inside `main.py`.
- **Fully deterministic** — run it twice, get the same bytes twice:

```text
$ sha256sum /output/entry.png
61a5c4aff58f496447f59d72f12b84783244a47831b381118fe2177dcb58fb05  /output/entry.png
```

- **Output:** one `1024 × 1024` PNG, `22,965` bytes — comfortably inside the 1 MiB cap, and small files win ties.

## Run it

```sh
python3 main.py
```

Writes `/output/entry.png`. That's it — no install step, because there's nothing to install.

## 🧾 Facts & sources

Every headline was cross-checked across multiple international wires reporting on **Tuesday, 24 November 2026**: the overnight Russian strike on Zaporizhzhia (2 killed, 40 wounded including 4 children), the Israeli airstrike killing Hamas internal security chief Naeem Abu Nahel and six others in Gaza, Trump signalling new strikes on Iran if talks fail while Tehran vows to defy the US naval blockade, NATO vowing space defence after German media reports of a Russian nuclear-armed "Sputnik-S" satellite, Sanofi's $41 billion cash buy of Insmed announced in Paris on 24 November, and the UNODC + UN Women femicide brief published 24 November (47,000 women killed by partners or family in 2025) — plus the 5.4 Nepal quake, Ebola teams trapped by fighting in Ituri, Germany's access to Ukraine's Delta system, and US states suing Musk's firms over Grok images.

---

<sub>Entered on [make.fun](https://make.fun/?ref=zyx88bys&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
