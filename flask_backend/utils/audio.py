from pydub import AudioSegment
from gtts import gTTS
import speech_recognition as sr

def convert_to_wav(input_path, output_path):
    audio = AudioSegment.from_file(input_path)
    audio.export(output_path, format="wav")

def text_to_speech(text, output_path, lang='vi'):
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save(output_path)

def listen(audio_file_path, language="vi-VN"):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language=language)
            return text
    except sr.UnknownValueError:
        return "Unable to recognize audio."
    except sr.RequestError as e:
        return f"API request error: {e}"
    except FileNotFoundError:
        return "Audio file not found. Please check the path."