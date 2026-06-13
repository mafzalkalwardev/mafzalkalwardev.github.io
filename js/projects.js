(function () {
  'use strict';
  const buttons = document.querySelectorAll('.filter-btn');
  const cards = document.querySelectorAll('.project-card-full');

  buttons.forEach((btn) => {
    btn.addEventListener('click', () => {
      buttons.forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      const filter = btn.dataset.filter;
      cards.forEach((card) => {
        const cats = card.dataset.category || '';
        const show = filter === 'all' || cats.includes(filter);
        card.classList.toggle('hidden', !show);
        if (show) {
          card.style.animation = 'none';
          card.offsetHeight;
          card.style.animation = '';
        }
      });
    });
  });
})();
