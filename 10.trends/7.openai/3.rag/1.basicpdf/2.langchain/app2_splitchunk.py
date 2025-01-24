# pip install pymupdf langchain openai

import fitz  # PyMuPDF
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

load_dotenv(dotenv_path="../.env")


def read_pdf(file_path):
    with fitz.open(file_path) as pdf:
        text = ""
        for page in pdf:
            text += page.get_text()
    return text

def chunk_text(text, chunk_size=1000, overlap=100):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

# OpenAI 설정
llm = ChatOpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"), 
    model_name="gpt-3.5-turbo",
    # temperature=0.7  # 기본값은 0.7
)

# 프롬프트 템플릿
prompt = ChatPromptTemplate.from_template("""
문서 내용:
{pdf_text}

질문: {question}

위 문서 내용만을 기반으로 명확하게 답변해주세요.
문서에 해당 내용이 없다면 그렇다고 말씀해주세요.
""")

# 응답 처리 체인
chain = prompt | llm | StrOutputParser()

def ask_question(pdf_text, question, verbose=False):
    chunks = chunk_text(pdf_text, chunk_size=500, overlap=50)
    chunk_responses = []
    
    if verbose:
        print(f"\n총 {len(chunks)}개의 청크 처리:")
    
    for i, chunk in enumerate(chunks):
        response = chain.invoke({
            "pdf_text": chunk,
            "question": question
        })
        
        if verbose:
            print(f"\n청크 {i+1} 응답:\n{response}")
        
        chunk_responses.append(response)
    
    summary_prompt = ChatPromptTemplate.from_template(
       "다음 응답들을 하나의 완성된 답변으로 요약해주세요:\n{responses}"
    )
    summary_chain = summary_prompt | llm | StrOutputParser()
    final_summary = summary_chain.invoke({"responses": "\n".join(chunk_responses)})
    
    if verbose:
        print(f"\n최종 요약:\n{final_summary}")
    return final_summary


if __name__ == "__main__":
    file_path = "../small_file.pdf"
    pdf_text = read_pdf(file_path)
    print(f"PDF 내용: {pdf_text[:500]}...\n")

    question = "문서의 주요 주제는 무엇인가요?"
    answer = ask_question(pdf_text, "문서의 주요 주제는 무엇인가요?", verbose=True)
    print(f"\n답변: {answer}")
