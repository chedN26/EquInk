from flask import Flask, request, render_template
from pdf2image import convert_from_path
from docx2pdf import convert
import os
import tempfile
import cv2
import numpy as np
from database import init_db, insert_upload, get_upload_history

app = Flask(__name__)
init_db()

def get_bw_percentage(image_path):
    img = cv2.imread(image_path)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    brightness = 0.299*r + 0.587*g + 0.114*b
    black_mask = brightness < 30
    white_mask = brightness > 225
    bw_mask = black_mask | white_mask
    total_pixels = img.shape[0] * img.shape[1]
    bw_pixels = np.count_nonzero(bw_mask)
    return round((bw_pixels / total_pixels) * 100, 2)

def analyze_pdf(file_path):
    images = convert_from_path(file_path, poppler_path=r"C:\poppler-25.11.0\bin")
    percentages = []
    for page in images:
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
            page.save(temp_file.name, "PNG")
            temp_path = temp_file.name
        try:
            percentages.append(get_bw_percentage(temp_path))
        finally:
            os.remove(temp_path)
    return round(sum(percentages)/len(percentages), 2)

def analyze_docx(file_path):
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_pdf:
        temp_pdf_path = temp_pdf.name
    try:
        convert(file_path, temp_pdf_path)
        return analyze_pdf(temp_pdf_path)
    finally:
        if os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)
            
def percentage_to_value(percent):
    match percent:
        case p if 91 <= p <= 100:
            return 20
        case p if 81 <= p <= 90:
            return 18
        case p if 71 <= p <= 80:
            return 16
        case p if 61 <= p <= 70:
            return 14
        case p if 51 <= p <= 60:
            return 12
        case p if 41 <= p <= 50:
            return 10
        case p if 31 <= p <= 40:
            return 8
        case p if 21 <= p <= 30:
            return 6
        case p if 6 <= p <= 20:
            return 4
        case p if 0 <= p <= 5:
            return 0
        case _:
            return 0  # default if percentage out of bounds


@app.route("/", methods=["GET"])
def index():
    history = get_upload_history()
    return render_template("index.html", history=history)

@app.route("/upload", methods=["POST"])
def upload():
    uploaded_file = request.files.get("file")
    if not uploaded_file:
        return render_template("index.html", result="No file uploaded")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.filename)[1]) as temp_file:
        uploaded_file.save(temp_file.name)
        temp_path = temp_file.name
    
    try:
        if uploaded_file.filename.lower().endswith(".pdf"):
            result = analyze_pdf(temp_path)
        elif uploaded_file.filename.lower().endswith(".docx"):
            result = analyze_docx(temp_path)
        else:
            result = "Invalid file type"
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
    color_percent = round(100 - result, 2)
    cost = percentage_to_value(round(color_percent, 0)) + 2
    
    # Save to database
    insert_upload(uploaded_file.filename,
                  uploaded_file.filename.split('.')[-1].lower(),
                  color_percent,
                  cost)
    
    # Optionally fetch updated history
    history = get_upload_history()
    
    return render_template("index.html", result=color_percent, cost=cost, history=history)

if __name__ == "__main__":
    app.run(debug=True)
