"""
Flask-based web application that provides endpoints for uploading and serving audio files.

This application allows users to upload audio files via a POST request, process the uploaded audio, 
and retrieve the processed audio via a GET request. The app supports cross-origin requests 
and stores uploaded files locally. It also returns a URL to access the uploaded file once it's processed.

Modules:
    - Flask: Used for creating the web application and handling HTTP requests and responses.
    - werkzeug.utils: Provides the secure_filename function to sanitize the filename before saving.
    - flask_cors: Used to enable Cross-Origin Resource Sharing (CORS) to allow access from different origins.
    - os: Used to interact with the file system for creating directories and file operations.
    - main: Imported from the `main` module, processes the uploaded audio file.
    - utils.helper: Imports the `get_ipv4_address` function to fetch the current IPv4 address of the server.

Configuration:
    - The application stores uploaded audio files in a local folder, defined by the constant `UPLOAD_FOLDER`.
    - The `UPLOAD_FOLDER` is created if it doesn't already exist.

Routes:
1. /upload (POST):
   - Accepts an audio file from the request and saves it to the server.
   - If the file is successfully uploaded, the application processes the file using the `main` function.
   - Returns a JSON response containing:
     - `audio_url`: A URL to access the uploaded audio file.
     - `content`: The processed content returned by the `main` function.
   - Returns a 400 error if no file is provided or if the file is empty.
   - Returns a 200 status on success.

2. /uploads/<filename> (GET):
   - Serves the audio file from the local server if it exists.
   - If the file is not found, returns a 404 error.
   - If serving the file fails, returns a 500 error with an error message.

Server Configuration:
    - The app runs on host '0.0.0.0' and listens on port 5000.
    - Debug mode is enabled for development purposes.

Dependencies:
    - Flask: For web framework.
    - werkzeug: For secure file handling.
    - flask_cors: For CORS support.
    - os: For file operations.
    - main: For processing audio content.
    - utils.helper: For obtaining the server's IP address.

Example Workflow:
    1. The client sends a POST request with an audio file to the `/upload` route.
    2. The server processes the file, saves it locally, and returns a URL to the audio file.
    3. The client can then use the returned URL to retrieve the processed file using a GET request.

"""

# Import necessary modules
from flask import Flask, request, send_file, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
from main import main
from utils.helper import get_ipv4_address

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define the route for uploading audio files
@app.route('/upload', methods=['POST'])
def upload_audio():
    """
    This route allows users to upload audio files.

    Steps:
    1. The user submits a POST request with a file.
    2. The server checks if the file is provided and if it has a valid filename.
    3. If valid, the file is saved to the specified upload folder.
    4. The server processes the file (via the `main` function) and generates a content result.
    5. The server returns a JSON response containing:
        - The URL where the uploaded audio file can be accessed.
        - The content generated from the file.
    
    Returns:
        - JSON response with `audio_url` and `content` if successful.
        - 400 error with a message if the file is missing or invalid.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        content = main(filepath)
        audio_url = f"http://{get_ipv4_address()}:5000/uploads/{filename}"
        return jsonify({"audio_url": audio_url, "content": content}), 200

# Define the route for serving audio files
@app.route('/uploads/<filename>', methods=['GET'])
def serve_file(filename):
    """
    This route serves the uploaded audio files to the user.

    Steps:
    1. The user sends a GET request for a specific file.
    2. The server checks if the requested file exists in the upload folder.
    3. If the file is found, it is served with the appropriate MIME type for audio files.
    4. If the file does not exist or there is an error, the server returns an error message.
    
    Args:
        filename (str): The name of the file to be served.

    Returns:
        - The audio file if found.
        - 404 error if the file does not exist.
        - 500 error if there is an issue serving the file.
    """
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404
    try:
        return send_file(filepath, mimetype='audio/mpeg')
    except Exception as e:
        return jsonify({"error": f"Failed to serve file: {str(e)}"}), 500

# Run the Flask application
if __name__ == '__main__':
    """
    Runs the Flask web server, enabling the application to accept incoming requests.

    The application will be available at:
        - Host: 0.0.0.0 (accessible from any IP)
        - Port: 5000

    The server runs in debug mode for easier development and testing.
    """
    app.run(debug=True, host='0.0.0.0', port=5000)

