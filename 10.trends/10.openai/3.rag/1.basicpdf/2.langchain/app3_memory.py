import fitz
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.schema import HumanMessage, AIMessage

load_dotenv(dotenv_path="../.env")


def read_pdf(file_path):
    with fitz.open(file_path) as pdf:
        return "".join(page.get_text() for page in pdf)


def chunk_text(text, chunk_size=1000, overlap=100):
    words = text.split()
    return [" ".join(words[i:i + chunk_size])
            for i in range(0, len(words), chunk_size - overlap)]


llm = ChatOpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    model_name="gpt-3.5-turbo"
)

history = ChatMessageHistory()

prompt = ChatPromptTemplate.from_template("""
이전 대화:
{chat_history}

현재 문서 내용:
{pdf_text}

질문: {question}

이전 대화와 현재 문서를 참고하여 답변해주세요.
한글로 자연스럽게 답변하되, 문서의 내용에 충실하게 답변해주세요.
""")

chain = prompt | llm | StrOutputParser()


def format_chat_history(messages):
    return "\n".join([
        f"{'사용자' if isinstance(m, HumanMessage) else '어시스턴트'}: {m.content}"
        for m in messages
    ])


def ask_question(pdf_text, question, verbose=False):
    chunks = chunk_text(pdf_text, chunk_size=500, overlap=50)
    chunk_responses = []

    chat_history = format_chat_history(history.messages)

    if verbose:
        print(f"\n총 {len(chunks)}개의 청크 처리 중:")

    for i, chunk in enumerate(chunks):
        response = chain.invoke({
            "pdf_text": chunk,
            "question": question,
            "chat_history": chat_history
        })
        if verbose:
            print(f"\n청크 {i+1} 응답:\n{response}")
        chunk_responses.append(response)

    history.add_user_message(question)
    history.add_ai_message("\n".join(chunk_responses))

    summary_prompt = ChatPromptTemplate.from_template("""
다음 응답들을 하나로 요약해주세요:
{responses}

한글로 자연스럽게, 하나의 완성된 답변으로 작성해주세요.
""")
    summary_chain = summary_prompt | llm | StrOutputParser()
    final_summary = summary_chain.invoke(
        {"responses": "\n".join(chunk_responses)})

    if verbose:
        print(f"\n최종 요약:\n{final_summary}")
    return final_summary


if __name__ == "__main__":
    file_path = "../small_file.pdf"
    pdf_text = read_pdf(file_path)

    print("\n질문 1: 개인정보의 개념은 무엇인가요?")
    answer1 = ask_question(pdf_text, "개인정보의 개념은 무엇인가요?", verbose=True)
    print(f"\n최종 답변 1: {answer1}\n")

    print("\n질문 2: 앞서 설명한 개념 중 가명정보는 어떻게 정의되나요?")
    answer2 = ask_question(
        pdf_text, "앞서 설명한 개념 중 가명정보는 어떻게 정의되나요?", verbose=True)
    print(f"\n최종 답변 2: {answer2}")
