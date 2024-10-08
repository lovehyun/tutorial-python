import requests
import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# 카카오 API REST 키
KAKAO_RESTAPI_KEY = os.getenv("KAKAO_RESTAPI_KEY")

# KoGPT API 요청 URL
KOGPT_API_URL = "https://api.kakaobrain.com/v1/inference/kogpt/generation"

# 요청 헤더 설정
HEADERS = {
    "Authorization": f"KakaoAK {KAKAO_RESTAPI_KEY}",
    "Content-Type": "application/json"
}

# KoGPT API 호출 함수
def kogpt_api(prompt, max_tokens, temperature=1.0, top_p=1.0, n=1):
    data = {
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": top_p,
        "n": n
    }
    response = requests.post(KOGPT_API_URL, headers=HEADERS, json=data)
    return response.json()

# 1. 다음 문장 만들기 예제
print("---------- 1. 다음 문장 만들기 ----------")
prompt1 = "인간처럼 생각하고, 행동하는 '지능'을 통해 인류가 이제까지 풀지 못했던"
response1 = kogpt_api(prompt1, max_tokens=64, temperature=0.7, top_p=0.8)
print("다음 문장 만들기 결과:", response1)
# print("결과 텍스트:", response1['generations'][0]['text'])
print("----------------------------------------\n")

# 2. 문장 분류하기 예제
print("---------- 2. 문장 분류하기 ----------")
prompt2 = '''상품 후기를 긍정 또는 부정으로 분류합니다.
가격대비좀 부족한게많은듯=부정
재구매 친구들이 좋은 향 난다고 해요=긍정
ㅠㅠ약간 후회가 됩니다..=부정
이전에 먹고 만족해서 재구매합니다=긍정
튼튼하고 잘 쓸수 있을 것 같습니다. 이 가격에 이 퀄리티면 훌륭하죠='''
response2 = kogpt_api(prompt2, max_tokens=1, temperature=0.4)
print("문장 분류하기 결과:", response2)
print("--------------------------------------\n")

# user_input = input("상품평 후기를 입력해주세요: ")
# prompt=f'''상품 후기를 긍정 또는 부정으로 분류합니다.
# 가격대비좀 부족한게많은듯=부정
# 재구매 친구들이 좋은 향 난다고 해요=긍정
# ㅠㅠ약간 후회가 됩니다..=부정
# 이전에 먹고 만족해서 재구매합니다=긍정
# {user_input}='''
# response2 = kogpt_api(prompt2, max_tokens=2, temperature=0.1)
# print("상품평 후기 감정분석:", response2)


# 3. 뉴스 한 줄 요약하기 예제
print("---------- 3. 뉴스 한 줄 요약하기 ----------")
prompt3 = '''카카오(대표이사 정신아)의 카카오프렌즈가 서울페스타 2024에 참여한다고 29일 밝혔다. 서울페스타는 서울시에서 주최하는 서울 대표 봄축제로 서울의 다양한 매력을 전 세계에 홍보하는 행사다. 카카오는 황금연휴 기간 서울 곳곳에서 카카오프렌즈를 활용한 행사로 나들이객들과 관광객들에게 색다른 즐거움을 선사할 계획이다.
먼저, 카카오는 5월 1일부터 6일까지 광화문광장에서 라이언과 춘식이로 꾸며진 포토존을 운영한다. 6m가 넘는 초대형 라이언과 춘식이 애드벌룬이 설치돼 축제 분위기를 한껏 살릴 예정이며, 라이언과 춘식이가 그려진 포토카드를 나눠주는 이벤트도 진행한다. 포토카드는 4일을 제외한 매일 11시부터 포토존 앞에서 선착순으로 배부한다.
또한, ‘프렌즈와 떠나는 별빛 여행’을 주제로 한강 드론 라이트 쇼를 선보인다. 1,000여 대의 드론이 라이언과 춘식이의 탄생 세계관과 K-컬처를 즐기는 라이언과 춘식이의 모습을 그려내며 한강의 밤하늘을 수놓을 예정이다. 5월 6일 저녁 8시 잠실한강공원에서 관람 가능하며, 자세한 내용은 라이언&춘식 인스타그램에서 확인할 수 있다.
한편, 카카오톡 ‘펑’에서 ‘라이언 서울로컬로드’ 콘텐츠도 연재한다. 광화문, 잠실을 시작으로 라이언이 서울의 다양한 지역을 직접 방문하고 소개하는 일상 공유 콘텐츠를 통해 팬들과 실시간으로 소통할 예정이다.
최선 카카오 프렌즈크리에이티브 리더는 “K-캐릭터인 카카오프렌즈의 매력을 서울 곳곳에서 발견할 수 있도록 이번 행사를 준비했다” 며 “앞으로도 시민들의 일상 속에 더 가까이 다가갈 수 있도록 카카오프렌즈의 다양한 활동들을 전개할 예정이니 많은 기대 바란다” 라고 전했다.

한줄 요약:'''
response3 = kogpt_api(prompt3, max_tokens=64, temperature=0.1)
print("뉴스 한 줄 요약하기 결과:", response3)
print("--------------------------------------------\n")

