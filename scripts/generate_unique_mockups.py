"""Generate 16 unique UI mockup PNGs — distinct theme per project."""
from __future__ import annotations

import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets" / "projects"
CACHE = ROOT / ".capture-cache" / "unique-mockups"

TARGETS = [
    "bulk-email-verifier",
    "dev",
    "devops2",
    "excel-mc-data-cleaner",
    "excel-state-extractor-formula",
    "forward-email-automation",
    "learningdashboard",
    "mouse-coordinate-tracker",
    "multi-smtp-email-automation",
    "mywebpagetask",
    "online-food-delivery",
    "pdf-mc-number-extractor",
    "python-sms-automation",
    "quickdraw-test",
    "python-smtp-email-automation",
    "quizmaster-online-testing-system",
]


def esc(s: str) -> str:
    return html.escape(s)


def wrap(body: str, *, font: str, bg: str) -> str:
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family={font}&display=swap" rel="stylesheet">
<style>*{{box-sizing:border-box;margin:0;padding:0}}body{{width:1280px;height:800px;font-family:{font.split(':')[0].replace('+',' ')},system-ui,sans-serif;background:{bg};overflow:hidden}}</style>
</head><body>{body}</body></html>"""


def bulk_email_verifier() -> str:
    return wrap("""
<div style="display:flex;height:100%;background:#f5f3ff">
  <aside style="width:240px;background:linear-gradient(180deg,#4c1d95,#6d28d9);color:#fff;padding:28px 20px">
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:32px">
      <div style="width:42px;height:42px;border-radius:12px;background:#fff;color:#6d28d9;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:18px">✉</div>
      <div><div style="font-weight:700;font-size:15px">VerifyMail</div><div style="font-size:11px;opacity:.75">Bulk Email Verifier</div></div>
    </div>
    <div style="font-size:13px;line-height:2.2;opacity:.9"><div style="opacity:1;font-weight:600">● Dashboard</div><div>Verify Email</div><div>Bulk Upload</div><div>API Keys</div><div>Reports</div></div>
    <div style="margin-top:auto;padding-top:40px;font-size:12px;opacity:.7">Self-hosted · SMTP checks</div>
  </aside>
  <main style="flex:1;padding:32px 36px">
    <h1 style="font-size:28px;color:#1e1b4b;font-weight:700">Bulk Email Verifier</h1>
    <p style="color:#6b7280;margin:6px 0 24px;font-size:14px">Syntax, MX &amp; mailbox validation — no paid APIs</p>
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:24px">
      <div style="background:#fff;border-radius:16px;padding:20px;box-shadow:0 4px 20px rgba(109,40,217,.08)"><div style="font-size:12px;color:#7c3aed;font-weight:600">TOTAL VERIFIED</div><div style="font-size:32px;font-weight:800;color:#4c1d95;margin-top:8px">125,430</div></div>
      <div style="background:#fff;border-radius:16px;padding:20px;box-shadow:0 4px 20px rgba(34,197,94,.08)"><div style="font-size:12px;color:#16a34a;font-weight:600">VALID</div><div style="font-size:32px;font-weight:800;color:#15803d;margin-top:8px">98,765</div></div>
      <div style="background:#fff;border-radius:16px;padding:20px;box-shadow:0 4px 20px rgba(239,68,68,.08)"><div style="font-size:12px;color:#dc2626;font-weight:600">INVALID</div><div style="font-size:32px;font-weight:800;color:#b91c1c;margin-top:8px">15,432</div></div>
      <div style="background:#fff;border-radius:16px;padding:20px;box-shadow:0 4px 20px rgba(245,158,11,.08)"><div style="font-size:12px;color:#d97706;font-weight:600">CATCH-ALL</div><div style="font-size:32px;font-weight:800;color:#b45309;margin-top:8px">11,233</div></div>
    </div>
    <div style="background:#fff;border-radius:16px;padding:24px;box-shadow:0 4px 24px rgba(0,0,0,.06);height:380px">
      <div style="font-size:13px;color:#6b7280;font-weight:600;margin-bottom:16px">VERIFICATION OVERVIEW · LAST 7 DAYS</div>
      <div style="height:280px;background:linear-gradient(180deg,rgba(124,58,237,.15) 0%,transparent 100%);border-radius:12px;border-bottom:3px solid #7c3aed;position:relative">
        <svg width="100%" height="100%" viewBox="0 0 800 200" preserveAspectRatio="none"><polyline fill="none" stroke="#7c3aed" stroke-width="3" points="0,160 100,120 200,140 300,80 400,100 500,40 600,60 700,20 800,30"/></svg>
      </div>
    </div>
  </main>
</div>""", font="Inter:wght@400;600;700;800", bg="#f5f3ff")


def dev_project() -> str:
    return wrap("""
