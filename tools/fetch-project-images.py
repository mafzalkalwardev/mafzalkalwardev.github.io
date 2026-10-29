#!/usr/bin/env python3
"""Fetch/create proper PNG thumbnails for portfolio projects that still use SVG placeholders."""
from __future__ import annotations

import json
import re
import subprocess
import time
from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "projects"
USER = "mafzalkalwardev"
W, H = 1280, 800  # capture; save as 640x400

# Newly added / placeholder SVG targets
TARGETS = [
    "indus-carrier-directory",
    "tony-ai-agent",
    "ipecs-auto-dialer",
    "indus-web-reviewer",
    "gv-auto-dialer-chrome-extension",
    "bpexch",
    "ecommerce-showcase-blazor",
    "ecommerce-showcase-web-blazor",
    "free-top-deals",
    "ft-solutions-hub",
    "graph-algorithms-cpp",
    "guillermo-tays-it-solutions",
    "inventory-control-system",
    "lasoado-and-jasmine",
    "margarito-ramirez-llc-nextjs-website",
    "mood-analyzer-cpp",
    "pakoption",
    "portfolio-storybook",
    "professional-portfolio",
    "restaurant-management",
    "school-management-system-cpp",
    "smart-bite",
    "student-management-system-blazor",
    "toolzology-chrome-extension",
    "travel-agency-inventory-cache",
    "travel-agency-website",
]

LIVE_HINTS = {
    "gv-auto-dialer-chrome-extension": "https://www.induswebagency.com",
    "guillermo-tays-it-solutions": "https://guillermo-tays-it-solutions.vercel.app",
    "travel-agency-website": "https://al-qibla-air-services.vercel.app",
    "pakoption": "https://pakoption.vercel.app",
    "free-top-deals": "https://free-top-deals.vercel.app",
    "ft-solutions-hub": "https://ft-solutions-hub.vercel.app",
    "professional-portfolio": "https://mafzalkalwardev.github.io",
    "portfolio-storybook": "https://mafzalkalwardev.github.io",
    "indus-carrier-directory": "https://indus-carrier-directory.vercel.app",
    "margarito-ramirez-llc-nextjs-website": "https://margarito-ramirez-llc-nextjs-website.vercel.app",
    "smart-bite": "https://smart-bite.vercel.app",
    "bpexch": "https://bpexch.vercel.app",
}


def load_projects():
    node = subprocess.run(
        [
            "node",
            "-e",
            "const fs=require('fs');const t=fs.readFileSync('js/projects-data.js','utf8').replace(/^\\uFEFF/,'');"
            "global.window=global;eval(t);process.stdout.write(JSON.stringify(window.PORTFOLIO_PROJECTS));",
        ],
        cwd=str(ROOT),
        capture_output=True,
    )
    return json.loads(node.stdout.decode("utf-8"))


def gh_api(path: str):
    p = subprocess.run(["gh", "api", path], capture_output=True, text=True)
    if p.returncode != 0:
        return None
    try:
        return json.loads(p.stdout)
    except json.JSONDecodeError:
        return None


def http_get(url: str, timeout=25) -> bytes | None:
    try:
        req = Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 portfolio-image-bot",
                "Accept": "*/*",
            },
        )
        with urlopen(req, timeout=timeout) as r:
            return r.read()
    except Exception:
        return None


def save_thumb(img: Image.Image, dest: Path) -> None:
    img = img.convert("RGB")
    # cover-fit 640x400
    tw, th = 640, 400
    scale = max(tw / img.width, th / img.height)
    nw, nh = int(img.width * scale), int(img.height * scale)
    img = img.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - tw) // 2
    top = (nh - th) // 2
    img = img.crop((left, top, left + tw, top + th))
    dest.parent.mkdir(parents=True, exist_ok=True)
    img.save(dest, "PNG", optimize=True)


def find_repo_images(repo: str) -> list[str]:
    """List image paths via GitHub git tree API (shallow)."""
    meta = gh_api(f"repos/{USER}/{repo}")
    if not meta:
        return []
    branch = meta.get("default_branch") or "main"
    tree = gh_api(f"repos/{USER}/{repo}/git/trees/{branch}?recursive=1")
    if not tree or "tree" not in tree:
        return []
    imgs = []
    prefer = re.compile(
        r"(screenshot|preview|demo|cover|hero|banner|og[-_]?image|readme|docs[/\\].*\.(png|jpe?g|webp)$)",
        re.I,
    )
    for item in tree["tree"]:
        if item.get("type") != "blob":
            continue
        path = item.get("path") or ""
        if not re.search(r"\.(png|jpe?g|webp)$", path, re.I):
            continue
        if any(
            skip in path.lower()
            for skip in [
                "node_modules",
                ".git/",
                "favicon",
                "icon-",
                "logo-only",
                "apple-touch",
            ]
        ):
            continue
        # skip tiny likely icons by name
        if re.search(r"(favicon|icon|logo)[-_]?\d*\.(png|jpe?g|webp)$", path, re.I):
            if "screenshot" not in path.lower() and "preview" not in path.lower():
                continue
        score = 0
        if prefer.search(path):
            score += 10
        if path.lower().startswith(("assets/", "public/", "docs/", "images/", "screenshots/", "media/")):
            score += 5
        if path.lower().count("/") <= 2:
            score += 1
        imgs.append((score, path))
    imgs.sort(key=lambda x: (-x[0], x[1]))
    urls = []
    for _, path in imgs[:12]:
        urls.append(f"https://raw.githubusercontent.com/{USER}/{repo}/{branch}/{path}")
    return urls


