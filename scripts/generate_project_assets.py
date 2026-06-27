"""Generate project metadata and professional SVG screenshots for portfolio."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

OWNER = "mafzalkalwardev"
ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets" / "projects"
SKIP = {
    "mafzalkalwardev",
    "professional-portfolio",
    "mafzalkalwardev.github.io",
    "odysseus",
    "rdp",
    "ft-solutions-hub",
}

CATEGORY_MAP = {
    "indus-transport-auto-dialer": "desktop",
    "python-auto-dialer-pro": "desktop",
    "google-voice-dispatch-agent": "automation",
    "bulk-email-verifier": "email",
    "mailforge": "email",
    "python-smtp-email-automation": "email",
    "multi-smtp-email-automation": "email",
    "email-verifier-pro": "email",
    "email-verification-platform": "email",
    "fiverr-lead-extractor-crm": "web",
    "CallAudit-X": "web",
    "playwright-website-scraper-pro": "scraper",
    "Canadian-Website-Scraper": "scraper",
    "safer-carrier-extractor": "scraper",
    "safer-web-scraper": "scraper",
    "fmcsa-safer-scraper": "scraper",
    "mnist-cnn-digit-recognition": "ml",
    "dat-stream-studio": "web",
    "excel-call-queue-automator": "desktop",
    "quizmaster-online-testing-system": "web",
    "indus-transports-dispatch-website": "website",
    "kb-transport-llc-website": "website",
    "one-stop-car-care-website": "website",
    "portfilio": "website",
    "LearningDashboard": "web",
    "clientreadyftsolutionsdombom": "web",
    "online-food-delivery": "web",
}


def gh_json(*args: str) -> list | dict:
    out = subprocess.check_output(["gh", *args], text=True)
    return json.loads(out)


def title(name: str) -> str:
    special = {"crm": "CRM", "api": "API", "smtp": "SMTP", "mc": "MC", "dat": "DAT", "x": "X"}
    return " ".join(special.get(p.lower(), p.capitalize()) for p in name.replace("_", "-").split("-"))


def category(name: str, lang: str | None) -> str:
    if name in CATEGORY_MAP:
        return CATEGORY_MAP[name]
    if lang in ("HTML", "EJS"):
        return "website"
    if lang in ("TypeScript", "JavaScript"):
        return "web"
    if lang == "Python":
        return "automation"
    if lang == "Go":
        return "email"
    return "web"


def svg_mockup(name: str, cat: str, desc: str) -> str:
    t = title(name)
    accent = "#2563eb"
    bg = "#f8fafc"
    panel = "#ffffff"
    border = "#e2e8f0"
    text = "#0f172a"
    muted = "#64748b"

    ui = ""
    if cat == "desktop":
        ui = f"""
        <rect x="48" y="72" width="704" height="360" rx="8" fill="{panel}" stroke="{border}"/>
        <rect x="48" y="72" width="704" height="36" rx="8" fill="#eef2f7"/>
        <circle cx="68" cy="90" r="5" fill="#cbd5e1"/><circle cx="84" cy="90" r="5" fill="#cbd5e1"/>
        <rect x="120" y="130" width="280" height="24" rx="4" fill="#eef2f7"/>
        <rect x="120" y="170" width="200" height="16" rx="3" fill="#eef2f7"/>
        <rect x="120" y="220" width="160" height="40" rx="6" fill="{accent}" opacity="0.9"/>
        <rect x="420" y="130" width="280" height="220" rx="6" fill="#eef2f7"/>
        """
    elif cat == "email":
        ui = f"""
        <rect x="80" y="90" width="640" height="320" rx="10" fill="{panel}" stroke="{border}"/>
        <rect x="110" y="130" width="580" height="48" rx="6" fill="#eef2f7"/>
        <rect x="110" y="190" width="420" height="14" rx="3" fill="#eef2f7"/>
        <rect x="110" y="214" width="360" height="14" rx="3" fill="#eef2f7"/>
        <rect x="110" y="260" width="120" height="36" rx="6" fill="{accent}" opacity="0.85"/>
        <circle cx="620" cy="154" r="16" fill="#dcfce7" stroke="#86efac"/>
        """
    elif cat == "scraper":
        ui = f"""
        <rect x="60" y="80" width="680" height="340" rx="10" fill="{panel}" stroke="{border}"/>
        <rect x="90" y="120" width="620" height="28" fill="#eef2f7"/>
        <rect x="90" y="160" width="620" height="20" fill="#f8fafc"/>
        <rect x="90" y="190" width="620" height="20" fill="#f8fafc"/>
        <rect x="90" y="220" width="620" height="20" fill="#f8fafc"/>
        <rect x="90" y="280" width="140" height="36" rx="6" fill="{accent}" opacity="0.85"/>
        """
    elif cat == "ml":
        ui = f"""
        <rect x="100" y="90" width="600" height="320" rx="10" fill="{panel}" stroke="{border}"/>
        <polyline points="140,340 220,280 300,300 380,220 460,240 540,160 620,180" fill="none" stroke="{accent}" stroke-width="3"/>
        <rect x="140" y="120" width="520" height="160" rx="6" fill="#eef2f7"/>
        """
    elif cat == "website":
        ui = f"""
        <rect x="140" y="70" width="520" height="360" rx="12" fill="{panel}" stroke="{border}"/>
        <rect x="140" y="70" width="520" height="48" fill="#eef2f7"/>
        <rect x="170" y="140" width="300" height="28" rx="4" fill="#eef2f7"/>
        <rect x="170" y="180" width="220" height="14" rx="3" fill="#eef2f7"/>
        <rect x="170" y="240" width="120" height="36" rx="6" fill="{accent}" opacity="0.85"/>
        """
    else:
        ui = f"""
        <rect x="70" y="85" width="660" height="330" rx="10" fill="{panel}" stroke="{border}"/>
        <rect x="100" y="120" width="280" height="180" rx="6" fill="#eef2f7"/>
        <rect x="410" y="120" width="280" height="24" rx="4" fill="#eef2f7"/>
        <rect x="410" y="156" width="240" height="14" rx="3" fill="#eef2f7"/>
        <rect x="410" y="200" width="160" height="36" rx="6" fill="{accent}" opacity="0.85"/>
        """

    desc_short = (desc or t)[:80].replace("&", "&amp;").replace("<", "&lt;")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="800" height="450" viewBox="0 0 800 450">
  <rect width="800" height="450" fill="{bg}"/>
  {ui}
  <text x="400" y="420" fill="{muted}" font-family="Segoe UI, Inter, Arial, sans-serif" font-size="13" text-anchor="middle">{desc_short}</text>
  <text x="400" y="36" fill="{text}" font-family="Segoe UI, Inter, Arial, sans-serif" font-size="20" font-weight="600" text-anchor="middle">{t}</text>
</svg>"""


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    repos = gh_json("repo", "list", OWNER, "--limit", "100", "--json", "name,description,primaryLanguage,isFork")
    projects = []
    for r in repos:
        if r.get("isFork") or r["name"] in SKIP:
            continue
        name = r["name"]
        lang = (r.get("primaryLanguage") or {}).get("name")
        desc = r.get("description") or f"Open source {title(name)} project."
        cat = category(name, lang)
        tags = []
        if lang:
            tags.append(lang)
        if cat == "desktop":
            tags.extend(["Python", "PyQt6"])
        elif cat == "email":
            tags.extend(["SMTP", "Automation"])
        elif cat == "scraper":
            tags.extend(["Playwright", "Python"])
        elif cat == "web":
            tags.extend(["React", "Node.js"])
        tags = list(dict.fromkeys(tags))[:4]
        slug_name = name.lower().replace(" ", "-")
        svg_path = ASSETS / f"{slug_name}.svg"
        png_path = ASSETS / f"{slug_name}.png"
        if not png_path.exists():
            svg_path.write_text(svg_mockup(name, cat, desc), encoding="utf-8")
        image = f"assets/projects/{slug_name}.png" if png_path.exists() else f"assets/projects/{slug_name}.svg"
        video_path = ROOT / "assets" / "videos" / f"{slug_name}.webm"
        entry = {
            "slug": slug_name,
            "name": title(name),
            "repo": name,
            "description": desc,
            "category": cat,
            "tags": tags,
            "url": f"https://github.com/{OWNER}/{name}",
            "image": image,
            "featured": name in {
                "indus-transport-auto-dialer", "bulk-email-verifier",
                "google-voice-dispatch-agent", "fiverr-lead-extractor-crm",
                "CallAudit-X", "playwright-website-scraper-pro",
            },
        }
        if video_path.exists():
            entry["video"] = f"assets/videos/{slug_name}.webm"
        projects.append(entry)

    projects.sort(key=lambda p: (not p["featured"], p["name"]))
    js = "window.PORTFOLIO_PROJECTS = " + json.dumps(projects, indent=2) + ";\n"
    (ROOT / "js" / "projects-data.js").write_text(js, encoding="utf-8")
    print(f"Generated {len(projects)} project screenshots and projects-data.js")


if __name__ == "__main__":
    main()