<div style="height:100%;background:#0a0f0a;color:#33ff66;font-family:Consolas,monospace;padding:0">
  <div style="background:#111;border-bottom:2px solid #33ff66;padding:12px 20px;display:flex;align-items:center;gap:12px">
    <span style="color:#ff5f57">●</span><span style="color:#febc2e">●</span><span style="color:#28c840">●</span>
    <span style="margin-left:12px;font-size:13px;color:#33ff66">dev-workspace — ~/projects/dev</span>
  </div>
  <div style="padding:24px;font-size:14px;line-height:1.9">
    <pre style="color:#33ff66;font-size:13px">╔══════════════════════════════════════╗
║   ██████  ███████ ██████             ║
║   ██   ██ ██      ██   ██   DEV HUB  ║
║   ██   ██ █████   ██   ██            ║
║   ██   ██ ██      ██   ██            ║
║   ██████  ███████ ██████             ║
╚══════════════════════════════════════╝</pre>
    <div style="margin-top:20px;color:#7dff9a">$ git status</div>
    <div style="color:#a3a3a3">On branch main · 3 commits ahead</div>
    <div style="margin-top:16px;color:#7dff9a">$ npm run dev</div>
    <div style="color:#fff">▸ Local: http://localhost:3000</div>
    <div style="color:#fff">▸ HTML/CSS/JS developer workspace ready</div>
    <div style="margin-top:24px;padding:16px;border:1px solid #33ff6644;border-radius:8px;background:#111">
      <div style="color:#33ff66;font-weight:700;margin-bottom:8px">// Dev Project</div>
      <div style="color:#ccc">Professional open source HTML development sandbox</div>
    </div>
  </div>
</div>""", font="JetBrains+Mono:wght@400;700", bg="#0a0f0a")


def devops2() -> str:
    return wrap("""
<div style="height:100%;background:#1a1a2e;color:#eee">
  <header style="background:linear-gradient(90deg,#e85d04,#f48c06);padding:18px 32px;display:flex;align-items:center;justify-content:space-between">
    <div style="display:flex;align-items:center;gap:14px">
      <div style="width:44px;height:44px;border-radius:10px;background:#fff;color:#e85d04;font-weight:800;display:flex;align-items:center;justify-content:center;font-size:20px">⚙</div>
      <div><div style="font-weight:800;font-size:20px;font-family:Poppins,sans-serif">DevOps Lab II</div><div style="font-size:12px;opacity:.85">GitHub Actions · Docker · CI/CD</div></div>
    </div>
    <div style="background:rgba(255,255,255,.2);padding:8px 16px;border-radius:8px;font-size:13px">Pipeline #847 · Running</div>
  </header>
  <div style="padding:32px">
    <div style="display:flex;gap:12px;align-items:center;margin-bottom:28px">
      <div style="flex:1;background:#16213e;border:2px solid #22c55e;border-radius:12px;padding:16px;text-align:center"><div style="color:#22c55e;font-weight:700">✓ Build</div><div style="font-size:11px;color:#94a3b8;margin-top:4px">2m 14s</div></div>
      <div style="color:#f48c06;font-size:24px">→</div>
      <div style="flex:1;background:#16213e;border:2px solid #22c55e;border-radius:12px;padding:16px;text-align:center"><div style="color:#22c55e;font-weight:700">✓ Test</div><div style="font-size:11px;color:#94a3b8;margin-top:4px">1m 08s</div></div>
      <div style="color:#f48c06;font-size:24px">→</div>
      <div style="flex:1;background:#16213e;border:2px solid #f48c06;border-radius:12px;padding:16px;text-align:center;box-shadow:0 0 20px rgba(244,140,6,.3)"><div style="color:#f48c06;font-weight:700">◉ Deploy</div><div style="font-size:11px;color:#94a3b8;margin-top:4px">In progress</div></div>
      <div style="color:#64748b;font-size:24px">→</div>
      <div style="flex:1;background:#16213e;border:2px solid #334155;border-radius:12px;padding:16px;text-align:center"><div style="color:#64748b;font-weight:700">Release</div></div>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">
      <div style="background:#16213e;border-radius:14px;padding:22px;border:1px solid #334155">
        <div style="font-weight:700;color:#f48c06;margin-bottom:14px">Docker Containers</div>
        <div style="font-size:13px;line-height:2;color:#cbd5e1"><div>🐳 app-web — healthy</div><div>🐳 app-api — healthy</div><div>🐳 mongo-db — healthy</div></div>
      </div>
      <div style="background:#16213e;border-radius:14px;padding:22px;border:1px solid #334155">
        <div style="font-weight:700;color:#f48c06;margin-bottom:14px">GitHub DevOps Labtask</div>
        <div style="font-size:13px;line-height:2;color:#cbd5e1"><div style="color:#22c55e">✓ ci.yml passed</div><div style="color:#22c55e">✓ deploy.yml passed</div><div style="color:#f48c06">◉ jenkins-build running</div></div>
      </div>
    </div>
  </div>
</div>""", font="Poppins:wght@400;600;700;800", bg="#1a1a2e")


def excel_mc_data_cleaner() -> str:
    return wrap("""
