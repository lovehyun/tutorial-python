import openai
import fitz
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")


def read_pdf(file_path):
    with fitz.open(file_path) as pdf:
        return "".join(page.get_text() for page in pdf)


def chunk_text(text, chunk_size=1000, overlap=100):
    words = text.split()
    return [" ".join(words[i:i + chunk_size])
            for i in range(0, len(words), chunk_size - overlap)]


def ask_question(text, question, verbose=False):
    chunks = chunk_text(text, chunk_size=500, overlap=50)
    responses = []

    if verbose:
        print(f"\n총 {len(chunks)}개의 청크 처리:")

    for i, chunk in enumerate(chunks):
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "주어진 문서 내용에 기반하여 답변하세요."},
                {"role": "user", "content": f"문서 내용:\n{chunk}\n\n질문: {question}"}
            ],
            temperature=0.3
        )
        if verbose:
            print(f"\n청크 {i+1} 응답:\n{response.choices[0].message.content}")
        responses.append(response.choices[0].message.content)

    # 최종 요약
    final_summary = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "다음 응답들을 하나의 답변으로 요약해주세요."},
            {"role": "user", "content": "\n".join(responses)}
        ],
        temperature=0.3
    )

    return final_summary.choices[0].message.content


pdf_text = read_pdf("../small_file.pdf")
answer = ask_question(pdf_text, "이 문서의 주요 내용은 무엇인가요?", verbose=True)
print(f"\n최종 답변: {answer}")
