"""
This module provides a main function to process an audio file, extract a query from it, 
retrieve relevant news content based on the query, and generate a speech response.

The `main` function utilizes helper functions from the `utils.audio` and `utils.news` modules for audio conversion, 
speech recognition, and news content retrieval.

Function:

    1. main(audio_path)

Dependencies:
- utils.audio: Contains helper functions `convert_to_wav`, `listen`, and `text_to_speech` for audio file manipulation and speech recognition.
- utils.news: Contains the `get_news_content` function for retrieving news content based on a query.
"""


# Import the required functions from the utils modules
from utils.audio import convert_to_wav, listen, text_to_speech
from utils.news import get_news_content

# Main function that processes an audio file and provides a spoken news summary
def main(audio_path):
    """
    Main function that processes an audio file and provides a spoken news summary.

    Args:
        audio_path (str): The path to the input audio file that will be processed.

    The function performs the following steps:
        1. Converts the input audio file to WAV format using `convert_to_wav`.
        2. Converts the audio content to text using `listen`.
        3. Retrieves news content related to the transcribed text using `get_news_content`.
        4. Converts the news content to speech and saves it as an audio file using `text_to_speech`.
    
    The resulting audio file is saved to the same path as the input audio file.

    Returns:
        str: The news content (text) that was converted to speech.
    """
    convert_to_wav(audio_path, audio_path)
    query = listen(audio_path)
    content = get_news_content(query)
    text_to_speech(content, audio_path)
    return content
