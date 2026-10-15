// Mobile menu
(function () {
  var menu = document.getElementById('mobile-menu');
  var open = document.querySelector('.menu-toggle');
  if (!menu || !open) return;
  var close = menu.querySelector('.close-btn');
  function setOpen(state) {
    menu.hidden = !state;
    open.setAttribute('aria-expanded', String(state));
    document.body.style.overflow = state ? 'hidden' : '';
    (state ? close : open).focus();
  }
  open.addEventListener('click', function () { setOpen(true); });
  close.addEventListener('click', function () { setOpen(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !menu.hidden) setOpen(false); });
  menu.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', function () { setOpen(false); }); });
})();

// Click-to-play YouTube: swaps the thumbnail for the player only when clicked
document.querySelectorAll('.yt[data-id]').forEach(function (btn) {
  btn.addEventListener('click', function () {
    var id = btn.getAttribute('data-id');
    var start = btn.getAttribute('data-start');
    var iframe = document.createElement('iframe');
    iframe.src = 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0' + (start ? '&start=' + start : '');
    iframe.title = btn.getAttribute('aria-label') || 'YouTube video';
    iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
    iframe.allowFullscreen = true;
    btn.replaceChildren(iframe);
    btn.style.cursor = 'default';
  }, { once: true });
});

// Booking form: replace with your existing form handler (e.g. Contact Form 7)
var form = document.getElementById('booking-form');
if (form) {
  form.addEventListener('submit', function (e) {
    if (!form.getAttribute('action') || form.getAttribute('action') === '#') {
      e.preventDefault();
      var note = document.getElementById('form-status');
      if (note) note.textContent = 'Form not yet connected. Please email rahilfoundbylove@gmail.com.';
    }
  });
}
