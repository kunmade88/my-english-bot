import requests
import random
import os
from gtts import gTTS

# 설정 정보
CHAT_ID = "1017565295"
TOKEN = "8437253425:AAGWr8az2R6jqMprMhgBsYUQ3YCn4jcHf6o"

# 화장품 연구원 전용 문장 데이터 (박람회 실전용)
messages = [
    # 1. Appearance & Pickup (외관 및 첫인상)
    {
        "en": "This formula has a bouncy, jelly-like texture that is fun to touch.",
        "kr": "이 제형은 만지기 즐거운 탄력 있는 젤리 같은 질감입니다.",
        "grammar": "Bouncy/Jelly-like: 형용사를 나열하여 시각적, 촉각적 이미지를 동시에 전달합니다.",
        "phrases": ["It has a bouncy feel.", "The texture is jelly-like.", "Fun-to-touch consistency."]
    },
    {
        "en": "It features a unique shape-memory technology.",
        "kr": "이 제품은 독특한 형상 기억 기술이 특징입니다.",
        "grammar": "Feature: '~을 특징으로 하다'. 제품의 핵심 기술을 소개할 때 쓰는 동사입니다.",
        "phrases": ["Features a patented tech.", "What features does it have?", "Unique features of this cream."]
    },
    {
        "en": "The water-to-serum transformation provides an instant cooling sensation.",
        "kr": "워터-투-세럼 변환 제형이 즉각적인 쿨링감을 줍니다.",
        "grammar": "[A]-to-[B] transformation: A에서 B로의 제형 변화를 나타내는 명사구입니다.",
        "phrases": ["Oil-to-milk transformation.", "Balm-to-oil texture.", "Instant cooling effect."]
    },
    {
        "en": "It’s an anhydrous formulation, meaning it’s water-free for higher stability.",
        "kr": "성분 안정성을 위해 물을 포함하지 않은 무수 제형입니다.",
        "grammar": "Anhydrous: '무수의'. 전문 용어를 쓴 뒤 'meaning~'으로 쉽게 풀어 설명하는 구조입니다.",
        "phrases": ["Water-free formula.", "Higher stability achieved.", "Preservative-free anhydrous balm."]
    },
    {
        "en": "This sorbet-textured balm melts instantly upon contact with the skin.",
        "kr": "이 샤베트 질감의 밤은 피부에 닿자마자 즉시 녹아듭니다.",
        "grammar": "Upon contact with: '~와 닿자마자'. 반응 속도를 강조할 때 쓰는 고급 표현입니다.",
        "phrases": ["Melts upon contact.", "Cooling upon application.", "Active upon contact."]
    },
    {
        "en": "It has a cloud-like, airy consistency.",
        "kr": "구름처럼 가볍고 공기 같은 질감을 가지고 있습니다.",
        "grammar": "Airy consistency: 질감이 매우 가벼움을 뜻하는 전문적인 묘사입니다.",
        "phrases": ["Lightweight consistency.", "Airy feel on skin.", "Cloud-like soft texture."]
    },
    {
        "en": "We’ve achieved a crystal-clear aesthetic without compromising viscosity.",
        "kr": "점도를 유지하면서도 수정처럼 투명한 외관을 구현했습니다.",
        "grammar": "Without compromising: '~을 해치지(타협하지) 않으면서'. 두 가지 장점을 다 잡았을 때 씁니다.",
        "phrases": ["Without compromising safety.", "Clear without compromising efficacy.", "Achieved high gloss."]
    },
    {
        "en": "The encapsulated active ingredients are visible in the gel base.",
        "kr": "젤 베이스 안에 캡슐화된 활성 성분이 눈에 보입니다.",
        "grammar": "Encapsulated: 캡슐화된. 성분 보호 기술을 강조할 때 쓰는 과거분사 형용사입니다.",
        "phrases": ["Visible actives.", "Encapsulated vitamins.", "Stabilized in the gel."]
    },
    {
        "en": "This is a high-viscosity cream that doesn't feel heavy.",
        "kr": "무겁지 않은 고점도 크림입니다.",
        "grammar": "High-viscosity: 고점도의. 'Heavy'와 반대되는 사용감을 대조시켰습니다.",
        "phrases": ["Low-viscosity lotion.", "Adjusting the viscosity.", "Rich but not heavy."]
    },
    {
        "en": "It’s a biphasic formula that needs to be shaken before use.",
        "kr": "사용 전 흔들어 쓰는 이층상 제형입니다.",
        "grammar": "Biphasic: 이층상의(물+오일 등). 'Need to be shaken'은 수동태로 사용 지침을 전달합니다.",
        "phrases": ["Shake it well.", "Separated layers.", "Oil and water phases."]
    },

    # 2. Playtime & Spreadability (발림성)
    {
        "en": "It offers an effortless glide across the skin surface.",
        "kr": "피부 표면에서 아주 부드럽게 미끄러지듯 발립니다.",
        "grammar": "Effortless glide: 힘들이지 않아도 매끄럽게 발리는 최상의 발림성을 뜻합니다.",
        "phrases": ["Glides on smoothly.", "Smooth glide.", "Superior glide properties."]
    },
    {
        "en": "The spreadability is optimized for facial massage.",
        "kr": "마사지에 적합하도록 발림성을 최적화했습니다.",
        "grammar": "Be optimized for: '~에 최적화되다'. 목적에 따른 설계를 강조합니다.",
        "phrases": ["Optimized for dry skin.", "Optimized absorption.", "Good spreadability."]
    },
    {
        "en": "You can feel the velvety smooth playtime during application.",
        "kr": "도포하는 동안 벨벳처럼 부드러운 사용감을 느끼실 수 있습니다.",
        "grammar": "Playtime: 화장품이 완전히 흡수되기 전까지 문지를 수 있는 시간/느낌을 뜻하는 업계 용어입니다.",
        "phrases": ["Long playtime.", "Velvety after-feel.", "During application."]
    },
    {
        "en": "It has a fast-absorbing, non-pilling formula.",
        "kr": "빠르게 흡수되며 밀리지 않는 포뮬러입니다.",
        "grammar": "Non-pilling: 밀림 현상(때처럼 나오는 것)이 없는 기술적 강점입니다.",
        "phrases": ["Absorbs instantly.", "No pilling issues.", "Layering without pilling."]
    },
    {
        "en": "This serum breaks into water droplets as you rub it in.",
        "kr": "문지르면 물방울이 터져 나오는 제형입니다.",
        "grammar": "Rub it in: 문질러 바르다. 'Break into'와 결합해 제형의 변화를 묘사합니다.",
        "phrases": ["Rub gently.", "Breaks upon rubbing.", "Water droplets appear."]
    },
    {
        "en": "It provides a sheer, weightless coverage.",
        "kr": "투명하고 무게감 없는 커버력을 선사합니다.",
        "grammar": "Sheer: 아주 얇고 투명한. 'Weightless'와 결합해 자연스러운 느낌을 줍니다.",
        "phrases": ["Sheer finish.", "Weightless texture.", "Full coverage."]
    },
    {
        "en": "The viscosity drops upon application for a refreshing finish.",
        "kr": "바르는 순간 점도가 낮아지며 산뜻하게 마무리됩니다.",
        "grammar": "Viscosity drops: 점도가 떨어진다. 셔벗 제형이 액체로 변하는 현상을 뜻합니다.",
        "phrases": ["Refreshing feel.", "Sudden viscosity drop.", "Cooling finish."]
    },
    {
        "en": "It creates a breathable, thin film on the skin.",
        "kr": "피부에 답답하지 않은 얇은 막을 형성합니다.",
        "grammar": "Breathable: '숨 쉴 수 있는'. 막 형성제(Film former)가 답답하지 않음을 강조합니다.",
        "phrases": ["Thin film formation.", "Breathable layer.", "Protective film."]
    },
    {
        "en": "We used natural-derived emollients for a silkier touch.",
        "kr": "더 실키한 촉감을 위해 천연 유래 에몰리언트를 사용했습니다.",
        "grammar": "Natural-derived: 천연에서 유래한. 성분의 기원을 강조하는 형용사구입니다.",
        "phrases": ["Derived from plants.", "Silky touch.", "Emollient properties."]
    },
    {
        "en": "The emulsion stability is maintained even at high temperatures.",
        "kr": "고온에서도 에멀젼 안정성이 유지됩니다.",
        "grammar": "Even at: '~조차도'. 가혹 조건에서도 안정하다는 점을 어필합니다.",
        "phrases": ["Formula stability.", "High temperature test.", "Maintains texture."]
    },

    # 3. After-feel & Finish (마무리감)
    {
        "en": "It leaves a dewy, glass-skin finish.",
        "kr": "촉촉하고 투명한 '유리 피부' 마무리감을 남깁니다.",
        "grammar": "Glass-skin: 한국식 뷰티 트렌드인 '광채 피부'를 뜻하는 전 세계 공통어입니다.",
        "phrases": ["Dewy look.", "Achieve glass skin.", "Glowing finish."]
    },
    {
        "en": "Experience a powdery, matte after-feel without dryness.",
        "kr": "건조함 없이 보송하고 매트한 마무리감을 경험해 보세요.",
        "grammar": "After-feel: 바르고 난 뒤 남는 감촉. 박람회에서 가장 많이 쓰는 단어 중 하나입니다.",
        "phrases": ["Matte finish.", "No dryness.", "Smooth after-feel."]
    },
    {
        "en": "It provides long-lasting hydration without any stickiness.",
        "kr": "끈적임 없는 장시간 보습을 제공합니다.",
        "grammar": "Long-lasting: 지속력이 좋은. 'Stickiness(끈적임)'는 고객들이 가장 기피하는 요소입니다.",
        "phrases": ["Non-sticky.", "24-hour hydration.", "Provides moisture."]
    },
    {
        "en": "The skin feels plump and supple immediately after use.",
        "kr": "사용 직후 피부가 탱탱하고 유연해지는 것을 느낄 수 있습니다.",
        "grammar": "Plump and supple: 화장품 효능을 설명할 때 '탱탱함'과 '부드러움'을 뜻하는 짝꿍 단어입니다.",
        "phrases": ["Plumping effect.", "Supple skin.", "Soft to touch."]
    },
    {
        "en": "It doesn't leave any greasy residue.",
        "kr": "끈적이는 잔여물을 남기지 않습니다.",
        "grammar": "Greasy residue: 기름진 잔여물. 오일감이 남지 않음을 강조할 때 씁니다.",
        "phrases": ["No residue.", "Clean finish.", "Non-greasy."]
    },
    {
        "en": "It gives a natural, healthy glow to the complexion.",
        "kr": "안색에 자연스럽고 건강한 광채를 부여합니다.",
        "grammar": "Glow to the complexion: 안색에 광채를 더하다. 색조나 기초 제품 공통 표현입니다.",
        "phrases": ["Healthy glow.", "Brighten complexion.", "Natural radiance."]
    },
    {
        "en": "The silky-smooth finish acts as a perfect primer for makeup.",
        "kr": "실키한 마무리가 메이크업을 위한 완벽한 프라이머 역할을 합니다.",
        "grammar": "Act as: '~로서 역할을 하다'. 제품의 다기능성을 설명할 때 유용합니다.",
        "phrases": ["Acts as a barrier.", "Primer effect.", "Silky finish."]
    },
    {
        "en": "It provides an instant blurring effect on pores.",
        "kr": "모공을 즉각적으로 가려주는 블러링 효과가 있습니다.",
        "grammar": "Blurring effect: 포토샵의 블러 처리처럼 모공/요철을 매끄럽게 보이게 하는 효과입니다.",
        "phrases": ["Blur pores.", "Instant effect.", "Smooth surface."]
    },
    {
        "en": "You’ll notice a cooling and soothing sensation.",
        "kr": "쿨링감과 진정 효과를 느끼실 수 있습니다.",
        "grammar": "Sensation: 피부로 느껴지는 구체적인 감각을 뜻합니다.",
        "phrases": ["Soothing effect.", "Cooling sensation.", "Feel the difference."]
    },
    {
        "en": "It strengthens the skin barrier with an occlusive layer.",
        "kr": "밀폐막을 통해 피부 장벽을 강화합니다.",
        "grammar": "Occlusive layer: 수분 증발을 막는 차단막. 연구원들이 자주 쓰는 전문 용어입니다.",
        "phrases": ["Barrier support.", "Occlusive property.", "Strengthen skin."]
    },

    # 4. Trends & Technology (트렌드/기술)
    {
        "en": "This is a Clean Beauty compliant formulation.",
        "kr": "클린 뷰티 기준을 준수하는 제형입니다.",
        "grammar": "Compliant: (규정 등을) 준수하는. 클린 뷰티 가이드라인에 맞췄음을 뜻합니다.",
        "phrases": ["Compliant with EU.", "Clean Beauty standards.", "Safety compliant."]
    },
    {
        "en": "We focused on Barrier Support using a ceramide complex.",
        "kr": "세라마이드 복합체를 사용해 장벽 지원에 집중했습니다.",
        "grammar": "Focus on: '~에 집중하다'. 개발 의도를 설명할 때 씁니다.",
        "phrases": ["Focused on hydration.", "Barrier repair.", "Ceramide based."]
    },
    {
        "en": "This product targets the Skin Microbiome balance.",
        "kr": "이 제품은 스킨 마이크로바이옴 균형을 타겟으로 합니다.",
        "grammar": "Target: '~을 목표로 하다'. 특정 효능이나 타겟 시장을 말할 때 씁니다.",
        "phrases": ["Target wrinkles.", "Microbiome care.", "Balanced skin."]
    },
    {
        "en": "It’s formulated with Exosomes for advanced regenerative care.",
        "kr": "최첨단 재생 케어를 위해 엑소좀을 배합했습니다.",
        "grammar": "Formulated with: '~가 배합된/처방된'. 주요 성분을 소개할 때 쓰는 정석 표현입니다.",
        "phrases": ["Formulated with Cica.", "Exosome technology.", "Regenerative care."]
    },
    {
        "en": "We emphasize Sustainable Sourcing for all raw materials.",
        "kr": "모든 원료의 지속 가능한 소싱을 강조합니다.",
        "grammar": "Emphasize: '강조하다'. 회사의 철학이나 제품의 특징을 부각합니다.",
        "phrases": ["Sustainable ingredients.", "Eco-friendly sourcing.", "Raw material quality."]
    },
    {
        "en": "This is a Multi-functional product (All-in-one).",
        "kr": "이것은 다기능성(올인원) 제품입니다.",
        "grammar": "Multi-functional: 다기능의. 스킵케어 트렌드와 연결되는 핵심어입니다.",
        "phrases": ["All-in-one care.", "Multi-purpose cream.", "Time-saving product."]
    },
    {
        "en": "It’s a Vegan-certified formula.",
        "kr": "비건 인증을 받은 포뮬러입니다.",
        "grammar": "Vegan-certified: 비건 인증 기관의 검증을 통과했음을 뜻합니다.",
        "phrases": ["Certified vegan.", "Cruelty-free.", "No animal testing."]
    },
    {
        "en": "We’ve achieved High Efficacy with minimal ingredients.",
        "kr": "최소한의 성분으로 높은 효능을 구현했습니다.",
        "grammar": "Minimal ingredients: 성분 다이어트(Minimalism) 트렌드를 반영한 표현입니다.",
        "phrases": ["High efficacy.", "Less is more.", "Key actives only."]
    },
    {
        "en": "This is an Anti-pollution shield for urban skin.",
        "kr": "도시 피부를 위한 안티 폴루션 보호막입니다.",
        "grammar": "Shield: '방패/보호막'. 외부 유해 환경으로부터 피부를 보호한다는 은유적 표현입니다.",
        "phrases": ["Urban protection.", "Pollution shield.", "Protect from dust."]
    },
    {
        "en": "It features Slow-aging benefits for a youthful look.",
        "kr": "젊은 피부를 위한 슬로우 에이징 혜택이 특징입니다.",
        "grammar": "Slow-aging: Anti-aging 대신 쓰이는 긍정적이고 트렌디한 노화 방지 용어입니다.",
        "phrases": ["Youthful look.", "Slow aging trend.", "Prevention care."]
    },

    # 5. Researcher's Pitch (전문적 설명)
    {
        "en": "Our goal was to balance sensoriality and stability.",
        "kr": "저희의 목표는 사용감과 안정성의 균형을 맞추는 것이었습니다.",
        "grammar": "Balance [A] and [B]: 연구원으로서 가장 힘든 '사용감과 안정성' 사이의 균형을 말합니다.",
        "phrases": ["Sensoriality.", "Formula stability.", "Hard to balance."]
    },
    {
        "en": "We utilized a cold-process emulsification to save energy.",
        "kr": "에너지 절감을 위해 저온 유화 공법을 활용했습니다.",
        "grammar": "Cold-process: 가열하지 않는 공정. 친환경 기술(Eco-tech) 어필용입니다.",
        "phrases": ["Save energy.", "Emulsification process.", "Utilize cold tech."]
    },
    {
        "en": "The particle size is minimized for deeper penetration.",
        "kr": "더 깊은 흡수를 위해 입자 크기를 최소화했습니다.",
        "grammar": "Minimize: 최소화하다. 나노 기술이나 흡수력 강화 기술 설명에 필수입니다.",
        "phrases": ["Deeper penetration.", "Miniaturized particles.", "Better absorption."]
    },
    {
        "en": "This formula is dermatologically tested for sensitive skin.",
        "kr": "민감성 피부를 위해 피부과 테스트를 거친 제형입니다.",
        "grammar": "Dermatologically tested: '피부과 테스트 완료'. 신뢰도를 높여주는 문구입니다.",
        "phrases": ["Hypoallergenic.", "Sensitive skin safe.", "Clinically tested."]
    },
    {
        "en": "We’ve optimized the pH balance for optimal skin health.",
        "kr": "피부 건강을 위해 최적의 pH 밸런스를 맞췄습니다.",
        "grammar": "Optimal: '최적의'. 약산성 제형 등을 설명할 때 쓰는 단어입니다.",
        "phrases": ["pH balanced.", "Skin health.", "Optimal result."]
    },
    {
        "en": "The synergy between the active ingredients is maximized.",
        "kr": "활성 성분 간의 시너지를 극대화했습니다.",
        "grammar": "Synergy: 성분 간의 궁합. 'Maximize(극대화하다)'와 찰떡궁합입니다.",
        "phrases": ["Ingredient synergy.", "Maximized efficacy.", "Combined power."]
    },
    {
        "en": "It’s a micro-plastic free formulation.",
        "kr": "미세 플라스틱이 없는 제형입니다.",
        "grammar": "[Something]-free: '~가 없는'. 클린 뷰티에서 가장 중요한 표현 방식입니다.",
        "phrases": ["Micro-plastic free.", "Silicone-free.", "Sulfate-free."]
    },
    {
        "en": "We used a patented delivery system for the actives.",
        "kr": "활성 성분을 위해 특허받은 전달 시스템을 사용했습니다.",
        "grammar": "Patented delivery system: 리포좀 등 성분을 피부 깊숙이 전달하는 특허 기술을 뜻합니다.",
        "phrases": ["Active delivery.", "Patented technology.", "Skin delivery."]
    },
    {
        "en": "This texture was inspired by K-Beauty’s 'Glass Skin' trend.",
        "kr": "이 제형은 K-뷰티의 '유리 피부' 트렌드에서 영감을 받았습니다.",
        "grammar": "Inspired by: '~에서 영감을 받은'. 제품 기획 배경을 설명할 때 씁니다.",
        "phrases": ["Inspired by nature.", "K-Beauty trend.", "Texture design."]
    },
    {
        "en": "We are leading the way in Eco-friendly formulation design.",
        "kr": "저희는 친환경 제형 설계의 앞장서고 있습니다.",
        "grammar": "Leading the way in: 특정 분야의 선구자임을 나타낼 때 쓰는 자신감 있는 표현입니다.",
        "phrases": ["Eco-friendly.", "Lead the market.", "Green chemistry."]
    }
]

def run():
    pick = random.choice(messages)
    
    # 텔레그램 메시지 꾸미기
    text = (
        f"🧪 **[Lab Note] 오늘의 연구원 영어**\n\n"
        f"🇺🇸 **Main:** `{pick['en']}`\n"
        f"🇰🇷 **뜻:** {pick['kr']}\n\n"
        f"━━━━━━━━━━━━━━\n"
        f"💡 **핵심 구동사 & 패턴**\n"
        f"{pick['grammar']}\n\n"
        f"🔥 **현장 응용 표현**\n"
        f"• {pick['phrases'][0]}\n"
        f"• {pick['phrases'][1]}\n"
        f"• {pick['phrases'][2]}\n"
        f"━━━━━━━━━━━━━━\n\n"
        f"박람회 대박 나세요! 화이팅! 💪"
    )

    # 1. 텍스트 전송
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                  data={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"})

    # 2. 음성 생성 및 전송
    try:
        tts = gTTS(text=pick['en'], lang='en')
        tts.save("v.mp3")
        with open("v.mp3", "rb") as f:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendVoice", 
                          data={"chat_id": CHAT_ID}, files={"voice": f})
        os.remove("v.mp3")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run()
