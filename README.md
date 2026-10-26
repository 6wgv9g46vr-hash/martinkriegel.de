# martinkriegel.de

Persönlicher Fachblog von Martin Kriegel. Statische Website mit Jekyll, gehostet über GitHub Pages.

## Aufbau

- `_posts/` veröffentlichte Beiträge (Markdown, Dateiname `JJJJ-MM-TT-titel.md`)
- `_drafts/` Entwürfe, erscheinen nur in der lokalen Vorschau mit `--drafts`
- `_layouts/`, `_includes/` Seitengerüst. `start.html` baut die Startseite, `uebersicht.html` die Beitragsübersicht; beide holen die Beiträge automatisch aus `_posts/`
- `assets/css/style.css` Gestaltung
- `assets/fonts/` selbst gehostete Schriften (Newsreader, Public Sans; SIL Open Font License)
- `assets/img/` Grafiken
- `index.md` (Startseite, Text im Kasten „Über den Autor"), `beitraege/index.md` (Einleitung der Übersicht), `ueber-mich.md`, `kontakt.md`, `impressum.md`, `datenschutz.md`, `404.md`. Alle Texte der Website liegen in Markdown-Dateien; Gestaltung und Technik in `_layouts/`, `_includes/`, `assets/css/`
- `CNAME` Domain für GitHub Pages

## Beitrag anlegen

Front Matter eines Beitrags:

```yaml
---
title: "Frage als Titel?"
date: 2026-11-02
themenfeld: Versorgungssicherheit
antwort: "Antwort in ein bis drei Sätzen. Erscheint als erster Absatz und als Vorschau."
grafik: /assets/img/dateiname.svg
grafik_alt: "Beschreibung der Grafik"
description: "Kurzbeschreibung für Suchmaschinen."
image:
  path: /assets/img/vorschau/titel.png
  width: 1200
  height: 630
---
```

Das Vorschaubild (für LinkedIn, Messenger, Suchmaschinen) erzeugt `python3 .github/vorschaubilder.py` aus Titel, Themenfeld, Datum und Grafik aller Beiträge in `_posts`. Es liegt dann unter `assets/img/vorschau/<titel>.png`. Seiten ohne eigenes Bild nutzen `standard.png` (festgelegt in `_config.yml`).

Abschnitt für die Politik und Quellenliste:

```html
<section class="folgt" markdown="1">
## Was folgt daraus?
...
</section>

## Quellen
<ol class="quellen">
<li><a href="https://...">Titel der Quelle</a>, Herausgeber, Datum.</li>
</ol>
```

## Lokale Vorschau

```
bundle install
bundle exec jekyll serve --drafts
```

## Auffindbarkeit

- `sitemap.xml`, `feed.xml` und die Meta-Tags erzeugen die Plugins jekyll-sitemap, jekyll-feed und jekyll-seo-tag.
- `robots.txt` verweist auf die Sitemap.
- IndexNow: Die Datei `<schluessel>.txt` im Hauptverzeichnis ist der Schlüssel. Der Workflow „Veröffentlichen" meldet nach jedem Lauf alle Seiten der Sitemap an api.indexnow.org (Bing und weitere Suchmaschinen). Google nimmt daran nicht teil.
- Google Search Console und Bing Webmaster Tools: Bestätigungscodes gehören in `_config.yml` unter `webmaster_verifications`.

## Grundsätze

Keine Cookies, kein Tracking, keine Inhalte von fremden Servern. Nichts geht ohne Freigabe von Martin Kriegel online.