<div style="height:100%;background:#e8e8e8">
  <div style="background:#217346;padding:8px 16px;color:#fff;font-size:13px;font-weight:600;display:flex;gap:20px">
    <span>File</span><span>Home</span><span>Insert</span><span style="background:#185c37;padding:4px 12px;border-radius:4px">Data Cleaner</span><span>View</span>
  </div>
  <div style="background:#f3f3f3;padding:6px 16px;font-size:12px;color:#333;border-bottom:1px solid #ccc;display:flex;gap:8px;align-items:center">
    <span style="background:#217346;color:#fff;padding:4px 10px;border-radius:4px;font-weight:600">Clean MC Data</span>
    <span style="background:#fff;border:1px solid #ccc;padding:4px 10px;border-radius:4px">Validate Emails</span>
    <span style="background:#fff;border:1px solid #ccc;padding:4px 10px;border-radius:4px">Extract States</span>
  </div>
  <div style="padding:20px">
    <div style="background:#fff;border:1px solid #bbb;border-radius:4px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.1)">
      <div style="background:#217346;color:#fff;padding:10px 16px;font-weight:700;font-size:15px;display:flex;align-items:center;gap:10px">
        <span style="font-size:20px">📊</span> Excel MC Data Cleaner — Carrier Dispatch Workbook
      </div>
      <table style="width:100%;border-collapse:collapse;font-size:13px;font-family:Calibri,sans-serif">
        <tr style="background:#217346;color:#fff"><th style="padding:10px;border:1px solid #185c37">MC #</th><th style="padding:10px;border:1px solid #185c37">Company</th><th style="padding:10px;border:1px solid #185c37">State</th><th style="padding:10px;border:1px solid #185c37">Email</th><th style="padding:10px;border:1px solid #185c37">Status</th></tr>
        <tr><td style="padding:9px;border:1px solid #ddd">1234567</td><td style="padding:9px;border:1px solid #ddd">Atlantic Freight LLC</td><td style="padding:9px;border:1px solid #ddd">FL</td><td style="padding:9px;border:1px solid #ddd">ops@atlantic.com</td><td style="padding:9px;border:1px solid #ddd;color:#217346">✓ Valid</td></tr>
        <tr style="background:#f9f9f9"><td style="padding:9px;border:1px solid #ddd">8901234</td><td style="padding:9px;border:1px solid #ddd">Fast Haul Inc</td><td style="padding:9px;border:1px solid #ddd">TX</td><td style="padding:9px;border:1px solid #ddd">dispatch@fast.com</td><td style="padding:9px;border:1px solid #ddd;color:#217346">✓ Valid</td></tr>
        <tr><td style="padding:9px;border:1px solid #ddd">5678901</td><td style="padding:9px;border:1px solid #ddd">National Carriers</td><td style="padding:9px;border:1px solid #ddd">CA</td><td style="padding:9px;border:1px solid #ddd">info@national.co</td><td style="padding:9px;border:1px solid #ddd;color:#dc2626">✗ Fixed</td></tr>
      </table>
    </div>
    <div style="margin-top:16px;font-size:12px;color:#555">VBA macro · 847 rows cleaned · emails validated · states extracted</div>
  </div>
</div>""", font="Calibri", bg="#e8e8e8")


def excel_state_extractor() -> str:
    return wrap("""
<div style="height:100%;background:#fafafa;font-family:Segoe UI,sans-serif">
  <div style="background:#fff;border-bottom:3px solid #107c41;padding:20px 32px">
    <div style="display:flex;align-items:center;gap:12px">
      <div style="width:40px;height:40px;background:#107c41;border-radius:8px;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:800">fx</div>
      <div><h1 style="font-size:22px;color:#107c41;font-weight:700">State Extractor Formula</h1><p style="font-size:13px;color:#666;margin-top:2px">Extract U.S. state abbreviations from address strings</p></div>
    </div>
  </div>
  <div style="padding:32px;max-width:900px">
    <div style="background:#fff;border:1px solid #ddd;border-radius:8px;padding:16px;margin-bottom:20px">
      <div style="font-size:11px;color:#888;margin-bottom:6px">FORMULA BAR</div>
      <code style="font-size:15px;color:#107c41;font-family:Consolas,monospace">=STATE_EXTRACT(B2)</code>
    </div>
    <table style="width:100%;border-collapse:collapse;font-size:14px;background:#fff;border:1px solid #ddd;border-radius:8px;overflow:hidden">
      <tr style="background:#107c41;color:#fff"><th style="padding:12px;text-align:left">Address</th><th style="padding:12px;text-align:left">Extracted State</th></tr>
      <tr><td style="padding:12px;border-bottom:1px solid #eee">2651 S Course Dr, Pompano Beach, FL 33069</td><td style="padding:12px;border-bottom:1px solid #eee;font-weight:700;color:#107c41">FL</td></tr>
      <tr style="background:#f9fafb"><td style="padding:12px;border-bottom:1px solid #eee">1200 Main St, Dallas, Texas 75201</td><td style="padding:12px;border-bottom:1px solid #eee;font-weight:700;color:#107c41">TX</td></tr>
      <tr><td style="padding:12px;border-bottom:1px solid #eee">500 Oak Ave, Los Angeles, CA 90001</td><td style="padding:12px;border-bottom:1px solid #eee;font-weight:700;color:#107c41">CA</td></tr>
      <tr style="background:#f9fafb"><td style="padding:12px">88 Lake Shore, Chicago, IL 60601</td><td style="padding:12px;font-weight:700;color:#107c41">IL</td></tr>
    </table>
  </div>
