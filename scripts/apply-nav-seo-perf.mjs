/**
 * Slim navbar across pages, add SEO/GEO head tags, cut decorative layers,
 * defer scripts, bump asset cache to v=21.
 */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const root = path.join(path.dirname(fileURLToPath(import.meta.url)), "..");
const VERSION = "21";
const SITE = "https://mafzalkalwardev.github.io";
const PROFILE = `${SITE}/assets/profile.png`;

const pages = {
  "index.html": {
    active: "Home",
    title: "Muhammad Afzal Kalwar | Full-Stack Developer & Python Automation Engineer",
    description:
      "Hire Muhammad Afzal Kalwar (@mafzalkalwardev) — full-stack developer and Python automation engineer for auto dialers, scrapers, email verification, CRM, and AI workflows. Remote worldwide.",
    path: "/",
    keywords:
      "Muhammad Afzal Kalwar, mafzalkalwardev, hire automation developer, auto dialer developer, web scraper freelancer, email verification, CRM developer, Python automation, full-stack developer Islamabad",
  },
  "about.html": {
    active: "About",
    title: "About Muhammad Afzal Kalwar | Full-Stack & Automation Engineer",
    description:
      "About Muhammad Afzal Kalwar (@mafzalkalwardev) — B.S. Computer Science, Air University Islamabad. Full-stack developer building dialers, scrapers, CRM, and AI tools for businesses.",
    path: "/about.html",
    keywords: "Muhammad Afzal Kalwar, about, Air University, full-stack developer, mafzalkalwardev",
  },
  "projects.html": {
    active: "Projects",
    title: "Projects | Muhammad Afzal Kalwar — Dialers, Scrapers, CRM & SaaS",
    description:
      "Portfolio projects by @mafzalkalwardev: Google Voice dialers, Playwright scrapers, bulk email verifiers, SMS CRM, travel platforms, and open-source automation tools.",
    path: "/projects.html",
    keywords: "portfolio projects, auto dialer, web scraper, email verifier, CRM, mafzalkalwardev",
  },
  "services.html": {
    active: "Services",
    title: "Automation Services for Hire | @mafzalkalwardev",
    description:
      "Hire Muhammad Afzal Kalwar for auto dialers, web scrapers, email verification, and CRM automation. Remote freelance. WhatsApp +92 307 9670503.",
    path: "/services.html",
    keywords: "hire automation developer, auto dialer developer, web scraper freelancer, CRM developer",
  },
  "services-dialers.html": {
    active: "Services",
    title: "Auto Dialer & Voice AI Developer for Hire | Muhammad Afzal Kalwar",
    description:
      "Hire a Google Voice / iPECS auto dialer and AI calling developer. Python, Selenium, FastAPI, Chrome extensions. Remote. WhatsApp +92 307 9670503.",
    path: "/services-dialers.html",
    keywords: "auto dialer developer, google voice dialer, ipecs dialer, AI call agent",
    image: `${SITE}/assets/projects/google-voice-dispatch-agent.png`,
  },
  "services-scrapers.html": {
    active: "Services",
    title: "Scrapers & Carrier Data Developer for Hire | @mafzalkalwardev",
    description:
      "Hire a Playwright/Selenium scraper and FMCSA SAFER carrier data developer. Logistics leads, site cloning, automation. WhatsApp +92 307 9670503.",
    path: "/services-scrapers.html",
    keywords: "web scraper developer, Playwright scraper, FMCSA SAFER, carrier data",
    image: `${SITE}/assets/projects/playwright-website-scraper-pro.png`,
  },
  "services-email-crm.html": {
    active: "Services",
    title: "Email Verification & CRM Developer for Hire | @mafzalkalwardev",
    description:
      "Hire for bulk email verification, SMTP automation, and lead CRM platforms. Full-stack dashboards. WhatsApp +92 307 9670503.",
    path: "/services-email-crm.html",
    keywords: "email verification developer, SMTP automation, lead CRM, mafzalkalwardev",
    image: `${SITE}/assets/projects/bulk-email-verifier.png`,
  },
  "contact.html": {
    active: "Contact",
    title: "Contact / Hire Muhammad Afzal Kalwar | @mafzalkalwardev",
    description:
      "Contact Muhammad Afzal Kalwar for freelance automation and full-stack work. WhatsApp +92 307 9670503 · LinkedIn/GitHub @mafzalkalwardev · Islamabad, remote worldwide.",
    path: "/contact.html",
    keywords: "hire Muhammad Afzal Kalwar, contact mafzalkalwardev, WhatsApp automation developer",
  },
  "skills.html": {
    active: "Home",
    title: "Skills & Tech Stack | Muhammad Afzal Kalwar",
    description:
      "Tech stack used by @mafzalkalwardev: Python, React, Node.js, Playwright, FastAPI, Docker, MongoDB, TypeScript, Go, and more.",
    path: "/skills.html",
    keywords: "Python, React, Playwright, FastAPI, Docker, developer skills",
  },
  "demos.html": {
    active: "Home",
    title: "Live Demo Videos | Muhammad Afzal Kalwar",
    description:
      "Safe demo previews of scrapers, email verifiers, dialers, and CRM tools by @mafzalkalwardev using sample data only.",
    path: "/demos.html",
    keywords: "demo videos, scraper demo, dialer demo, email verifier demo",
  },
};

