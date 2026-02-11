import requests
import random

# 사용자님의 정보 (수정 완료)
CHAT_ID = "1017565295" 
TOKEN = "8437253425:AAGWr8az2R6jqMprMhgBsYUQ3YCn4jcHf6o"

# 매일 돌아가며 나올 영어 문장들 (원하시는 대로 계속 추가 가능!)
messages = [
    {"en": "Consistency is the key to success.", "kr": "꾸준함이 성공의 열쇠입니다."},
    {"en": "The best way to predict the future is to create it.", "kr": "미래를 예측하는 가장 좋은 방법은 그것을 만드는 것입니다."},
    {"en": "Believe in yourself.", "kr": "자기 자신을 믿으세요."},
    {"en": "Every day is a second chance.", "kr": "매일은 두 번째 기회입니다."}
]

def send_daily_english():
    pick = random.choice(messages)
    text = f"☀️ 오늘의 영어 한 문장\n\n🇺🇸: {pick['en']}\n🇰🇷: {pick['kr']}\n\n오늘도 화이팅하세요! 🔥"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

if __name__ == "__main__":
    send_daily_english()
