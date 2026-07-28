"use strict";

(() => {   

    // ==========================
    // DARK MODE TOGGLE
    // ==========================

    const themeToggles = document.querySelectorAll(".dark-mode-toggle");
    const icons = document.querySelectorAll(".dark-mode-toggle img");

    const savedTheme = localStorage.getItem("theme");


    if (savedTheme === "dark") {

        document.documentElement.setAttribute("data-theme", "dark");

        icons.forEach(icon => {
            icon.src = "/static/images/sun.png";
        });

    } else {

        document.documentElement.setAttribute("data-theme", "light");

        icons.forEach(icon => {
            icon.src = "/static/images/moon.png";
        });

    }


    themeToggles.forEach(toggle => {

        toggle.addEventListener("click", () => {

            const currentTheme = document.documentElement.getAttribute("data-theme");


            if (currentTheme === "dark") {

                document.documentElement.setAttribute("data-theme", "light");

                localStorage.setItem("theme", "light");

                icons.forEach(icon => {
                    icon.src = "/static/images/moon.png";
                });

            } else {

                document.documentElement.setAttribute("data-theme", "dark");

                localStorage.setItem("theme", "dark");

                icons.forEach(icon => {
                    icon.src = "/static/images/sun.png";
                });

            }

        });

    });

    // ==========================
    // HAMBURGER MENU
    // ==========================

    const hamburger = document.querySelector(".hamburger");
    const mobileMenu = document.querySelector(".mobile-menu");
    const menuOverlay = document.querySelector(".menu-overlay");

    // Variable to store the scroll position when the menu is opened.
    let scrollPosition = 0;

    function setMenuOpen(isOpen) {

        mobileMenu.classList.toggle("open", isOpen);
        menuOverlay.classList.toggle("active", isOpen);
        document.body.classList.toggle("menu-open", isOpen);

        // Prevent background scrolling when the menu is open.
        if (isOpen) {
            scrollPosition = window.scrollY;
            document.body.style.top = `-${scrollPosition}px`;
        } else {
            document.body.style.top = "";
            window.scrollTo(0, scrollPosition);
        }

        // Update ARIA attributes for accessibility.
        hamburger.setAttribute("aria-label", isOpen ? "Close menu" : "Open menu");
        hamburger.setAttribute("aria-pressed", String(isOpen));
        mobileMenu.setAttribute("aria-hidden", String(!isOpen));
        hamburger.setAttribute("aria-expanded", String(isOpen));
        menuOverlay.setAttribute("aria-hidden", String(!isOpen));

    }

    if (hamburger && mobileMenu && menuOverlay) {

        // Toggle the menu open/closed when the hamburger icon is clicked.
        hamburger.addEventListener("click", () => {
            setMenuOpen(!mobileMenu.classList.contains("open"));
        });

        // Close the menu when clicking outside of it (menu overlay).
        menuOverlay.addEventListener("click", () => {
            setMenuOpen(false);
        });

        // Close the menu when pressing the Escape key.
        document.addEventListener("keydown", (event) => {
            if (event.key === "Escape" && mobileMenu.classList.contains("open")) {
                setMenuOpen(false);
            }
        });

        // Close the menu when clicking on any link inside it.
        mobileMenu.querySelectorAll("a").forEach((link) => {
            link.addEventListener("click", () => {
                setMenuOpen(false);
            });
        });

    }

})();