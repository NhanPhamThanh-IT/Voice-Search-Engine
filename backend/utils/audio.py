"""
This module provides functions for handling audio-related tasks, including audio file conversion, text-to-speech generation,
and speech recognition. It uses the `pydub` library for audio format conversion, `gTTS` (Google Text-to-Speech) for text-to-speech 
synthesis, and `speech_recognition` for converting speech from audio to text.

Functions:
1. convert_to_wav(input_path, output_path):
   - Converts an audio file to the WAV format.
   - Uses `pydub.AudioSegment` to read an input audio file and export it as a WAV file.
   - Arguments:
     - `input_path`: The path to the input audio file.
     - `output_path`: The path where the WAV file will be saved.
   
2. text_to_speech(text, output_path, lang='vi'):
   - Converts the given text into speech and saves it as an audio file.
   - Uses `gTTS` to generate speech from text and save it as an audio file.
   - Arguments:
     - `text`: The text to be converted to speech.
     - `output_path`: The path where the generated speech audio will be saved.
     - `lang`: The language code for the speech (default is 'vi' for Vietnamese).

3. listen(audio_file_path, language="vi-VN"):
   - Converts speech from an audio file to text.
   - Uses `speech_recognition` to recognize speech from the provided audio file.
   - Arguments:
     - `audio_file_path`: The path to the audio file containing speech.
     - `language`: The language code for speech recognition (default is "vi-VN" for Vietnamese).
   - Returns:
     - The recognized text if successful.
     - Error messages for different exceptions:
       - "Unable to recognize audio" if speech recognition fails.
       - "API request error: <error_message>" if there is a problem with the recognition service.
       - "Audio file not found. Please check the path." if the file cannot be found.

Dependencies:
- pydub: For audio file manipulation and conversion.
- gTTS: For generating speech from text.
- speech_recognition: For speech-to-text conversion.
"""

# Importing necessary libraries
from pydub import AudioSegment
from gtts import gTTS
import speech_recognition as sr

# Function to convert an audio file to WAV format
def convert_to_wav(input_path, output_path):
    """
    Converts an audio file to WAV format.

    Args:
        input_path (str): The path to the input audio file.
        output_path (str): The path where the converted WAV file will be saved.
    
    The function reads the audio file from the input path, converts it to WAV format,
    and exports it to the specified output path.

    Returns:
        None
    """
    audio = AudioSegment.from_file(input_path)
    audio.export(output_path, format="wav")

# Function to convert text to speech and save as an audio file
def text_to_speech(text, output_path, lang='vi'):
    """
    Converts text to speech and saves the resulting audio as a file.

    Args:
        text (str): The text to be converted into speech.
        output_path (str): The path where the audio file will be saved.
        lang (str, optional): The language for the speech synthesis (default is 'vi' for Vietnamese).
    
    The function generates a speech audio file from the provided text and saves it in the
    specified path as an audio file.

    Returns:
        None
    """
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save(output_path)

# Function to convert speech from an audio file to text
def listen(audio_file_path, language="vi-VN"):
    """
    Converts speech from an audio file to text using Google Web Speech API.

    Args:
        audio_file_path (str): The path to the audio file that contains the speech.
        language (str, optional): The language code to be used for speech recognition (default is 'vi-VN' for Vietnamese).
    
    The function listens to the provided audio file, processes it, and converts the speech
    to text using the Google Web Speech API. It returns the recognized text or an error message.

    Returns:
        str: The recognized text from the audio file, or an error message in case of failure.
    """
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
