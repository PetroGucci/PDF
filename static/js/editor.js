var image = document.getElementById('image');
var cropper = new Cropper(image, {
    aspectRatio: NaN, // Recorte libre sin relación de aspecto fija
    viewMode: 1
    });

    // Función que obtiene los datos del recorte y los envía al servidor
function submitForm(actionType) {
    var data = cropper.getData(true);  // Obtiene los datos reales redondeados
    document.getElementById('x').value = data.x;
    document.getElementById('y').value = data.y;
    document.getElementById('width').value = data.width;
    document.getElementById('height').value = data.height;
    var form = document.getElementById('crop-form');
    var actionInput = document.getElementById('action_input');
        if (!actionInput) {
            actionInput = document.createElement('input');
            actionInput.type = 'hidden';
            actionInput.name = 'action';
            actionInput.id = 'action_input';
            form.appendChild(actionInput);
        }
        actionInput.value = actionType;
        form.submit();
    }

document.getElementById('download-crop').addEventListener('click', function() {
    submitForm('crop_pdf');
});

document.getElementById('download-scan').addEventListener('click', function() {
    submitForm('crop_scan_pdf');
});
// Botón de cancelar: redirige al inicio
    document.getElementById('cancelEdit').addEventListener('click', function() {
    window.location.href = "/";
});