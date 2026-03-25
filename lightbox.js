(function () {
  var overlay, img, closeBtn;

  function buildOverlay() {
    overlay = document.createElement('div');
    overlay.className = 'lightbox-overlay';

    closeBtn = document.createElement('button');
    closeBtn.className = 'lightbox-close';
    closeBtn.setAttribute('aria-label', 'Close image');
    closeBtn.textContent = '×';

    img = document.createElement('img');

    overlay.appendChild(closeBtn);
    overlay.appendChild(img);
    document.body.appendChild(overlay);

    overlay.addEventListener('click', function (e) {
      if (e.target !== img) close();
    });
    closeBtn.addEventListener('click', close);
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') close();
    });
  }

  function open(src, alt) {
    if (!overlay) buildOverlay();
    img.src = src;
    img.alt = alt || '';
    overlay.style.display = 'flex';
    requestAnimationFrame(function () {
      overlay.classList.add('is-visible');
    });
    document.body.style.overflow = 'hidden';
  }

  function close() {
    overlay.classList.remove('is-visible');
    document.body.style.overflow = '';
    overlay.addEventListener('transitionend', function hide() {
      overlay.style.display = 'none';
      overlay.removeEventListener('transitionend', hide);
    });
  }

  document.addEventListener('click', function (e) {
    var target = e.target;
    if (
      target.tagName === 'IMG' &&
      !target.closest('.card') &&
      target.closest('main')
    ) {
      open(target.src, target.alt);
    }
  });
})();
