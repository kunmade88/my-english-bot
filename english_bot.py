import requests
import random

# 정보 입력
TELEGRAM_TOKEN = '8437253425:AAGWr8az2R6jqMprMhgBsYUQ3YCn4jcHf6o'
CHAT_ID = '7605258280' # 사용자님의 텔레그램 ID

# 오늘의 영어 문장 후보들
contents = [
    {"en": "Consistency is more important than perfection.", "kr": "꾸준함이 완벽함보다 중요하다."},
    {"en": "Keep pushing forward.", "kr": "계속 앞으로 나아가세요."},
    {"en": "Small steps lead to big changes.", "kr": "작은 발걸음이 큰 변화를 만든다."},
    {"en": "Believe in yourself.", "kr": "당신 자신을 믿으세요."}
]

def send_message():
    item = random.choice(contents)
    text = f"☀️ 오늘의 영어 공부\n\n🇺🇸: {item['en']}\n🇰🇷: {item['kr']}\n\n오늘도 멋진 하루 되세요! ✨"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

if __name__ == "__main__":
    send_message()
