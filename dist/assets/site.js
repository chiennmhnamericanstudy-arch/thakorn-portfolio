document.documentElement.classList.add('js');
const toggle = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#main-nav');
function closeNavigation(returnFocus = false) {
  if (!toggle || !navigation) return;
  toggle.setAttribute('aria-expanded', 'false');
  toggle.setAttribute('aria-label', 'Open navigation');
  navigation.classList.remove('open');
  if (returnFocus) toggle.focus();
}
if (toggle && navigation) {
  toggle.addEventListener('click', () => {
    const opening = toggle.getAttribute('aria-expanded') !== 'true';
    toggle.setAttribute('aria-expanded', String(opening));
    toggle.setAttribute('aria-label', opening ? 'Close navigation' : 'Open navigation');
    navigation.classList.toggle('open', opening);
  });
  navigation.addEventListener('click', event => {
    if (event.target.closest('a')) closeNavigation();
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') closeNavigation(true);
  });
  document.addEventListener('pointerdown', event => {
    if (toggle.getAttribute('aria-expanded') === 'true' &&
        !navigation.contains(event.target) && !toggle.contains(event.target)) {
      closeNavigation();
    }
  });
  window.matchMedia('(min-width: 1241px)').addEventListener('change', event => {
    if (event.matches) closeNavigation();
  });
}

// Keep previously shared category links useful after splitting the collections.
if (window.location.pathname.replace(/\/$/, '') === '/projects' &&
    ['#community-impact', '#entrepreneurship'].includes(window.location.hash)) {
  window.location.replace('/initiatives-impact/' + window.location.search + window.location.hash);
}
