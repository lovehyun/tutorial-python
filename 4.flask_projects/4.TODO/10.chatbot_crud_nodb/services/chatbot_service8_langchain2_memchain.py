import os
import logging
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI

from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory  # 또는 FileChatMessageHistory

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

# 4. 체인 정의

# 4-1. 세션별 InMemory 히스토리 관리 (딕셔너리)
_session_memory_store = {}

def get_memory(session_id: str):
    if session_id not in _session_memory_store:
        _session_memory_store[session_id] = InMemoryChatMessageHistory()
    return _session_memory_store[session_id]

# 4-2. 체인 정의
def build_todo_list_text(todos: list) -> str:
    if not todos:
        return "할 일이 없습니다."

    lines = []
    for i, t in enumerate(todos, start=1):
        status = "완료됨" if t["completed"] else "미완료"
        lines.append(f"{i}. {t['text']} [{status}]")
        
    return "\n".join(lines)

def build_chat_chain() -> RunnableWithMessageHistory:
    chain = (
        {
            "question": lambda x: x["question"],
            "todo_list": lambda x: build_todo_list_text(x["todos"]),
            "chat_history": lambda x: x["chat_history"]
        }
        | prompt
        | llm
        # | parser   # RunnableWithMessageHistory 는 output 에 담겨 있어야 WARNING이 안나와서 parser 제외
    )

    return RunnableWithMessageHistory(
        chain,
        get_memory,
        input_messages_key="question",
        history_messages_key="chat_history",
    )


# 메인 핸들러
def handle_chat8(question: str, session_id: str = "default") -> dict:
    action = process_chat(question, todo.to_llm_format(), session_id)
    answer = _apply_action_and_build_answer(action)

    return {
        "answer": answer,
        "todos": todo.get_all()
    }

# LangChain을 통한 챗봇 응답 처리
def process_chat(question: str, todos_data: list, session_id: str = "default") -> dict:
    logger.debug("[LLM 요청 메시지]\n%s", question)
    
    try:
        chat_chain = build_chat_chain()  # 체인 생성
        llm_response  = chat_chain.invoke({
            "question": question,
            "todos": todos_data,
        },
        config={
            "configurable": {
                "session_id": session_id  # Memory 사용시 반드시 필요함
            }
        })
        
        # 파싱을 별도로 수행 - AIMessage 객체에서 content 추출 후 파싱
        content = llm_response.content
        result = parser.parse(content)
        logger.debug("[LLM 응답 JSON] %s", result)

    except Exception as e:
        logger.error("[LangChain 처리 실패] %s", e, exc_info=True)
        result = {"action": "", "text": ""}

    return result

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
        list_text = todo.list_verbose()
        if text and text != list_text:
            return f"{text}\n\n{list_text}"
        else:
            return list_text

    if action == "summary":
        total, done, pending = todo.summary()
        summary = f"총 {total}개 중 완료 {done}개, 미완료 {pending}개입니다.\n\n{todo.list_compact()}"
        if text:
            return f"{text}\n\n{summary}"
        else:
            return summary
        
    return "무슨 작업을 해야 할지 잘 모르겠어요. 현재는 단순 업무만 지원하며 일괄 처리는 지원하지 않습니다. (지원: add, done, delete, list, summary)"
