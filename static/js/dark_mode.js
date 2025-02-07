document.addEventListener("DOMContentLoaded", function () {
  const toggleDarkModeButton = document.getElementById("toggleDarkMode");
  const themeStylesheet = document.getElementById("themeStylesheet");

  if (!toggleDarkModeButton || !themeStylesheet) {
      console.error("Falta el botón o el <link> de estilos en el HTML.");
      return;
  }

  // Rutas de los estilos
  const lightModeURL = "{{ url_for('static', filename='css/style.css') }}";
  const darkModeURL = "{{ url_for('static', filename='css/dark_mode.css') }}";

  // Función para cambiar entre temas
  function updateTheme() {
      if (localStorage.getItem("darkMode") === "enabled") {
          themeStylesheet.setAttribute("href", darkModeURL);
          toggleDarkModeButton.textContent = "☀️ Modo Claro";
      } else {
          themeStylesheet.setAttribute("href", lightModeURL);
          toggleDarkModeButton.textContent = "🌙 Modo Oscuro";
      }
  }

  // Verificar si el usuario tenía activado el modo oscuro
  if (localStorage.getItem("darkMode") === "enabled") {
      themeStylesheet.setAttribute("href", darkModeURL);
  } else {
      themeStylesheet.setAttribute("href", lightModeURL);
  }

  updateTheme(); // Aplicar el tema al cargar la página

  // Evento para alternar entre los temas
  toggleDarkModeButton.addEventListener("click", function () {
      if (localStorage.getItem("darkMode") === "enabled") {
          localStorage.setItem("darkMode", "disabled");
      } else {
          localStorage.setItem("darkMode", "enabled");
      }

      updateTheme(); // Aplicar el cambio
  });
});
