import os
import io
import zipfile
from flask import Flask, render_template, request, redirect, url_for, send_file, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image, ImageOps, ImageEnhance
import fitz  # PyMuPDF

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Crea la carpeta uploads si no existe
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Ruta principal con drag & drop
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            return redirect(url_for('process_file', filename=filename))
    return render_template("index.html")

# Ruta para procesar el archivo subido
@app.route("/process/<filename>", methods=["GET", "POST"])
def process_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file_ext = filename.split('.')[-1].lower()
    context = {"filename": filename, "file_type": file_ext}
    
    if request.method == "POST":
        action = request.form.get("action")
        
        # Procesamiento para PDF: extraer imágenes y descargarlas en un ZIP
        if file_ext == "pdf":
            if action in ["extract_color", "extract_bw"]:
                color = True if action == "extract_color" else False
                images = extract_images(file_path, color=color)
                if images:
                    zip_io = io.BytesIO()
                    with zipfile.ZipFile(zip_io, mode="w", compression=zipfile.ZIP_DEFLATED) as zipf:
                        for idx, img in enumerate(images):
                            img = img.convert("RGB")
                            img_io = io.BytesIO()
                            img.save(img_io, format="JPEG", quality=85, optimize=True)
                            img_io.seek(0)
                            zipf.writestr(f"extracted_{idx+1}.jpg", img_io.read())
                    zip_io.seek(0)
                    return send_file(zip_io, mimetype="application/zip", as_attachment=True, download_name="extracted_images.zip")
        
        # Procesamiento para imágenes (PNG, JPG, JPEG)
        elif file_ext in ["png", "jpg", "jpeg"]:
            if action == "edit_crop":
                # Redirecciona al editor para recorte manual
                return redirect(url_for('editor', filename=filename))
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

# Ruta del editor de recorte
@app.route("/editor/<filename>", methods=["GET", "POST"])
def editor(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if request.method == "POST":
        try:
            x = float(request.form.get('x', 0))
            y = float(request.form.get('y', 0))
            width = float(request.form.get('width', 0))
            height = float(request.form.get('height', 0))
        except (ValueError, TypeError):
            return "Error en los parámetros de recorte.", 400
        
        action = request.form.get('action')
        image = Image.open(file_path)
        cropped = image.crop((x, y, x + width, y + height))
        
        # Si se eligió aplicar el filtro escáner, se procesa el recorte
        if action == 'crop_scan_pdf':
            cropped = apply_scanner_filter(cropped)
        
        pdf_io = io.BytesIO()
        cropped.convert("RGB").save(pdf_io, format="PDF")
        pdf_io.seek(0)
        download_name = 'cropped_scanned.pdf' if action == 'crop_scan_pdf' else 'cropped.pdf'
        return send_file(pdf_io, mimetype='application/pdf', as_attachment=True, download_name=download_name)
    
    return render_template("editor.html", filename=filename)

# Ruta para servir los archivos subidos
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Función para extraer imágenes de un PDF
def extract_images(pdf_path, color=True):
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

# Filtro escáner: convierte a escala de grises y aumenta el contraste
def apply_scanner_filter(image):
    grayscale = ImageOps.grayscale(image)
    enhancer = ImageEnhance.Contrast(grayscale)
    enhanced = enhancer.enhance(2.5)
    return enhanced

# Función para enviar una imagen para descarga
def send_image(image, filename):
    img_io = io.BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png', as_attachment=True, download_name=filename)

if __name__ == '__main__':
    app.run(debug=True)
