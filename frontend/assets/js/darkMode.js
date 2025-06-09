function initializeDarkMode() {
    const toggleButton = document.getElementById("darkModeToggle");
    const body = document.body;
    const header = document.querySelector(".header");

    if (localStorage.getItem("theme") === "dark") {
        body.classList.add("dark-mode");
        if (header) header.classList.add("dark-mode");
        toggleButton.textContent = "☀️";
    }

    toggleButton.addEventListener("click", () => {
        body.classList.toggle("dark-mode");
        if (header) header.classList.toggle("dark-mode");
        const isDark = body.classList.contains("dark-mode");
        localStorage.setItem("theme", isDark ? "dark" : "light");
        toggleButton.textContent = isDark ? "☀️" : "🌙";
    });
}

document.addEventListener('DOMContentLoaded', initializeDarkMode); 