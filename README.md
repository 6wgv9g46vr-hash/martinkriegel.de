# martinkriegel.de

Persönlicher Fachblog von Martin Kriegel. Statische Website mit Jekyll, gehostet über GitHub Pages.

## Aufbau

- `_posts/` veröffentlichte Beiträge (Markdown, Dateiname `JJJJ-MM-TT-titel.md`)
- `_drafts/` Entwürfe, erscheinen nur in der lokalen Vorschau mit `--drafts`
- `_layouts/`, `_includes/` Seitengerüst
- `assets/css/style.css` Gestaltung
- `assets/fonts/` selbst gehostete Schriften (Newsreader, Public Sans; SIL Open Font License)
- `assets/img/` Grafiken
- `index.html`, `beitraege/`, `ueber-mich.md`, `kontakt.md`, `impressum.md`, `datenschutz.md`, `404.html`
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
---
```

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

## Grundsätze

Keine Cookies, kein Tracking, keine Inhalte von fremden Servern. Nichts geht ohne Freigabe von Martin Kriegel online.
