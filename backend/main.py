from utils.audio import convert_to_wav, listen, text_to_speech
from utils.news import get_news_content

def main(audio_path):
    convert_to_wav(audio_path, audio_path)
    query = listen(audio_path)
    content = get_news_content(query)
    text_to_speech(content, audio_path)
    return content
