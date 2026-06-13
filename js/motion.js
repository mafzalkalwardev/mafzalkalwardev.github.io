(function () {
  'use strict';

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ── Hero title word stagger ── */
  function initHeroWords() {
    const h1 = document.querySelector('.hero-content h1[data-split]');
    if (!h1 || reducedMotion) return;
    const text = h1.textContent.trim();
    const words = text.split(/\s+/);
    h1.innerHTML = words
      .map((w, i) => `<span class="hero-word" style="animation-delay:${0.15 + i * 0.08}s">${w}</span>`)
      .join(' ');
  }

  /* ── Counter animation ── */
  function initCounters() {
    document.querySelectorAll('[data-count]').forEach((el) => {
      const target = parseInt(el.dataset.count, 10);
      if (Number.isNaN(target)) return;
      const suffix = el.dataset.suffix || '';
      const obs = new IntersectionObserver(
        (entries) => {
          entries.forEach((e) => {
            if (!e.isIntersecting) return;
            if (reducedMotion) {
              el.textContent = target + suffix;
              obs.unobserve(el);
              return;
            }
            const duration = 1600;
            const start = performance.now();
            function step(now) {
              const p = Math.min((now - start) / duration, 1);
              const eased = 1 - Math.pow(1 - p, 4);
              el.textContent = Math.floor(eased * target) + suffix;
              if (p < 1) requestAnimationFrame(step);
              else el.textContent = target + suffix;
            }
            requestAnimationFrame(step);
            obs.unobserve(el);
          });
        },
        { threshold: 0.4 }
      );
      obs.observe(el);
    });
  }

  /* ── Scroll reveal ── */
  function initReveal(els) {
    const targets = els || document.querySelectorAll('.reveal, .reveal-left, .reveal-scale, .stagger-grid');
    const obs = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add('visible');
            obs.unobserve(e.target);
          }
        });
      },
      { threshold: 0.06, rootMargin: '0px 0px -48px 0px' }
    );
    targets.forEach((el) => obs.observe(el));
  }
  window.initReveal = initReveal;

  /* ── Parallax background ── */
  function initParallax() {
    const mesh = document.querySelector('.bg-mesh-inner');
    if (!mesh || reducedMotion) return;
    let ticking = false;
    window.addEventListener(
      'scroll',
      () => {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(() => {
          const y = window.scrollY * 0.15;
          mesh.style.transform = `translateY(${y}px)`;
          ticking = false;
        });
      },
      { passive: true }
    );
  }

  /* ── Subtle 3D tilt on cards ── */
  function initTilt(selector, maxDeg) {
    if (reducedMotion || window.innerWidth < 768) return;
    document.querySelectorAll(selector).forEach((card) => {
      if (card.dataset.tiltBound) return;
      card.dataset.tiltBound = '1';
      card.addEventListener('mousemove', (e) => {
        const r = card.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width - 0.5;
        const y = (e.clientY - r.top) / r.height - 0.5;
        card.style.transform = `perspective(800px) rotateY(${x * maxDeg}deg) rotateX(${-y * maxDeg}deg) translateY(-4px)`;
        card.style.boxShadow = '0 20px 40px rgba(15, 23, 42, 0.1)';
      });
      card.addEventListener('mouseleave', () => {
        card.style.transform = '';
        card.style.boxShadow = '';
      });
    });
  }
  window.initTilt = initTilt;

  /* ── Magnetic buttons ── */
  function initMagneticButtons() {
    if (reducedMotion || window.innerWidth < 768) return;
    document.querySelectorAll('.btn-primary').forEach((btn) => {
      btn.addEventListener('mousemove', (e) => {
        const r = btn.getBoundingClientRect();
        const x = e.clientX - r.left - r.width / 2;
        const y = e.clientY - r.top - r.height / 2;
        btn.style.transform = `translate(${x * 0.12}px, ${y * 0.12}px) translateY(-2px)`;
      });
      btn.addEventListener('mouseleave', () => {
        btn.style.transform = '';
      });
    });
  }

  /* ── Nav scroll state ── */
  function initNav() {
    const nav = document.getElementById('nav');
    const toggle = document.getElementById('navToggle');
    const links = document.getElementById('navLinks');
    if (!nav) return;

    window.addEventListener(
      'scroll',
      () => nav.classList.toggle('scrolled', window.scrollY > 12),
      { passive: true }
    );

    if (toggle && links) {
      toggle.addEventListener('click', () => links.classList.toggle('open'));
      links.querySelectorAll('a').forEach((a) => {
        a.addEventListener('click', () => links.classList.remove('open'));
      });
    }
  }

  /* ── Year ── */
  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* ── Skill bars ── */
  function initSkillBars() {
    document.querySelectorAll('.skill-fill[data-width]').forEach((fill) => {
      const obs = new IntersectionObserver(
        (entries) => {
          entries.forEach((e) => {
            if (!e.isIntersecting) return;
            fill.style.width = fill.dataset.width + '%';
            obs.unobserve(fill);
          });
        },
        { threshold: 0.3 }
      );
      obs.observe(fill);
    });
  }

  /* ── Featured projects ── */
  function initFeatured() {
    const el = document.getElementById('featuredProjects');
    if (!el || !window.PORTFOLIO_PROJECTS || typeof window.renderProjectCard !== 'function') return;
    const featured = window.PORTFOLIO_PROJECTS.filter((p) => p.featured).slice(0, 6);
    el.innerHTML = featured.map((p, i) => window.renderProjectCard(p, i)).join('');
    el.classList.add('stagger-grid');
    initReveal([el]);
    initTilt('#featuredProjects .project-card', 4);
  }

  /* ── Boot ── */
  initNav();
  initHeroWords();
  initCounters();
  initReveal();
  initParallax();
  initMagneticButtons();
  initSkillBars();
  initFeatured();
  initTilt('.service-card', 3);
  initTilt('.bento-card', 2.5);
})();
