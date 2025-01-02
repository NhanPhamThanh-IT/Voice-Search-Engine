import os
from utils.audio import convert_to_wav, listen, text_to_speech
from utils.news import get_news_content
from utils.summary import summarize_text_with_openai

def main(audio_path):
    convert_to_wav(audio_path, audio_path)
    query = listen(audio_path)
    content = get_news_content(query)
    content = """ Đội tuyển bóng đá Việt Nam hiện đang tham gia Giải vô địch bóng đá Đông Nam Á (ASEAN Cup) 2024. Đội đã xuất sắc vượt qua vòng bảng, giành 13 điểm và đứng đầu bảng B. Trong bán kết, họ thắng Singapore với tổng tỷ số 5-1, và đang chuẩn bị đối đầu với Thái Lan trong trận chung kết lượt đi vào ngày 2/1/2025. Đội tuyển có sự góp mặt của các cầu thủ như Quang Hải, Xuân Trường, Tiến Linh, và Văn Hậu. Sau thành tích vào chung kết, đội đã nhận thưởng 1 tỷ đồng từ Agribank và Acecook Việt Nam. Trận chung kết lượt về sẽ diễn ra vào ngày 5/1/2025.
    """
    text_to_speech(content, audio_path)
    return content
