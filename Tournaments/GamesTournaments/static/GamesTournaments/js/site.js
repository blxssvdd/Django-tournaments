document.addEventListener("DOMContentLoaded", () => {
    const currentPath = window.location.pathname;

    document.querySelectorAll("[data-nav-match]").forEach((link) => {
        const pattern = link.dataset.navMatch;
        if (currentPath.startsWith(pattern)) {
            link.classList.add("active");
        }
    });

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
