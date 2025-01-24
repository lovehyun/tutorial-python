import openai
import fitz
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")


class ConversationHistory:
    def __init__(self):
        self.messages = []

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})

    def get_formatted_history(self):
        return "\n".join([f"{msg['role']}: {msg['content']}" for msg in self.messages])


def read_pdf(file_path):
    with fitz.open(file_path) as pdf:
        return "".join(page.get_text() for page in pdf)


def chunk_text(text, chunk_size=1000, overlap=100):
    words = text.split()
    return [" ".join(words[i:i + chunk_size])
            for i in range(0, len(words), chunk_size - overlap)]


def ask_question(text, question, history, verbose=False):
    chunks = chunk_text(text, chunk_size=500, overlap=50)
    responses = []
    chat_history = history.get_formatted_history()

    if verbose:
        print(f"\n총 {len(chunks)}개의 청크 처리:")

    for i, chunk in enumerate(chunks):
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "이전 대화 기록과 문서 내용을 참고하여 답변하세요."},
                {"role": "user", "content": f"대화 기록:\n{chat_history}\n\n문서 내용:\n{chunk}\n\n질문: {question}"}
            ],
            temperature=0.3
        )
        if verbose:
            print(f"\n청크 {i+1} 응답:\n{response.choices[0].message.content}")
        responses.append(response.choices[0].message.content)

    final_summary = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "대화 기록을 고려하여 응답들을 요약해주세요."},
            {"role": "user", "content": f"대화 기록:\n{
                chat_history}\n\n응답들:\n{' '.join(responses)}"}
        ],
        temperature=0.3
    )

    summary = final_summary.choices[0].message.content
    history.add_message("user", question)
    history.add_message("assistant", summary)
    return summary


if __name__ == "__main__":
    history = ConversationHistory()
    pdf_text = read_pdf("../small_file.pdf")

    print("\n질문 1: 개인정보의 개념은 무엇인가요?")
    answer1 = ask_question(pdf_text, "개인정보의 개념은 무엇인가요?", history, verbose=True)
    print(f"\n최종 답변 1: {answer1}")

    print("\n질문 2: 앞서 설명한 개념 중 가명정보는 어떻게 정의되나요?")
    answer2 = ask_question(pdf_text, "앞서 설명한 개념 중 가명정보는 어떻게 정의되나요?", history, verbose=True)
    print(f"\n최종 답변 2: {answer2}")
