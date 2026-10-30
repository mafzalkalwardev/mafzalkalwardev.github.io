#!/usr/bin/env python3
"""Generate SEO service landing pages for inbound marketing.

The published HTML is maintained directly. Re-running this script overwrites
services.html and the older dialer, scraper, and email/CRM pages.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SHELL_HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{description}" />
  <link rel="canonical" href="https://mafzalkalwardev.github.io/{filename}" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="{og_title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:url" content="https://mafzalkalwardev.github.io/{filename}" />
  <meta property="og:image" content="https://mafzalkalwardev.github.io/{og_image}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="keywords" content="{keywords}" />
  <link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32.png" />
  <link rel="icon" type="image/png" sizes="16x16" href="assets/favicon-16.png" />
  <link rel="apple-touch-icon" href="assets/apple-touch-icon.png" />
  <meta name="theme-color" content="#1d4ed8" media="(prefers-color-scheme: light)" />
  <meta name="theme-color" content="#0f172a" media="(prefers-color-scheme: dark)" />
  <script>
  (function(){{try{{var s=localStorage.getItem('portfolio-theme');var d=window.matchMedia('(prefers-color-scheme:dark)').matches;var t=s==='dark'||s==='light'?s:(d?'dark':'light');document.documentElement.setAttribute('data-theme',t);document.documentElement.style.colorScheme=t;}}catch(e){{}}}})();
  </script>
  <link rel="stylesheet" href="css/styles.css?v=19" />
  <link rel="stylesheet" href="css/animations.css?v=14" />
  <link rel="stylesheet" href="css/dark.css?v=14" />
  <link rel="stylesheet" href="css/patterns.css?v=14" />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
  <style>
    .svc-hero-shot {{ width:100%; max-height:360px; object-fit:cover; border-radius:12px; margin:1rem 0 1.5rem; border:1px solid rgba(148,163,184,.25); }}
    .svc-grid {{ display:grid; gap:1rem; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); margin:1.25rem 0; }}
    .svc-card {{ padding:1.1rem 1.2rem; border-radius:12px; border:1px solid rgba(148,163,184,.25); background:rgba(15,23,42,.03); }}
    .svc-card h3 {{ margin:0 0 .4rem; font-size:1rem; }}
    .svc-card p {{ margin:0; color:var(--text-muted); font-size:.9rem; line-height:1.55; }}
    .svc-cta {{ display:flex; flex-wrap:wrap; gap:.75rem; margin:1.5rem 0; }}
    .svc-faq details {{ margin:.6rem 0; padding: .85rem 1rem; border-radius:10px; border:1px solid rgba(148,163,184,.25); }}
    .svc-faq summary {{ cursor:pointer; font-weight:600; }}
    .svc-faq p {{ margin:.55rem 0 0; color:var(--text-muted); }}
    .svc-list {{ margin:.5rem 0 0 1.1rem; color:var(--text-muted); }}
    .svc-list a {{ color:var(--accent,#2563eb); }}
  </style>
</head>
<body>
  <div class="scroll-progress" id="scrollProgress" aria-hidden="true"></div>
  <div class="bg-aurora" aria-hidden="true"><span></span><span></span><span></span></div>
  <div class="bg-dots" aria-hidden="true"></div>
  <nav class="nav" id="nav">
    <a class="nav-brand" href="index.html">
      <img class="nav-avatar" src="assets/profile.png" alt="" width="36" height="36" />
      <span class="nav-name">Muhammad Afzal<span>Full-Stack Developer</span></span>
    </a>
    <button class="nav-toggle" id="navToggle" aria-label="Menu"><span></span><span></span><span></span></button>
    <ul class="nav-links" id="navLinks">
      <li><a href="index.html">Home</a></li>
      <li><a href="about.html">About</a></li>
      <li><a href="projects.html">Projects</a></li>
      <li><a href="services.html" class="{services_active}">Services</a></li>
      <li><a href="index.html#hire-me">Hire Me</a></li>
      <li><a href="contact.html">Contact</a></li>
      <li><a href="assets/Muhammad-Afzal-Kalwar-Services.pdf" class="nav-cv" download>Services PDF</a></li>
      <li>
        <button class="theme-toggle" id="themeToggle" type="button" aria-label="Toggle color mode">
          <svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
          <svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>
        </button>
      </li>
      <li><a href="https://github.com/mafzalkalwardev" class="nav-cta" target="_blank" rel="noopener">GitHub</a></li>
    </ul>
  </nav>
  <main>
    <div class="container">
'''

SHELL_FOOT = '''
    </div>
  </main>
  <footer class="footer">
    <div class="footer-links">
      <a href="services.html">Services</a>
      <a href="https://github.com/mafzalkalwardev" target="_blank" rel="noopener">GitHub @mafzalkalwardev</a>
      <a href="https://www.linkedin.com/in/mafzalkalwardev/" target="_blank" rel="noopener">LinkedIn @mafzalkalwardev</a>
      <a href="https://wa.me/923079670503" target="_blank" rel="noopener">WhatsApp +92 307 9670503</a>
      <a href="contact.html">Contact</a>
    </div>
    <p>&copy; <span id="year"></span> Muhammad Afzal Kalwar</p>
  </footer>
  <script src="js/site.js?v=14"></script>
  <script src="js/theme.js?v=14"></script>
</body>
</html>
'''

WA = "https://wa.me/923079670503?text=Hi%20Afzal%2C%20I%20found%20your%20{slug}%20service%20page%20and%20want%20to%20hire%20you"


def page(meta: dict, body: str) -> str:
    head = SHELL_HEAD.format(
        title=meta["title"],
        description=meta["description"],
        filename=meta["filename"],
        og_title=meta["og_title"],
        og_image=meta["og_image"],
        keywords=meta["keywords"],
        services_active=meta.get("services_active", ""),
    )
    return head + body + SHELL_FOOT


def cta(slug: str) -> str:
    return f'''
        <div class="svc-cta">
          <a class="btn btn-primary btn-lg" href="{WA.format(slug=slug)}" target="_blank" rel="noopener">WhatsApp +92 307 9670503</a>
          <a class="btn btn-secondary btn-lg" href="https://www.linkedin.com/in/mafzalkalwardev/" target="_blank" rel="noopener">LinkedIn @mafzalkalwardev</a>
          <a class="btn btn-secondary btn-lg" href="https://github.com/mafzalkalwardev" target="_blank" rel="noopener">GitHub @mafzalkalwardev</a>
          <a class="btn btn-cv btn-lg" href="assets/Muhammad-Afzal-Kalwar-Services.pdf" download>Services PDF</a>
        </div>
        <p style="color:var(--text-muted);font-size:.9rem">Remote worldwide · Freelance &amp; contract · Built by Muhammad Afzal Kalwar (<strong>@mafzalkalwardev</strong>)</p>
'''


PAGES = []

# Hub
PAGES.append((
    "services.html",
    {
        "title": "Services | Auto Dialers, Scrapers, Email & CRM | Muhammad Afzal Kalwar",
        "description": "Hire Muhammad Afzal Kalwar (@mafzalkalwardev) for auto dialers, web scrapers, email verification, and CRM automation. Remote freelance. WhatsApp +92 307 9670503.",
        "filename": "services.html",
        "og_title": "Automation Services by @mafzalkalwardev",
        "og_image": "assets/profile.png",
        "keywords": "hire automation developer, auto dialer developer, web scraper freelancer, email verification developer, CRM developer, mafzalkalwardev",
        "services_active": "active",
    },
    f'''
      <header class="page-header reveal">
        <h1 class="page-title">Services</h1>
        <p class="page-subtitle">Inbound-ready offers for businesses that need dialers, scrapers, and email/CRM systems — built by <strong>@mafzalkalwardev</strong>.</p>
      </header>
      <div class="svc-grid reveal">
        <a class="svc-card" href="services-dialers.html" style="text-decoration:none;color:inherit">
          <h3>Auto dialers &amp; voice AI</h3>
          <p>Google Voice / iPECS dialers, AI call scripts, operator consoles, Windows outbound tools.</p>
        </a>
        <a class="svc-card" href="services-scrapers.html" style="text-decoration:none;color:inherit">
          <h3>Web scrapers &amp; carrier data</h3>
          <p>Playwright/Selenium pipelines, FMCSA SAFER extractors, logistics lead systems.</p>
        </a>
        <a class="svc-card" href="services-email-crm.html" style="text-decoration:none;color:inherit">
          <h3>Email verification &amp; CRM</h3>
          <p>Bulk email verification, SMTP automation, lead CRMs, and admin dashboards.</p>
        </a>
      </div>
      {cta("services")}
'''
))

PAGES.append((
    "services-dialers.html",
    {
        "title": "Auto Dialer & Voice AI Developer for Hire | Muhammad Afzal Kalwar",
        "description": "Hire a Google Voice / iPECS auto dialer and AI calling developer. Python, Selenium, FastAPI, Chrome extensions. Remote. WhatsApp +92 307 9670503. @mafzalkalwardev",
        "filename": "services-dialers.html",
        "og_title": "Auto Dialers & Voice AI — Hire @mafzalkalwardev",
        "og_image": "assets/projects/google-voice-dispatch-agent.png",
        "keywords": "auto dialer developer, google voice dialer, ipecs dialer, AI call agent, dispatch dialer freelance, mafzalkalwardev",
        "services_active": "active",
    },
    f'''
      <header class="page-header reveal">
        <h1 class="page-title">Auto dialers &amp; voice AI</h1>
        <p class="page-subtitle">Custom outbound calling systems for dispatch and sales teams — Google Voice, iPECS, Windows dialers, and AI call assistants.</p>
      </header>
      <img class="svc-hero-shot reveal" src="assets/projects/google-voice-dispatch-agent.png" alt="Google Voice dispatch dialer preview" width="960" height="400" />
      <section class="reveal">
        <h2>Who this is for</h2>
        <p style="color:var(--text-muted)">Logistics/dispatch companies, outbound sales teams, and agencies that need reliable dialing without expensive call-center stacks.</p>
        <div class="svc-grid">
          <div class="svc-card"><h3>Google Voice dialers</h3><p>Queue dialing, scripts, voicemail handling, operator consoles.</p></div>
          <div class="svc-card"><h3>iPECS / Chrome dialers</h3><p>Manifest V3 extensions for cloud PBX outbound workflows.</p></div>
          <div class="svc-card"><h3>Windows desktop dialers</h3><p>Excel-driven campaigns, resume/hotkeys, local logs (PyQt / automation).</p></div>
          <div class="svc-card"><h3>AI call assist</h3><p>LLM scripts, STT/TTS hooks, call-state detection, CRM logging.</p></div>
        </div>
        <h2>Proof</h2>
        <ul class="svc-list">
          <li><a href="https://github.com/mafzalkalwardev/google-voice-dispatch-agent" target="_blank" rel="noopener">google-voice-dispatch-agent</a></li>
          <li><a href="https://github.com/mafzalkalwardev/python-auto-dialer-pro" target="_blank" rel="noopener">python-auto-dialer-pro</a></li>
          <li><a href="https://github.com/mafzalkalwardev/gv-auto-dialer-chrome-extension" target="_blank" rel="noopener">gv-auto-dialer-chrome-extension</a></li>
          <li><a href="https://github.com/mafzalkalwardev/ipecs-auto-dialer" target="_blank" rel="noopener">ipecs-auto-dialer</a></li>
          <li><a href="assets/Case-Study-Google-Voice-Dispatch-Agent.pdf">Case study PDF</a></li>
        </ul>
        {cta("auto-dialers")}
        <div class="svc-faq">
          <h2>FAQ</h2>
          <details open><summary>Can you customize a dialer for my workflow?</summary><p>Yes — Excel lists, CRM hooks, Google Voice or iPECS, pacing, and logging. Message on WhatsApp with your use case.</p></details>
          <details><summary>Do you work remotely?</summary><p>Yes. Based in Islamabad, Pakistan — remote worldwide as @mafzalkalwardev.</p></details>
        </div>
      </section>
'''
))

PAGES.append((
    "services-scrapers.html",
    {
        "title": "Web Scraper & FMCSA Data Developer for Hire | Muhammad Afzal Kalwar",
        "description": "Hire a Playwright/Selenium scraper and FMCSA SAFER carrier data developer. Logistics leads, site cloning, automation. WhatsApp +92 307 9670503. @mafzalkalwardev",
        "filename": "services-scrapers.html",
        "og_title": "Scrapers & Carrier Data — Hire @mafzalkalwardev",
        "og_image": "assets/projects/playwright-website-scraper-pro.png",
        "keywords": "web scraper freelancer, playwright developer, selenium scraper, FMCSA SAFER scraper, carrier data extraction, mafzalkalwardev",
        "services_active": "active",
    },
    f'''
      <header class="page-header reveal">
        <h1 class="page-title">Web scrapers &amp; carrier data</h1>
        <p class="page-subtitle">Playwright/Selenium pipelines and FMCSA SAFER extractors that turn websites into structured leads and datasets.</p>
      </header>
      <img class="svc-hero-shot reveal" src="assets/projects/playwright-website-scraper-pro.png" alt="Playwright scraper preview" width="960" height="400" />
      <section class="reveal">
        <h2>Who this is for</h2>
        <p style="color:var(--text-muted)">Freight brokers, dispatch marketers, agencies, and ops teams that need repeatable data extraction — not one-off copy/paste.</p>
        <div class="svc-grid">
          <div class="svc-card"><h3>Playwright scrapers</h3><p>Multi-page capture, screenshots, assets, anti-flake waits, exports.</p></div>
          <div class="svc-card"><h3>FMCSA / SAFER</h3><p>Carrier/MC lookups, phones, emails, addresses for logistics prospecting.</p></div>
          <div class="svc-card"><h3>Lead pipelines</h3><p>Queues, databases, Excel/CSV exports, scheduled runs.</p></div>
          <div class="svc-card"><h3>Site clone toolkits</h3><p>Audit/redesign captures with structured project output.</p></div>
        </div>
        <h2>Proof</h2>
        <ul class="svc-list">
          <li><a href="https://github.com/mafzalkalwardev/playwright-website-scraper-pro" target="_blank" rel="noopener">playwright-website-scraper-pro</a></li>
          <li><a href="https://github.com/mafzalkalwardev/safer-web-scraper" target="_blank" rel="noopener">safer-web-scraper</a></li>
          <li><a href="https://github.com/mafzalkalwardev/fmcsa-safer-scraper" target="_blank" rel="noopener">fmcsa-safer-scraper</a></li>
          <li><a href="https://github.com/mafzalkalwardev/indus-carrier-directory" target="_blank" rel="noopener">indus-carrier-directory</a></li>
        </ul>
        {cta("web-scrapers")}
        <div class="svc-faq">
          <h2>FAQ</h2>
          <details open><summary>Can you scrape a specific site for my business?</summary><p>Usually yes — share the target, fields you need, and volume. I design ethical, maintainable scrapers with clear deliverables.</p></details>
          <details><summary>Do you build carrier directories?</summary><p>Yes — searchable FMCSA-style directories and lead UIs like Indus Carrier Directory.</p></details>
        </div>
      </section>
'''
))

PAGES.append((
    "services-email-crm.html",
    {
        "title": "Email Verification & CRM Developer for Hire | Muhammad Afzal Kalwar",
        "description": "Hire for bulk email verification, SMTP automation, and lead CRM platforms. Full-stack dashboards. WhatsApp +92 307 9670503. GitHub/LinkedIn @mafzalkalwardev",
        "filename": "services-email-crm.html",
        "og_title": "Email Verification & CRM — Hire @mafzalkalwardev",
        "og_image": "assets/projects/bulk-email-verifier.png",
        "keywords": "email verification developer, SMTP automation freelance, lead CRM developer, bulk email verifier, mafzalkalwardev",
        "services_active": "active",
    },
    f'''
      <header class="page-header reveal">
        <h1 class="page-title">Email verification &amp; CRM</h1>
        <p class="page-subtitle">Bulk verification platforms, SMTP outreach tooling, and lead CRMs with admin dashboards — built for ops teams.</p>
      </header>
      <img class="svc-hero-shot reveal" src="assets/projects/bulk-email-verifier.png" alt="Bulk email verifier preview" width="960" height="400" />
      <section class="reveal">
        <h2>Who this is for</h2>
        <p style="color:var(--text-muted)">Agencies, GTM teams, and operators who need clean lists, controlled sending, and CRM workflows — not fragile scripts.</p>
        <div class="svc-grid">
          <div class="svc-card"><h3>Email verification</h3><p>Syntax/MX/SMTP checks, bulk CSV uploads, history &amp; analytics.</p></div>
          <div class="svc-card"><h3>SMTP automation</h3><p>Multi-sender campaigns, retries, templates, safe pacing.</p></div>
          <div class="svc-card"><h3>Lead CRMs</h3><p>Scraped/imported leads, queues, exports, Electron/desktop packaging.</p></div>
          <div class="svc-card"><h3>Admin dashboards</h3><p>Auth, roles, reporting, API integrations.</p></div>
        </div>
        <h2>Proof</h2>
        <ul class="svc-list">
          <li><a href="https://github.com/mafzalkalwardev/email-verification-platform" target="_blank" rel="noopener">email-verification-platform</a></li>
          <li><a href="https://github.com/mafzalkalwardev/bulk-email-verifier" target="_blank" rel="noopener">bulk-email-verifier</a></li>
          <li><a href="https://github.com/mafzalkalwardev/fiverr-lead-extractor-crm" target="_blank" rel="noopener">fiverr-lead-extractor-crm</a></li>
          <li><a href="https://github.com/mafzalkalwardev/multi-smtp-email-automation" target="_blank" rel="noopener">multi-smtp-email-automation</a></li>
        </ul>
        {cta("email-crm")}
        <div class="svc-faq">
          <h2>FAQ</h2>
          <details open><summary>Can you build a private verification tool for my team?</summary><p>Yes — self-hosted or cloud, with auth, bulk uploads, and reporting. WhatsApp to scope it.</p></details>
          <details><summary>Do you build custom CRMs?</summary><p>Yes — lead intake, workers/queues, Excel export, and admin UI tailored to your process.</p></details>
        </div>
      </section>
'''
))


def main():
    for filename, meta, body in PAGES:
        html = page(meta, body)
        (ROOT / filename).write_text(html, encoding="utf-8", newline="\n")
        print("wrote", filename)

    # sitemap
    urls = [
        ("https://mafzalkalwardev.github.io/", "weekly", "1.0"),
        ("https://mafzalkalwardev.github.io/about.html", "monthly", "0.8"),
        ("https://mafzalkalwardev.github.io/projects.html", "weekly", "0.9"),
        ("https://mafzalkalwardev.github.io/skills.html", "monthly", "0.8"),
        ("https://mafzalkalwardev.github.io/contact.html", "monthly", "0.8"),
        ("https://mafzalkalwardev.github.io/services.html", "weekly", "0.95"),
        ("https://mafzalkalwardev.github.io/services-dialers.html", "weekly", "0.9"),
        ("https://mafzalkalwardev.github.io/services-scrapers.html", "weekly", "0.9"),
        ("https://mafzalkalwardev.github.io/services-email-crm.html", "weekly", "0.9"),
        ("https://mafzalkalwardev.github.io/demos.html", "monthly", "0.7"),
    ]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, freq, pri in urls:
        sm.append(f"  <url><loc>{loc}</loc><changefreq>{freq}</changefreq><priority>{pri}</priority></url>")
    sm.append("</urlset>")
    sm.append("")
    (ROOT / "sitemap.xml").write_text("\n".join(sm), encoding="utf-8", newline="\n")
    print("wrote sitemap.xml")

    # Patch index hire-me cards to link to service pages if present
    idx = ROOT / "index.html"
    t = idx.read_text(encoding="utf-8")
    if "services-dialers.html" not in t:
        t = t.replace(
            "<h3>Auto dialers &amp; voice AI</h3>",
            '<h3><a href="services-dialers.html" style="color:inherit;text-decoration:none">Auto dialers &amp; voice AI</a></h3>',
            1,
        )
        t = t.replace(
            "<h3>Scrapers &amp; carrier data</h3>",
            '<h3><a href="services-scrapers.html" style="color:inherit;text-decoration:none">Scrapers &amp; carrier data</a></h3>',
            1,
        )
        t = t.replace(
            "<h3>Email &amp; CRM platforms</h3>",
            '<h3><a href="services-email-crm.html" style="color:inherit;text-decoration:none">Email &amp; CRM platforms</a></h3>',
            1,
        )
        # add Services nav if missing
        if 'href="services.html"' not in t:
            t = t.replace(
                '<li><a href="projects.html">Projects</a></li>',
                '<li><a href="projects.html">Projects</a></li>\n      <li><a href="services.html">Services</a></li>',
                1,
            )
        idx.write_text(t, encoding="utf-8", newline="\n")
        print("patched index.html")

    # Patch other main pages nav lightly
    for name in ("about.html", "projects.html", "skills.html", "contact.html", "demos.html"):
        path = ROOT / name
        if not path.exists():
            continue
        c = path.read_text(encoding="utf-8")
        if 'href="services.html"' in c:
            continue
        if '<li><a href="projects.html">Projects</a></li>' in c:
            c = c.replace(
                '<li><a href="projects.html">Projects</a></li>',
                '<li><a href="projects.html">Projects</a></li>\n      <li><a href="services.html">Services</a></li>',
                1,
            )
            path.write_text(c, encoding="utf-8", newline="\n")
            print("nav", name)

    readme = ROOT / "README.md"
    if readme.exists():
        r = readme.read_text(encoding="utf-8")
        block = """
## Service landing pages (SEO / inbound)

- [Services hub](https://mafzalkalwardev.github.io/services.html)
- [Auto dialers & voice AI](https://mafzalkalwardev.github.io/services-dialers.html)
- [Web scrapers & carrier data](https://mafzalkalwardev.github.io/services-scrapers.html)
- [Email verification & CRM](https://mafzalkalwardev.github.io/services-email-crm.html)
"""
        if "Service landing pages" not in r:
            readme.write_text(r.rstrip() + "\n" + block + "\n", encoding="utf-8", newline="\n")
            print("patched README")


if __name__ == "__main__":
    main()