const slimBg = `  <div class="scroll-progress" id="scrollProgress" aria-hidden="true"></div>
  <div class="bg-mesh" aria-hidden="true"><div class="bg-mesh-inner"></div></div>
  <div class="bg-dots" aria-hidden="true"></div>
  <div class="bg-orbs" aria-hidden="true">
    <span class="orb orb-1"></span>
    <span class="orb orb-2"></span>
  </div>`;

function navHtml(active) {
  const item = (label, href) =>
    `<li><a href="${href}"${label === active ? ' class="active"' : ""}>${label}</a></li>`;
  return `  <nav class="nav" id="nav" aria-label="Primary">
    <a class="nav-brand" href="index.html">
      <img class="nav-avatar" src="assets/profile.png" alt="Muhammad Afzal Kalwar" width="38" height="38" />
      <span class="nav-name">Muhammad Afzal<span>Full-Stack Developer</span></span>
    </a>
    <button class="nav-toggle" id="navToggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="navLinks"><span></span><span></span><span></span></button>
    <ul class="nav-links" id="navLinks">
      ${item("Home", "index.html")}
      ${item("About", "about.html")}
      ${item("Projects", "projects.html")}
      ${item("Services", "services.html")}
      ${item("Contact", "contact.html")}
      <li>
        <button class="theme-toggle" id="themeToggle" type="button" aria-label="Toggle color mode">
          <svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
          <svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>
        </button>
      </li>
      <li><a href="contact.html" class="nav-cta">Hire Me</a></li>
    </ul>
  </nav>`;
}

function seoHead(meta) {
  const url = `${SITE}${meta.path === "/" ? "/" : meta.path}`;
  const image = meta.image || PROFILE;
  return `  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>${meta.title}</title>
  <meta name="description" content="${meta.description}" />
  <meta name="keywords" content="${meta.keywords}" />
  <meta name="author" content="Muhammad Afzal Kalwar" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
  <link rel="canonical" href="${url}" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="Muhammad Afzal Kalwar" />
  <meta property="og:title" content="${meta.title}" />
  <meta property="og:description" content="${meta.description}" />
  <meta property="og:url" content="${url}" />
  <meta property="og:image" content="${image}" />
  <meta property="og:locale" content="en_US" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="${meta.title}" />
  <meta name="twitter:description" content="${meta.description}" />
  <meta name="twitter:image" content="${image}" />
  <meta name="twitter:creator" content="@mafzalkalwardev" />
  <link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32.png" />
  <link rel="icon" type="image/png" sizes="16x16" href="assets/favicon-16.png" />
  <link rel="apple-touch-icon" href="assets/apple-touch-icon.png" />
  <link rel="manifest" href="site.webmanifest" />
  <meta name="theme-color" content="#1d4ed8" media="(prefers-color-scheme: light)" />
  <meta name="theme-color" content="#0f172a" media="(prefers-color-scheme: dark)" />
  <script>
  (function(){try{var s=localStorage.getItem('portfolio-theme');var d=window.matchMedia('(prefers-color-scheme:dark)').matches;var t=s==='dark'||s==='light'?s:(d?'dark':'light');document.documentElement.setAttribute('data-theme',t);document.documentElement.style.colorScheme=t;}catch(e){}})();
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="stylesheet" href="css/styles.css?v=${VERSION}" />
  <link rel="stylesheet" href="css/dark.css?v=${VERSION}" />
  <link rel="stylesheet" href="css/animations.css?v=${VERSION}" />
  <link rel="stylesheet" href="css/patterns.css?v=${VERSION}" media="print" onload="this.media='all'" />
  <noscript><link rel="stylesheet" href="css/patterns.css?v=${VERSION}" /></noscript>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />`;
}

