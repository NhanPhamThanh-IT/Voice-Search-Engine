import os
from utils.audio import convert_to_wav, listen, text_to_speech
from utils.news import get_news_content
from utils.summary import summarize_text_with_openai

def main(input_path):
    convert_to_wav(input_path, input_path)
    query = listen(input_path)
    content = get_news_content(query)
    text_to_speech(content, input_path)
