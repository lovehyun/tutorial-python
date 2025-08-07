# 필수 라이브러리 불러오기
import os
from dotenv import load_dotenv  # .env 파일에서 환경 변수 불러오기

# LangChain에서 제공하는 PDF 문서 로더
from langchain_community.document_loaders import PyPDFLoader

# 긴 문서를 작은 조각으로 나누기 위한 텍스트 분할 도구
from langchain.text_splitter import RecursiveCharacterTextSplitter

# FAISS 벡터 저장소: 문서 임베딩을 저장하고 검색하기 위해 사용
from langchain_community.vectorstores import FAISS

# OpenAI 임베딩 모델: 문장을 벡터로 변환
from langchain_openai import OpenAIEmbeddings

# .env 파일에서 OPENAI_API_KEY 환경 변수 불러오기
load_dotenv('../../.env')  # 상위 폴더의 .env 파일 경로
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 메인 실행 로직
if __name__ == "__main__":
    # 벡터 저장소를 저장할 경로 설정
    DB_FAISS_PATH = 'vectorstore/db_faiss'
    
    # PDF 문서 로딩
    loader = PyPDFLoader("./random machine learing pdf.pdf")
    docs = loader.load()  # 문서 전체를 로드하여 LangChain 문서 객체 리스트로 반환

    # 문서 분할 설정: chunk_size=1000자, chunk_overlap=200자
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)  # 문서 리스트를 여러 청크로 분할

    # 분할된 문서를 OpenAI Embedding으로 벡터화하여 FAISS에 저장
    vectorstore = FAISS.from_documents(
        documents=splits,
        embedding=OpenAIEmbeddings(api_key=OPENAI_API_KEY)
    )

    # 벡터 저장소를 로컬 디렉토리에 저장
    vectorstore.save_local(DB_FAISS_PATH)
