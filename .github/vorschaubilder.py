#!/usr/bin/env python3
"""Erzeugt Vorschaubilder (1200 x 630, PNG) für das Teilen in sozialen Netzwerken.

Aufruf aus dem Hauptverzeichnis:  python3 .github/vorschaubilder.py
Erzeugt für jeden Beitrag in _posts ein Bild assets/img/vorschau/<slug>.png
sowie assets/img/vorschau/standard.png für alle übrigen Seiten.
Benötigt Playwright mit Chromium (npm i playwright, npx playwright install chromium).
"""
import datetime
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "img" / "vorschau"
MONATE = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli",
          "August", "September", "Oktober", "November", "Dezember"]


def front_matter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"')
    return fm


def datum(s):
    d = datetime.date.fromisoformat(s[:10])
    return f"{d.day}. {MONATE[d.month - 1]} {d.year}"


def svg_inline(path):
    svg = (ROOT / path.lstrip("/")).read_text(encoding="utf-8")
    svg = re.sub(r"<metadata>.*?</metadata>", "", svg, flags=re.S)
    svg = re.sub(r"<\?xml[^>]*\?>", "", svg)
    return svg


CSS = f"""
@font-face {{ font-family: "Newsreader"; font-weight: 200 800; font-style: normal;
  src: url("file://{ROOT}/assets/fonts/newsreader-latin-wght-normal.woff2") format("woff2"); }}
@font-face {{ font-family: "Newsreader"; font-weight: 200 800; font-style: italic;
  src: url("file://{ROOT}/assets/fonts/newsreader-latin-wght-italic.woff2") format("woff2"); }}
@font-face {{ font-family: "Public Sans"; font-weight: 400;
  src: url("file://{ROOT}/assets/fonts/public-sans-latin-400-normal.woff2") format("woff2"); }}
@font-face {{ font-family: "Public Sans"; font-weight: 600;
  src: url("file://{ROOT}/assets/fonts/public-sans-latin-600-normal.woff2") format("woff2"); }}
:root {{ --bg:#F2F5F4; --ink:#16241F; --text:#2C3D37; --muted:#4A5C55; --panel:#E3EAE7;
  --accent:#F2A33A; --accent-text:#A3550B; --rule:#C3CFCA; }}
* {{ box-sizing: border-box; margin: 0; }}
html, body {{ width: 1200px; height: 630px; overflow: hidden; }}
body {{ background: var(--bg); color: var(--ink); font-family: "Public Sans", sans-serif;
  display: grid; grid-template-columns: 480px 1fr; gap: 40px; padding: 56px 56px 52px 64px; }}
.rule {{ position: absolute; left: 64px; top: 0; width: 72px; height: 6px; background: var(--accent); }}
.text {{ display: flex; flex-direction: column; }}
.kicker {{ font-size: 18px; font-weight: 600; letter-spacing: .06em; text-transform: uppercase;
  color: var(--muted); margin-bottom: 20px; }}
.title {{ font-family: "Newsreader", serif; font-weight: 500; font-size: 54px; line-height: 1.08;
  letter-spacing: -0.01em; }}
.title.lang {{ font-size: 46px; }}
.absender {{ margin-top: auto; padding-top: 24px; border-top: 1px solid var(--rule); display: flex;
  align-items: baseline; gap: 16px; }}
.absender .name {{ font-family: "Newsreader", serif; font-size: 30px; font-weight: 500; }}
.absender .domain {{ font-size: 18px; color: var(--accent-text); font-weight: 600; letter-spacing: .02em; }}
.figure {{ background: var(--panel); align-self: center; padding: 20px; }}
.figure svg {{ width: 100%; height: auto; }}

body.standard {{ display: flex; flex-direction: column; justify-content: center; align-items: center;
  text-align: center; padding: 0 64px; }}
body.standard .site {{ font-family: "Newsreader", serif; font-weight: 500; font-size: 116px;
  letter-spacing: -0.02em; line-height: 1; }}
body.standard .tagline {{ font-family: "Newsreader", serif; font-style: italic; font-size: 38px;
  color: var(--accent-text); margin-top: 18px; }}
body.standard .domain {{ margin-top: 56px; font-size: 22px; font-weight: 600; letter-spacing: .06em;
  text-transform: uppercase; color: var(--muted); }}
body.standard .rule {{ left: 564px; }}
"""


def html_post(fm):
    lang = " lang" if len(fm["title"]) > 60 else ""
    kicker = " · ".join(x for x in [fm.get("themenfeld", ""), datum(fm["date"])] if x)
    fig = f'<div class="figure">{svg_inline(fm["grafik"])}</div>' if fm.get("grafik") else ""
    return f"""<!doctype html><html lang="de"><head><meta charset="utf-8"><style>{CSS}</style></head>
<body><div class="rule"></div>
<div class="text"><p class="kicker">{kicker}</p><h1 class="title{lang}">{fm["title"]}</h1>
<div class="absender"><span class="name">Martin Kriegel</span><span class="domain">martinkriegel.de</span></div></div>
{fig}</body></html>"""


def html_standard(cfg):
    return f"""<!doctype html><html lang="de"><head><meta charset="utf-8"><style>{CSS}</style></head>
<body class="standard"><div class="rule"></div>
<h1 class="site">{cfg["title"]}</h1><p class="tagline">{cfg["tagline"]}</p>
<p class="domain">martinkriegel.de</p></body></html>"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    cfg = {}
    for line in (ROOT / "_config.yml").read_text(encoding="utf-8").splitlines():
        if line.startswith(("title:", "tagline:")):
            k, v = line.split(":", 1)
            cfg[k] = v.strip()
    jobs = [(OUT / "standard.png", html_standard(cfg))]
    for post in sorted((ROOT / "_posts").glob("*.md")):
        fm = front_matter(post.read_text(encoding="utf-8"))
        slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", post.stem)
        jobs.append((OUT / f"{slug}.png", html_post(fm)))
    tmp = ROOT / ".github" / "_vorschau_tmp"
    tmp.mkdir(exist_ok=True)
    liste = []
    for png, html in jobs:
        h = tmp / (png.stem + ".html")
        h.write_text(html, encoding="utf-8")
        liste.append({"html": str(h), "png": str(png)})
    (tmp / "jobs.json").write_text(json.dumps(liste))
    node = r"""
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
  for (const j of jobs) {
    await page.goto('file://' + j.html);
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: j.png, type: 'png' });
    console.log('erzeugt', j.png);
  }
  await browser.close();
})();
"""
    (tmp / "render.js").write_text(node)
    subprocess.run(["node", str(tmp / "render.js"), str(tmp / "jobs.json")], check=True)
    for f in tmp.iterdir():
        f.unlink()
    tmp.rmdir()


if __name__ == "__main__":
    sys.exit(main())
