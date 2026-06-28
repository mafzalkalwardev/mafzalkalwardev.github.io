"""Capture real project screenshots and demo videos for portfolio + READMEs."""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

OWNER = "mafzalkalwardev"
ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets" / "projects"
VIDEOS = ROOT / "assets" / "videos"
CACHE = ROOT / ".capture-cache"
DATA_JS = ROOT / "js" / "projects-data.js"
AUTO_DIALER_ROOT = Path(r"d:\Dispatch Softwares\Auto Dialer")

SKIP = {
    "mafzalkalwardev",
    "professional-portfolio",
    "mafzalkalwardev.github.io",
    "odysseus",
    "rdp",
    "ft-solutions-hub",
    "quickdraw-test",
    "devops",
    "devops2",
    "dev",
}

# Explicit capture rules (override auto-detection)
CAPTURE_RULES: dict[str, dict] = {
    "indus-transport-auto-dialer": {
        "screenshot": "repo_path:docs/screenshots/live-calls-dark.png",
        "video": "repo_path:docs/screenshots/settings-light.png",
    },
    "one-stop-car-care-website": {"serve": "index.html", "pages": ["index.html"]},
    "kb-transport-llc-website": {"serve": "index.html"},
    "indus-transports-dispatch-website": {
        "serve": "index.html",
        "pages": ["index.html", "contact.html", "earnings.html"],
    },
    "bulk-email-verifier": {
        "serve": "public/index.html",
        "pages": ["public/index.html", "public/dashboard.html", "public/bulk.html"],
    },
    "mailforge": {"serve": "public/index.html", "pages": ["public/index.html"]},
    "email-verifier-pro": {"serve": "public/index.html"},
    "email-verification-platform": {"serve": "client/index.html", "fallback": "public/index.html"},
    "quizmaster-online-testing-system": {"serve": "views/index.ejs", "fallback": "public/index.html"},
    "online-food-delivery": {"serve": "views/index.ejs", "fallback": "public/index.html"},
    "portfilio": {"url": "https://243472-hash.github.io/portfilio/"},
    "mywebpagetask": {"serve": "index.html"},
    "LearningDashboard": {"serve": "wwwroot/index.html", "fallback": "Pages/Index.cshtml"},
    "CallAudit-X": {"serve": "app/page.tsx", "skip_dev": True},
    "fiverr-lead-extractor-crm": {"skip_dev": True},
    "playwright-website-scraper-pro": {"screenshot": "repo_path:docs/screenshots/home.png"},
    "logistics-pro-website": {"serve": "index.html"},
    "apex-transit-llc-website": {"serve": "index.html"},
    "wooly-wool-storefront": {"serve": "index.html"},
    "kb-transport-llc-website": {"serve": "index.html"},
    "andaaz-e-pakwaan-restaurant": {"serve": "index.html", "fallback": "public/index.html"},
    "portfolio-afzal-kalwar-vite": {"skip_dev": True},
    "indus-web-agency": {"skip_dev": True},
    "mnist-cnn-digit-recognition": {"serve": "gui.py", "type": "python_gui"},
    "professional-portfolio": {"url": "https://mafzalkalwardev.github.io/"},
}


def slug(name: str) -> str:
    return name.lower().replace(" ", "-")


def project_title(name: str) -> str:
    special = {"crm": "CRM", "api": "API", "smtp": "SMTP", "mc": "MC", "dat": "DAT", "x": "X"}
    return " ".join(special.get(p.lower(), p.capitalize()) for p in name.replace("_", "-").split("-"))


def gh_json(*args: str) -> list | dict:
    out = subprocess.check_output(["gh", *args], text=True, stderr=subprocess.DEVNULL)
    return json.loads(out)


def clone_repo(repo: str) -> Path:
    dest = CACHE / repo
    if dest.exists():
        return dest
    CACHE.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["gh", "repo", "clone", f"{OWNER}/{repo}", str(dest), "--", "--depth", "1"],
        check=True,
        capture_output=True,
    )
    return dest


def download_raw(repo: str, path: str, dest: Path) -> bool:
    url = f"https://raw.githubusercontent.com/{OWNER}/{repo}/main/{path}"
    try:
        dest.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(url, dest)
        return dest.stat().st_size > 500
    except Exception:
        for branch in ("master", "main"):
            try:
                url = f"https://raw.githubusercontent.com/{OWNER}/{repo}/{branch}/{path}"
                urllib.request.urlretrieve(url, dest)
                if dest.stat().st_size > 500:
                    return True
            except Exception:
                pass
    return False


