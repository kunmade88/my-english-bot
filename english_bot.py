import requests
import random
import os
from gtts import gTTS

# 1. 고유 정보 설정
CHAT_ID = "1017565295" 
TOKEN = "8437253425:AAGWr8az2R6jqMprMhgBsYUQ3YCn4jcHf6o"

# 2. 업그레이드된 학습 데이터
messages = [
    {
        "en": "I'm looking forward to meeting you.",
        "kr": "당신을 만나기를 고대하고 있어요.",
        "grammar": "look forward to + ~ing: 여기서 'to'는 전치사입니다. 뒤에 동사원형이 오면 안 되고 반드시 명사나 동명사(~ing)가 와야 해요!",
        "phrases": [
            "I'm looking forward to the weekend. (주말이 너무 기다려져요.)",
            "She's looking forward to her trip. (그녀는 여행을 고대하고 있어요.)",
            "We look forward to working with you. (함께 일하기를 기대합니다.)"
        ]
    },
    {
        "en": "Let's call it a day.",
        "kr": "오늘은 이만 합시다 (퇴근합시다).",
        "grammar": "call it a day: 하던 일을 멈추고 끝낼 때 쓰는 원어민 표현입니다. 퇴근할 때나 공부를 마칠 때 '이만하자'는 느낌으로 써요.",
        "phrases": [
            "It's already 6 PM. Let's call it a day. (벌써 6시네요. 퇴근합시다.)",
            "I'm too tired. Shall we call it a day? (너무 피곤한데 이만 할까요?)",
            "Let's call it a day and go grab some beer. (이만 하고 맥주나 마시러 가죠.)"
        ]
    },
    {
        "en": "You've got to make up your mind.",
        "kr": "이제 마음을 정해야 해요 (결정하세요).",
        "grammar": "make up one's mind: '결심하다'라는 뜻입니다. 여러 고민 끝에 최종적으로 마음을 굳혔을 때 자주 사용합니다.",
        "phrases": [
            "I can't make up my mind what to eat. (뭘 먹을지 결정을 못 하겠어.)",
            "Have you made up your mind yet? (벌써 결정했나요?)",
            "It's hard to make up my mind. (결정하기 참 어렵네요.)"
        ]
    }
]

def send_premium_english():
    # 랜덤으로 문장 하나 선택
    pick = random.choice(messages)
    
    # 3. 텍스트 메시지 구성 (Markdown 활용)
    text = (
        f"☀️ **오늘의 영어 공부**\n\n"
        f"🇺🇸 **Main:** `{pick['en']}`\n"
        f"🇰🇷 **뜻:** {pick['kr']}\n\n"
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

    # 4. 음성 파일 생성 (gTTS)
    try:
        tts = gTTS(text=pick['en'], lang='en')
        tts.save("today_voice.mp3")
        
        # 5. 텔레그램으로 전송
        # (1) 텍스트 전송
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
        
        # 임시 파일 삭제
        os.remove("today_voice.mp3")
        print("✅ 전송 완료!")
        
    except Exception as e:
        print(f"❌ 에러 발생: {e}")

if __name__ == "__main__":
    send_premium_english()
