document.addEventListener("DOMContentLoaded", function () {
  const toggleDarkModeButton = document.getElementById("toggleDarkMode");
  const body = document.body;

  //Funcion para actualizar el texto del boton
  function updateButtonText() {
    if (body.classList.contains("dark-mode")) {
      toggleDarkModeButton.textContent = "☀️ Modo Claro";
    }else{
      toggleDarkModeButton.textContent = "🌙 Modo Oscuro";
    }
  }

  // Verificar si el usuario tenía activado el modo oscuro antes
  if (localStorage.getItem("darkMode") === "enabled") {
      body.classList.add("dark-mode");
  }
  
  // Actualizar el texto del botón al cargar la página
  updateButtonText();

  toggleDarkModeButton.addEventListener("click", function () {
      body.classList.toggle("dark-mode");

      // Guardar la preferencia en localStorage
      if (body.classList.contains("dark-mode")) {
          localStorage.setItem("darkMode", "enabled");
      } else {
          localStorage.setItem("darkMode", "disabled");
      }
       
      // Actualizar el texto del botón
      updateButtonText();
  });
});
