(function () {
  'use strict';

  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  const nav = document.getElementById('nav');
  const navToggle = document.getElementById('navToggle');
  const navLinks = document.getElementById('navLinks');

  window.addEventListener('scroll', () => {
    if (nav) nav.classList.toggle('scrolled', window.scrollY > 8);
  });

  if (navToggle && navLinks) {
    navToggle.addEventListener('click', () => navLinks.classList.toggle('open'));
    navLinks.querySelectorAll('a').forEach((a) => {
      a.addEventListener('click', () => navLinks.classList.remove('open'));
    });
  }

  function initReveal(els) {
    const revealEls = els || document.querySelectorAll('.reveal');
    const revealObs = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add('visible');
            revealObs.unobserve(e.target);
          }
        });
      },
      { threshold: 0.08, rootMargin: '0px 0px -32px 0px' }
    );
    revealEls.forEach((el) => revealObs.observe(el));
  }
  window.initReveal = initReveal;
  initReveal();

  const skillFills = document.querySelectorAll('.skill-fill[data-width]');
  const skillObs = new IntersectionObserver(
    (entries) => {
      entries.forEach((e) => {
        if (!e.isIntersecting) return;
        e.target.style.width = e.target.dataset.width + '%';
        skillObs.unobserve(e.target);
      });
    },
    { threshold: 0.3 }
  );
  skillFills.forEach((el) => skillObs.observe(el));

  const featuredEl = document.getElementById('featuredProjects');
  if (featuredEl && window.PORTFOLIO_PROJECTS && typeof window.renderProjectCard === 'function') {
    const featured = window.PORTFOLIO_PROJECTS.filter((p) => p.featured).slice(0, 6);
    featuredEl.innerHTML = featured.map((p, i) => window.renderProjectCard(p, i)).join('');
    initReveal(featuredEl.querySelectorAll('.reveal'));
  }
})();
