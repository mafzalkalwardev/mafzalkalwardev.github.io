"""Re-capture demo videos for featured portfolio projects."""
from __future__ import annotations

from pathlib import Path

from capture_project_media import ASSETS, VIDEOS, capture_static_pages

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    VIDEOS.mkdir(parents=True, exist_ok=True)
    targets = [
        ("bulk-email-verifier", ["public/index.html", "public/dashboard.html"]),
        ("playwright-website-scraper-pro", ["frontend/index.html", "public/index.html"]),
        ("CallAudit-X", ["app/page.tsx"]),  # uses repo screenshot fallback in batch
    ]
    for repo, pages in targets:
        print(f"Recording {repo}...")
        _, webm = capture_static_pages(repo, pages, True)
        print(f"  -> {webm}")

    # Slide-style video for google-voice-dispatch-agent from PNG
    from playwright.sync_api import sync_playwright

    png = ASSETS / "google-voice-dispatch-agent.png"
    webm = VIDEOS / "google-voice-dispatch-agent.webm"
    if png.exists():
        html = ROOT / ".capture-cache" / "gv-video.html"
        html.parent.mkdir(parents=True, exist_ok=True)
        html.write_text(
            f'<!DOCTYPE html><html><body style="margin:0;background:#111">'
            f'<img src="file:///{png.resolve().as_posix()}" width="1280"></body></html>',
            encoding="utf-8",
        )
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                record_video_dir=str(VIDEOS),
                viewport={"width": 1280, "height": 800},
            )
            page = context.new_page()
            page.goto(html.as_uri())
            page.wait_for_timeout(2800)
            path = page.video.path() if page.video else None
            context.close()
            browser.close()
            if path and Path(path).exists():
                Path(path).replace(webm)
        print(f"  google-voice -> {webm.exists()}")


if __name__ == "__main__":
    main()
