import os
from src.utils.audio_utils import convert_to_wav, listen
from src.utils.news_utils import get_news_content
from src.utils.openai_utils import summarize_text_with_openai

def main():
    input_audio = os.path.join(os.path.join(os.getcwd(), 'src'), 'uploads', 'recording.wav')
    convert_to_wav(input_audio, input_audio)
    query = listen(input_audio)
    content = "Không nhận diện được âm thanh. Vui lòng thử lại." if query == "Unable to recognize audio." else get_news_content(query) if query else "Không nhận diện được âm thanh. Vui lòng thử lại."
    print(content)