/**
 * Record portfolio demo videos with system Edge/Chrome (Playwright).
 * Usage: node tools/record-demos/record-demo.mjs
 */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { chromium } from "playwright";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "../..");
const OUT_DIR = path.join(ROOT, "public/demos/raw");
const FINAL = path.join(ROOT, "public/demos/portfolio-demo.webm");
const POSTER = path.join(ROOT, "public/demos/portfolio-demo-poster.png");
const PORT = Number(process.env.PORT || 8765);

async function launchBrowser() {
  for (const channel of ["msedge", "chrome"]) {
    try {
      return await chromium.launch({ channel, headless: true });
    } catch {
      /* next */
    }
  }
  return chromium.launch({ headless: true });
}

async function main() {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  fs.mkdirSync(path.dirname(FINAL), { recursive: true });

  const { createServer } = await import("http");
  const handler = (await import("serve-handler")).default;
  const server = createServer((req, res) =>
    handler(req, res, { public: ROOT, cleanUrls: false })
  );
  await new Promise((r) => server.listen(PORT, r));
  const base = `http://127.0.0.1:${PORT}`;

  const browser = await launchBrowser();
  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    recordVideo: { dir: OUT_DIR, size: { width: 1440, height: 900 } },
  });
  const page = await context.newPage();

  const steps = [
    { url: `${base}/index.html`, wait: 2500 },
    { url: `${base}/projects.html`, wait: 2000 },
    { url: `${base}/demos.html`, wait: 2000 },
    { url: `${base}/contact.html`, wait: 2000 },
  ];

  for (const step of steps) {
    await page.goto(step.url, { waitUntil: "domcontentloaded", timeout: 60000 });
    await page.waitForTimeout(step.wait);
  }

  await page.screenshot({ path: POSTER, fullPage: false });
  const video = page.video();
  await context.close();
  await browser.close();
  server.close();

  if (video) {
    const src = await video.path();
    if (src && fs.existsSync(src)) {
      fs.copyFileSync(src, FINAL);
      console.log(`Saved ${FINAL}`);
    }
  }
  console.log(`Poster ${POSTER}`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
