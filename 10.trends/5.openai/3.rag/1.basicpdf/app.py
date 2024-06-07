# pip install pymupdf langchain openai

import fitz  # PyMuPDF
from langchain import OpenAI, ConversationChain
from langchain.chat_models import ChatOpenAI

# PDF 파일 읽기 함수
def read_pdf(file_path):
    pdf_document = fitz.open(file_path)
    text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text

# PDF 파일 읽기
file_path = "path_to_your_pdf_file.pdf"
pdf_text = read_pdf(file_path)
print(f"PDF 내용: {pdf_text[:500]}...")  # 전체 내용을 출력하면 너무 길어질 수 있으므로 일부만 출력

# OpenAI GPT 모델 설정
openai_api_key = "your_openai_api_key"
llm = ChatOpenAI(api_key=openai_api_key, model_name="gpt-3.5-turbo")

# 대화 체인 설정
conversation = ConversationChain(
    llm=llm,
    prompt="You are an assistant that helps answer questions based on the content of a PDF document. Here is the document content:\n\n" + pdf_text
)

# 질문에 대한 대화
def ask_question(question):
    response = conversation.run(input=question)
    return response

# 예제 질문
question = "What is the main topic of the document?"
response = ask_question(question)
print(f"Response: {response}")
