from flask import Flask, request, jsonify, send_file
import base64
import os
from src.main import upload_audio
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/audio', methods=['POST'])
def receive_audio_data():
    try:
        data = request.get_json()
        audio_base64 = data.get('audio', '')
        
        if not audio_base64:
            return jsonify({"message": "No audio data received"}), 400

        audio_data = base64.b64decode(audio_base64)
        output_path = os.path.join('src', 'uploads', 'recording.wav')

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'wb') as audio_file:
            audio_file.write(audio_data)

        upload_audio()

        response_file = os.path.join('src', 'uploads', 'response.wav')

        if not os.path.exists(response_file):
            return jsonify({"message": "Processed audio not found"}), 404

        return send_file(response_file, as_attachment=True)

    except Exception as e:
        return jsonify({"message": f"Error processing audio: {str(e)}"}), 500

if __name__ == '__main__':
    uploads_dir = os.path.join('src', 'uploads')
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
