import os
import io
import zipfile
from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from PIL import Image, ImageOps, ImageEnhance
import fitz  # PyMuPDF

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Crear la carpeta de uploads si no existe
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            # Redirecciona a la ruta de procesamiento
            return redirect(url_for('process_file', filename=filename))
    return render_template("index.html")

@app.route("/process/<filename>", methods=["GET", "POST"])
def process_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file_ext = filename.split('.')[-1].lower()
    context = {"filename": filename, "file_type": file_ext}
    
    if request.method == "POST":
        action = request.form.get("action")
        
        # Procesar PDF: extraer imágenes y devolver un ZIP
        if file_ext == "pdf":
            if action in ["extract_color", "extract_bw"]:
                color = True if action == "extract_color" else False
                images = extract_images(file_path, color=color)
                if images:
                    # Crear un ZIP con todas las imágenes
                    zip_io = io.BytesIO()
                    with zipfile.ZipFile(zip_io, mode="w", compression=zipfile.ZIP_DEFLATED) as zipf:
                        for idx, img in enumerate(images):
                            # Convertir imagen a RGB (para JPEG) y guardarla en memoria
                            img = img.convert("RGB")
                            img_io = io.BytesIO()
                            # Guardamos con calidad optimizada: buena calidad y peso reducido.
                            img.save(img_io, format="JPEG", quality=85, optimize=True)
                            img_io.seek(0)
                            zipf.writestr(f"extracted_{idx+1}.jpg", img_io.read())
                    zip_io.seek(0)
                    return send_file(zip_io, mimetype="application/zip", as_attachment=True, download_name="extracted_images.zip")
        
        # Procesar imágenes (PNG, JPG, JPEG)
        elif file_ext in ["png", "jpg", "jpeg"]:
            if action == "edit_crop":
                image = Image.open(file_path)
                cropped = crop_center(image)
                return send_image(cropped, 'cropped.png')
            elif action == "scan_filter":
                image = Image.open(file_path)
                scanned = apply_scanner_filter(image)
                return send_image(scanned, 'scanned.png')
            elif action == "convert_pdf":
                image = Image.open(file_path)
                pdf_io = io.BytesIO()
                image.convert("RGB").save(pdf_io, format="PDF")
                pdf_io.seek(0)
                return send_file(pdf_io, mimetype='application/pdf',
                                 as_attachment=True, download_name='converted.pdf')
    return render_template("process.html", **context)

def extract_images(pdf_path, color=True):
    """
    Extrae las imágenes de cada página de un PDF.
    Si color es False, las convierte a blanco y negro con filtro escáner.
    """
    doc = fitz.open(pdf_path)
    images = []
    for page in doc:
        image_list = page.get_images(full=True)
        for img in image_list:
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            if not color:
                image = apply_scanner_filter(image)
            images.append(image)
    return images

def apply_scanner_filter(image):
    """
    Simula un filtro escáner:
      - Convierte a escala de grises.
      - Aumenta el contraste para imitar el efecto de un escáner real.
    """
    grayscale = ImageOps.grayscale(image)
    enhancer = ImageEnhance.Contrast(grayscale)
    # Factor de 2.5: ajústalo según lo que necesites para lograr el efecto deseado.
    enhanced = enhancer.enhance(2.5)
    return enhanced

def crop_center(image):
    """Recorta la imagen al centro (cuadrado)."""
    width, height = image.size
    crop_size = min(width, height)
    left = (width - crop_size) // 2
    top = (height - crop_size) // 2
    return image.crop((left, top, left + crop_size, top + crop_size))

def send_image(image, filename):
    """Envía una imagen en memoria para su descarga."""
    img_io = io.BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png', as_attachment=True, download_name=filename)

if __name__ == '__main__':
    app.run(debug=True)
