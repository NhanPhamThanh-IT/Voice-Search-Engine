from flask import Flask, request, send_file
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
from main import main

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        return {"error": "No file part"}, 400
    file = request.files['file']
    if file.filename == '':
        return {"error": "No selected file"}, 400
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        audio_url = f"http://{request.host}/uploads/{filename}"
        return {"audio_url": audio_url}

@app.route('/uploads/<filename>', methods=['GET'])
def serve_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    main(filepath)
    return send_file(filepath)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

