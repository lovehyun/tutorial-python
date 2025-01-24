import openai
import fitz
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")
openai.api_key = os.environ.get("OPENAI_API_KEY")


def read_pdf(file_path):
    with fitz.open(file_path) as pdf:
        return "".join(page.get_text() for page in pdf)


def ask_question(text, question):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "주어진 문서 내용에 기반하여 질문에 답하세요."
            },
            {
                "role": "user",
                "content": f"문서 내용:\n{text}\n\n질문: {question}"
            }
        ],
        temperature=0.3  # 0~1 사이 값, 낮을수록 일관된 답변
    )
    return response.choices[0].message.content


pdf_text = read_pdf("../small_file.pdf")
answer = ask_question(pdf_text, "이 문서의 주요 내용은 무엇인가요?")
print(f"답변: {answer}")
