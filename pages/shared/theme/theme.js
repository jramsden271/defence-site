// Wires up the header's dark/light theme toggle button. The initial theme
// itself is already set on <html data-theme="..."> by the inline init
// script in <head> (before this file even loads) — this just handles clicks.

function setThemeIcon(button, theme) {
    button.textContent = theme === 'dark' ? '☀️' : '🌙';
    button.setAttribute('aria-label', theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
}

document.addEventListener('DOMContentLoaded', function () {
    const toggle = document.getElementById('themeToggle');
    if (!toggle) return;

    setThemeIcon(toggle, document.documentElement.getAttribute('data-theme'));

    toggle.addEventListener('click', function () {
        const current = document.documentElement.getAttribute('data-theme');
        const next = current === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', next);
        localStorage.setItem('theme', next);
        setThemeIcon(toggle, next);
    });
});