def find_repo_screenshot(repo: str) -> str | None:
    for folder in ("docs/screenshots", "docs/images", "screenshots", "assets"):
        try:
            items = gh_json("api", f"repos/{OWNER}/{repo}/contents/{folder}")
            for item in items:
                name = item.get("name", "")
                if name.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                    if "placeholder" not in name.lower():
                        return f"{folder}/{name}"
        except subprocess.CalledProcessError:
            continue
    return None


def find_serve_entry(repo_path: Path) -> str | None:
    candidates = [
        "index.html",
        "public/index.html",
        "client/index.html",
        "frontend/index.html",
        "src/index.html",
        "wwwroot/index.html",
        "app/index.html",
    ]
    for c in candidates:
        if (repo_path / c).exists():
            return c
    for html in repo_path.rglob("index.html"):
        rel = html.relative_to(repo_path).as_posix()
        if "node_modules" not in rel and ".git" not in rel:
            return rel
    return None


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args) -> None:
        pass


def start_server(directory: Path) -> tuple[ThreadingHTTPServer, int]:
    handler = lambda *a, **k: QuietHandler(*a, directory=str(directory), **k)  # noqa: E731
    for port in range(8765, 8795):
        try:
            server = ThreadingHTTPServer(("127.0.0.1", port), handler)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            return server, port
        except OSError:
            continue
    raise RuntimeError("No free port for static server")


def capture_browser(
    url: str,
    png_out: Path,
    webm_out: Path | None,
    viewport: tuple[int, int] = (1280, 800),
) -> bool:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("  playwright not installed")
        return False

    png_out.parent.mkdir(parents=True, exist_ok=True)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context_kwargs: dict = {"viewport": {"width": viewport[0], "height": viewport[1]}}
            if webm_out:
                webm_out.parent.mkdir(parents=True, exist_ok=True)
                context_kwargs["record_video_dir"] = str(webm_out.parent)
                context_kwargs["record_video_size"] = {"width": viewport[0], "height": viewport[1]}
            context = browser.new_context(**context_kwargs)
            page = context.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(2000)
            page.screenshot(path=str(png_out), full_page=False)
            if webm_out:
                page.evaluate("window.scrollBy(0, Math.min(400, document.body.scrollHeight * 0.3))")
                page.wait_for_timeout(1800)
                page.evaluate("window.scrollTo(0, 0)")
                page.wait_for_timeout(600)
            video = page.video
            context.close()
            browser.close()
            if webm_out and video:
                tmp = video.path()
                if tmp and Path(tmp).exists():
                    shutil.move(tmp, webm_out)
        return png_out.exists() and png_out.stat().st_size > 2000
    except Exception as exc:
        print(f"  browser capture failed: {exc}")
        if png_out.exists() and png_out.stat().st_size < 2000:
            png_out.unlink(missing_ok=True)
        return False


def capture_static_pages(repo: str, pages: list[str], record_video: bool) -> tuple[Path | None, Path | None]:
    repo_path = clone_repo(repo)
    server, port = start_server(repo_path)
    png_out = ASSETS / f"{slug(repo)}.png"
    webm_out = VIDEOS / f"{slug(repo)}.webm" if record_video else None
    ok = False
    try:
        for page in pages:
            rel = page.replace("\\", "/")
            url = f"http://127.0.0.1:{port}/{rel}"
            if capture_browser(url, png_out, webm_out if not ok else None):
                ok = True
                break
    finally:
        server.shutdown()
        server.server_close()
    return (png_out if ok else None, webm_out if ok and webm_out and webm_out.exists() else None)


def capture_from_url(url: str, repo: str, record_video: bool) -> tuple[Path | None, Path | None]:
    png_out = ASSETS / f"{slug(repo)}.png"
    webm_out = VIDEOS / f"{slug(repo)}.webm" if record_video else None
    if capture_browser(url, png_out, webm_out):
        return png_out, webm_out if webm_out and webm_out.exists() else None
    return None, None


def capture_from_repo_file(repo: str, rel_path: str) -> Path | None:
    png_out = ASSETS / f"{slug(repo)}.png"
    tmp = png_out.with_suffix(".tmp.png")
    if download_raw(repo, rel_path, tmp):
        shutil.copy(tmp, png_out)
        tmp.unlink(missing_ok=True)
        return png_out
    return None


