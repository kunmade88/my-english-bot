import requests
import random
import os
from gtts import gTTS

# 설정 정보
CHAT_ID = "1017565295" 
TOKEN = "8437253425:AAGWr8az2R6jqMprMhgBsYUQ3YCn4jcHf6o"

# 학습 데이터
messages = [
    {
        "en": "I'm looking forward to meeting you.",
        "kr": "당신을 만나기를 고대하고 있어요.",
        "grammar": "look forward to + ~ing: 'to'가 전치사라 뒤에 동명사가 오는 게 핵심입니다.",
        "phrases": [
            "I'm looking forward to the weekend. (주말이 기다려져요.)",
            "She's looking forward to her trip. (그녀는 여행을 고대해요.)",
            "We look forward to working with you. (함께 일하길 기대합니다.)"
        ]
    }
]

def run():
    pick = random.choice(messages)
    text = (
        f"☀️ **오늘의 영어 공부**\n\n"
        f"🇺🇸 **Main:** `{pick['en']}`\n"
        f"🇰🇷 **뜻:** {pick['kr']}\n\n"
        f"💡 **문법 포인트:**\n{pick['grammar']}\n\n"
        f"🔥 **생활 표현:**\n• {pick['phrases'][0]}\n• {pick['phrases'][1]}\n• {pick['phrases'][2]}\n\n"
        f"오늘도 화이팅! 🚀"
    )

    # 텍스트 전송
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                  data={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"})

    # 음성 파일 생성 및 전송
    try:
        tts = gTTS(text=pick['en'], lang='en')
        tts.save("voice.mp3")
        with open("voice.mp3", "rb") as f:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendVoice", 
                          data={"chat_id": CHAT_ID}, files={"voice": f})
        os.remove("voice.mp3")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run()