</div>""", font="Segoe+UI", bg="#fafafa")


def forward_email_automation() -> str:
    return wrap("""
<div style="height:100%;background:linear-gradient(135deg,#fff7ed,#ffedd5)">
  <header style="background:#c2410c;color:#fff;padding:20px 32px;display:flex;align-items:center;gap:14px">
    <div style="width:48px;height:48px;background:#fff;border-radius:50%;color:#c2410c;display:flex;align-items:center;justify-content:center;font-size:22px">↪</div>
    <div><div style="font-size:22px;font-weight:700;font-family:Georgia,serif">Forward Email Automation</div><div style="font-size:13px;opacity:.9">Carrier outreach · dispatch communication</div></div>
  </header>
  <div style="padding:28px 32px;display:grid;grid-template-columns:1fr 1fr;gap:24px">
    <div style="background:#fff;border-radius:16px;padding:24px;box-shadow:0 8px 24px rgba(194,65,12,.12);border-left:4px solid #ea580c">
      <div style="font-size:13px;color:#c2410c;font-weight:700;margin-bottom:12px">INBOX QUEUE</div>
      <div style="font-size:14px;line-height:2.2;color:#444"><div>📧 carrier_list_june.xlsx — 240 contacts</div><div>📧 dispatch_outreach.csv — 89 contacts</div><div>📧 follow_up_batch.txt — 56 contacts</div></div>
    </div>
    <div style="background:#fff;border-radius:16px;padding:24px;box-shadow:0 8px 24px rgba(194,65,12,.12)">
      <div style="font-size:13px;color:#c2410c;font-weight:700;margin-bottom:12px">FORWARD STATUS</div>
      <div style="font-size:14px;line-height:2.2;color:#444"><div style="color:#16a34a">✓ Batch 1 — 50/50 forwarded</div><div style="color:#2563eb">◉ Batch 2 — 32/50 sending...</div><div style="color:#94a3b8">○ Batch 3 — queued</div></div>
    </div>
    <div style="grid-column:span 2;background:#292524;color:#fed7aa;border-radius:16px;padding:20px;font-family:Consolas,monospace;font-size:13px;line-height:1.8">
      [INFO] Python email forwarding pipeline started<br>[OK] Contact processed: Atlantic Freight LLC<br>[OK] Template randomized · delay 4.2s · retry enabled
    </div>
  </div>
</div>""", font="Lora:wght@400;600;700", bg="#fff7ed")


def learningdashboard() -> str:
    return wrap("""
<div style="height:100%;background:linear-gradient(160deg,#ede9fe,#ddd6fe)">
  <nav style="background:#512bd4;padding:16px 32px;display:flex;align-items:center;justify-content:space-between;color:#fff">
    <div style="display:flex;align-items:center;gap:12px">
      <div style="width:40px;height:40px;background:#fff;border-radius:10px;color:#512bd4;font-weight:800;display:flex;align-items:center;justify-content:center">.NET</div>
      <span style="font-size:20px;font-weight:700;font-family:Segoe UI,sans-serif">Learning Dashboard</span>
    </div>
    <span style="font-size:13px;opacity:.85">Blazor Server · SQLite</span>
  </nav>
  <div style="padding:28px 32px">
    <div style="font-size:14px;color:#5b21b6;margin-bottom:8px;font-style:italic">"The only way to do great work is to love what you do."</div>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin:20px 0">
      <div style="background:#fff;border-radius:14px;padding:20px;box-shadow:0 4px 16px rgba(81,43,212,.15)"><div style="font-size:12px;color:#7c3aed;font-weight:600">COURSES</div><div style="font-size:36px;font-weight:800;color:#512bd4">8</div></div>
      <div style="background:#fff;border-radius:14px;padding:20px;box-shadow:0 4px 16px rgba(81,43,212,.15)"><div style="font-size:12px;color:#7c3aed;font-weight:600">COMPLETED</div><div style="font-size:36px;font-weight:800;color:#512bd4">5</div></div>
      <div style="background:#fff;border-radius:14px;padding:20px;box-shadow:0 4px 16px rgba(81,43,212,.15)"><div style="font-size:12px;color:#7c3aed;font-weight:600">HOURS</div><div style="font-size:36px;font-weight:800;color:#512bd4">124</div></div>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:18px">
      <div style="background:#fff;border-radius:14px;padding:20px"><div style="font-weight:700;color:#512bd4;margin-bottom:12px">C# Advanced</div><div style="height:8px;background:#ede9fe;border-radius:4px"><div style="width:78%;height:100%;background:#512bd4;border-radius:4px"></div></div><div style="font-size:12px;color:#666;margin-top:6px">78% complete</div></div>
      <div style="background:#fff;border-radius:14px;padding:20px"><div style="font-weight:700;color:#512bd4;margin-bottom:12px">Blazor Server</div><div style="height:8px;background:#ede9fe;border-radius:4px"><div style="width:62%;height:100%;background:#512bd4;border-radius:4px"></div></div><div style="font-size:12px;color:#666;margin-top:6px">62% complete</div></div>
    </div>
  </div>
