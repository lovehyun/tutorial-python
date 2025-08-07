import os
import json
import logging
from dotenv import load_dotenv
from collections import deque

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI

from services import todo_service as todo

logger = logging.getLogger(__name__)

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set")


# 1. 프롬프트 템플릿
prompt = ChatPromptTemplate.from_messages([
    ("system", """당신은 To-Do 목록을 도와주는 비서입니다. 사용자의 질문을 이해하고 아래 예시처럼 반드시 JSON만 반환하세요.

[할 일 목록]
{todo_list}

[출력 형식]
{{
  "action": "add" | "done" | "undone" | "delete" | "list" | "summary",
  "text": "내용"
}}"""),
    ("user", "{question}")
])

# 2. LangChain LLM 인스턴스
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2,
    api_key=API_KEY,
)

# 3. 파서 정의
parser = JsonOutputParser()


# 대화 기록 저장소
HISTORY = deque(maxlen=20)

# 히스토리 저장
def store_history(role: str, content: str):
    HISTORY.append({"role": role, "content": content})


# 메인 핸들러
def handle_chat7(question: str) -> dict:
    action = process_chat(question, todo.to_llm_format())
    answer = _apply_action_and_build_answer(action)

    store_history("assistant", answer) # 응답 메시지 저장

    return {
        "answer": answer,
        "todos": todo.get_all()
    }

# LangChain을 통한 챗봇 응답 처리
def process_chat(question: str, todos_data: list) -> dict:
    # 할일 목록을 GPT가 이해하기 좋은 자연어로 변환
    todo_list = "\n".join(
        [f"{i}. {t['text']} [{'완료됨' if t['completed'] else '미완료'}]" for i, t in enumerate(todos_data, start=1)]
    ) or "할 일이 없습니다."

    try:
        # 메시지 구성 및 모델 호출
        messages = prompt.invoke({
            "todo_list": todo_list,
            "question": question
        })
        logger.debug("[LLM 요청 메시지]\n%s", messages)

        raw_output = llm.invoke(messages)
        logger.debug("[LLM 응답 메시지]\n%s", raw_output.content)

        parsed = parser.invoke(raw_output)
        logger.debug("[파싱된 JSON]\n%s", parsed)
        return parsed

    except Exception as e:
        logger.error("[LangChain 처리 실패] %s", e, exc_info=True)
        return {"action": "", "text": ""}


# 액션 수행 함수
def _apply_action_and_build_answer(action_item: dict) -> str:
    action = (action_item.get("action") or "").lower()
    text = (action_item.get("text") or "").strip()

    if action == "add":
        if not text:
            return "추가할 작업 내용을 알려주세요."

        todo.add(text)
        return f"할 일(“{text}”)을 추가했어요\n\n{todo.list_compact()}"

    if action == "done":
        item = todo.find(text)
        if not item:
            return f"완료 표시할 항목(“{text}”)을 찾지 못했어요"

        todo.toggle(item["id"])
        return f"“{item['task']}” 완료 처리했어요\n\n{todo.list_compact()}"

    if action == "undone":
        item = todo.find(text)
        if not item:
            return f"완료취소 표시할 항목(“{text}”)을 찾지 못했어요"

        todo.toggle(item["id"])
        return f"“{item['task']}” 완료취소 처리했어요\n\n{todo.list_compact()}"

    if action == "delete":
        item = todo.find(text)
        if not item:
            return f"삭제할 항목(“{text}”)을 찾지 못했어요"

        todo.delete(item["id"])
        return f"“{item['task']}” 삭제했어요\n\n{todo.list_compact()}"

    if action == "list":
        return todo.list_verbose()

    if action == "summary":
        total, done, pending = todo.summary()
        return f"총 {total}개 중 완료 {done}개, 미완료 {pending}개입니다.\n\n{todo.list_compact()}"

    return "무슨 작업을 해야 할지 잘 모르겠어요. 현재는 단순 업무만 지원하며 일괄 처리는 지원하지 않습니다. (지원: add, done, delete, list, summary)"
