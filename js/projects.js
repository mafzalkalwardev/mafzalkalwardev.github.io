(function () {
  'use strict';

  function fixText(str) {
    if (!str) return '';
    return str
      .replace(/\u00e2\u20ac\u201d/g, '—')
      .replace(/\u00e2\u20ac\u201c/g, '"')
      .replace(/\u00e2\u20ac\u2122/g, "'")
      .replace(/â€"/g, '—')
      .replace(/â€"/g, '"');
  }

  function escapeHtml(str) {
    const d = document.createElement('div');
    d.textContent = str;
    return d.innerHTML;
  }

  function projectCard(project, index) {
    const delay = index % 3 === 1 ? ' delay-1' : index % 3 === 2 ? ' delay-2' : '';
    const tags = (project.tags || [])
      .map((t) => `<span class="tag">${escapeHtml(t)}</span>`)
      .join('');
    const desc = escapeHtml(fixText(project.description));
    const name = escapeHtml(project.name);
    const url = escapeHtml(project.url);
    const img = escapeHtml(project.image);
    const video = project.video ? escapeHtml(project.video) : '';
    const category = escapeHtml(project.category || '');
    const media = video
      ? `<video class="project-video" src="${video}" muted loop playsinline preload="metadata" poster="${img}"></video>
         <img src="${img}" alt="${name} screenshot" loading="lazy" width="640" height="400" />`
      : `<img src="${img}" alt="${name} screenshot" loading="lazy" width="640" height="400" />`;

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
            <a href="${url}" target="_blank" rel="noopener">View on GitHub</a>
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