</div>""", font="Playfair+Display:wght@600;700", bg="#ede9fe")


def mouse_coordinate_tracker() -> str:
    return wrap("""
<div style="height:100%;background:#000;color:#0f0;font-family:Consolas,monospace;padding:0">
  <div style="background:#111;border-bottom:1px solid #0f0;padding:10px 20px;font-size:13px;display:flex;justify-content:space-between">
    <span>🖱 Mouse Coordinate Tracker v1.0</span><span style="color:#0f0">● LIVE</span>
  </div>
  <div style="padding:24px">
    <div style="border:1px solid #0f0;border-radius:4px;padding:20px;margin-bottom:20px;background:#0a0a0a">
      <div style="font-size:28px;font-weight:700;text-align:center;letter-spacing:4px">X: 842 &nbsp; Y: 516</div>
      <div style="text-align:center;margin-top:8px;font-size:12px;color:#0a0">Real-time click coordinates for PyAutoGUI</div>
    </div>
    <div style="font-size:13px;line-height:2;color:#0f0">
      [LIVE] x=842 y=516 (click logged)<br>
      [LIVE] x=1120 y=744 (click logged)<br>
      [LIVE] x=456 y=312 (click logged)<br>
      [SAVE] coordinates.txt updated<br>
      [INFO] Lightweight Python utility · automation scripting
    </div>
    <div style="margin-top:24px;display:flex;gap:12px">
      <div style="border:1px solid #0f0;padding:8px 16px;border-radius:4px">Start Tracking</div>
      <div style="border:1px solid #333;padding:8px 16px;border-radius:4px;color:#666">Export CSV</div>
    </div>
  </div>
</div>""", font="Courier+Prime:wght@400;700", bg="#000")


def multi_smtp_automation() -> str:
    return wrap("""
<div style="height:100%;background:#1c1917;color:#fafaf9">
  <header style="background:linear-gradient(90deg,#be123c,#9f1239);padding:20px 32px;display:flex;align-items:center;gap:14px">
    <div style="width:44px;height:44px;background:#fff;border-radius:12px;color:#be123c;font-weight:900;font-size:18px;display:flex;align-items:center;justify-content:center">SMTP</div>
    <div><div style="font-size:22px;font-weight:800">Multi SMTP Email Automation</div><div style="font-size:13px;opacity:.85">Parallel multi-account sender · retries · templates</div></div>
  </header>
  <div style="padding:28px;display:grid;grid-template-columns:repeat(3,1fr);gap:16px">
    <div style="background:#292524;border:1px solid #44403c;border-radius:12px;padding:18px"><div style="color:#fb7185;font-weight:700;font-size:13px">Account 1</div><div style="font-size:24px;font-weight:800;margin:8px 0">847 sent</div><div style="font-size:12px;color:#a8a29e">smtp1@gmail.com · 0 failures</div></div>
    <div style="background:#292524;border:1px solid #44403c;border-radius:12px;padding:18px"><div style="color:#fb7185;font-weight:700;font-size:13px">Account 2</div><div style="font-size:24px;font-weight:800;margin:8px 0">623 sent</div><div style="font-size:12px;color:#a8a29e">smtp2@gmail.com · 2 retries</div></div>
    <div style="background:#292524;border:1px solid #44403c;border-radius:12px;padding:18px"><div style="color:#fb7185;font-weight:700;font-size:13px">Account 3</div><div style="font-size:24px;font-weight:800;margin:8px 0">512 sent</div><div style="font-size:12px;color:#a8a29e">smtp3@gmail.com · running</div></div>
  </div>
  <div style="margin:0 28px;background:#0c0a09;border-radius:12px;padding:20px;font-family:monospace;font-size:13px;line-height:1.9;color:#fca5a5">
    [PARALLEL] 3 SMTP workers active · recipient distribution enabled<br>[TEMPLATE] Randomized subject line applied · delay 3.8s<br>[LOG] Batch complete — 1,982 emails · 99.1% success rate
  </div>
</div>""", font="Rubik:wght@400;600;700", bg="#1c1917")


def mywebpagetask() -> str:
    return wrap("""
