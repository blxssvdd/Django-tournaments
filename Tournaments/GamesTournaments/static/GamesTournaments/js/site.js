document.addEventListener("DOMContentLoaded", () => {
    const currentPath = window.location.pathname;
    const THEME_KEY = "arena-theme";

    document.querySelectorAll("[data-nav-match]").forEach((link) => {
        const pattern = link.dataset.navMatch;
        if (currentPath.startsWith(pattern)) {
            link.classList.add("active");
        }
    });

    const applyTheme = (theme) => {
        const root = document.documentElement;
        root.setAttribute("data-theme", theme);
        const toggleIcon = document.querySelector(".theme-toggle__icon");
        if (toggleIcon) {
            toggleIcon.textContent = theme === "light" ? "☀️" : "🌙";
        }
    };

    const savedTheme = localStorage.getItem(THEME_KEY) || "dark";
    applyTheme(savedTheme);

    const toggleButton = document.getElementById("themeToggle");
    if (toggleButton) {
        toggleButton.addEventListener("click", () => {
            const current = document.documentElement.getAttribute("data-theme") === "light" ? "light" : "dark";
            const next = current === "light" ? "dark" : "light";
            localStorage.setItem(THEME_KEY, next);
            applyTheme(next);
        });
    }

    const alerts = document.querySelectorAll(".message-alert");
    alerts.forEach((alert, index) => {
        const delay = 4000 + index * 600;
        setTimeout(() => {
            alert.classList.add("fade-out");
            alert.addEventListener("transitionend", () => {
                alert.remove();
            }, { once: true });
        }, delay);
    });

    const cards = document.querySelectorAll(".tournament-card, .registration-card");
    cards.forEach((card) => {
        card.addEventListener("mousemove", (event) => {
            const rect = card.getBoundingClientRect();
            const x = event.clientX - rect.left;
            const y = event.clientY - rect.top;
            card.style.setProperty("--mouse-x", `${x}px`);
            card.style.setProperty("--mouse-y", `${y}px`);
        });
        card.addEventListener("mouseleave", () => {
            card.style.removeProperty("--mouse-x");
            card.style.removeProperty("--mouse-y");
        });
    });
});
