document.addEventListener("DOMContentLoaded", function () {
    const darkModeButton = document.getElementById("toggleDarkMode");
    const body = document.body;

    // Detectar el modo del sistema
    const prefersDarkScheme = window.matchMedia("(prefers-color-scheme: dark)");

    // Comprobar si el usuario ya tiene una preferencia guardada
    let darkMode = localStorage.getItem("dark-mode");

    if (darkMode === "enabled") {
        body.classList.add("dark-mode");
    } else if (darkMode === "disabled") {
        body.classList.remove("dark-mode");
    } else {
        // Si no hay preferencia guardada, aplicar la del sistema
        if (prefersDarkScheme.matches) {
            body.classList.add("dark-mode");
            localStorage.setItem("dark-mode", "enabled");
        }
    }

    // Cambiar el texto del botón según el estado actual
    darkModeButton.textContent = body.classList.contains("dark-mode") ? "Modo Claro ☀️" : "Modo Oscuro 🌙";

    // Evento para cambiar el modo
    darkModeButton.addEventListener("click", function () {
        body.classList.toggle("dark-mode");

        if (body.classList.contains("dark-mode")) {
            localStorage.setItem("dark-mode", "enabled");
            darkModeButton.textContent = "Modo Claro ☀️";
        } else {
            localStorage.setItem("dark-mode", "disabled");
            darkModeButton.textContent = "Modo Oscuro 🌙";
        }
    });
});