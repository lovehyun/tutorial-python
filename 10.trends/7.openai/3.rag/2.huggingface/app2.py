# pip install transformers faiss-cpu datasets torch accelerate

from transformers import RagTokenizer, RagSequenceForGeneration, RagRetriever
from datasets import load_dataset
import faiss
import torch
from torch.utils.data import DataLoader

# 1. 데이터셋 로드
# Natural Questions 데이터셋: Google에서 제공하는 대규모 QA 데이터셋.
# 학습 시간을 줄이기 위해 상위 5000개의 샘플만 로드.
print("Loading dataset...")
dataset = load_dataset("natural_questions", split="train[:5000]")  # 샘플 데이터로 제한
print("Dataset example:", dataset[0])

# 2. 문서(패시지)와 질문 추출
# 각 샘플에서 문서(패시지)와 질문을 추출.
documents = [item['document'] for item in dataset]
questions = [item['question'] for item in dataset]

# 3. 문서 임베딩 생성 (DPR 문서 인코더)
# DPR Context Encoder를 사용해 각 문서를 벡터(임베딩)로 변환.
from transformers import DPRContextEncoder, DPRContextEncoderTokenizer

print("Encoding documents...")
context_encoder = DPRContextEncoder.from_pretrained("facebook/dpr-ctx_encoder-single-nq-base")
context_tokenizer = DPRContextEncoderTokenizer.from_pretrained("facebook/dpr-ctx_encoder-single-nq-base")

# 문서를 벡터로 변환하여 FAISS에 추가
context_embeddings = []
for doc in documents:
    inputs = context_tokenizer(doc, return_tensors="pt", truncation=True, padding="longest")
    embeddings = context_encoder(**inputs).pooler_output
    context_embeddings.append(embeddings.detach().numpy())
context_embeddings = torch.tensor(context_embeddings).squeeze()

# 4. FAISS 인덱스 생성
# 문서 임베딩을 FAISS 인덱스에 추가하여 검색 가능하도록 설정.
print("Building FAISS index...")
faiss_index = faiss.IndexFlatIP(context_embeddings.size(1))  # 내적 기반 검색
faiss_index.add(context_embeddings.numpy())

# 5. RAG Retriever 설정
# RagRetriever를 설정하여 FAISS와 문서 리스트를 연결.
print("Setting up RagRetriever...")
retriever = RagRetriever.from_pretrained("facebook/rag-sequence-nq", index=faiss_index, passages=documents)

# 6. RAG 모델 로드
# 사전 학습된 RAG 모델을 로드하여 검색된 문서로부터 답변을 생성.
print("Loading RAG model...")
rag_tokenizer = RagTokenizer.from_pretrained("facebook/rag-sequence-nq")
rag_model = RagSequenceForGeneration.from_pretrained("facebook/rag-sequence-nq")

# 7. 데이터 로더 생성
# 질문 데이터를 RAG Tokenizer를 통해 전처리 후 DataLoader 생성.
print("Preparing data loader...")
def preprocess_function(examples):
    inputs = rag_tokenizer(examples["question"], return_tensors="pt", truncation=True, padding="longest")
    return {"input_ids": inputs.input_ids, "attention_mask": inputs.attention_mask}

dataloader = DataLoader(dataset.map(preprocess_function), batch_size=8)

# 8. 학습 루프 설정
# 학습 데이터에서 배치 단위로 질문과 문서를 모델에 전달하여 학습.
optimizer = torch.optim.AdamW(rag_model.parameters(), lr=5e-5)

print("Starting training...")
rag_model.train()
for epoch in range(3):  # 3 epochs for demonstration
    for batch in dataloader:
        inputs = {
            "input_ids": batch["input_ids"].squeeze(1),
            "attention_mask": batch["attention_mask"].squeeze(1),
        }
        outputs = rag_model(**inputs, labels=inputs["input_ids"])
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        print(f"Epoch {epoch}, Loss: {loss.item()}")

# 9. 질문 입력 및 답변 생성
# 새로운 질문을 입력하면 RagRetriever가 문서를 검색하고 RAG 모델이 답변을 생성.
# 결과
#  - 검색된 문서: 질문과 가장 관련 있는 문서.
#  - 생성된 답변: RAG 모델이 생성한 자연어 답변.
print("Testing model...")
question = "What is GPT-3?"
retrieved_docs = retriever(question)  # 질문에 대한 검색된 문서

input_ids = rag_tokenizer(question, retrieved_docs, return_tensors="pt", truncation=True, padding="longest").input_ids
outputs = rag_model.generate(input_ids=input_ids)

print("Question:", question)
print("Retrieved Documents:", retrieved_docs)
print("Generated Answer:", rag_tokenizer.batch_decode(outputs, skip_special_tokens=True)[0])
