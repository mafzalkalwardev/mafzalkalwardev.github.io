"""Apply shared head, nav, background, and script updates to all HTML pages."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
V = "9"
PAGES = ["index.html", "about.html", "projects.html", "skills.html", "contact.html"]

HEAD_EXTRA = f"""
  <link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32.png" />
  <link rel="icon" type="image/png" sizes="16x16" href="assets/favicon-16.png" />
  <link rel="apple-touch-icon" href="assets/apple-touch-icon.png" />
  <link rel="manifest" href="site.webmanifest" />
  <meta name="theme-color" content="#1d4ed8" media="(prefers-color-scheme: light)" />
  <meta name="theme-color" content="#0f172a" media="(prefers-color-scheme: dark)" />
  <script>
  (function(){{try{{var s=localStorage.getItem('portfolio-theme');var d=window.matchMedia('(prefers-color-scheme:dark)').matches;var t=s==='dark'||s==='light'?s:(d?'dark':'light');document.documentElement.setAttribute('data-theme',t);document.documentElement.style.colorScheme=t;}}catch(e){{}}}})();
  </script>
  <link rel="stylesheet" href="css/styles.css?v={V}" />
  <link rel="stylesheet" href="css/animations.css?v={V}" />
  <link rel="stylesheet" href="css/dark.css?v={V}" />
  <link rel="stylesheet" href="css/patterns.css?v={V}" />"""

BG_EXTRA = """
  <div class="scroll-progress" id="scrollProgress" aria-hidden="true"></div>
  <div class="bg-aurora" aria-hidden="true"><span></span><span></span><span></span></div>
  <div class="bg-pattern-cross" aria-hidden="true"></div>
  <div class="bg-pattern-waves" aria-hidden="true"></div>
  <div class="bg-particles" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i></div>"""

THEME_BTN = """
      <li>
        <button class="theme-toggle" id="themeToggle" type="button" aria-label="Toggle color mode">
          <svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
          <svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>
        </button>
      </li>"""

BASE_SCRIPTS = f"""
  <script src="js/site.js?v={V}"></script>
  <script src="js/theme.js?v={V}"></script>
  <script src="js/cv-download.js?v={V}"></script>
  <script src="js/motion.js?v={V}"></script>"""


def patch(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = re.sub(
        r'  <link rel="stylesheet" href="css/styles\.css\?v=\d+" />\s*'
        r'<link rel="stylesheet" href="css/animations\.css\?v=\d+" />',
        HEAD_EXTRA.strip(),
        text,
        count=1,
    )
    if "scroll-progress" not in text:
        text = text.replace("<body>", "<body>" + BG_EXTRA, 1)
    text = text.replace("https://github.com/mafzalkalwardev.png", "assets/profile.png")
    if "themeToggle" not in text:
        text = text.replace(
            '      <li><a href="https://github.com/mafzalkalwardev" class="nav-cta"',
            THEME_BTN + '\n      <li><a href="https://github.com/mafzalkalwardev" class="nav-cta"',
        )
    text = re.sub(r'js/site\.js\?v=\d+', f"js/site.js?v={V}", text)
    text = re.sub(r'js/theme\.js\?v=\d+', f"js/theme.js?v={V}", text)
    text = re.sub(r'js/cv-download\.js\?v=\d+', f"js/cv-download.js?v={V}", text)
    text = re.sub(r'js/motion\.js\?v=\d+', f"js/motion.js?v={V}", text)
    text = re.sub(r'js/tech-stack\.js\?v=\d+', f"js/tech-stack.js?v={V}", text)
    text = re.sub(r'js/projects\.js\?v=\d+', f"js/projects.js?v={V}", text)
    text = re.sub(r'js/projects-data\.js\?v=\d+', f"js/projects-data.js?v={V}", text)
    text = re.sub(r'js/contact\.js\?v=\d+', f"js/contact.js?v={V}", text)
    if "js/site.js" not in text:
        text = text.replace(
            "<script src=\"js/motion.js",
            BASE_SCRIPTS.strip().replace(f'<script src="js/motion.js?v={V}"></script>\n', "")
            + '\n  <script src="js/motion.js',
        )
    if "js/theme.js" not in text:
        text = text.replace('<script src="js/motion.js', f'<script src="js/site.js?v={V}"></script>\n  <script src="js/theme.js?v={V}"></script>\n  <script src="js/cv-download.js?v={V}"></script>\n  <script src="js/motion.js')
    path.write_text(text, encoding="utf-8")
    print(f"Patched {path.name}")


def main() -> None:
    for name in PAGES:
        patch(ROOT / name)


if __name__ == "__main__":
    main()
