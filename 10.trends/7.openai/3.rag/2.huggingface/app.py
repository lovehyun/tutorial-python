# pip install transformers faiss-cpu datasets
# pip install torch
# - Transformers: Hugging Face의 사전 학습된 모델과 토크나이저 사용
# - faiss-cpu: 문서 검색 및 최근접 이웃(Nearest Neighbor) 검색을 위한 라이브러리
# - torch: PyTorch를 사용하여 모델 실행

# 1. 질문 인코더 및 토크나이저 로드
# DPR (Dense Passage Retrieval): RAG에서 사용하는 검색 단계 모델로, 질문과 문서를 벡터로 인코딩합니다.
#  - DPRQuestionEncoder: 질문(queries)을 벡터로 변환
#  - DPRContextEncoder: 문서(contexts)를 벡터로 변환
#  - 각 모델은 Hugging Face에서 제공하는 사전 학습된 DPR 모델을 사용합니다.

from transformers import DPRQuestionEncoder, DPRQuestionEncoderTokenizer
from transformers import DPRContextEncoder, DPRContextEncoderTokenizer

question_encoder = DPRQuestionEncoder.from_pretrained("facebook/dpr-question_encoder-single-nq-base")
question_tokenizer = DPRQuestionEncoderTokenizer.from_pretrained("facebook/dpr-question_encoder-single-nq-base")

# 2. 문서 인코더 및 토크나이저 로드
context_encoder = DPRContextEncoder.from_pretrained("facebook/dpr-ctx_encoder-single-nq-base")
context_tokenizer = DPRContextEncoderTokenizer.from_pretrained("facebook/dpr-ctx_encoder-single-nq-base")

# 3. 예제 문서들
# 문서: 검색 가능한 텍스트 데이터(3개의 문서)
#  - context_tokenizer: 각 문서를 토큰화
#  - context_encoder: 문서를 벡터(임베딩)로 변환
# 최종 결과:
#  - context_embeddings: 모든 문서의 벡터 표현을 포함하는 텐서
documents = [
    "OpenAI is an AI research and deployment company.",
    "GPT-3 is a state-of-the-art language processing AI model developed by OpenAI.",
    "RAG stands for Retrieval-Augmented Generation."
]

# 문서 인코딩
import torch

context_embeddings = []
for doc in documents:
    inputs = context_tokenizer(doc, return_tensors='pt')
    embeddings = context_encoder(**inputs).pooler_output
    context_embeddings.append(embeddings)
context_embeddings = torch.cat(context_embeddings, dim=0)

# 4. 질문 인코딩
# 질문: "What is GPT-3?"
#  - question_tokenizer: 질문을 토큰화
#  - question_encoder: 질문을 벡터(임베딩)로 변환
# 결과: question_embedding이라는 질문 벡터가 생성됩니다.
question = "What is GPT-3?"
inputs = question_tokenizer(question, return_tensors='pt')
question_embedding = question_encoder(**inputs).pooler_output

# 5. FAISS를 사용하여 최근접 이웃 검색
# FAISS: 효율적인 벡터 검색 및 유사성 매칭 라이브러리
# IndexFlatIP: 내적(dot product) 기반 최근접 이웃 검색을 수행
#  - index.add: 문서 벡터(context_embeddings)를 색인에 추가
#  - index.search: 질문 벡터(question_embedding)와 유사한 문서를 검색
#  - k=1: 가장 유사한 1개의 문서 반환
# D: 유사도 점수
# I: 검색된 문서의 인덱스
# retrieved_doc: 검색된 문서 텍스트
import faiss

index = faiss.IndexFlatIP(context_embeddings.size(1))
index.add(context_embeddings.detach().numpy())
D, I = index.search(question_embedding.detach().numpy(), k=1)

# 검색된 문서
retrieved_doc = documents[I[0][0]]
print("Retrieved document:", retrieved_doc)

# 6. RAG 모델 로드
# RAG 모델:
# - RagTokenizer: 질문과 검색된 문서를 하나의 입력으로 결합
# - RagSequenceForGeneration: RAG 모델로 최종 응답을 생성
# 입력 생성:
# - question + retrieved_doc를 RAG에 전달하기 위한 입력 토큰 생성
# - truncation=True: 입력이 길면 잘라냄
# 응답 생성:
# - generate: RAG 모델이 최종 답변 텍스트를 생성
# - batch_decode: 응답 토큰을 사람이 읽을 수 있는 텍스트로 디코딩

from transformers import RagTokenizer, RagSequenceForGeneration

rag_tokenizer = RagTokenizer.from_pretrained("facebook/rag-sequence-nq")
rag_model = RagSequenceForGeneration.from_pretrained("facebook/rag-sequence-nq")

# RAG를 사용하여 응답 생성
input_ids = rag_tokenizer(question, retrieved_doc, return_tensors="pt", truncation=True, padding="longest").input_ids
outputs = rag_model.generate(input_ids=input_ids)

print("Generated response:", rag_tokenizer.batch_decode(outputs, skip_special_tokens=True)[0])

# 전체 과정 요약
# 1. DPR로 질문과 문서를 임베딩하여 문서 검색 수행
# 2. FAISS를 사용해 질문과 가장 유사한 문서를 검색
# 3. RAG로 검색된 문서를 기반으로 답변 생성
# 이 코드는 RAG의 "검색-생성" 파이프라인을 보여주는 기본 예제입니다.
