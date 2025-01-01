import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

def summarize_text_with_openai(text):
    response = openai.ChatCompletion.create(
        model="chatgpt-4o-latest",
        messages=[
            {"role": "user", "content": f"Rephrase the following content to be concise and complete: '{text}'"},
        ],
        temperature=0.7,
        max_tokens=150
    )
    return response.choices[0].message["content"]