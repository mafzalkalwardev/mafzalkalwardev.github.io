(function () {
  'use strict';
  const form = document.getElementById('contactForm');
  if (!form) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const data = new FormData(form);
    const name = data.get('name');
    const email = data.get('email');
    const type = data.get('type');
    const message = data.get('message');
    const subject = encodeURIComponent(`Project inquiry: ${type} — from ${name}`);
    const body = encodeURIComponent(`Hi Muhammad,\n\n${message}\n\n— ${name}\n${email}`);
    window.location.href = `mailto:kalwarmuhammadafzal3@gmail.com?subject=${subject}&body=${body}`;
  });
})();
