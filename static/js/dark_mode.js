document.addEventListener("DOMContentLoaded", function () {
    const darkModeButton = document.getElementById("toggleDarkMode");
    const body = document.body;

    // Verificar si el usuario ya tiene activado el modo oscuro
    if (localStorage.getItem("dark-mode") === "enabled") {
        body.classList.add("dark-mode");
        darkModeButton.textContent = "Modo Claro ☀️";
    }

    // Alternar modo oscuro al hacer clic en el botón
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