def capture_local_auto_dialer() -> Path | None:
    png_out = ASSETS / "indus-transport-auto-dialer.png"
    sources = [
        AUTO_DIALER_ROOT / "docs" / "screenshots" / "live-calls-dark.png",
        AUTO_DIALER_ROOT / "docs" / "screenshots" / "settings-light.png",
    ]
    for src in sources:
        if src.exists():
            shutil.copy(src, png_out)
            return png_out
    rel = find_repo_screenshot("indus-transport-auto-dialer")
    if rel:
        return capture_from_repo_file("indus-transport-auto-dialer", rel)
    return None


def try_nextjs_dev(repo: str, record_video: bool) -> tuple[Path | None, Path | None]:
    repo_path = clone_repo(repo)
    if not (repo_path / "package.json").exists():
        return None, None
    png_out = ASSETS / f"{slug(repo)}.png"
    webm_out = VIDEOS / f"{slug(repo)}.webm" if record_video else None
    env = {**os.environ, "PORT": "3000"}
    proc = subprocess.Popen(
        ["npm", "run", "dev", "--", "-p", "3000"],
        cwd=repo_path,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
        shell=True,
    )
    try:
        for _ in range(40):
            time.sleep(2)
            if capture_browser("http://127.0.0.1:3000", png_out, webm_out):
                return png_out, webm_out if webm_out and webm_out.exists() else None
        return None, None
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=8)
        except subprocess.TimeoutExpired:
            proc.kill()


def capture_cli_card(repo: str, title_text: str, desc: str, lines: list[str]) -> Path | None:
    """Render a terminal-style preview for CLI-only projects."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return None
    png_out = ASSETS / f"{slug(repo)}.png"
    body = "\\n".join(lines[:8])
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
body{{margin:0;background:#0f172a;font-family:Consolas,monospace;display:flex;align-items:center;justify-content:center;min-height:100vh;padding:32px}}
.card{{width:760px;border-radius:14px;overflow:hidden;box-shadow:0 24px 48px rgba(0,0,0,.35);border:1px solid #334155}}
.bar{{background:#1e293b;padding:10px 14px;color:#94a3b8;font-size:13px;display:flex;gap:8px;align-items:center}}
.dot{{width:10px;height:10px;border-radius:50%}}
.term{{background:#020617;color:#e2e8f0;padding:20px;font-size:13px;line-height:1.55;white-space:pre-wrap}}
h1{{font-family:Segoe UI,sans-serif;color:#f8fafc;font-size:18px;margin:0 0 6px}}
p{{font-family:Segoe UI,sans-serif;color:#94a3b8;font-size:12px;margin:0 0 14px}}
</style></head><body><div class="card">
<div class="bar"><span class="dot" style="background:#ef4444"></span><span class="dot" style="background:#eab308"></span><span class="dot" style="background:#22c55e"></span><span>{title_text}</span></div>
<div class="term"><h1>{title_text}</h1><p>{desc[:120]}</p>{body}</div></div></body></html>"""
    tmp = png_out.with_suffix(".html")
    tmp.write_text(html, encoding="utf-8")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 900, "height": 560})
            page.goto(tmp.as_uri(), wait_until="domcontentloaded")
            page.screenshot(path=str(png_out))
            browser.close()
        tmp.unlink(missing_ok=True)
        return png_out if png_out.exists() else None
    except Exception:
        tmp.unlink(missing_ok=True)
        return None


