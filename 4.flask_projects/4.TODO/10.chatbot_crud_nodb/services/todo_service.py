# services/todo_service.py
from typing import List, Dict, Optional, Tuple

# In-memory 상태 (필요 시 DB로 교체 가능)
_todos: List[Dict] = []
_next_id: int = 1

def get_all() -> List[Dict]:
    """전체 To-Do 반환"""
    return _todos

def add(task: str) -> Dict:
    """할 일 추가"""
    global _next_id
    item = {"id": _next_id, "task": task, "done": False}
    _todos.append(item)
    _next_id += 1
    return item

def toggle(todo_id: int) -> Optional[Dict]:
    """완료/미완료 토글"""
    for t in _todos:
        if t["id"] == todo_id:
            t["done"] = not t["done"]
            return t
    return None

def delete(todo_id: int) -> bool:
    """항목 삭제"""
    for t in list(_todos):
        if t["id"] == todo_id:
            _todos.remove(t)
            return True
    return False

def summary() -> Tuple[int, int, int]:
    """(total, done, pending)"""
    total = len(_todos)
    done = sum(1 for t in _todos if t["done"])
    pending = total - done
    return total, done, pending

# ---- LLM/챗봇 편의 함수들 ----
def to_llm_format() -> List[Dict]:
    """LLM 입력용 포맷으로 변환"""
    return [{"text": t["task"], "completed": t["done"]} for t in _todos]

def find(hint: str) -> Optional[Dict]:
    """숫자(id) 또는 부분 문자열로 항목 찾기"""
    if not hint:
        return None
    if hint.isdigit():
        tid = int(hint)
        for t in _todos:
            if t["id"] == tid:
                return t
    h = hint.lower()
    for t in _todos:
        if h in t["task"].lower():
            return t
    return None

def list_verbose() -> str:
    if not _todos:
        return "할 일이 없습니다."
    return "\n".join([f"{t['id']}. {t['task']} [{'완료' if t['done'] else '미완료'}]" for t in _todos])

def list_compact() -> str:
    if not _todos:
        return "할 일이 없습니다."
    return "현재 목록:\n" + ", ".join(
        [f"{t['id']}. {t['task']}{'(완료)' if t['done'] else ''}" for t in _todos]
    )

# ---- 테스트/초기화용 (선택) ----
def reset(seed: Optional[List[str]] = None) -> None:
    """테스트 편의용 초기화"""
    global _todos, _next_id
    _todos = []
    _next_id = 1
    if seed:
        for s in seed:
            add(s)