# 4. 질문에 답변하기 예제
print("---------- 4. 질문에 답변하기 ----------")
prompt4 = '''의료 스타트업으로 구성된 원격의료산업협의회가 10월부터 열리는 국정감사 시기에 맞춰 국회와 정부에 비대면 진료법 근거 마련을 촉구하는 정책제안서를 제출한다. 코로나19 사태에 비대면 진료의 한시 허용으로 원격 진료, 의약품 배송 등 서비스가 속속 등장하는 가운데 제도화 논의를 서둘러야 한다는 목소리가 높아질 것으로 전망된다. 코리아스타트업포럼 산하 원격의료산업협의회는 '위드(with) 코로나' 방역 체계 전환을 염두에 두고 비대면 진료 제도화 촉구를 위한 공동 대응 작업을 추진하고 있다. 협의회는 닥터나우, 엠디스퀘어, SH바이오, 메디버디 등 의료 스타트업 13개사로 구성됐다. 협의회는 국정감사 시기를 겨냥해 국회와 주무 부처인 보건복지부에 비대면 진료의 법적 근거 마련을 촉구할 방침이다. 이를 위해 주요 의원실과 관련 의견을 교환하고 있다. 협의회는 궁극적으로 의료법과 약사법 개정이 필요하지만 의료법 테두리 안에서 시행령 개정 등으로도 비대면 진료 가능성과 대상·의료기관 등을 구체화할 수 있다는 복안이다. 복지부 장관령으로 비대면 진료 기간을 명시하는 방안 등을 통해 사업 리스크도 줄일 수 있다. 올해 안에 국내 방역체계 패러다임이 바뀔 것으로 예상되는 점도 비대면 진료 제도화의 필요성을 높이고 있다. 최근 코로나19 백신 접종이 속도를 내면서 방역 당국은 위드 코로나 방역체계 전환을 고려하고 있다. 인구 대비 백신 접종 완료율이 70%가 되는 오는 10월 말에는 전환 논의가 수면 위로 뜰 것으로 보인다.
정책제안서를 제출하는 시기는 언제인가?:'''
response4 = kogpt_api(prompt4, max_tokens=128, temperature=0.2)
print("질문에 답변하기 결과:", response4)
print("----------------------------------------\n")

# 5. 특정 정보 추려내기 예제
print("---------- 5. 특정 정보 추려내기 ----------")
prompt5 = '''임진왜란(壬辰倭亂)은 1592년(선조 25년) 도요토미 정권이 조선을 침략하면서 발발하여 1598년(선조 31년)까지 이어진 전쟁이다. 또한 임진왜란은 동아시아에 막대한 영향을 끼쳤으며, 두번의 침입이 있어서 제2차 침략은 정유재란이라 따로 부르기도 한다. 또한 이때 조선은 경복궁과 창덕궁 등 2개의 궁궐이 소실되었으며 약 백만명의 인구가 소실되었다.

명칭
일반적으로 임진년에 일어난 왜의 난리란 뜻으로 지칭되며 그 밖에 조선과 일본 사이에 일어난 전쟁이란 뜻에서 조일전쟁(朝日戰爭), 임진년에 일어난 전쟁이란 뜻에서 임진전쟁(壬辰戰爭), 도자기공들이 일본으로 납치된 후 일본에 도자기 문화가 전파되었다 하여 도자기 전쟁(陶瓷器戰爭)이라고도 한다. 일본에서는 당시 연호를 따서 분로쿠의 역(일본어: 文禄の役 분로쿠노에키[*])이라 하며, 중화인민공화국과 중화민국에서는 당시 명나라 황제였던 만력제의 호를 따 만력조선전쟁(萬曆朝鮮戰爭, 중국어: 萬曆朝鮮之役), 혹은 조선을 도와 왜와 싸웠다 하여 항왜원조(抗倭援朝)라고도 하며, 조선민주주의인민공화국에서는 임진조국전쟁(壬辰祖國戰爭)이라고 한다. 그밖에도 7년간의 전쟁이라 하여 7년 전쟁(七年戰爭)으로도 부른다.

임진왜란 때 조선의 왕은?

답:'''
response5 = kogpt_api(prompt5, max_tokens=1, temperature=0.3)
print("특정 정보 추려내기 결과:", response5)
print("----------------------------------------\n")

# 6. 말투 바꾸기 예제
print("---------- 6. 말투 바꾸기 ----------")
prompt6 = '''주어진 문장을 존댓말 문장으로 바꿔주세요.

문장:하지마!
존댓말:하지 말아주세요.

문장:나랑 같이 놀러가자
존댓말:저랑 같이 놀러가지 않으실래요?

문장:배고파 밥줘
존댓말:배가고픈데 밥을 먹어도 될까요?

문장:그거 재밌어?
존댓말:그것은 재미 있나요?

문장:뭐하는거야 지금
존댓말:지금 무엇을 하시는 건가요?

문장:당장 제자리에 돌려놔
존댓말:'''
response6 = kogpt_api(prompt6, max_tokens=10, temperature=0.7)
print("말투 바꾸기 결과:", response6)
print("----------------------------------------\n")

# 7. 채팅하기 예제
print("---------- 7. 채팅하기 ----------")
prompt7 = '''정보:거주지 서울, 나이 30대, 성별 남자, 자녀 두 명, 전공 인공지능, 말투 친절함
정보를 바탕으로 질문에 답하세요.
Q:안녕하세요 반갑습니다. 자기소개 부탁드려도 될까요?
A:안녕하세요. 저는 서울에 거주하고 있는 30대 남성입니다.
Q:오 그렇군요, 결혼은 하셨나요?
A:'''
response7 = kogpt_api(prompt7, max_tokens=32, temperature=0.3, top_p=0.85)
print("채팅하기 결과:", response7)
print("----------------------------------------\n")
