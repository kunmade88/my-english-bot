import requests
import random
import os
from gtts import gTTS

# 1. 기본 정보 설정
CHAT_ID = "1017565295" 
TOKEN = "8437253425:AAGWr8az2R6jqMprMhgBsYUQ3YCn4jcHf6o"

# 2. 고퀄리티 영어 학습 데이터 (여기에 공부하고 싶은 문장을 계속 추가하세요!)
messages = [
    {
        "en": "I'm looking forward to meeting you.",
        "kr": "당신을 만나기를 고대하고 있어요.",
        "grammar": "look forward to + 명사/동명사(~ing): '~를 간절히 기다리다'라는 뜻입니다. 여기서 'to'는 전치사이기 때문에 뒤에 동사원형이 오면 안 된다는 게 핵심 포인트!",
        "phrases": [
            "I'm looking forward to the weekend. (주말이 너무 기다려져요.)",
            "She's looking forward to her trip. (그녀는 여행을 고대하고 있어요.)",
            "We look forward to working with you. (함께 일하기를 기대합니다.)"
        ]
    },
    {
        "en": "You've got to make up your mind.",
        "kr": "이제 마음을 정해야 해요.",
        "grammar": "make up one's mind: '결심하다(decide)'의 아주 흔한 구어체 표현입니다. 단순히 결정하는 것을 넘어, 고민 끝에 마음을 정했다는 뉘앙스가 강해요.",
        "phrases": [
            "I can't make up my mind what to eat. (뭘 먹을지 결정을 못 하겠어.)",
            "Have you made up your mind yet? (벌써 결정했나요?)",
            "It's hard to make up my mind. (결정하기 참 어렵네요.)"
        ]
    },
    {
        "en": "Let's call it a day.",
        "kr": "오늘은 이만 하죠 (마칩시다).",
        "grammar": "call it a day: 하던 일을 멈추고 끝내려 할 때 쓰는 아주 유용한 표현입니다. 주로 퇴근하거나 공부를 마칠 때 '이만하자!'라는 느낌으로 써요.",
        "phrases": [
            "I'm exhausted. Let's call it a day. (너무 피곤하다. 오늘은 여기까지만 하자.)",
            "We've done enough. Let's call it a day. (할 만큼 했어. 이만 마칩시다.)",
            "Wait! Don't call it a day yet. (잠깐! 아직 끝내지 마세요.)"
        ]
    }
]

def send_premium_english():
    # 데이터 중 하나 선택
    pick = random.choice(messages)
    
    # 3. 텍스트 메시지 구성 (가독성 좋게 꾸미기)
    text = (
        f"☀️ **오늘의 영어 한 문장**\n\n"
        f"🇺🇸 **Main:** `{pick['en']}`\n"
        f"🇰🇷 **Meaning:** {pick['kr']}\n\n"
        f"━━━━━━━━━━━━━━\n"
        f"💡 **핵심 포인트 (Grammar)**\n"
        f"{pick['grammar']}\n\n"
        f"🔥 **실생활 활용 (Life Expressions)**\n"
        f"• {pick['phrases'][0]}\n"
        f"• {pick['phrases'][1]}\n"
        f"• {pick['phrases'][2]}\n"
        f"━━━━━━━━━━━━━━\n\n"
        f"오늘도 성장하는 하루 되세요! 💪"
    )

    # 4. 음성 파일 생성 (gTTS 활용)
    # 핵심 문장(en)을 영어(en) 원어민 발음으로 변환
    tts = gTTS(text=pick['en'], lang='en')
    tts.save("today_voice.mp3")

    # 5. 텔레그램 전송
    # (1) 텍스트 메시지 전송
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
        data={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    )
    
    # (2) 음성 파일(.mp3) 전송
    with open("today_voice.mp3", "rb") as audio:
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendVoice", 
            data={"chat_id": CHAT_ID}, 
            files={"voice": audio}
        )
    
    # 임시 생성된 음성 파일 삭제
    if os.path.exists("today_voice.mp3"):
        os.remove("today_voice.mp3")

if __name__ == "__main__":
    send_premium_english()