def try_download_image(urls: list[str]) -> Image.Image | None:
    for url in urls:
        data = http_get(url)
        if not data or len(data) < 8000:
            continue
        try:
            img = Image.open(BytesIO(data))
            if img.width < 200 or img.height < 120:
                continue
            return img.convert("RGB")
        except Exception:
            continue
    return None


def branded_card(name: str, desc: str, tags: list[str], accent="#F5A623") -> Image.Image:
    img = Image.new("RGB", (W, H), "#0B1F3A")
    draw = ImageDraw.Draw(img)
    # gradient-ish bars
    for i in range(H):
        mix = int(15 + (i / H) * 40)
        draw.line([(0, i), (W, i)], fill=(11, 31 + mix // 3, 58 + mix // 2))
    # frame
    draw.rounded_rectangle([40, 40, W - 40, H - 40], radius=28, outline=accent, width=3)
    draw.rounded_rectangle([56, 56, W - 56, H - 56], radius=22, outline="#1e3a5f", width=2)
    # accent pill
    draw.rounded_rectangle([80, 90, 260, 130], radius=16, fill=accent)
    try:
        font_title = ImageFont.truetype("segoeui.ttf", 54)
        font_body = ImageFont.truetype("segoeui.ttf", 28)
        font_small = ImageFont.truetype("segoeui.ttf", 22)
        font_pill = ImageFont.truetype("segoeuib.ttf", 20)
    except Exception:
        font_title = font_body = font_small = font_pill = ImageFont.load_default()
    draw.text((100, 98), "PROJECT", fill="#0B1F3A", font=font_pill)
    # title wrap
    title = name[:48]
    draw.text((80, 170), title, fill="#FFFFFF", font=font_title)
    # description
    words = (desc or "")[:180].split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if len(trial) > 58:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    y = 280
    for line in lines[:4]:
        draw.text((80, y), line, fill="#94A3B8", font=font_body)
        y += 40
    # tags
    x = 80
    y = H - 140
    for tag in (tags or [])[:4]:
        tw = max(90, len(tag) * 14 + 28)
        draw.rounded_rectangle([x, y, x + tw, y + 44], radius=12, fill="#1e3a5f")
        draw.text((x + 14, y + 10), tag[:18], fill="#E2E8F0", font=font_small)
        x += tw + 14
    draw.text((80, H - 80), "Muhammad Afzal Kalwar  ·  @mafzalkalwardev", fill="#64748B", font=font_small)
    return img


def screenshot_urls(urls: list[str], out_path: Path) -> bool:
    """Use playwright CLI via node script for reliability."""
    script = ROOT / "tools" / "_shot.mjs"
    script.write_text(
        """
import { chromium } from 'playwright';
import fs from 'fs';

const urls = JSON.parse(process.argv[2]);
const out = process.argv[3];

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
let ok = false;
for (const url of urls) {
  try {
    const res = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 25000 });
    if (!res || res.status() >= 400) continue;
    await page.waitForTimeout(1800);
    // hide cookie banners roughly
    await page.addStyleTag({ content: 'html,body{overflow:hidden!important}' }).catch(()=>{});
    await page.screenshot({ path: out, type: 'png', fullPage: false });
    const st = fs.statSync(out);
    if (st.size > 20000) { ok = true; break; }
  } catch (e) {
    // try next
  }
}
await browser.close();
process.exit(ok ? 0 : 1);
""",
        encoding="utf-8",
    )
    tmp = out_path.with_suffix(".raw.png")
    p = subprocess.run(
        ["node", str(script), json.dumps(urls), str(tmp)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if p.returncode != 0 or not tmp.exists():
        return False
    try:
        img = Image.open(tmp)
        save_thumb(img, out_path)
        tmp.unlink(missing_ok=True)
        return out_path.exists() and out_path.stat().st_size > 8000
    except Exception:
        return False


def candidate_live_urls(slug: str, repo: str, project: dict) -> list[str]:
    urls = []
    if project.get("live"):
        urls.append(project["live"])
    if slug in LIVE_HINTS:
        urls.append(LIVE_HINTS[slug])
    # common vercel / github pages guesses
    urls += [
        f"https://{repo}.vercel.app",
        f"https://{USER}.github.io/{repo}/",
        f"https://{slug}.vercel.app",
    ]
    # dedupe keep order
    seen = set()
    out = []
    for u in urls:
        if u and u not in seen and "localhost" not in u:
            seen.add(u)
            out.append(u)
    return out


def main():
    projects = {p["slug"]: p for p in load_projects()}
    # also map by lowercase repo
    by_repo = {p["repo"].lower(): p for p in load_projects()}
    results = []
    ASSETS.mkdir(parents=True, exist_ok=True)

    for slug in TARGETS:
        p = projects.get(slug) or by_repo.get(slug)
        if not p:
            results.append({"slug": slug, "status": "missing-in-data"})
            continue
        repo = p["repo"]
        dest = ASSETS / f"{slug}.png"
        print(f"[{slug}] start", flush=True)

        # Skip if we already have a real PNG from a previous pass
        if dest.exists() and dest.stat().st_size > 40000:
            p["image"] = f"assets/projects/{slug}.png"
            results.append(
                {
                    "slug": slug,
                    "status": "ok",
                    "source": "existing-png",
                    "bytes": dest.stat().st_size,
                }
            )
            print(f"[{slug}] existing-png -> {dest.stat().st_size}", flush=True)
            continue

        # 1) repo embedded images
        img = try_download_image(find_repo_images(repo))
        source = "repo-asset" if img else None

        # 2) live / pages screenshots
        if img is None:
            lives = candidate_live_urls(slug, repo, p)
            tmp_png = ASSETS / f"{slug}.shot.png"
            if screenshot_urls(lives, tmp_png):
                with Image.open(tmp_png) as im:
                    img = im.convert("RGB").copy()
                source = "live-shot"
            try:
                tmp_png.unlink(missing_ok=True)
            except PermissionError:
                pass

        # 3) GitHub repo page screenshot as last real capture
        if img is None:
            tmp_png = ASSETS / f"{slug}.gh.png"
            if screenshot_urls([p["url"]], tmp_png):
                with Image.open(tmp_png) as im:
                    img = im.convert("RGB").copy()
                source = "github-page"
            try:
                tmp_png.unlink(missing_ok=True)
            except PermissionError:
                pass

        # 4) branded card fallback
        if img is None:
            img = branded_card(p.get("name") or slug, p.get("description") or "", p.get("tags") or [])
            source = "branded-card"

        save_thumb(img, dest)
        # point data at png
        p["image"] = f"assets/projects/{slug}.png"
        # remove weak svg placeholder if present
        svg = ASSETS / f"{slug}.svg"
        if svg.exists() and svg.stat().st_size < 2500:
            svg.unlink()
        results.append({"slug": slug, "status": "ok", "source": source, "bytes": dest.stat().st_size})
        print(f"[{slug}] {source} -> {dest.stat().st_size}", flush=True)
        time.sleep(0.3)

    # rewrite projects-data.js with updated image paths
    all_projects = load_projects()
    by_slug = {r["slug"]: r for r in results if r.get("status") == "ok"}
    for p in all_projects:
        if p["slug"] in by_slug:
            p["image"] = f"assets/projects/{p['slug']}.png"

    def js_str(s):
        return json.dumps(s, ensure_ascii=False)

    lines = ["window.PORTFOLIO_PROJECTS = ["]
    for i, p in enumerate(all_projects):
        lines.append("  {")
        for key in ("slug", "name", "repo", "description", "category", "tags", "url", "image"):
            lines.append(f"    {key}: {js_str(p[key])},")
        if p.get("live"):
            lines.append(f"    live: {js_str(p['live'])},")
        if p.get("video"):
            lines.append(f"    video: {js_str(p['video'])},")
        comma = "," if i < len(all_projects) - 1 else ""
        lines.append(f"    featured: {'true' if p.get('featured') else 'false'}")
        lines.append(f"  }}{comma}")
    lines.append("];")
    lines.append("")
    (ROOT / "js" / "projects-data.js").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

    # bump cache
    for html_name in ("index.html", "projects.html", "about.html", "demos.html"):
        path = ROOT / html_name
        if not path.exists():
            continue
        t = path.read_text(encoding="utf-8")
        t = re.sub(r"projects-data\.js\?v=\d+", "projects-data.js?v=16", t)
        path.write_text(t, encoding="utf-8", newline="\n")

    print(json.dumps(results, indent=2))
    ok = sum(1 for r in results if r.get("status") == "ok")
    print(f"DONE ok={ok}/{len(results)}")


if __name__ == "__main__":
    main()
