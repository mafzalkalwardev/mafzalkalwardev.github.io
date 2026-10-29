#!/usr/bin/env python3
"""Sync js/projects-data.js from public GitHub repos; keep curated metadata."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "js" / "projects-data.js"
ASSETS = ROOT / "assets" / "projects"

SKIP = {
    "mafzalkalwardev",
    "ayesha",
    "ayesha-desires",
    "little-world-of-ayesha",
    "confession",
    "memory-scrapbook",
    "desires",
    "quickdraw-test",
    "mywebpagetask",
    "rdp",
    "dev",
    "portfilio",
    "mafzalkalwardev.github.io",
}
SOFT_SKIP = {"devops", "devops2"}
FEATURED_EXTRA = {
    "indus-carrier-directory",
    "tony-ai-agent",
    "gv-auto-dialer-chrome-extension",
    "ipecs-auto-dialer",
    "indus-web-reviewer",
    "python-auto-dialer-pro",
}


def gh_json(args: list[str]):
    p = subprocess.run(["gh", *args], capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit(p.stderr)
    return json.loads(p.stdout)


def load_existing():
    node = subprocess.run(
        [
            "node",
            "-e",
            "const fs=require('fs');"
            "const t=fs.readFileSync('js/projects-data.js','utf8').replace(/^\\uFEFF/, '');"
            "global.window=global; eval(t);"
            "console.log(JSON.stringify(window.PORTFOLIO_PROJECTS));",
        ],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    if node.returncode != 0:
        raise SystemExit(node.stderr)
    return json.loads(node.stdout)


def list_repos():
    repos = []
    page = 1
    while True:
        batch = gh_json(
            [
                "api",
                f"user/repos?per_page=100&page={page}&affiliation=owner&sort=updated",
            ]
        )
        if not batch:
            break
        for r in batch:
            if r.get("fork") or r.get("private") or r.get("archived"):
                continue
            if r["name"].lower() in SKIP:
                continue
            repos.append(r)
        if len(batch) < 100:
            break
        page += 1
    return repos


def pretty_name(repo: str) -> str:
    words = []
    for w in repo.replace("_", "-").split("-"):
        low = w.lower()
        if low in {
            "ai",
            "crm",
            "sms",
            "smtp",
            "pdf",
            "ocr",
            "api",
            "ui",
            "gv",
            "fmcsa",
            "dat",
            "cnn",
            "mnist",
            "cpp",
            "seo",
            "mc",
            "dot",
        }:
            words.append(w.upper())
        else:
            words.append(w[:1].upper() + w[1:] if w else w)
    return " ".join(words)


def category_for(name, desc, lang, topics):
    blob = f"{name} {desc} {' '.join(topics)}".lower()
    if any(k in blob for k in ["dialer", "electron", "pyqt", "desktop"]):
        return "desktop"
    if any(
        k in blob
        for k in [
            "ml",
            "cnn",
            "mnist",
            "ai-agent",
            "voice-ai",
            "tensorflow",
            "nlp",
            "fake-news",
            "tony",
        ]
    ):
        return "ml"
    if any(
        k in blob
        for k in [
            "scraper",
            "selenium",
            "playwright",
            "automation",
            "smtp",
            "sms",
            "excel",
            "pdf",
            "ocr",
            "verifier",
        ]
    ):
        return "automation"
    if lang in ("C++", "C"):
        return "systems"
    return "web"


def tags_for(name, desc, lang, topics):
    tags = []
    if lang:
        tags.append("C++" if lang == "C++" else lang)
    blob = f"{name} {desc}".lower()
    mapping = [
        ("react", "React"),
        ("next", "Next.js"),
        ("fastapi", "FastAPI"),
        ("playwright", "Playwright"),
        ("selenium", "Selenium"),
        ("chrome", "Chrome Extension"),
        ("dialer", "Auto Dialer"),
        ("email", "Email"),
        ("smtp", "SMTP"),
        ("sms", "SMS"),
        ("crm", "CRM"),
        ("fmcsa", "FMCSA"),
        ("scraper", "Web Scraping"),
        ("blazor", "Blazor"),
        ("electron", "Electron"),
        ("ai", "AI"),
        ("voice", "Voice AI"),
        ("dispatch", "Dispatch"),
        ("logistics", "Logistics"),
        ("carrier", "Carriers"),
        ("trucking", "Trucking"),
    ]
    for key, label in mapping:
        if key in blob and label not in tags:
            tags.append(label)
    for t in topics[:4]:
        label = t.replace("-", " ").title()
        if label not in tags and len(tags) < 5:
            tags.append(label)
    return tags[:5] or ["Open Source"]


def image_for(slug: str) -> str:
    png = ASSETS / f"{slug}.png"
    svg = ASSETS / f"{slug}.svg"
    if png.exists():
        return f"assets/projects/{slug}.png"
    if svg.exists():
        return f"assets/projects/{slug}.svg"
    title = pretty_name(slug)[:28].replace("&", "and")
    svg.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="640" height="400" viewBox="0 0 640 400">'
        '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0%" stop-color="#0B1F3A"/>'
        '<stop offset="100%" stop-color="#1e3a5f"/></linearGradient></defs>'
        '<rect width="640" height="400" fill="url(#g)"/>'
        '<rect x="24" y="24" width="592" height="352" rx="16" fill="none" stroke="#F5A623" stroke-width="2" opacity="0.7"/>'
        f'<text x="320" y="190" text-anchor="middle" fill="#F5A623" font-family="Segoe UI, Arial" font-size="22" font-weight="700">{title}</text>'
        '<text x="320" y="230" text-anchor="middle" fill="#94a3b8" font-family="Segoe UI, Arial" font-size="14">Muhammad Afzal Kalwar</text>'
        "</svg>\n",
        encoding="utf-8",
    )
    return f"assets/projects/{slug}.svg"


def emit(final: list[dict]) -> None:
    def js_str(s):
        return json.dumps(s, ensure_ascii=False)

    lines = ["window.PORTFOLIO_PROJECTS = ["]
    for i, p in enumerate(final):
        lines.append("  {")
        for key in ("slug", "name", "repo", "description", "category", "tags", "url", "image"):
            lines.append(f"    {key}: {js_str(p[key])},")
        if p.get("live"):
            lines.append(f"    live: {js_str(p['live'])},")
        if p.get("video"):
            lines.append(f"    video: {js_str(p['video'])},")
        comma = "," if i < len(final) - 1 else ""
        lines.append(f"    featured: {'true' if p.get('featured') else 'false'}")
        lines.append(f"  }}{comma}")
    lines.append("];")
    lines.append("")
    DATA.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def main():
    existing = load_existing()
    repos = list_repos()
    print(f"existing={len(existing)} public_eligible={len(repos)}")

    merged = []
    seen = set()
    for p in existing:
        repo = p["repo"]
        if repo.lower() in SKIP:
            continue
        seen.add(repo.lower())
        img = p.get("image") or ""
        if not img or not (ROOT / img).exists():
            p["image"] = image_for(p.get("slug") or repo.lower())
        merged.append(p)

    added = []
    for r in repos:
        name = r["name"]
        key = name.lower()
        if key in seen or key in SOFT_SKIP:
            continue
        topics = r.get("topics") or []
        desc = (r.get("description") or "").strip() or f"{pretty_name(name)} by Muhammad Afzal Kalwar."
        lang = r.get("language") or ""
        item = {
            "slug": key,
            "name": pretty_name(name),
            "repo": name,
            "description": desc[:280],
            "category": category_for(name, desc, lang, topics),
            "tags": tags_for(name, desc, lang, topics),
            "url": r.get("html_url") or f"https://github.com/mafzalkalwardev/{name}",
            "image": image_for(key),
            "featured": name in FEATURED_EXTRA or key in FEATURED_EXTRA,
        }
        hp = (r.get("homepage") or "").strip()
        if (
            hp
            and "github.io" not in hp.lower()
            and "localhost" not in hp.lower()
            and hp.startswith("http")
        ):
            item["live"] = hp
        merged.append(item)
        added.append(name)
        seen.add(key)

    featured = [p for p in merged if p.get("featured")]
    rest = sorted(
        [p for p in merged if not p.get("featured")], key=lambda p: p["name"].lower()
    )
    final = featured + rest
    emit(final)
    print(f"total={len(final)} added={len(added)}")
    for name in added:
        print(f"  + {name}")


if __name__ == "__main__":
    main()