<div style="height:100%;background:linear-gradient(135deg,#fce7f3,#ddd6fe,#bfdbfe)">
  <nav style="padding:20px 40px;display:flex;justify-content:space-between;align-items:center">
    <div style="font-size:24px;font-weight:800;color:#7c3aed;font-family:Nunito,sans-serif">MyWebPage ✦</div>
    <div style="display:flex;gap:24px;font-size:14px;color:#6b21a8;font-weight:600"><span>Home</span><span>About</span><span>Projects</span><span>Contact</span></div>
  </nav>
  <div style="text-align:center;padding:60px 40px 40px">
    <h1 style="font-size:52px;font-weight:800;color:#581c87;line-height:1.15;font-family:Nunito,sans-serif">Build Beautiful<br>Web Pages</h1>
    <p style="font-size:18px;color:#7e22ce;margin:20px auto 32px;max-width:520px">Responsive HTML/CSS project — modern layouts, clean typography, professional open source web design.</p>
    <div style="display:inline-block;background:linear-gradient(90deg,#a855f7,#ec4899);color:#fff;padding:14px 32px;border-radius:50px;font-weight:700;font-size:16px;box-shadow:0 8px 24px rgba(168,85,247,.4)">Get Started →</div>
  </div>
  <div style="display:flex;justify-content:center;gap:20px;padding:0 40px">
    <div style="width:200px;height:140px;background:#fff;border-radius:20px;box-shadow:0 8px 32px rgba(0,0,0,.08);padding:20px;text-align:left"><div style="font-size:28px">🎨</div><div style="font-weight:700;color:#581c87;margin-top:8px">Design</div></div>
    <div style="width:200px;height:140px;background:#fff;border-radius:20px;box-shadow:0 8px 32px rgba(0,0,0,.08);padding:20px;text-align:left"><div style="font-size:28px">⚡</div><div style="font-weight:700;color:#581c87;margin-top:8px">Fast</div></div>
    <div style="width:200px;height:140px;background:#fff;border-radius:20px;box-shadow:0 8px 32px rgba(0,0,0,.08);padding:20px;text-align:left"><div style="font-size:28px">📱</div><div style="font-weight:700;color:#581c87;margin-top:8px">Responsive</div></div>
  </div>
</div>""", font="Nunito:wght@400;600;700;800", bg="#fce7f3")


def online_food_delivery() -> str:
    return wrap("""
<div style="height:100%;background:#fffbeb">
  <header style="background:#dc2626;color:#fff;padding:16px 32px;display:flex;align-items:center;justify-content:space-between">
    <div style="display:flex;align-items:center;gap:12px">
      <div style="width:42px;height:42px;background:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:22px">🍕</div>
      <span style="font-size:22px;font-weight:800;font-family:Montserrat,sans-serif">FoodDash</span>
    </div>
    <div style="display:flex;gap:16px;font-size:14px"><span>Menu</span><span>Orders</span><span>Cart (3)</span></div>
  </header>
  <div style="padding:28px 32px">
    <h2 style="font-size:26px;color:#991b1b;font-weight:800;margin-bottom:20px">Online Food Delivery</h2>
    <p style="color:#666;font-size:14px;margin-bottom:24px">Node.js · MongoDB · Docker · Jenkins CI/CD</p>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:18px">
      <div style="background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 16px rgba(220,38,38,.12)"><div style="height:100px;background:linear-gradient(135deg,#fca5a5,#dc2626)"></div><div style="padding:16px"><div style="font-weight:700;color:#991b1b">Margherita Pizza</div><div style="font-size:13px;color:#666;margin-top:4px">$12.99 · 25 min</div></div></div>
      <div style="background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 16px rgba(220,38,38,.12)"><div style="height:100px;background:linear-gradient(135deg,#fdba74,#ea580c)"></div><div style="padding:16px"><div style="font-weight:700;color:#991b1b">Chicken Burger</div><div style="font-size:13px;color:#666;margin-top:4px">$9.49 · 18 min</div></div></div>
      <div style="background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 16px rgba(220,38,38,.12)"><div style="height:100px;background:linear-gradient(135deg,#86efac,#16a34a)"></div><div style="padding:16px"><div style="font-weight:700;color:#991b1b">Caesar Salad</div><div style="font-size:13px;color:#666;margin-top:4px">$8.99 · 12 min</div></div></div>
    </div>
  </div>
</div>""", font="Montserrat:wght@400;600;700;800", bg="#fffbeb")


def pdf_mc_extractor() -> str:
    return wrap("""
<div style="height:100%;background:#fef3c7">
  <header style="background:#92400e;color:#fff;padding:18px 32px;display:flex;align-items:center;gap:14px">
    <div style="width:44px;height:44px;background:#fff;border-radius:8px;color:#92400e;font-weight:900;display:flex;align-items:center;justify-content:center;font-size:14px">PDF</div>
    <div><div style="font-size:20px;font-weight:700">PDF MC Number Extractor</div><div style="font-size:12px;opacity:.85">Extract · dedupe · sort · save to text</div></div>
  </header>
  <div style="padding:28px 32px;display:grid;grid-template-columns:1fr 1fr;gap:24px">
    <div style="background:#fff;border:2px dashed #d97706;border-radius:12px;padding:40px;text-align:center">
      <div style="font-size:48px;margin-bottom:12px">📄</div>
      <div style="font-weight:700;color:#92400e">Drop PDF files here</div>
      <div style="font-size:13px;color:#78716c;margin-top:8px">carrier_list.pdf · mc_batch_02.pdf</div>
    </div>
    <div style="background:#fff;border-radius:12px;padding:24px;border:1px solid #fcd34d">
      <div style="font-weight:700;color:#92400e;margin-bottom:14px">Extracted MC Numbers</div>
      <div style="font-family:monospace;font-size:14px;line-height:2;color:#444">
        1234567<br>2345678<br>3456789<br>4567890<br>5678901
      </div>
      <div style="margin-top:16px;font-size:12px;color:#16a34a">✓ 847 unique · sorted · saved to output.txt</div>
    </div>
  </div>