CLI_PREVIEWS: dict[str, list[str]] = {
    "multi-smtp-email-automation": [
        "$ python send_emails.py --accounts 5 --recipients leads.xlsx",
        "[INFO] Loaded 5 SMTP accounts, 1,240 recipients",
        "[OK]   Sent 50/50 batch #1 — 0 failures",
        "[OK]   Sent 50/50 batch #2 — 1 retry succeeded",
        "[DONE] Campaign complete — logs/smtp_run_2026-06-02.csv",
    ],
    "python-smtp-email-automation": [
        "$ python main.py --sheet contacts.xlsx",
        "[INFO] Gmail SMTP authenticated",
        "[OK]   Personalized template applied per row",
        "[OK]   120 emails queued with safe delays",
    ],
    "python-sms-automation": [
        "$ python sms_bot.py",
        "[INFO] Excel contacts loaded: 86 rows",
        "[OK]   PyAutoGUI sending personalized SMS",
        "[OK]   Progress saved — resume supported",
    ],
    "forward-email-automation": [
        "$ python forward.py --carrier-list mc_numbers.txt",
        "[INFO] Parsing carrier contacts",
        "[OK]   Forwarding pipeline active",
        "[OK]   Dispatch outreach batch complete",
    ],
    "fmcsa-safer-scraper": [
        "$ python safer_scraper.py --mc 123456",
        "[INFO] Selenium session started",
        "[OK]   Company: Example Logistics LLC",
        "[OK]   Phone / email extracted to output.csv",
    ],
    "safer-web-scraper": [
        "$ jupyter notebook safer_pipeline.ipynb",
        "[INFO] FMCSA SAFER toolkit ready",
        "[OK]   Carrier records normalized",
        "[OK]   Export saved to data/carriers.csv",
    ],
    "safer-carrier-extractor": [
        "$ python extract.py --state TX --limit 100",
        "[INFO] Querying SAFER database",
        "[OK]   100 carriers parsed",
        "[OK]   Written to carriers_tx.csv",
    ],
    "pdf-mc-number-extractor": [
        "$ python extract_mc.py invoices.pdf",
        "[INFO] Scanning 48 pages",
        "[OK]   Found 312 unique MC numbers",
        "[OK]   Saved mc_numbers.txt (sorted)",
    ],
    "excel-mc-data-cleaner": [
        "$ Excel VBA macro: CleanCarrierData",
        "[INFO] Validating email columns",
        "[OK]   States extracted from addresses",
        "[OK]   MC records formatted for dispatch",
    ],
    "excel-state-extractor-formula": [
        "=STATE_FROM_ADDRESS(\"742 Evergreen Terrace, Springfield IL\")",
        "→ IL",
        "Batch formula applied across 2,000 rows",
    ],
    "mouse-coordinate-tracker": [
        "$ python tracker.py",
        "[LIVE] x=842 y=516  (click to log)",
        "[LIVE] x=1120 y=744 (click to log)",
        "[SAVE] coordinates.txt updated",
    ],
    "excel-call-queue-automator": [
        "$ python call_queue.py --excel leads.xlsx",
        "[INFO] 450 numbers loaded",
        "[HOTKEY] F8 dial · F9 hangup · F10 skip",
        "[OK]   CSV call log exported",
    ],
    "python-auto-dialer-pro": [
        "$ python autodialer_gui.py",
        "[INFO] Excel contacts loaded",
        "[OK]   PyAutoGUI dial pad automation ready",
        "[OK]   Resume + keyboard shortcuts enabled",
    ],
    "google-voice-dispatch-agent": [],  # has real screenshot
    "dat-stream-studio": [
        "$ python dat_stream_studio.py",
        "[INFO] PyQt DAT workspace started",
        "[OK]   Proxy profiles loaded",
        "[OK]   Embedded browser + extension bridge active",
    ],
    "fiverr-lead-extractor-crm": [
        "$ npm run dev",
        "▲ Next.js CRM — Fiverr Lead Extractor",
        "[OK]   Playwright review extraction ready",
        "[OK]   MongoDB + BullMQ worker connected",
    ],
}


def resolve_project(repo: str, featured: bool) -> tuple[Path | None, Path | None]:
    s = slug(repo)
    record_video = featured
    rules = CAPTURE_RULES.get(repo, {})

    if repo == "indus-transport-auto-dialer":
        png = capture_local_auto_dialer()
        webm = None
        settings = AUTO_DIALER_ROOT / "docs" / "screenshots" / "settings-light.png"
        if record_video and settings.exists():
            VIDEOS.mkdir(parents=True, exist_ok=True)
            # Use second screenshot as poster; short web capture if we add later
            poster = VIDEOS / "indus-transport-auto-dialer-poster.png"
            shutil.copy(settings, poster)
        return png, webm

    if "url" in rules:
        return capture_from_url(rules["url"], repo, record_video)

    if "screenshot" in rules and rules["screenshot"].startswith("repo_path:"):
        rel = rules["screenshot"].split(":", 1)[1]
        png = capture_from_repo_file(repo, rel)
        return png, None

    if "serve" in rules or "pages" in rules:
        pages = rules.get("pages")
        if not pages:
            entry = rules["serve"]
            if not (CACHE / repo).exists():
                clone_repo(repo)
            repo_path = CACHE / repo
            if not (repo_path / entry).exists() and rules.get("fallback"):
                entry = rules["fallback"]
            if (repo_path / entry).exists():
                pages = [entry]
            else:
                pages = [find_serve_entry(repo_path) or "index.html"]
        return capture_static_pages(repo, pages, record_video)

    if rules.get("fallback_url") and not rules.get("skip_dev"):
        png, webm = try_nextjs_dev(repo, record_video)
        if png:
            return png, webm

    # Auto: existing repo screenshots
    rel = find_repo_screenshot(repo)
    if rel:
        png = capture_from_repo_file(repo, rel)
        if png:
            return png, None

    # Auto: static HTML in repo
    repo_path = clone_repo(repo)
    entry = find_serve_entry(repo_path)
    if entry and entry.endswith(".html"):
        return capture_static_pages(repo, [entry], record_video)

    # Auto: README images at repo root
    for name in ("image.png", "screenshot.png", "preview.png", "demo.png"):
        if (repo_path / name).exists():
            shutil.copy(repo_path / name, ASSETS / f"{s}.png")
            return ASSETS / f"{s}.png", None

    # CLI terminal card fallback
    if repo in CLI_PREVIEWS and CLI_PREVIEWS[repo]:
        try:
            desc = gh_json("api", f"repos/{OWNER}/{repo}").get("description") or repo
        except Exception:
            desc = repo
        png = capture_cli_card(repo, project_title(repo), desc, CLI_PREVIEWS[repo])
        if png:
            return png, None

    return None, None


