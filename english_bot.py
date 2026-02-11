import requests
import random
import os
from gtts import gTTS

CHAT_ID = "1017565295"
TOKEN = "8437253425:AAGWr8az2R6jqMprMhgBsYUQ3YCn4jcHf6o"

messages = [
    {
        "en": "I'm looking forward to meeting you.",
        "kr": "당신을 만나기를 고대하고 있어요.",
        "grammar": "look forward to + ~ing: 여기서 to는 전치사라 뒤에 동명사가 옵니다.",
        "phrases": ["I'm looking forward to it.", "She's looking forward to her trip.", "We look forward to it."]
    }
]

def run():
    pick = random.choice(messages)
    text = f"☀️ 오늘의 영어\n\n🇺🇸: `{pick['en']}`\n🇰🇷: {pick['kr']}\n\n💡 포인트: {pick['grammar']}"
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"})
    
    tts = gTTS(text=pick['en'], lang='en')
    tts.save("v.mp3")
    with open("v.mp3", "rb") as f:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendVoice", data={"chat_id": CHAT_ID}, files={"voice": f})
    os.remove("v.mp3")

if __name__ == "__main__":
    run()
