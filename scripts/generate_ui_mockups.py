"""Generate polished UI mockup PNGs for portfolio projects via Playwright."""
from __future__ import annotations

import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets" / "projects"

# Skip — real screenshots provided by user
SKIP = {
    "mailforge",
    "fiverr-lead-extractor-crm",
    "python-auto-dialer-pro",
    "indus-transport-auto-dialer",
}

MOCKUPS: dict[str, dict] = {
    "bulk-email-verifier": {
        "title": "Bulk Email Verifier",
        "subtitle": "Self-hosted SMTP verification dashboard",
        "accent": "#2563eb",
        "type": "dashboard",
        "stats": [("Total Verified", "12,480"), ("Valid", "9,842"), ("Invalid", "1,203"), ("Unknown", "1,435")],
    },
    "callaudit-x": {
        "title": "CallAudit-X",
        "subtitle": "AI call auditing & analytics SaaS",
        "accent": "#7c3aed",
        "type": "analytics",
        "stats": [("Calls Today", "248"), ("Avg Score", "87%"), ("Transcribed", "196"), ("Flagged", "12")],
    },
    "playwright-website-scraper-pro": {
        "title": "Playwright Scraper Pro",
        "subtitle": "Multi-page website cloning & export",
        "accent": "#0d9488",
        "type": "scraper",
    },
    "dev": {"title": "Dev Project", "subtitle": "GitHub development workspace", "accent": "#6366f1", "type": "devops"},
    "devops": {"title": "DevOps Lab", "subtitle": "CI/CD pipeline & GitHub Actions", "accent": "#059669", "type": "devops"},
    "devops2": {"title": "DevOps Lab II", "subtitle": "Container deployment workflow", "accent": "#0891b2", "type": "devops"},
    "mouse-coordinate-tracker": {
        "title": "Mouse Coordinate Tracker",
        "subtitle": "Real-time click coordinate logger",
        "accent": "#64748b",
        "type": "utility",
    },
    "mywebpagetask": {"title": "My Web Page Task", "subtitle": "Responsive HTML/CSS project", "accent": "#3b82f6", "type": "website"},
    "mnist-cnn-digit-recognition": {
        "title": "MNIST Digit Recognition",
        "subtitle": "CNN handwritten digit classifier",
        "accent": "#8b5cf6",
        "type": "ml",
    },
    "learningdashboard": {
        "title": "Learning Dashboard",
        "subtitle": ".NET Blazor course progress tracker",
        "accent": "#512bd4",
        "type": "dashboard",
        "stats": [("Courses", "8"), ("Completed", "5"), ("Hours", "124"), ("Streak", "12d")],
    },
    "forward-email-automation": {
        "title": "Forward Email Automation",
        "subtitle": "Carrier outreach email pipeline",
        "accent": "#ea580c",
        "type": "email",
    },
    "excel-mc-data-cleaner": {
        "title": "Excel MC Data Cleaner",
        "subtitle": "VBA macro for carrier data cleanup",
        "accent": "#16a34a",
        "type": "excel",
    },
    "excel-state-extractor-formula": {
        "title": "State Extractor Formula",
        "subtitle": "Excel formula for US state parsing",
        "accent": "#15803d",
        "type": "excel",
    },
    "fmcsa-safer-scraper": {
        "title": "FMCSA SAFER Scraper",
        "subtitle": "Carrier MC data extraction tool",
        "accent": "#dc2626",
        "type": "scraper",
    },
    "excel-call-queue-automator": {
        "title": "Excel Call Queue Automator",
        "subtitle": "Excel phone list dial automation",
        "accent": "#1d4ed8",
        "type": "desktop",
    },
    "email-verifier-pro": {
        "title": "Email Verifier Pro",
        "subtitle": "Full-stack bulk email validation",
        "accent": "#2563eb",
        "type": "dashboard",
        "stats": [("Verified", "8,420"), ("Valid", "7,102"), ("Invalid", "891"), ("Risky", "427")],
    },
    "email-verification-platform": {
        "title": "Email Verification Platform",
        "subtitle": "JWT auth · CSV/XLSX bulk validation",
        "accent": "#4f46e5",
        "type": "dashboard",
        "stats": [("Lists", "34"), ("Emails", "45K"), ("Valid Rate", "92%"), ("API Calls", "1.2M")],
    },
    "dat-stream-studio": {
        "title": "DAT Stream Studio",
        "subtitle": "PyQt DAT workspace & proxy browser",
        "accent": "#0369a1",
        "type": "desktop",
    },
    "clientreadyftsolutionsdombom": {
        "title": "FT Solutions DOM/BOM",
        "subtitle": "Client-ready web automation toolkit",
        "accent": "#0f766e",
        "type": "devops",
    },
    "multi-smtp-email-automation": {
        "title": "Multi-SMTP Automation",
        "subtitle": "Parallel multi-account email sender",
        "accent": "#be123c",
        "type": "email",
    },
    "online-food-delivery": {
        "title": "Online Food Delivery",
        "subtitle": "Node.js · MongoDB · DevOps stack",
        "accent": "#f97316",
        "type": "website",
    },
    "pdf-mc-number-extractor": {
        "title": "PDF MC Number Extractor",
        "subtitle": "Extract & sort MC numbers from PDFs",
        "accent": "#b45309",
        "type": "utility",
    },
    "portfilio": {
        "title": "Portfolio Website",
        "subtitle": "Personal developer portfolio",
        "accent": "#6366f1",
        "type": "website",
    },
    "python-smtp-email-automation": {
        "title": "Python SMTP Automation",
        "subtitle": "Gmail App Password bulk sender",
        "accent": "#dc2626",
        "type": "email",
    },
    "quickdraw-test": {
        "title": "QuickDraw Test",
        "subtitle": "QuickDraw ML classification test",
        "accent": "#a855f7",
        "type": "ml",
    },
    "quizmaster-online-testing-system": {
        "title": "QuizMaster",
        "subtitle": "Online quiz & testing platform",
        "accent": "#0891b2",
        "type": "dashboard",
        "stats": [("Quizzes", "42"), ("Students", "380"), ("Attempts", "2.1K"), ("Avg Score", "76%")],
    },
    "google-voice-dispatch-agent": {
        "title": "GV Dispatch Agent",
        "subtitle": "AI Google Voice sales automation",
        "accent": "#22c55e",
        "type": "automation",
    },
}


