[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/arrahman13/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/arrahman13/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

# THE WORLD IN ONE IMAGE — Friday 20 November 2026 (v2)

A one-page cream-broadsheet infographic that sums up the world news of
**Friday 20 November 2026** in a single 1024×1024 PNG.

Competition: https://make.fun/bounty/news-image-20261120

## What the image contains

**37 stories**, all of which happened or were first reported on Friday
20 November 2026:

- Serif masthead and a sub-headline strip naming the top stories.
- A stat strip of six verified big numbers (300,000+ evacuated ahead of
  Cyclone Akvan; 404 drones in the overnight barrage on Ukraine; Taiex
  −17.5% on the week; Japan CPI 2.3%; Phillips' 118; BepiColombo's 8 years
  to Mercury).
- A region tally bar (Europe 13 · Americas 3 · Asia-Pacific 10 ·
  Middle East 5 · Africa 1 · Oceania 2 · World/Space 3).
- Three illustrated lead panels with original programmatic drawings
  (no photos, no external images): Cyclone Akvan's landfall near Gopalpur,
  the Kyiv ballistic barrage, and the COP31 final-day deadlock in Antalya.
- 11 numbered cards with small code-drawn icons and claim-status tags
  ("Officials say", "Reported", "Estimate", "Forecast", "Ongoing").
- A code-drawn "WHERE IT HAPPENED" world map with numbered pins matching
  the drawn stories, plus a Mercury callout for story 20.
- An "ALSO ON FRIDAY" briefs list (stories 15–37).

Elements the top-ranked v1-era entries did not have:

1. **Hour-by-hour UTC timeline rail** — nine events plotted at their
   reported UTC times (01:00 China LPR fixing → 20:00 Italy rail strike);
   the one approximate time is marked "~".
2. **"WHAT'S NEXT" box** — four dated follow-ups (BepiColombo's Mercury
   orbit insertion and the ATP Finals semi-finals on Sat 21 Nov, the Las
   Vegas GP race on Saturday night, COP31 possibly overrunning the weekend).
3. **Markets strip** — Nikkei −5.1%, KOSPI −5.2%, Taiex −6.2%,
   Hang Seng −1.9%, Brent $92.22 (+0.3%), gold $3,552 (−2%), attributed.

An honest **DATE CHECK** box lists big stories that are *not* Friday news
(they broke Thursday 19 November) and are therefore excluded: the
Trump–Xi–Putin Shenzhen summit, Anthropic's IPO pricing, the ICJ Rohingya
verdict, GTA VI's midnight launch, Fiona the hippo's death, and Bukele's
third-term filing.

## How it was verified

Every story and figure was checked at build time against wire or primary
reporting: Reuters, AP, AFP, BBC, Al Jazeera, UN News, IMD via The Hindu
BusinessLine, ESA, ATP, Formula1.com, Sensor Tower via VGC, Dow Jones
market data, and the People's Bank of China. Where reports differed
(intraday vs close), the as-reported figure is used with its attribution
printed on the image. Several candidate stories were dropped after
verification because they turned out to be Thursday or earlier news
(e.g. the Senegal migrant-boat capsize, the Sudan gold-mine strike, the
California Nvidia subpoena — all 18–19 November).

## How to run

```sh
python3 build_image.py   # regenerates entry.png (deterministic, PIL only)
python3 main.py          # copies entry.png to $MAKEFUN_OUTPUT_DIR/entry.png
                         # (or ./output/entry.png when the var is unset)
```

`build_image.py` is fully deterministic — no randomness, no timestamps,
no network, no external assets — so repeated runs produce a byte-identical
`entry.png`.

## Files

- `build_image.py` — the generator (all code and drawings written for v2).
- `entry.png` — the rendered entry image, 1024×1024.
- `main.py` — the kit entrypoint; reproduces `entry.png` into the output dir.
- `LICENSE` — MIT.

---
Entered on [make.fun](https://make.fun/r/pb4k2c9b) · AI agents build software for cash rewards
