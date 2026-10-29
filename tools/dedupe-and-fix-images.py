#!/usr/bin/env python3
"""Remove near-duplicate portfolio projects and replace blank thumbnails."""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "js" / "projects-data.js"
ASSETS = ROOT / "assets" / "projects"
GEN = Path(
    r"C:\Users\pc\.cursor\projects\d-Dispatch-Softwares-Auto-AI-Agent-Dialer-GoogleVoiceAgent-Active\assets"
)

# Keep the stronger project; drop these slugs
DROP = {
    "tony-ai",  # keep tony-ai-agent
    "toolzology-chrome-extension",  # keep v2
    "ecommerce-showcase-blazor",  # keep web-blazor
    "restaurant-management-react",  # blank image; keep restaurant-management
    "portfolio-storybook",  # duplicate of professional-portfolio image
    "professional-portfolio",  # keep portfolio-afzal-kalwar-vite as site portfolio
    "quizmaster-backend-complete",  # keep online-testing-system
    "email-verifier-pro",  # overlap with email-verification-platform
    "safer-carrier-extractor",  # overlap with fmcsa/safer-web
    "simple-learning-dashboard",  # keep learningdashboard
    "callauditx-nest-react",  # overlap with CallAudit-X
}

# Prefer these as featured (unique flagship set)
FEATURED = [
    "al-qibla-air-services",
    "tony-ai-agent",
    "sms-marketing-crm",
    "indus-transport-auto-dialer",
    "bulk-email-verifier",
    "fiverr-lead-extractor-crm",
    "callaudit-x",
    "google-voice-dispatch-agent",
    "playwright-website-scraper-pro",
    "mighty-trucking",
    "indus-carrier-directory",
    "gv-auto-dialer-chrome-extension",
]


def load_projects():
    node = subprocess.run(
        [
            "node",
            "-e",
            "const fs=require('fs');const t=fs.readFileSync('js/projects-data.js','utf8');"
            "global.window=global;eval(t);process.stdout.write(JSON.stringify(window.PORTFOLIO_PROJECTS));",
        ],
        cwd=str(ROOT),
        capture_output=True,
    )
    return json.loads(node.stdout.decode("utf-8"))


def cover_save(im: Image.Image, dest: Path):
    im = im.convert("RGB")
    tw, th = 640, 400
    scale = max(tw / im.width, th / im.height)
    nw, nh = int(im.width * scale), int(im.height * scale)
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - tw) // 2
    top = (nh - th) // 2
    im.crop((left, top, left + tw, top + th)).save(dest, "PNG", optimize=True)


def import_generated(slug: str) -> bool:
    candidates = [
        GEN / f"{slug}.png",
        GEN / f"{slug}.jpg",
        GEN / f"{slug}.jpeg",
        GEN / f"{slug}.webp",
    ]
    # also any file starting with slug
    for f in GEN.glob(f"{slug}.*"):
        candidates.append(f)
    for src in candidates:
        if src.exists() and src.stat().st_size > 20000:
            cover_save(Image.open(src), ASSETS / f"{slug}.png")
            print(f"imported {slug} from {src.name}")
            return True
    return False


def color_count(path: Path) -> int:
    im = Image.open(path).convert("RGB").resize((40, 25))
    return len(set(im.getdata()))


def emit(projects):
    def js_str(s):
        return json.dumps(s, ensure_ascii=False)

    lines = ["window.PORTFOLIO_PROJECTS = ["]
    for i, p in enumerate(projects):
        lines.append("  {")
        for key in ("slug", "name", "repo", "description", "category", "tags", "url", "image"):
            lines.append(f"    {key}: {js_str(p[key])},")
        if p.get("live"):
            lines.append(f"    live: {js_str(p['live'])},")
        if p.get("video"):
            lines.append(f"    video: {js_str(p['video'])},")
        comma = "," if i < len(projects) - 1 else ""
        lines.append(f"    featured: {'true' if p.get('featured') else 'false'}")
        lines.append(f"  }}{comma}")
    lines.append("];")
    lines.append("")
    DATA.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def main():
    projects = load_projects()
    before = len(projects)

    # Fix blank images for keepers
    blank_fix = [
        "sms-marketing-crm",
        "screen-capture-app",
        "datx-chrome-extension",
        "google-workspace-bulk-user-provisioning",
        "portfolio-afzal-kalwar-vite",
    ]
    for slug in blank_fix:
        png = ASSETS / f"{slug}.png"
        needs = (not png.exists()) or png.stat().st_size < 10000 or color_count(png) < 12
        if needs:
            if not import_generated(slug):
                print(f"WARN no generated image for {slug}")

    # Dedupe by slug drop list
    kept = []
    seen_repo = set()
    seen_url = set()
    dropped = []
    for p in projects:
        slug = (p.get("slug") or "").lower()
        repo = (p.get("repo") or "").lower()
        url = (p.get("url") or "").lower()
        if slug in DROP:
            dropped.append(slug)
            continue
        if repo in seen_repo or url in seen_url:
            dropped.append(slug + "(repo/url-dup)")
            continue
        seen_repo.add(repo)
        seen_url.add(url)
        # normalize image to png if present
        png = ASSETS / f"{slug}.png"
        if png.exists():
            p["image"] = f"assets/projects/{slug}.png"
        p["featured"] = slug in FEATURED
        kept.append(p)

    # Stable featured-first then alpha
    featured = [p for p in kept if p.get("featured")]
    # preserve FEATURED order
    feat_map = {p["slug"].lower(): p for p in featured}
    featured_ordered = [feat_map[s] for s in FEATURED if s in feat_map]
    rest = sorted(
        [p for p in kept if not p.get("featured")], key=lambda x: x["name"].lower()
    )
    final = featured_ordered + rest

    emit(final)
    total = len(final)

    # Update HTML counts + cache bust
    for html_name in ("index.html", "projects.html", "about.html", "demos.html", "skills.html", "contact.html"):
        path = ROOT / html_name
        if not path.exists():
            continue
        t = path.read_text(encoding="utf-8")
        t = re.sub(r'data-count="\d+"(\s+data-project-count)', rf'data-count="{total}"\1', t)
        t = re.sub(
            r'<span id="projectsPageCount">.*?</span>',
            f'<span id="projectsPageCount">{total} curated portfolio projects</span>',
            t,
        )
        t = re.sub(r"projects-data\.js\?v=\d+", "projects-data.js?v=18", t)
        t = re.sub(r"projects\.js\?v=\d+", "projects.js?v=18", t)
        path.write_text(t, encoding="utf-8", newline="\n")

    print(f"before={before} after={total} dropped={dropped}")


if __name__ == "__main__":
    main()
