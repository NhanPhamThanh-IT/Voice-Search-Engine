"""
This module provides functions to perform a search query on Google, extract relevant snippets from search results, 
and find the best matching answer using cosine similarity.

It leverages external APIs, text vectorization, and cosine similarity to process search results and identify the most relevant answer.

Functions:

    1. search_by_query(query)
    2. extract_snippets(content, max_snippets=10)
    3. find_best_answer(question, answers)
    4. get_news_content(query)

Dependencies:
    - json: For encoding and decoding JSON data.
    - requests: For making HTTP requests to the Serper API to retrieve search results.
    - sklearn.feature_extraction.text.TfidfVectorizer: For vectorizing the text data (used in calculating cosine similarity).
    - sklearn.metrics.pairwise.cosine_similarity: For calculating cosine similarity between vectors.
    - dotenv: For loading environment variables from a `.env` file.
    - os: For interacting with the operating system, specifically retrieving the API key from environment variables.

Environment Variables:
    - X-API-KEY: The API key used for authenticating requests to the Serper API. Should be defined in a `.env` file.
"""

# Import necessary libraries
import json
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
x_api_key = os.getenv("X-API-KEY")

# Function to search for a query on Google using the Serper API
def search_by_query(query):
    """
    Searches for a query on Google using a custom search API.

    Args:
        query (str): The search query to be sent to the search engine.

    The function sends a POST request to the search engine API with the query and returns the response in JSON format.
    
    Returns:
        dict: The JSON response containing the search results.
              If the request fails or there is an issue, an empty dictionary is returned.
    """
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query, "gl": "vn", "hl": "vi", "engine": "google"})
    headers = {
        'X-API-KEY': x_api_key,  # Make sure x_api_key is defined somewhere
        'Content-Type': 'application/json'
    }
    with requests.Session() as session:
        response = session.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            return response.json()
    return {}

# Function to extract relevant snippets from the search results
def extract_snippets(content, max_snippets=10):
    """
    Extracts relevant snippets from the search result content.

    Args:
        content (dict): The JSON response content from the search API.
        max_snippets (int, optional): The maximum number of snippets to return (default is 10).
    
    The function attempts to extract the answer or snippets from the content based on predefined keys.
    It first looks for an answer, then a snippet, and if neither is found, it extracts snippets from
    the organic search results, excluding those with '...'.
    
    Returns:
        list: A list of strings, each representing a snippet or answer from the content.
    """
    print(content)
    answer = content.get('answerBox', {}).get('answer', {})
    if answer:
        return [answer]
    answer = content.get('answerBox', {}).get('snippet', {})
    if answer:
        return [answer]
    lst = [result['snippet'] for result in content.get('organic', []) if '...' not in result['snippet']][:max_snippets]
    return lst

# Function to find the best matching answer to a question from a list of answers
def find_best_answer(question, answers):
    """
    Finds the best matching answer to a question from a list of answers using cosine similarity.

    Args:
        question (str): The question for which an answer is being searched.
        answers (list): A list of potential answer strings.
    
    The function calculates the cosine similarity between the question and each answer and returns the answer
    with the highest similarity.
    
    Returns:
        str: The best matching answer from the provided list of answers.
    """
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([question] + answers)
    similarity_matrix = cosine_similarity(vectors[0:1], vectors[1:])
    best_match_index = similarity_matrix.argsort()[0][-1]

    return answers[best_match_index]

# Function to get the best matching answer for a query
def get_news_content(query):
    """
    Retrieves the best answer for a query from search engine results.

    Args:
        query (str): The query for which to find news content or relevant answers.
    
    The function performs a search for the given query, extracts relevant snippets, and finds the best
    matching answer based on the cosine similarity between the query and the snippets.
    
    Returns:
        str: The best matching answer to the query from the search results.
    """
    content = search_by_query(query)
    snippets = extract_snippets(content)
    return find_best_answer(query, snippets)