from flask import Flask, render_template, request, redirect, url_for, send_file
from PIL import Image
from fpdf import FPDF
import os

app = Flask(__name__)

# Directory to store uploaded images temporarily
UPLOAD_FOLDER = 'uploads/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Route to handle the main page (file upload form)
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the file upload and conversion to PDF
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'document' not in request.files:
        return redirect(request.url)
    
    file = request.files['document']
    
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        # Save the uploaded file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # Convert image to PDF
        pdf_path = convert_image_to_pdf(filepath)
        
        # Send the PDF file to the user for download
        return send_file(pdf_path, as_attachment=True)

# Function to convert the uploaded image to PDF
def convert_image_to_pdf(image_path):
    # Open the image
    image = Image.open(image_path)
    
    # Create a PDF using FPDF
    pdf = FPDF()
    pdf.add_page()
    
    # Convert image to RGB (required for Pillow to avoid issues)
    image = image.convert('RGB')
    
    # Save the image as a temporary PDF file
    pdf_output_path = image_path.rsplit('.', 1)[0] + '.pdf'
    image.save(pdf_output_path, "PDF", resolution=100.0)
    
    # Return the path to the generated PDF
    return pdf_output_path

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

