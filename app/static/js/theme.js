// Dark-mode toggle, persisted client-side for now (Stage 1). Once auth
// exists (Stage 2+), this is a natural place to also sync the choice to
// the signed-in user's account server-side.
(function () {
  const STORAGE_KEY = 'agrivision-theme';
  const root = document.documentElement;

  function applyTheme(theme) {
    root.setAttribute('data-theme', theme);
  }

  document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.getElementById('dark-mode-toggle');
    if (!toggle) return;

    toggle.checked = root.getAttribute('data-theme') === 'dark';

    toggle.addEventListener('change', () => {
      const theme = toggle.checked ? 'dark' : 'light';
      applyTheme(theme);
      localStorage.setItem(STORAGE_KEY, theme);
    });
  });
})();
