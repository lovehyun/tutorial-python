# services/chatbot_service.py
import os
import json
from dotenv import load_dotenv

from openai import OpenAI
from services import todo_service as todo

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set")

client = OpenAI(api_key=API_KEY)


# 메인 핸들러
def handle_chat(question: str) -> dict:
    """질문을 받아 LLM 호출 → 액션 수행 → 응답"""
    action = process_chat(question, todo.to_llm_format())
    answer = _apply_action_and_build_answer(action)
    return {
        "answer": answer,
        "todos": todo.get_all()
    }

# 챗봇 대화 수행
def process_chat(question: str, todos_data: list) -> dict:
    """LLM 호출하여 action/text JSON 반환"""
    todo_list = "\n".join(
        [f"{i}. {t['text']} [{'완료됨' if t['completed'] else '미완료'}]" for i, t in enumerate(todos_data, start=1)]
    ) or "할 일이 없습니다."

    system_prompt = f"""
당신은 To-Do 목록을 도와주는 비서입니다. 사용자의 질문을 이해하고 아래 예시처럼 반드시 JSON만 반환하세요.

[할 일 목록]
{todo_list}

[출력 형식]
{{ "action": "add" | "done" | "delete" | "list" | "summary", "text": "내용" }}
"""

    print("\n---\n[시스템 프롬프트]\n", system_prompt)
    print("\n---\n[사용자 프롬프트]\n", question)
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            temperature=0.2
        )

        reply = response.choices[0].message.content.strip()
        
        print("\n---\n[GPT 응답]\n", reply)
        # 출력값 Sanitization
        reply = reply.replace("```json", "").replace("```", "").strip()
        
        # JSON 디코딩 시도
        action_json = json.loads(reply)

        # 필수 필드 유효성 검사
        if "action" not in action_json:
            raise ValueError("Missing 'action' field in response")

        return action_json

    except Exception as e:
        print(f"[ERROR] GPT 응답 처리 중 오류 발생: {e}\n원본 응답: {reply}")
        # fallback 값
        return {"action": "error", "text": "올바른 JSON 응답을 받지 못했어요. 다시 질문해 주세요."}

# 액션 수행
def _apply_action_and_build_answer(action_item: dict) -> str:
    action = (action_item.get("action") or "").lower()
    text = (action_item.get("text") or "").strip()

    if action == "add":
        if not text:
            return "추가할 작업 내용을 알려주세요."

        todo.add(text)
        return f"할 일을 추가했어요: “{text}”\n\n{todo.list_compact()}"

    if action == "done":
        item = todo.find(text)
        if not item:
            return f"완료 표시할 항목을 찾지 못했어요: “{text}”"
        
        todo.toggle(item["id"])
        return f"완료 처리했어요: “{item['task']}”\n\n{todo.list_compact()}"

    if action == "delete":
        item = todo.find(text)
        if not item:
            return f"삭제할 항목을 찾지 못했어요: “{text}”"
            
        todo.delete(item["id"])
        return f"삭제했어요: “{item['task']}”\n\n{todo.list_compact()}"

    if action == "list":
        return todo.list_verbose()

    if action == "summary":
        total, done, pending = todo.summary()
        return f"총 {total}개 중 완료 {done}개, 미완료 {pending}개입니다.\n\n{todo.list_compact()}"

    if action == "error":
        return text

    return "무슨 작업을 해야 할지 잘 모르겠어요. (지원: add, done, delete, list, summary)"
