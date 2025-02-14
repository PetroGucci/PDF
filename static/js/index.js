let dropArea = document.getElementById('drop-area');
let fileInput = document.getElementById('fileElem');
let form = document.getElementById('file-form');

    // Evitar comportamiento por defecto
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false);
    document.body.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults (e) {
    e.preventDefault();
    e.stopPropagation();
}  // Resaltar el área cuando se arrastra el archivo
['dragenter', 'dragover'].forEach(eventName => {     
    dropArea.addEventListener(eventName, () => dropArea.classList.add('highlight'), false);
});

['dragleave', 'drop'].forEach(eventName => {     
    dropArea.addEventListener(eventName, () => dropArea.classList.remove('highlight'), false);
});

// Manejar el drop
dropArea.addEventListener('drop', handleDrop, false);

function handleDrop(e) {
    let dt = e.dataTransfer;
    let files = dt.files;
    fileInput.files = files;
    form.submit();
}

// También, si el usuario hace clic en el área, abrir el selector de archivos
dropArea.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', () => form.submit());