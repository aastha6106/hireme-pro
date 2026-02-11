(function () {
    var STORAGE_KEY = "hireme-theme";
    var btn = null;

    function applyTheme(theme) {
        if (theme === "dark") {
            document.body.classList.add("dark");
        } else {
            document.body.classList.remove("dark");
        }

        if (btn) {
            var icon = btn.querySelector(".toggle-icon");
            var label = btn.querySelector(".toggle-label");
            if (theme === "dark") {
                icon.textContent = "\u2600";
                label.textContent = "Light";
            } else {
                icon.textContent = "\u263E";
                label.textContent = "Dark";
            }
        }
    }

    function handleClick() {
        var isDark = document.body.classList.contains("dark");
        var newTheme = isDark ? "light" : "dark";
        localStorage.setItem(STORAGE_KEY, newTheme);
        applyTheme(newTheme);
    }

    function init() {
        btn = document.getElementById("theme-toggle");

        var saved = localStorage.getItem(STORAGE_KEY);
        if (!saved) {
            saved = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
        }

        applyTheme(saved);

        if (btn) {
            btn.addEventListener("click", handleClick);
        }
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();