const indexSchema = `
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "WebSite",
        "@id": "${SITE}/#website",
        "url": "${SITE}/",
        "name": "Muhammad Afzal Kalwar",
        "description": "Full-Stack Developer & Python Automation Engineer portfolio",
        "publisher": { "@id": "${SITE}/#person" },
        "inLanguage": "en"
      },
      {
        "@type": "Person",
        "@id": "${SITE}/#person",
        "name": "Muhammad Afzal Kalwar",
        "alternateName": ["mafzalkalwardev", "Afzal Kalwar"],
        "url": "${SITE}/",
        "image": "${PROFILE}",
        "jobTitle": "Full-Stack Developer & Python Automation Engineer",
        "email": "mailto:kalwarmuhammadafzal3@gmail.com",
        "telephone": "+923079670503",
        "address": {
          "@type": "PostalAddress",
          "addressLocality": "Islamabad",
          "addressCountry": "PK"
        },
        "alumniOf": {
          "@type": "CollegeOrUniversity",
          "name": "Air University",
          "address": { "@type": "PostalAddress", "addressLocality": "Islamabad", "addressCountry": "PK" }
        },
        "sameAs": [
          "https://github.com/mafzalkalwardev",
          "https://www.linkedin.com/in/mafzalkalwardev/",
          "https://wa.me/923079670503"
        ],
        "knowsAbout": [
          "Python automation",
          "Auto dialers",
          "Web scraping",
          "Email verification",
          "CRM systems",
          "React",
          "Node.js",
          "Playwright"
        ]
      },
      {
        "@type": "ProfessionalService",
        "@id": "${SITE}/#services",
        "name": "Muhammad Afzal Kalwar — Automation & Full-Stack Services",
        "url": "${SITE}/services.html",
        "image": "${PROFILE}",
        "provider": { "@id": "${SITE}/#person" },
        "areaServed": "Worldwide",
        "availableLanguage": ["English", "Urdu"],
        "serviceType": [
          "Auto dialer development",
          "Web scraping & carrier data",
          "Email verification & CRM",
          "Full-stack product builds"
        ]
      }
    ]
  }
  </script>`;

function replaceHead(html, meta) {
  return html.replace(/<head>[\s\S]*?<\/head>/i, `<head>\n${seoHead(meta)}\n</head>`);
}

function replaceNav(html, active) {
  return html.replace(/<nav class="nav"[\s\S]*?<\/nav>/i, navHtml(active));
}

function replaceBg(html) {
  return html.replace(
    /<div class="scroll-progress"[\s\S]*?(?=<nav class="nav")/i,
    slimBg + "\n\n"
  );
}

function deferScripts(html) {
  return html
    .replace(/\?v=\d+/g, `?v=${VERSION}`)
    .replace(/<script src="(js\/[^"]+)"><\/script>/g, '<script src="$1" defer></script>');
}

function enrichFooter(html) {
  if (!html.includes('class="footer"')) return html;
  if (html.includes("footer-sitemap")) return html;
  return html.replace(
    /<div class="footer-links">[\s\S]*?<\/div>/,
    `<div class="footer-links footer-sitemap">
      <a href="index.html">Home</a>
      <a href="about.html">About</a>
      <a href="projects.html">Projects</a>
      <a href="services.html">Services</a>
      <a href="skills.html">Skills</a>
      <a href="demos.html">Demos</a>
      <a href="contact.html">Contact</a>
      <a href="https://github.com/mafzalkalwardev" target="_blank" rel="noopener">GitHub</a>
      <a href="https://www.linkedin.com/in/mafzalkalwardev/" target="_blank" rel="noopener">LinkedIn</a>
      <a href="assets/Muhammad-Afzal-Kalwar-CV.pdf" download>CV</a>
      <a href="assets/Muhammad-Afzal-Kalwar-Services.pdf" download>Services PDF</a>
      <a href="mailto:kalwarmuhammadafzal3@gmail.com">Email</a>
      <a href="https://wa.me/923079670503" target="_blank" rel="noopener">WhatsApp</a>
    </div>`
  );
}

for (const [file, meta] of Object.entries(pages)) {
  const full = path.join(root, file);
  if (!fs.existsSync(full)) {
    console.warn("missing", file);
    continue;
  }
  let html = fs.readFileSync(full, "utf8");
  html = replaceHead(html, meta);
  html = replaceNav(html, meta.active);
  html = replaceBg(html);
  html = deferScripts(html);
  html = enrichFooter(html);
  if (file === "index.html" && !html.includes("application/ld+json")) {
    html = html.replace("</head>", `${indexSchema}\n</head>`);
  }
  if (file === "index.html") {
    html = html.replace(
      /<img class="hero-photo"[^>]*>/,
      '<img class="hero-photo" src="assets/profile.png" alt="Muhammad Afzal Kalwar" width="120" height="120" fetchpriority="high" decoding="async" />'
    );
  }
  fs.writeFileSync(full, html);
  console.log("updated", file);
}

console.log("done");
