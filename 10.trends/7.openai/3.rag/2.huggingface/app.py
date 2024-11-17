# pip install transformers faiss-cpu datasets
# pip install torch

from transformers import DPRQuestionEncoder, DPRQuestionEncoderTokenizer
from transformers import DPRContextEncoder, DPRContextEncoderTokenizer
from transformers import RagRetriever, RagTokenizer, RagSequenceForGeneration
import torch

# 질문 인코더 및 토크나이저 로드
question_encoder = DPRQuestionEncoder.from_pretrained("facebook/dpr-question_encoder-single-nq-base")
question_tokenizer = DPRQuestionEncoderTokenizer.from_pretrained("facebook/dpr-question_encoder-single-nq-base")

# 문서 인코더 및 토크나이저 로드
context_encoder = DPRContextEncoder.from_pretrained("facebook/dpr-ctx_encoder-single-nq-base")
context_tokenizer = DPRContextEncoderTokenizer.from_pretrained("facebook/dpr-ctx_encoder-single-nq-base")

# 예제 문서들
documents = [
    "OpenAI is an AI research and deployment company.",
    "GPT-3 is a state-of-the-art language processing AI model developed by OpenAI.",
    "RAG stands for Retrieval-Augmented Generation."
]

# 문서 인코딩
context_embeddings = []
for doc in documents:
    inputs = context_tokenizer(doc, return_tensors='pt')
    embeddings = context_encoder(**inputs).pooler_output
    context_embeddings.append(embeddings)
context_embeddings = torch.cat(context_embeddings, dim=0)

# 질문 인코딩
question = "What is GPT-3?"
inputs = question_tokenizer(question, return_tensors='pt')
question_embedding = question_encoder(**inputs).pooler_output

# FAISS를 사용하여 최근접 이웃 검색
import faiss

index = faiss.IndexFlatIP(context_embeddings.size(1))
index.add(context_embeddings.detach().numpy())
D, I = index.search(question_embedding.detach().numpy(), k=1)

# 검색된 문서
retrieved_doc = documents[I[0][0]]
print("Retrieved document:", retrieved_doc)

# RAG 모델 로드
rag_tokenizer = RagTokenizer.from_pretrained("facebook/rag-sequence-nq")
rag_model = RagSequenceForGeneration.from_pretrained("facebook/rag-sequence-nq")

# RAG를 사용하여 응답 생성
input_ids = rag_tokenizer(question, retrieved_doc, return_tensors="pt", truncation=True, padding="longest").input_ids
outputs = rag_model.generate(input_ids=input_ids)

print("Generated response:", rag_tokenizer.batch_decode(outputs, skip_special_tokens=True)[0])
