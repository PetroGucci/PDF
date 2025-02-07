document.addEventListener("DOMContentLoaded", function () {
    const toggleDarkModeButton = document.getElementById("toggleDarkMode");

    if (!toggleDarkModeButton) {
        console.error("Falta el botón en el HTML.");
        return;
    }

    // Aplicar el tema guardado en localStorage
    if (localStorage.getItem("darkMode") === "enabled") {
        document.body.classList.add("dark-mode");
        toggleDarkModeButton.textContent = "☀️ Modo Claro";
    } else {
        document.body.classList.remove("dark-mode");
        toggleDarkModeButton.textContent = "🌙 Modo Oscuro";
    }

    // Evento para alternar entre los temas
    // toggleDarkModeButton.addEventListener("click", function () {
    //     if (toggleDarkModeButton.classList.contains("light-mode")) {
    //         toggleDarkModeButton.classList.remove("light-mode");
    //         toggleDarkModeButton.classList.add("dark-mode")
    //         localStorage.setItem("darkMode", "disabled");
    //         toggleDarkModeButton.textContent = "🌙 Modo Oscuro";
    //     } else {
    //         toggleDarkModeButton.classList.remove("dark-mode");
    //         toggleDarkModeButton.classList.add("light-mode")
    //         localStorage.setItem("lightMode", "enabled");
    //         toggleDarkModeButton.textContent = "☀️ Modo Claro";
    //     }
    // });


    toggleDarkModeButton.addEventListener("click", function () {
        if (document.body.classList.contains("light-mode")) {
            document.body.classList.remove("light-mode");
            document.body.classList.add("dark-mode")
            localStorage.setItem("darkMode", "disabled");
            toggleDarkModeButton.textContent = "🌙 Modo Oscuro";
        } else {
            document.body.classList.remove("dark-mode");
            document.body.classList.add("light-mode")
            localStorage.setItem("lightMode", "enabled");
            toggleDarkModeButton.textContent = "☀️ Modo Claro";
        }
    });
});
