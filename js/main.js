(function () {
  'use strict';

  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // Nav scroll + mobile toggle
  const nav = document.getElementById('nav');
  const navToggle = document.getElementById('navToggle');
  const navLinks = document.getElementById('navLinks');

  window.addEventListener('scroll', () => {
    if (nav) nav.classList.toggle('scrolled', window.scrollY > 40);
  });

  if (navToggle && navLinks) {
    navToggle.addEventListener('click', () => navLinks.classList.toggle('open'));
    navLinks.querySelectorAll('a').forEach((a) => {
      a.addEventListener('click', () => navLinks.classList.remove('open'));
    });
  }

  // Scroll reveal
  const revealEls = document.querySelectorAll('.reveal');
  const revealObs = new IntersectionObserver(
    (entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) {
          e.target.classList.add('visible');
          revealObs.unobserve(e.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
  );
  revealEls.forEach((el) => revealObs.observe(el));

  // Typing effect (home page)
  const typingEl = document.getElementById('typing');
  if (typingEl) {
    const phrases = [
      'Full-Stack Developer',
      'Python Engineer',
      'Automation Specialist',
      'Open Source Builder',
      'Available for Hire',
    ];
    let pi = 0;
    let ci = 0;
    let deleting = false;

    function tick() {
      const phrase = phrases[pi];
      if (!deleting) {
        typingEl.textContent = phrase.slice(0, ++ci);
        if (ci === phrase.length) {
          deleting = true;
          setTimeout(tick, 2000);
          return;
        }
      } else {
        typingEl.textContent = phrase.slice(0, --ci);
        if (ci === 0) {
          deleting = false;
          pi = (pi + 1) % phrases.length;
        }
      }
      setTimeout(tick, deleting ? 40 : 80);
    }
    tick();
  }

  // Counter animation
  const statNums = document.querySelectorAll('.stat-num[data-count]');
  const countObs = new IntersectionObserver(
    (entries) => {
      entries.forEach((e) => {
        if (!e.isIntersecting) return;
        const el = e.target;
        const target = parseInt(el.dataset.count, 10);
        const duration = 1500;
        const start = performance.now();
        function step(now) {
          const p = Math.min((now - start) / duration, 1);
          const eased = 1 - Math.pow(1 - p, 3);
          el.textContent = Math.floor(eased * target);
          if (p < 1) requestAnimationFrame(step);
          else el.textContent = target;
        }
        requestAnimationFrame(step);
        countObs.unobserve(el);
      });
    },
    { threshold: 0.5 }
  );
  statNums.forEach((el) => countObs.observe(el));

  // Skill bars
  const skillFills = document.querySelectorAll('.skill-fill[data-width]');
  const skillObs = new IntersectionObserver(
    (entries) => {
      entries.forEach((e) => {
        if (!e.isIntersecting) return;
        const fill = e.target;
        fill.style.setProperty('--w', fill.dataset.width + '%');
        fill.classList.add('animated');
        fill.style.width = fill.dataset.width + '%';
        skillObs.unobserve(fill);
      });
    },
    { threshold: 0.3 }
  );
  skillFills.forEach((el) => skillObs.observe(el));

  // Page transition on internal links
  document.querySelectorAll('a[href]').forEach((a) => {
    const href = a.getAttribute('href');
    if (!href || href.startsWith('http') || href.startsWith('mailto') || href.startsWith('#')) return;
    a.addEventListener('click', (ev) => {
      if (ev.metaKey || ev.ctrlKey) return;
      ev.preventDefault();
      document.body.style.opacity = '0';
      document.body.style.transition = 'opacity 0.25s';
      setTimeout(() => { window.location.href = href; }, 200);
    });
  });
})();
