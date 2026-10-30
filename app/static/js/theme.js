// Dark/Light theme toggle with localStorage persistence
(function () {
  const STORAGE_KEY = 'agrivision-theme';
  const root = document.documentElement;

  function applyTheme(theme) {
    root.setAttribute('data-theme', theme);
    try {
      localStorage.setItem(STORAGE_KEY, theme);
    } catch (e) {}
    updateButtons(theme);
  }

  function updateButtons(theme) {
    const isDark = theme === 'dark';
    document.querySelectorAll('.theme-toggle-btn').forEach(btn => {
      btn.textContent = isDark ? 'Light' : 'Dark';
      btn.setAttribute('title', isDark ? 'Switch to light theme' : 'Switch to dark theme');
    });
  }

  window.toggleAppTheme = function () {
    const current = root.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
    const next = current === 'dark' ? 'light' : 'dark';
    applyTheme(next);
  };

  document.addEventListener('DOMContentLoaded', () => {
    const saved = localStorage.getItem(STORAGE_KEY);
    const current = saved || root.getAttribute('data-theme') || 'light';
    applyTheme(current);
  });
})();