</div>""", font="Merriweather:wght@400;700", bg="#fef3c7")


def python_sms_automation() -> str:
    return wrap("""
<div style="height:100%;background:linear-gradient(180deg,#dbeafe,#eff6ff);display:flex;align-items:center;justify-content:center">
  <div style="width:380px;background:#fff;border-radius:32px;box-shadow:0 24px 48px rgba(37,99,235,.2);overflow:hidden;border:8px solid #1e293b">
    <div style="background:#2563eb;color:#fff;padding:16px 20px;font-weight:700;display:flex;align-items:center;gap:10px">
      <span style="font-size:20px">💬</span> SMS Automation
    </div>
    <div style="padding:20px;min-height:420px;background:#f0f9ff">
      <div style="background:#e2e8f0;border-radius:16px 16px 16px 4px;padding:12px 16px;max-width:75%;font-size:14px;color:#334155;margin-bottom:12px">Hi John, your dispatch load is ready for pickup.</div>
      <div style="background:#2563eb;color:#fff;border-radius:16px 16px 4px 16px;padding:12px 16px;max-width:75%;margin-left:auto;font-size:14px;margin-bottom:12px">Thanks! On my way.</div>
      <div style="background:#e2e8f0;border-radius:16px 16px 16px 4px;padding:12px 16px;max-width:75%;font-size:14px;color:#334155">PyAutoGUI · Excel contacts · bulk personalized SMS</div>
    </div>
    <div style="padding:12px 16px;border-top:1px solid #e2e8f0;display:flex;gap:8px;align-items:center">
      <div style="flex:1;background:#f1f5f9;border-radius:20px;padding:10px 16px;font-size:13px;color:#94a3b8">Type a message...</div>
      <div style="width:36px;height:36px;background:#2563eb;border-radius:50%;color:#fff;display:flex;align-items:center;justify-content:center">→</div>
    </div>
  </div>
</div>""", font="SF+Pro+Display", bg="#dbeafe")


def quickdraw_test() -> str:
    return wrap("""
<div style="height:100%;background:#fff">
  <header style="padding:16px 32px;border-bottom:1px solid #eee;display:flex;align-items:center;gap:12px">
    <div style="width:40px;height:40px;background:linear-gradient(135deg,#4285f4,#ea4335,#fbbc04,#34a853);border-radius:8px"></div>
    <span style="font-size:20px;font-weight:700;color:#202124;font-family:Roboto,sans-serif">QuickDraw Test</span>
  </header>
  <div style="padding:32px;text-align:center">
    <div style="font-size:18px;color:#5f6368;margin-bottom:24px">Draw: <strong style="color:#202124">cat</strong> · ML classification test</div>
    <div style="width:500px;height:320px;margin:0 auto;border:2px solid #dadce0;border-radius:12px;background:#fafafa;position:relative">
      <svg width="500" height="320" viewBox="0 0 500 320"><path d="M120,200 Q140,120 180,140 Q200,100 240,130 Q280,90 320,140 Q360,110 380,180 Q340,220 280,240 Q200,260 120,200" fill="none" stroke="#4285f4" stroke-width="4" stroke-linecap="round"/><circle cx="200" cy="160" r="8" fill="#ea4335"/><circle cx="280" cy="160" r="8" fill="#ea4335"/><path d="M220,190 Q250,210 280,190" fill="none" stroke="#34a853" stroke-width="3"/></svg>
    </div>
    <div style="margin-top:24px;display:flex;justify-content:center;gap:16px">
      <div style="padding:10px 24px;background:#4285f4;color:#fff;border-radius:8px;font-weight:600;font-size:14px">Predict: cat (94%)</div>
      <div style="padding:10px 24px;border:1px solid #dadce0;border-radius:8px;font-size:14px;color:#5f6368">Clear canvas</div>
    </div>
  </div>
</div>""", font="Roboto:wght@400;500;700", bg="#fff")


def python_smtp_automation() -> str:
    return wrap("""
