from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv('../../.env')

# OpenAI 셋업
openai_api_key = os.environ.get('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)

# 각 학년별 커리큘럼 데이터
curriculums = {
    1: ["기초 인사", "간단한 문장", "동물 이름"],
    2: ["학교 생활", "가족 소개", "자기 소개"],
    3: ["취미와 운동", "날씨 묘사", "간단한 이야기"],
    4: ["쇼핑과 가격", "음식 주문", "여행 이야기"],
    5: ["역사와 문화", "과학과 자연", "사회 이슈"],
    6: ["미래 계획", "진로 탐색", "세계 여행"]
}

@app.route('/')
def home():
    return render_template('home.html', grades=curriculums.keys())

@app.route('/grade/<int:grade>')
def grade(grade):
    if grade in curriculums:
        curriculums_with_index = list(enumerate(curriculums[grade]))
        return render_template('grade.html', grade=grade, curriculums=curriculums_with_index, grades=curriculums.keys(), current_grade=grade)
    return "해당 학년은 존재하지 않습니다.", 404

@app.route('/grade/<int:grade>/curriculum/<int:curriculum_id>', methods=['GET', 'POST'])
def curriculum(grade, curriculum_id):
    if grade in curriculums and 0 <= curriculum_id < len(curriculums[grade]):
        curriculum_title = curriculums[grade][curriculum_id]
        if request.method == 'POST':
            user_input = request.form['user_input']
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                # messages=[
                #     {"role": "system", "content": f"당신은 학생이 {curriculum_title}에 대해 학습하도록 돕는 교사입니다."},
                #     {"role": "user", "content": user_input}
                # ]
                messages=[
                    {
                        "role": "system",
                        "content": (
                            f"당신은 초등학교 {grade}학년 학생을 위한 영어 교사입니다. "
                            f"학생이 {curriculum_title}에 대해 학습할 수 있도록 도와주세요. "
                            f"학생이 한국말로 문의를 하더라도 영어로 다시 해당 한국어에 대해서 질문을 할 수 있도록 답변을 유도해야 합니다. "
                            f"학생이 영어를 못하는 경우에는 한국말로 설명을 하면서 영어를 가르쳐주세요. "
                            f"예를 들어, '이 문장을 따라서 간단한 인사말을 해보세요: \"Good morning\" 이라는 단어를 따라해보세요.'"
                            f"라는 형태로 지금의 {curriculum_title} 에 해당하는 분야의 대화를 통해 학생의 영어 실력을 향상시키는 것이 목표입니다."
                        )
                    },
                    {"role": "user", "content": user_input}
                ]
            )
            chat_response = response.choices[0].message.content.strip()
            return jsonify({'response': chat_response})
        return render_template('curriculum.html', grade=grade, curriculum_title=curriculum_title, grades=curriculums.keys(), current_grade=grade)
    return "해당 커리큘럼은 존재하지 않습니다.", 404

if __name__ == '__main__':
    app.run(debug=True)
