document.addEventListener('DOMContentLoaded', function() {
    const htmlTag = document.documentElement;
    const toggleButton = document.getElementById('toggleTheme');
    const icon = toggleButton.querySelector('i');

    // Check for saved theme preference
    const savedTheme = localStorage.getItem('theme') || 'light';
    applyTheme(savedTheme);

    // Toggle theme on button click
    toggleButton.addEventListener('click', function() {
        const currentTheme = htmlTag.getAttribute('data-bs-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        applyTheme(newTheme);
        localStorage.setItem('theme', newTheme);
    });

    function applyTheme(theme) {
        htmlTag.setAttribute('data-bs-theme', theme);
        
        // Update button icon
        if (icon) {
            icon.className = theme === 'light' ? 'bi bi-moon-stars' : 'bi bi-sun';
        }

        // Update button text
        toggleButton.innerHTML = `<i class="${icon.className}"></i> ${theme === 'light' ? 'Dark' : 'Light'} Mode`;

        // Apply additional theme-specific styles
        document.body.classList.toggle('dark-mode', theme === 'dark');
    }
}); 