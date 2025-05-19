from flask import Flask, request, jsonify, send_file, render_template
import qrcode
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from urllib.parse import quote

import os
import shutil

# Ensure templates folder exists and move index.html
if not os.path.exists("templates"):
    os.makedirs("templates")
if os.path.exists("index.html"):
    shutil.move("index.html", os.path.join("templates", "index.html"))

# Ensure static folder exists and move style.css
if not os.path.exists("static"):
    os.makedirs("static")
if os.path.exists("style.css"):
    shutil.move("style.css", os.path.join("static", "style.css"))



app = Flask(__name__)

if not os.path.exists("QR Code"):
    os.makedirs("QR Code")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_qr_code():
    data = request.json
    title = secure_filename(data.get('title', 'default_title'))
    link = data.get('link', '')
    location = data.get('location', '')

    if not link and not location:
        return jsonify({"error": "Please provide either a link or a location"}), 400

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"{title}_{timestamp}.png"
    filepath = os.path.join("QR Code", filename)

    if location:
        qr_data = f"https://www.google.com/maps/dir//{quote(location)}"
    else:
        qr_data = link

    img = qrcode.make(qr_data)
    img.save(filepath)

    return jsonify({"message": "QR Code generated successfully", "filename": filepath})

@app.route('/download/<path:filename>', methods=['GET'])
def download_qr_code(filename):
    filepath = os.path.join(os.getcwd(), filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
