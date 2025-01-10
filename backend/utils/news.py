import json
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
import os

load_dotenv()

x_api_key = os.getenv("X-API-KEY")

def search_by_query(query):
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query, "gl": "vn", "hl": "vi", "engine": "google"})
    headers = {
        'X-API-KEY': x_api_key,
        'Content-Type': 'application/json'
    }
    with requests.Session() as session:
        response = session.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            return response.json()
    return {}

def extract_snippets(content, max_snippets=10):
    print(content)
    answer = content.get('answerBox', {}).get('answer', {})
    if answer:
        return [answer]
    answer = content.get('answerBox', {}).get('snippet', {})
    if answer:
        return [answer]
    lst = [result['snippet'] for result in content.get('organic', []) if '...' not in result['snippet']][:max_snippets]
    return lst

def find_best_answer(question, answers):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([question] + answers)
    similarity_matrix = cosine_similarity(vectors[0:1], vectors[1:])
    best_match_index = similarity_matrix.argsort()[0][-1]

    return answers[best_match_index]

def get_news_content(query):
    content = search_by_query(query)
    snippets = extract_snippets(content)
    return find_best_answer(query, snippets)