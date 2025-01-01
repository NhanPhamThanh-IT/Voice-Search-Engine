import requests
import json
from bs4 import BeautifulSoup

def search_news(query):
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query, "gl": "vn", "hl": "vi"})
    headers = {'X-API-KEY': '6dcbc49f7a598635738062e18099179214293c1b', 'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        data = response.json()
        if 'answerBox' in data:
            return {'answerBox': data.get('answerBox',[])}
        return {'organic': data.get('organic', [])}
    return {}

def get_news_content(query, content = "Không tìm thấy nội dung bạn cần. Vui lòng thử lại."):
    news_results = search_news(query)
    if 'answerBox' in news_results:
        answer_box = news_results.get('answerBox', None)
        content = 'answer' in answer_box if answer_box['title'] + " " + answer_box['answer'] else (answer_box['snippet'] if 'snippet' in answer_box else content)
    else:
        organic_results = news_results.get('organic', [])
        if organic_results:
            content = organic_results[0].get('snippet', '')
    return content