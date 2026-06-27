(function () {
  'use strict';

  const CV_PATH = window.SITE?.cvPath || 'assets/Muhammad-Afzal-Kalwar-CV.pdf';
  const CV_NAME = window.SITE?.cvFilename || 'Muhammad-Afzal-Kalwar-CV.pdf';

  document.querySelectorAll('a[download*="CV"], a.nav-cv, a.btn-cv').forEach((link) => {
    if (!link.href.includes('.pdf')) {
      link.href = CV_PATH;
    }
    link.setAttribute('download', CV_NAME);
    link.addEventListener('click', (e) => {
      if (link.origin !== window.location.origin && !link.href.startsWith(window.location.origin)) return;
      if (!link.href.endsWith('.pdf')) {
        e.preventDefault();
        const a = document.createElement('a');
        a.href = CV_PATH;
        a.download = CV_NAME;
        a.rel = 'noopener';
        document.body.appendChild(a);
        a.click();
        a.remove();
      }
    });
  });
})();