def esc(s: str) -> str:
    return html.escape(s)


def build_html(cfg: dict) -> str:
    t = cfg["title"]
    sub = cfg["subtitle"]
    accent = cfg.get("accent", "#2563eb")
    kind = cfg.get("type", "dashboard")
    stats = cfg.get("stats", [])

    stats_html = ""
    if stats:
        cards = "".join(
            f'<div class="stat"><span>{esc(l)}</span><strong>{esc(v)}</strong></div>' for l, v in stats
        )
        stats_html = f'<div class="stats">{cards}</div>'

    if kind == "ml":
        body = """
        <div class="grid-ml">
          <div class="panel"><h3>Training Loss</h3><div class="chart"></div></div>
          <div class="panel digits"><h3>Predictions</h3>
            <div class="digit-row">7 3 1 9 4 0 8 2 5 6</div>
            <div class="digit-grid">""" + "".join(
            f'<div class="cell">{i}</div>' for i in range(10)
        ) + """</div></div>
        </div>"""
    elif kind == "scraper":
        body = """
        <div class="panel wide"><h3>Scrape Queue</h3>
          <div class="row"><span class="dot g"></span> https://example.com — 142 pages — Complete</div>
          <div class="row"><span class="dot b"></span> https://target-site.com — 38 pages — Running</div>
          <div class="row"><span class="dot y"></span> https://data-source.io — 12 pages — Queued</div>
        </div>"""
    elif kind == "devops":
        body = """
        <div class="pipeline">
          <div class="step done">Build</div><div class="arrow">→</div>
          <div class="step done">Test</div><div class="arrow">→</div>
          <div class="step active">Deploy</div><div class="arrow">→</div>
          <div class="step">Release</div>
        </div>
        <div class="panel wide"><h3>GitHub Actions</h3>
          <div class="row"><span class="dot g"></span> ci.yml — passed · 2m 14s</div>
          <div class="row"><span class="dot g"></span> deploy.yml — passed · 1m 08s</div>
        </div>"""
    elif kind == "excel":
        body = """
        <div class="panel wide excel"><h3>Workbook</h3>
          <table><tr><th>MC</th><th>Company</th><th>State</th><th>Email</th></tr>
          <tr><td>123456</td><td>Example Logistics</td><td>TX</td><td>ops@example.com</td></tr>
          <tr><td>789012</td><td>Fast Freight LLC</td><td>CA</td><td>dispatch@fast.com</td></tr>
          <tr><td>345678</td><td>National Carriers</td><td>IL</td><td>info@national.co</td></tr></table>
        </div>"""
    elif kind == "desktop":
        body = """
        <div class="desktop">
          <div class="titlebar"><span></span><span></span><span></span> """ + esc(t) + """</div>
          <div class="desktop-body">
            <div class="sidebar-mini"><div class="active">Dashboard</div><div>Settings</div><div>Logs</div></div>
            <div class="main-mini"><div class="btn">Load Excel</div><div class="btn primary">Start</div><div class="log">Ready — waiting for input...</div></div>
          </div>
        </div>"""
    elif kind == "utility":
        body = """
        <div class="panel wide"><h3>Live Output</h3>
          <div class="code">[LIVE] x=842 y=516 (click logged)<br>[LIVE] x=1120 y=744 (click logged)<br>[SAVE] coordinates.txt updated</div>
        </div>"""
    elif kind == "website":
        body = """
        <div class="website-mock">
          <div class="nav-mock"><span>Home</span><span>Menu</span><span>Contact</span></div>
          <div class="hero-mock"><h2>Welcome</h2><p>Modern responsive web application</p><div class="btn primary">Get Started</div></div>
        </div>"""
    elif kind == "email":
        body = """
        <div class="panel wide"><h3>Campaign Status</h3>
          <div class="row"><span class="dot g"></span> Batch #1 — 50/50 sent — 0 failures</div>
          <div class="row"><span class="dot b"></span> Batch #2 — 32/50 sending...</div>
          <div class="row"><span class="dot y"></span> Batch #3 — queued</div>
        </div>"""
    elif kind == "analytics":
        body = stats_html + """
        <div class="grid-ml">
          <div class="panel"><h3>Call Scores</h3><div class="chart"></div></div>
          <div class="panel"><h3>Transcripts</h3><div class="row">Call #1842 — Score 92 — Passed</div><div class="row">Call #1841 — Score 78 — Review</div></div>
        </div>"""
    else:
        body = stats_html + """
        <div class="grid-ml">
          <div class="panel"><h3>Overview</h3><div class="chart"></div></div>
          <div class="panel"><h3>Recent Activity</h3><div class="row">Verification job completed</div><div class="row">New list imported — 2,400 rows</div></div>
        </div>"""

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1280px;height:800px;background:linear-gradient(145deg,#0f172a 0%,#1e293b 100%);font-family:Segoe UI,Inter,sans-serif;color:#e2e8f0;padding:28px}}
.window{{background:#111827;border:1px solid #334155;border-radius:16px;overflow:hidden;box-shadow:0 24px 48px rgba(0,0,0,.45);height:100%;display:flex;flex-direction:column}}
.top{{padding:20px 24px;border-bottom:1px solid #334155;background:linear-gradient(90deg,{accent}22,transparent)}}
.top h1{{font-size:26px;font-weight:700;color:#f8fafc}}
.top p{{color:#94a3b8;font-size:14px;margin-top:4px}}
.content{{padding:24px;flex:1;display:flex;flex-direction:column;gap:16px}}
.stats{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}}
.stat{{background:#1e293b;border:1px solid #334155;border-radius:12px;padding:16px;text-align:center}}
.stat span{{display:block;font-size:11px;color:#94a3b8;text-transform:uppercase;letter-spacing:.06em}}
.stat strong{{display:block;font-size:24px;color:{accent};margin-top:6px}}
.panel{{background:#1e293b;border:1px solid #334155;border-radius:12px;padding:18px}}
.panel h3{{font-size:13px;color:#94a3b8;margin-bottom:12px;text-transform:uppercase;letter-spacing:.05em}}
.panel.wide{{flex:1}}
.row{{padding:10px 12px;background:#0f172a;border-radius:8px;margin-bottom:8px;font-size:13px;color:#cbd5e1}}
.dot{{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:8px}}
.g{{background:#22c55e}}.b{{background:#3b82f6}}.y{{background:#eab308}}
.grid-ml{{display:grid;grid-template-columns:1.2fr 1fr;gap:16px;flex:1}}
.chart{{height:140px;background:linear-gradient(180deg,{accent}44,transparent);border-radius:8px;border-bottom:3px solid {accent}}}
.digit-row{{font-size:28px;letter-spacing:12px;text-align:center;margin:16px 0;color:{accent}}}
.digit-grid{{display:grid;grid-template-columns:repeat(5,1fr);gap:8px}}
.cell{{background:#0f172a;border:1px solid #334155;border-radius:8px;padding:16px;text-align:center;font-size:20px}}
.pipeline{{display:flex;align-items:center;gap:8px;padding:12px 0}}
.step{{padding:10px 18px;border-radius:8px;background:#1e293b;border:1px solid #334155;font-size:13px;font-weight:600}}
.step.done{{border-color:#22c55e;color:#86efac}}.step.active{{border-color:{accent};color:#93c5fd;background:{accent}22}}
.arrow{{color:#64748b}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
th,td{{padding:10px;border-bottom:1px solid #334155;text-align:left}}
th{{color:#94a3b8;font-size:11px;text-transform:uppercase}}
.desktop{{border:1px solid #334155;border-radius:12px;overflow:hidden;flex:1}}
.titlebar{{background:#374151;padding:10px 14px;font-size:13px;display:flex;align-items:center;gap:8px}}
.titlebar span{{width:10px;height:10px;border-radius:50%;background:#64748b}}
.desktop-body{{display:flex;height:220px}}
.sidebar-mini{{width:140px;background:#1e293b;padding:12px;font-size:12px}}
.sidebar-mini div{{padding:8px;border-radius:6px;margin-bottom:4px;color:#94a3b8}}
.sidebar-mini .active{{background:{accent}33;color:#f8fafc}}
.main-mini{{flex:1;padding:16px}}
.btn{{display:inline-block;padding:8px 14px;border-radius:6px;background:#334155;font-size:12px;margin-right:8px;margin-bottom:12px}}
.btn.primary{{background:{accent};color:#fff}}
.log{{background:#0f172a;border-radius:8px;padding:12px;font-family:Consolas,monospace;font-size:12px;color:#86efac;margin-top:8px}}
.code{{font-family:Consolas,monospace;font-size:13px;line-height:1.8;color:#86efac}}
.website-mock{{border-radius:12px;overflow:hidden;border:1px solid #334155;flex:1}}
.nav-mock{{display:flex;gap:24px;padding:14px 20px;background:#1e293b;font-size:13px;color:#94a3b8}}
.hero-mock{{padding:48px 32px;background:linear-gradient(135deg,{accent}33,#0f172a)}}
.hero-mock h2{{font-size:28px;color:#f8fafc}}
.hero-mock p{{color:#94a3b8;margin:8px 0 20px}}
</style></head><body><div class="window"><div class="top"><h1>{esc(t)}</h1><p>{esc(sub)}</p></div><div class="content">{body}</div></div></body></html>"""


def main() -> None:
    from playwright.sync_api import sync_playwright

    ASSETS.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        for slug, cfg in MOCKUPS.items():
            if slug in SKIP:
                print(f"skip {slug} (real screenshot)")
                continue
            out = ASSETS / f"{slug}.png"
            tmp = ROOT / ".capture-cache" / f"{slug}-mock.html"
            tmp.parent.mkdir(parents=True, exist_ok=True)
            tmp.write_text(build_html(cfg), encoding="utf-8")
            page.goto(tmp.as_uri(), wait_until="domcontentloaded")
            page.wait_for_timeout(400)
            page.screenshot(path=str(out))
            print(f"generated {out.name}")
        browser.close()
    print("Done.")


if __name__ == "__main__":
    main()
