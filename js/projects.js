(function () {
  'use strict';

  if (window.PORTFOLIO_PROJECTS) {
    const total = window.PORTFOLIO_PROJECTS.length;
    document.querySelectorAll('[data-project-count]').forEach((el) => {
      el.dataset.count = String(total);
    });
    document.querySelectorAll('[data-project-total]').forEach((el) => {
      el.textContent = String(total);
    });
    const viewAll = document.getElementById('viewAllProjectsLink');
    if (viewAll) viewAll.textContent = `View all ${total} projects`;
    const subtitle = document.getElementById('projectsPageCount');
    if (subtitle) {
      subtitle.textContent = `${total} curated portfolio projects`;
    }
  }

  function fixText(str) {
    if (!str) return '';
    return str
      .replace(/\u00e2\u20ac\u201d/g, '-')
      .replace(/\u00e2\u20ac\u201c/g, '"')
      .replace(/\u00e2\u20ac\u2122/g, "'");
  }

  function escapeHtml(str) {
    const d = document.createElement('div');
    d.textContent = str;
    return d.innerHTML;
  }

  const SERVICE_LINKS = {
    "gv-auto-dialer-chrome-extension": ["services/auto-dialer-development.html", "Auto dialer development"],
    "ipecs-auto-dialer": ["services/auto-dialer-development.html", "Auto dialer development"],
    "indus-transport-auto-dialer": ["services/auto-dialer-development.html", "Auto dialer development"],
    "python-auto-dialer-pro": ["services/auto-dialer-development.html", "Auto dialer development"],
    "excel-call-queue-automator": ["services/auto-dialer-development.html", "Auto dialer development"],
    "google-voice-dispatch-agent": ["services/ai-call-agent-development.html", "AI call agent development"],
    "CallAudit-X": ["services/ai-call-agent-development.html", "AI call agent development"],
    "google-voice-call-state-detector": ["services/ai-call-agent-development.html", "AI call agent development"],
    "google-voice-call-detector-prototype": ["services/ai-call-agent-development.html", "AI call agent development"],
    "fiverr-lead-extractor-crm": ["services/web-scraping-services.html", "Web scraping"],
    "fmcsa-safer-scraper": ["services/web-scraping-services.html", "Web scraping"],
    "safer-web-scraper": ["services/web-scraping-services.html", "Web scraping"],
    "indus-carrier-directory": ["services/web-scraping-services.html", "Web scraping"],
    "playwright-website-scraper-pro": ["services/web-scraping-services.html", "Web scraping"],
    "pdf-mc-number-extractor": ["services/web-scraping-services.html", "Web scraping"],
    "Canadian-Website-Scraper": ["services/web-scraping-services.html", "Web scraping"],
    "bulk-email-verifier": ["services/email-verification-tools.html", "Email verification"],
    "mailforge": ["services/email-verification-tools.html", "Email verification"],
    "email-verification-platform": ["services/email-verification-tools.html", "Email verification"],
    "multi-smtp-email-automation": ["services/email-verification-tools.html", "Email verification"],
    "python-smtp-email-automation": ["services/email-verification-tools.html", "Email verification"],
    "forward-email-automation": ["services/email-verification-tools.html", "Email verification"],
    "google-workspace-bulk-user-provisioning": ["services/python-automation-services.html", "Python automation"],
    "excel-mc-data-cleaner": ["services/python-automation-services.html", "Python automation"],
    "python-sms-automation": ["services/python-automation-services.html", "Python automation"],
  };

  function serviceLink(project) {
    const hit = SERVICE_LINKS[project.repo] || ["services/", "Automation services"];
    return `<a href="${hit[0]}">Service: ${escapeHtml(hit[1])}</a>`;
  }

  function projectCard(project, index) {
    const delay = index % 3 === 1 ? ' delay-1' : index % 3 === 2 ? ' delay-2' : '';
    const tags = (project.tags || [])
      .map((t) => `<span class="tag">${escapeHtml(t)}</span>`)
      .join('');
    const desc = escapeHtml(fixText(project.description));
    const name = escapeHtml(project.name);
    const url = escapeHtml(project.url);
    const live = project.live ? escapeHtml(project.live) : '';
    const coverSrc = project.cover || project.image;
    const img = escapeHtml(coverSrc);
    const screenshot = escapeHtml(project.image || coverSrc);
    const video = project.video ? escapeHtml(project.video) : '';
    const category = escapeHtml(project.category || '');
    const fallback =
      "data:image/svg+xml," +
      encodeURIComponent(
        `<svg xmlns="http://www.w3.org/2000/svg" width="640" height="400"><rect width="640" height="400" fill="#0B1F3A"/><text x="320" y="200" text-anchor="middle" fill="#F5A623" font-family="Segoe UI,Arial" font-size="22">${name.replace(/[<>&]/g, "")}</text></svg>`
      );
    const imgTag = `<img src="${img}" alt="${name} cover thumbnail" loading="lazy" width="640" height="400" onerror="this.onerror=null;this.src='${fallback}'" />`;
    const media = video
      ? `<video class="project-video" src="${video}" muted loop playsinline preload="metadata" poster="${img}"></video>
         ${imgTag}`
      : imgTag;

    return `
      <article class="project-card reveal${delay}" data-category="${category}"${video ? ' data-has-video="true"' : ''}>
        <div class="project-shot">
          ${media}
        </div>
        <div class="project-body">
          <h3>${name}</h3>
          <p>${desc}</p>
          <div class="tags">${tags}</div>
          <div class="project-links">
            ${live ? `<a href="${live}" target="_blank" rel="noopener">Live site</a>` : ''}
            <a href="${url}" target="_blank" rel="noopener">View on GitHub</a>
            ${serviceLink(project)}
          </div>
        </div>
      </article>`;
  }

  window.renderProjectCard = projectCard;
  window.fixProjectText = fixText;

  const grid = document.getElementById('projectsGrid');
  if (!grid || !window.PORTFOLIO_PROJECTS) return;

  const projects = window.PORTFOLIO_PROJECTS.slice().sort((a, b) => {
    if (a.featured && !b.featured) return -1;
    if (!a.featured && b.featured) return 1;
    return a.name.localeCompare(b.name);
  });

  grid.innerHTML = projects.map(projectCard).join('');

  grid.querySelectorAll('[data-has-video="true"]').forEach((card) => {
    const video = card.querySelector('.project-video');
    if (!video) return;
    card.addEventListener('mouseenter', () => { video.play().catch(() => {}); });
    card.addEventListener('mouseleave', () => { video.pause(); video.currentTime = 0; });
  });

  if (window.initTilt) window.initTilt('#projectsGrid .project-card', 4);
  if (window.initReveal) {
    window.initReveal(grid.querySelectorAll('.reveal'));
    grid.classList.add('stagger-grid');
    window.initReveal([grid]);
  }

  const buttons = document.querySelectorAll('.filter-btn');
  buttons.forEach((btn) => {
    btn.addEventListener('click', () => {
      buttons.forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      const filter = btn.dataset.filter;
      grid.querySelectorAll('.project-card').forEach((card) => {
        const cat = card.dataset.category || '';
        const show = filter === 'all' || cat === filter;
        card.classList.toggle('hidden', !show);
      });
    });
  });
})();
