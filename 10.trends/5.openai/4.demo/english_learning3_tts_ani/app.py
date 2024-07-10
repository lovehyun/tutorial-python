# pip install google-cloud-texttospeech

from flask import Flask, render_template, request, jsonify, send_file
from openai import OpenAI
from dotenv import load_dotenv
import os
from google.cloud import texttospeech
import uuid
import re
import glob

app = Flask(__name__)

load_dotenv('../../.env')

# OpenAI 셋업
openai_api_key = os.environ.get('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)

# Google Cloud TTS 설정
tts_client = texttospeech.TextToSpeechClient()

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

            # 1. Google TTS 호출
            # synthesis_input = texttospeech.SynthesisInput(text=chat_response)
            # voice = texttospeech.VoiceSelectionParams(
            #     language_code="ko-KR", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
            # )
            # audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

            # tts_response = tts_client.synthesize_speech(
            #     input=synthesis_input, voice=voice, audio_config=audio_config
            # )

            # audio_content = tts_response.audio_content
            # audio_filename = f"audio/{uuid.uuid4()}.mp3"
            # with open(audio_filename, 'wb') as out:
            #     out.write(audio_content)

            # ----------
            # 2. 문장 단위로 분할
            # sentences = chat_response.split('. ') # 점 으로만 문장을 구분
            sentences = re.split(r'(?<=[.?!])\s+', chat_response) # (?<=[.?!]) positive lookbehind assertion (.?! 뒤의 공백을 찾아서 문장을 구분)
            combined_audio_content = b''

            for sentence in sentences:
                # 한국어 문장인지 영어 문장인지 감지
                lang_code = "ko-KR" if any('\u3131' <= char <= '\u3163' or '\uac00' <= char <= '\ud7a3' for char in sentence) else "en-US"
                synthesis_input = texttospeech.SynthesisInput(text=sentence)
                voice = texttospeech.VoiceSelectionParams(
                    language_code=lang_code, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
                )
                audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

                tts_response = tts_client.synthesize_speech(
                    input=synthesis_input, voice=voice, audio_config=audio_config
                )

                combined_audio_content += tts_response.audio_content

            audio_filename = f"audio/{uuid.uuid4()}.mp3"
            with open(audio_filename, 'wb') as out:
                out.write(combined_audio_content)

            # ----------
            # 3. 단어 단위로 분할 - 공백과 쌍따옴표로 문장을 분할하여 언어 선택
            words = re.findall(r'\"[^\"]*\"|\S+', chat_response) # 단어를 공백과 쌍따옴표인 경우에만 분할
            # print(words)
            combined_audio_content = b''

            def synthesize_text(text, lang_code):
                synthesis_input = texttospeech.SynthesisInput(text=text)
                voice = texttospeech.VoiceSelectionParams(
                    language_code=lang_code, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
                )
                audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

                tts_response = tts_client.synthesize_speech(
                    input=synthesis_input, voice=voice, audio_config=audio_config
                )

                return tts_response.audio_content

            current_language = "en-US"
            buffer = ""

            for word in words:
                if any('\u3131' <= char <= '\u3163' or '\uac00' <= char <= '\ud7a3' for char in word):
                    # 한국어 단어 감지
                    if current_language == "en-US" and buffer:
                        combined_audio_content += synthesize_text(buffer.strip(), current_language)
                        buffer = ""
                    current_language = "ko-KR"
                else:
                    # 영어 단어 감지
                    if current_language == "ko-KR" and buffer:
                        combined_audio_content += synthesize_text(buffer.strip(), current_language)
                        buffer = ""
                    current_language = "en-US"

                buffer += word + " "

            if buffer:
                combined_audio_content += synthesize_text(buffer.strip(), current_language)

            audio_filename = f"audio/{uuid.uuid4()}.mp3"
            with open(audio_filename, 'wb') as out:
                out.write(combined_audio_content)

            # 최근 10개 파일만 남기고 나머지 삭제
            manage_audio_files()

            return jsonify({'response': chat_response, 'audio_path': audio_filename})
        
        return render_template('curriculum.html', grade=grade, curriculum_title=curriculum_title, grades=curriculums.keys(), current_grade=grade)
    return "해당 커리큘럼은 존재하지 않습니다.", 404

@app.route('/audio/<path:filename>')
def get_audio(filename):
    return send_file(filename)

def manage_audio_files():
    audio_files = sorted(glob.glob('audio/*.mp3'), key=os.path.getctime, reverse=True)
    for file in audio_files[10:]:
        os.remove(file)

if __name__ == '__main__':
    app.run(debug=True)