<div style="height:100%;background:#f8fafc">
  <div style="background:#fff;border-bottom:1px solid #e2e8f0;padding:16px 32px;display:flex;align-items:center;gap:12px;box-shadow:0 1px 3px rgba(0,0,0,.06)">
    <div style="width:36px;height:36px;background:linear-gradient(135deg,#ea4335,#fbbc04);border-radius:8px;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800;font-size:14px">G</div>
    <div><div style="font-size:18px;font-weight:700;color:#1e293b">Python SMTP Email Automation</div><div style="font-size:12px;color:#64748b">Gmail App Password · Excel data · randomized templates</div></div>
  </div>
  <div style="padding:32px;display:grid;grid-template-columns:280px 1fr;gap:24px">
    <div style="background:#fff;border-radius:12px;padding:20px;border:1px solid #e2e8f0">
      <div style="font-size:13px;font-weight:700;color:#64748b;margin-bottom:14px">COMPOSE</div>
      <div style="font-size:13px;line-height:2.4;color:#334155"><div><strong>To:</strong> contacts.xlsx (847 rows)</div><div><strong>From:</strong> sender@gmail.com</div><div><strong>Template:</strong> Random #3</div></div>
      <div style="margin-top:16px;background:#ea4335;color:#fff;text-align:center;padding:10px;border-radius:8px;font-weight:600;font-size:14px">Send Batch</div>
    </div>
    <div style="background:#fff;border-radius:12px;padding:24px;border:1px solid #e2e8f0">
      <div style="font-size:13px;font-weight:700;color:#64748b;margin-bottom:14px">SEND LOG</div>
      <div style="font-family:monospace;font-size:13px;line-height:2;color:#475569">
        [OK] Sent to ops@carrier1.com · delay 4.1s<br>[OK] Sent to dispatch@haul.com · delay 3.8s<br>[RETRY] smtp timeout · retry 1/3 · success<br>[INFO] 847/847 complete · safe delays enabled
      </div>
    </div>
  </div>
</div>""", font="Open+Sans:wght@400;600;700", bg="#f8fafc")


def quizmaster() -> str:
    return wrap("""
<div style="height:100%;background:#0c4a6e;color:#fff">
  <header style="background:#075985;padding:18px 32px;display:flex;align-items:center;justify-content:space-between;border-bottom:3px solid #0ea5e9">
    <div style="display:flex;align-items:center;gap:12px">
      <div style="width:42px;height:42px;background:#0ea5e9;border-radius:10px;font-weight:900;display:flex;align-items:center;justify-content:center;font-size:18px">Q</div>
      <span style="font-size:22px;font-weight:800;font-family:Merriweather,serif">QuizMaster</span>
    </div>
    <div style="background:#0ea5e9;padding:8px 16px;border-radius:8px;font-weight:700;font-family:monospace">⏱ 14:32</div>
  </header>
  <div style="padding:36px 48px">
    <div style="font-size:13px;color:#7dd3fc;margin-bottom:8px">QUESTION 7 OF 20 · Computer Science</div>
    <h2 style="font-size:26px;font-weight:700;margin-bottom:28px;line-height:1.4">Which data structure uses LIFO (Last In, First Out) ordering?</h2>
    <div style="display:grid;gap:12px;max-width:700px">
      <div style="background:#075985;border:2px solid #0ea5e9;border-radius:10px;padding:16px 20px;font-size:16px">A) Queue</div>
      <div style="background:#164e63;border:2px solid #22d3ee;border-radius:10px;padding:16px 20px;font-size:16px;box-shadow:0 0 20px rgba(14,165,233,.3)">B) Stack ✓</div>
      <div style="background:#075985;border:2px solid #0369a1;border-radius:10px;padding:16px 20px;font-size:16px">C) Linked List</div>
      <div style="background:#075985;border:2px solid #0369a1;border-radius:10px;padding:16px 20px;font-size:16px">D) Binary Tree</div>
    </div>
    <div style="margin-top:28px;display:flex;gap:20px;font-size:13px;color:#7dd3fc"><span>380 students</span><span>·</span><span>Leaderboard</span><span>·</span><span>Node.js · MongoDB · EJS</span></div>
  </div>
</div>""", font="Merriweather:wght@400;700", bg="#0c4a6e")


BUILDERS = {
    "bulk-email-verifier": bulk_email_verifier,
    "dev": dev_project,
    "devops2": devops2,
    "excel-mc-data-cleaner": excel_mc_data_cleaner,
    "excel-state-extractor-formula": excel_state_extractor,
    "forward-email-automation": forward_email_automation,
    "learningdashboard": learningdashboard,
    "mouse-coordinate-tracker": mouse_coordinate_tracker,
    "multi-smtp-email-automation": multi_smtp_automation,
    "mywebpagetask": mywebpagetask,
    "online-food-delivery": online_food_delivery,
    "pdf-mc-number-extractor": pdf_mc_extractor,
    "python-sms-automation": python_sms_automation,
    "quickdraw-test": quickdraw_test,
    "python-smtp-email-automation": python_smtp_automation,
    "quizmaster-online-testing-system": quizmaster,
}


def main() -> None:
    from playwright.sync_api import sync_playwright

    ASSETS.mkdir(parents=True, exist_ok=True)
    CACHE.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 800, "device_scale_factor": 2})
        for slug in TARGETS:
            builder = BUILDERS.get(slug)
            if not builder:
                print(f"skip {slug} — no builder")
                continue
            html_doc = builder()
            tmp = CACHE / f"{slug}.html"
            tmp.write_text(html_doc, encoding="utf-8")
            page.goto(tmp.as_uri(), wait_until="networkidle")
            page.wait_for_timeout(600)
            out = ASSETS / f"{slug}.png"
            page.screenshot(path=str(out))
            print(f"generated {out.name} ({out.stat().st_size // 1024} KB)")
        browser.close()
    print(f"Done — {len(TARGETS)} mockups.")


if __name__ == "__main__":
    main()
