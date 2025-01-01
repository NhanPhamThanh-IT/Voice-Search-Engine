from flask import Flask, request, jsonify
import base64
import os
from src.main import main

app = Flask(__name__)

@app.route('/api/audio', methods=['POST'])
def receive_audio_data():
    try:
        data = request.get_json()
        audio_base64 = data.get('audio', '')
        if not audio_base64:
            return jsonify({"message": "No audio data received"}), 400
        audio_data = base64.b64decode(audio_base64)
        output_path = os.path.join('src', 'uploads', 'recording.wav')
        with open(output_path, 'wb') as audio_file:
            audio_file.write(audio_data)
        print(f"Audio saved to {output_path}")
        main()
        return jsonify({"message": "Audio uploaded successfully", "file_path": output_path}), 200
    except Exception as e:
        return jsonify({"message": f"Error processing audio: {str(e)}"}), 500

if __name__ == '__main__':
    if not os.path.exists(os.path.join('src', 'uploads')):
        os.makedirs(os.path.join('src', 'uploads'))
    app.run(debug=True, host='0.0.0.0', port=5000)
