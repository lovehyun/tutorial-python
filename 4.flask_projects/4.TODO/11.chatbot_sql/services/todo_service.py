# services/todo_service.py
import database5 as db
from typing import List, Dict, Optional, Tuple

def get_all() -> List[Dict]:
    """전체 To-Do 반환"""
    return db.get_all_todos()

def add(task: str) -> Dict:
    """할 일 추가"""
    return db.add_todo(task)

def toggle(todo_id: int) -> Optional[Dict]:
    """완료/미완료 토글"""
    return db.toggle_todo(todo_id)

def delete(todo_id: int) -> bool:
    """항목 삭제"""
    return db.delete_todo(todo_id)

def summary() -> Tuple[int, int, int]:
    """(total, done, pending)"""
    return db.get_summary()

# ---- LLM/챗봇 편의 함수 ----
def to_llm_format() -> List[Dict]:
    """LLM 입력용 포맷"""
    todos = db.get_all_todos()
    return [{"text": t["task"], "completed": t["done"]} for t in todos]

def find(hint: str) -> Optional[Dict]:
    """ID 또는 부분 문자열 검색"""
    if not hint:
        return None
    if hint.isdigit():
        return db.get_todo_by_id(int(hint))
    return db.find_todo_by_text(hint)

def list_verbose() -> str:
    todos = db.get_all_todos()
    if not todos:
        return "할 일이 없습니다."
    return "\n".join(
        [f"{t['id']}. {t['task']} [{'완료' if t['done'] else '미완료'}]" for t in todos]
    )

def list_compact() -> str:
    todos = db.get_all_todos()
    if not todos:
        return "할 일이 없습니다."
    return "현재 목록:\n" + ", ".join(
        [f"{t['id']}. {t['task']}{'(완료)' if t['done'] else ''}" for t in todos]
    )
