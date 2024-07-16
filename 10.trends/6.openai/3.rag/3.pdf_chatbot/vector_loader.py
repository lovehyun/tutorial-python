#import Essential dependencies
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# Load the environment variables from the .env file
load_dotenv('../../.env')
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

#create a new file named vectorstore in your current directory.
if __name__=="__main__":
        DB_FAISS_PATH = 'vectorstore/db_faiss'
        loader = PyPDFLoader("./random machine learing pdf.pdf")
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)
        vectorstore = FAISS.from_documents(documents=splits, embedding=OpenAIEmbeddings(api_key=OPENAI_API_KEY))
        vectorstore.save_local(DB_FAISS_PATH)
