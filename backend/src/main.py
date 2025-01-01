import os
from src.utils.audio import convert_to_wav, listen, text_to_speech
from src.utils.news import get_news_content
from src.utils.summary import summarize_text_with_openai

def upload_audio():
    input_audio = os.path.join(os.path.join(os.getcwd(), 'src'), 'uploads', 'recording.wav')
    output_audio = os.path.join(os.path.join(os.getcwd(), 'src'), 'uploads', 'response.wav')
    convert_to_wav(input_audio, output_audio)
    query = listen(output_audio)
    content = "Không nhận diện được âm thanh. Vui lòng thử lại." if query == "Unable to recognize audio." else get_news_content(query) if query else "Không nhận diện được âm thanh. Vui lòng thử lại."
    text_to_speech(content, output_audio)

