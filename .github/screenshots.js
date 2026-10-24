// Erzeugt Bildschirmfotos der gebauten Website aus _site.
// Läuft nur in der GitHub-Aktion "Vorschau", nicht auf der Website.
const { chromium } = require("playwright");
const http = require("http");
const fs = require("fs");
const path = require("path");

const root = path.resolve("_site");
const out = path.resolve("screenshots");
fs.mkdirSync(out, { recursive: true });

const types = { ".html": "text/html; charset=utf-8", ".css": "text/css", ".svg": "image/svg+xml", ".woff2": "font/woff2", ".xml": "application/xml", ".png": "image/png", ".jpg": "image/jpeg" };

const server = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split("?")[0]);
  if (p.endsWith("/")) p += "index.html";
  let file = path.join(root, p);
  if (!fs.existsSync(file) && fs.existsSync(file + ".html")) file += ".html";
  if (!fs.existsSync(file) || fs.statSync(file).isDirectory()) { res.writeHead(404); res.end("404"); return; }
  res.writeHead(200, { "Content-Type": types[path.extname(file)] || "application/octet-stream" });
  fs.createReadStream(file).pipe(res);
});

const pages = [
  ["startseite", "/"],
  ["beitraege", "/beitraege/"],
  ["beitrag", "/beitraege/stromausfall-im-krankenhaus/"],
  ["ueber-mich", "/ueber-mich/"],
  ["kontakt", "/kontakt/"],
  ["impressum", "/impressum/"],
  ["datenschutz", "/datenschutz/"],
];
const widths = [["desktop", 1280], ["mobil", 390]];

(async () => {
  await new Promise((r) => server.listen(4100, r));
  const browser = await chromium.launch();
  for (const [name, width] of widths) {
    const ctx = await browser.newContext({ viewport: { width, height: 900 }, deviceScaleFactor: 1 });
    const page = await ctx.newPage();
    for (const [slug, url] of pages) {
      const resp = await page.goto("http://localhost:4100" + url, { waitUntil: "networkidle" });
      if (!resp || resp.status() !== 200) { console.log("FEHLER", url, resp && resp.status()); continue; }
      await page.screenshot({ path: path.join(out, `${slug}-${name}.png`), fullPage: true });
      console.log("ok", url, name);
    }
    await ctx.close();
  }
  await browser.close();
  server.close();
})();
