"use strict";

(() => {

    // Wrap everything in an IIFE to avoid leaking variables into the global scope.

    // ==========================
    // DARK MODE TOGGLE
    // ==========================

    const themeToggles = document.querySelectorAll(".dark-mode-toggle");
    const icons = document.querySelectorAll(".dark-mode-toggle img");

    // The inline script in <head> already sets data-theme before paint (FOUC fix).
    // This then syncs the toggle icon to whatever theme is currently active.
    function syncThemeIcon() {

        const isDark = document.documentElement.getAttribute("data-theme") === "dark";

        icons.forEach(icon => {
            icon.src = isDark ? "/static/images/sun.png" : "/static/images/moon.png";
        });

    }

    syncThemeIcon();

    themeToggles.forEach(toggle => {

        toggle.addEventListener("click", () => {

            const currentTheme = document.documentElement.getAttribute("data-theme");
            const newTheme = currentTheme === "dark" ? "light" : "dark";

            document.documentElement.setAttribute("data-theme", newTheme);
            localStorage.setItem("theme", newTheme);

            syncThemeIcon();

        });

    });


    // ==========================
    // HAMBURGER MENU
    // ==========================

    const hamburger = document.querySelector(".hamburger");
    const mobileMenu = document.querySelector(".mobile-menu");
    const menuOverlay = document.querySelector(".menu-overlay");

    let scrollPosition = 0;

    function setMenuOpen(isOpen) {

        mobileMenu.classList.toggle("open", isOpen);
        menuOverlay.classList.toggle("active", isOpen);
        document.body.classList.toggle("menu-open", isOpen);

        if (isOpen) {

            scrollPosition = window.scrollY;
            document.body.style.top = `-${scrollPosition}px`;

        } else {

            document.body.style.top = "";
            window.scrollTo(0, scrollPosition);

        }

        hamburger.setAttribute("aria-label", isOpen ? "Close menu" : "Open menu");
        hamburger.setAttribute("aria-pressed", String(isOpen));
        mobileMenu.setAttribute("aria-hidden", String(!isOpen));
        hamburger.setAttribute("aria-expanded", String(isOpen));
        menuOverlay.setAttribute("aria-hidden", String(!isOpen));

    }


    if (hamburger && mobileMenu && menuOverlay) {

        hamburger.addEventListener("click", () => {
            setMenuOpen(!mobileMenu.classList.contains("open"));
        });


        menuOverlay.addEventListener("click", () => {
            setMenuOpen(false);
        });


        document.addEventListener("keydown", (event) => {

            if (event.key === "Escape" && mobileMenu.classList.contains("open")) {
                setMenuOpen(false);
            }

        });


        mobileMenu.querySelectorAll("a").forEach(link => {

            link.addEventListener("click", () => {
                setMenuOpen(false);
            });

        });

    }


    // ====================================
    // SEARCH AUTOCOMPLETE & CLEAR BUTTON
    // ====================================

    const searchInput = document.getElementById("searchInput");
    const clearBtn = document.getElementById("clearBtn");
    const suggestions = document.getElementById("suggestions");

    let timeout;
    let latestQuery = "";


    function clearAutocomplete() {

        if (!suggestions) return;

        suggestions.innerHTML = "";
        suggestions.classList.remove("open");

    }


    if (searchInput && suggestions) {

        searchInput.addEventListener("input", () => {

            const query = searchInput.value.trim();
            latestQuery = query;

            clearBtn?.classList.toggle("visible", query !== "");

            clearAutocomplete();

            clearTimeout(timeout);


            if (query.length < 2) return;


            timeout = setTimeout(async () => {

                try {

                    const response = await fetch(
                        `/auto-complete/?q=${encodeURIComponent(query)}`
                    );


                    if (!response.ok) {
                        throw new Error("Autocomplete request failed");
                    }


                    const results = await response.json();

                    // Ignore outdated results
                    if (latestQuery !== query) return; 

                    const limitedResults = results.slice(0, 8);


                    limitedResults.forEach(title => {

                        const item = document.createElement("div");

                        item.className = "suggestion";
                        item.textContent = title;


                        item.addEventListener("click", () => {

                            searchInput.value = title;

                            clearAutocomplete();

                            clearBtn?.classList.add("visible");

                        });


                        suggestions.appendChild(item);

                    });


                    if (limitedResults.length > 0) {
                        suggestions.classList.add("open");
                    }


                } catch (error) {

                    console.error("Autocomplete error:", error);

                    clearAutocomplete();

                }


            }, 250);

        });


        clearBtn?.addEventListener("click", () => {

            searchInput.value = "";

            searchInput.focus();

            clearAutocomplete();

            clearBtn.classList.remove("visible");

        });


        searchInput.addEventListener("keydown", event => {

            if (event.key === "Escape") {

                // Prevent the default behavior of the Escape key, to close the dropdown first before clearing the input.
                event.preventDefault();

                const isOpen = suggestions.classList.contains("open");

                if (isOpen) {
                    clearAutocomplete();
                } else {

                    searchInput.value = "";

                    clearBtn?.classList.remove("visible");

                }
            }

        });

        // Close the autocomplete dropdown if the user clicks outside of the search input, suggestions, or clear button.
        document.addEventListener("click", event => {

            const clickedInsideSearch =
                searchInput?.contains(event.target) ||
                suggestions?.contains(event.target) ||
                clearBtn?.contains(event.target);

            if (!clickedInsideSearch) {
                clearAutocomplete();
            }

        });


        clearBtn?.classList.toggle(
            "visible",
            searchInput.value.trim() !== ""
        );

    }


    // ==========================
    // LOADING OVERLAY
    // ==========================


    document.querySelectorAll("a").forEach(link => {

        link.addEventListener("click", () => {


            // Ignore external links and anchor links
            if (
                link.hostname !== window.location.hostname ||
                link.pathname === window.location.pathname && link.hash
            ) {
                return;
            }


            const overlay = document.getElementById("loading-overlay");


            if (overlay) {
                overlay.classList.remove("hidden");
            }


        });

    });


    const searchForm = document.querySelector(".search-form");


    if (searchForm) {

        searchForm.addEventListener("submit", () => {

            const overlay = document.getElementById("loading-overlay");


            if (overlay) {
                overlay.classList.remove("hidden");
            }

        });

    }

    // ==========================
    // PASSWORD VISIBILITY TOGGLE
    // ==========================

    function setupPasswordToggle(toggleId, inputId, iconId) {

        const toggle = document.getElementById(toggleId);
        const passwordInput = document.getElementById(inputId);
        const eyeicon = document.getElementById(iconId);

        if (!toggle || !passwordInput || !eyeicon) {
            return;
        }

        const openIcon = toggle.dataset.open;
        const closedIcon = toggle.dataset.closed;

        toggle.addEventListener("click", () => {

            if (passwordInput.type === "password") {

                passwordInput.type = "text";

                eyeicon.src = closedIcon;

                toggle.setAttribute("aria-label", "Hide password");
                toggle.setAttribute("aria-pressed", "true");
                toggle.setAttribute("title", "true");

            } else {

                passwordInput.type = "password";

                eyeicon.src = openIcon;

                toggle.setAttribute("aria-label", "Show password");
                toggle.setAttribute("aria-pressed", "false");
                toggle.setAttribute("title", "false");

            }

        });

    }

    // Setup password toggles for the three password fields - signup password, confirm password, and login password.
    setupPasswordToggle("togglePassword1", "id_password1", "password-eye1");
    setupPasswordToggle("togglePassword2", "id_password2", "password-eye2");
    setupPasswordToggle("togglePassword", "id_password", "password-eye");

    // Password reset
    setupPasswordToggle("togglePassword1", "id_new_password1", "password-eye1");
    setupPasswordToggle("togglePassword2", "id_new_password2", "password-eye2");

    // Password change
    setupPasswordToggle("togglePassword", "id_old_password", "password-eye");

    // ==========================
    // PROFILE IMAGE PREVIEW
    // ==========================

    // Get the preset images, preview, file input and selected preset.
    const profileImageOptions = document.querySelectorAll(".profile-image-option");
    const profileImagePreview = document.getElementById("profileImagePreview");
    const imageInput = document.getElementById("id_image");
    const presetImageInput = document.getElementById("presetImage");

    // Handle preset image selection.
    profileImageOptions.forEach(option => {

        option.addEventListener("click", () => {

            const image = option.dataset.image;
            presetImageInput.value = option.dataset.imageName;

            // Show the selected image in the preview.
            profileImagePreview.src = image;

            // Update which preset appears selected.
            profileImageOptions.forEach(item => {
                item.classList.remove("selected");
            });

            option.classList.add("selected");

        });

    });

    // Preview a custom image before uploading it.
    if (imageInput) {

        imageInput.addEventListener("change", () => {

            presetImageInput.value = "";

            const file = imageInput.files[0];

            if (!file) return;

            profileImagePreview.src = URL.createObjectURL(file);

            // Remove preset selection when using a custom image.
            profileImageOptions.forEach(item => {
                item.classList.remove("selected");
            });

        });

    }

    // ==========================
    // LOCAL TIMEZONE
    // ==========================

    // Convert UTC timestamps to the user's local timezone.
    document.querySelectorAll(".comment-timestamp, .article-timestamp, .message-timestamp").forEach(element => {

        const timestamp = element.dataset.timestamp;

        if (!timestamp) return;

        // Convert the timestamp to a Date object and format it to the user's local timezone.
        const date = new Date(timestamp.replace(" ", "T").replace(" +0000", "Z"));

        // Check if the date is valid before formatting
        if (!isNaN(date.getTime())) {
            element.textContent = new Intl.DateTimeFormat(undefined, {
                dateStyle: "medium",
                timeStyle: "short"
            }).format(date);
        }

    });

    // ==================================
    // LOAD NEWEST MESSAGES ON PAGE LOAD
    // ==================================

    const messages = document.querySelector('.messaging-messages');

    if (messages) {
        messages.scrollTop = messages.scrollHeight;
    }


    // ===================================
    // AUTO-DISMISS DJANGO MESSAGE ALERTS
    // ===================================

    document.querySelectorAll('.alert').forEach(alert => {

    setTimeout(() => {
        alert.remove();
    }, 5000);

});

})();