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
        return "".join(page.get_text() for page in pdf)


file_path = "../small_file.pdf"
pdf_text = read_pdf(file_path)
print(f"PDF 내용: {pdf_text[:500]}...")

llm = ChatOpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    model_name="gpt-3.5-turbo"
)

prompt = ChatPromptTemplate.from_template("""
문서 내용:
{pdf_text}

질문: {question}
답변:""")

chain = prompt | llm | StrOutputParser()


def ask_question(question):
    return chain.invoke({"pdf_text": pdf_text, "question": question})


question = "이 문서의 주요 내용은 무엇인가요?"
response = ask_question(question)
print(f"응답: {response}")