def sync_projects_data(results: dict[str, dict]) -> None:
    if not DATA_JS.exists():
        return
    text = DATA_JS.read_text(encoding="utf-8")
    for s, info in results.items():
        if not info.get("png"):
            continue
        pattern = rf'(slug:\s*"{re.escape(s)}"[\s\S]*?image:\s*")[^"]+(")'
        repl = rf'\1assets/projects/{s}.png\2'
        text, n = re.subn(pattern, repl, text, count=1)
        if n == 0:
            pattern2 = rf'(repo:\s*"[^"]*"[\s\S]*?slug:\s*"{re.escape(s)}"[\s\S]*?image:\s*")[^"]+(")'
            text = re.sub(pattern2, repl, text, count=1)
    DATA_JS.write_text(text, encoding="utf-8")


def main_portfolio_only() -> int:
    """Capture screenshots only for repos listed in js/projects-data.js."""
    ASSETS.mkdir(parents=True, exist_ok=True)
    text = DATA_JS.read_text(encoding="utf-8")
    repos = re.findall(r'repo:\s*"([^"]+)"', text)
    featured = {
        "indus-transport-auto-dialer", "bulk-email-verifier",
        "google-voice-dispatch-agent", "fiverr-lead-extractor-crm",
        "CallAudit-X", "playwright-website-scraper-pro", "callauditx-nest-react",
        "mighty-trucking", "al-qibla-air-services", "tony-ai", "sms-marketing-crm",
    }
    results: dict[str, dict] = {}
    captured = 0
    for name in repos:
        s = slug(name)
        print(f"Capturing {name}...", flush=True)
        try:
            png, webm = resolve_project(name, name in featured)
        except Exception as exc:
            print(f"  error: {exc}")
            png, webm = None, None
        if png and png.exists():
            results[s] = {"png": str(png), "webm": str(webm) if webm else None}
            captured += 1
            print(f"  OK screenshot -> {png.name}")
        else:
            print("  skipped (no capture)")
    sync_projects_data(results)
    print(f"\nPortfolio capture done: {captured}/{len(repos)} projects with real screenshots.")
    return 0


def main() -> int:
    ASSETS.mkdir(parents=True, exist_ok=True)
    repos = gh_json("repo", "list", OWNER, "--limit", "100", "--json", "name,isFork")
    featured = {
        "indus-transport-auto-dialer", "bulk-email-verifier",
        "google-voice-dispatch-agent", "fiverr-lead-extractor-crm",
        "CallAudit-X", "playwright-website-scraper-pro",
    }
    results: dict[str, dict] = {}
    captured = 0

    for r in repos:
        name = r["name"]
        if r.get("isFork") or name in SKIP:
            continue
        s = slug(name)
        print(f"Capturing {name}...", flush=True)
        try:
            png, webm = resolve_project(name, name in featured)
        except Exception as exc:
            print(f"  error: {exc}")
            png, webm = None, None
        if png and png.exists():
            results[s] = {"png": str(png), "webm": str(webm) if webm else None}
            captured += 1
            print(f"  OK screenshot -> {png.name}")
            if webm:
                print(f"  OK video -> {webm.name}")
        else:
            print("  skipped (no capture)")

    sync_projects_data(results)
    print(f"\nDone: {captured} projects with real screenshots.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--portfolio-only":
        sys.exit(main_portfolio_only())
    sys.exit(main())
