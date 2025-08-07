document.addEventListener('DOMContentLoaded', async () => {
    const todoForm = document.getElementById('todo-form');
    const taskInput = document.getElementById('task-input');

    // To-Do 추가
    todoForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const task = taskInput.value.trim();
        if (!task) return;

        try {
            const res = await fetch('/api/todo', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ task }),
            });
            if (!res.ok) {
                const err = await checkJson(res);
                throw new Error(err?.error || `POST /api/todo 실패 (${res.status})`);
            }
            taskInput.value = '';
            loadTodos();
        } catch (err) {
            console.error(err);
            alert('추가 중 오류가 발생했습니다.');
        }
    });

    // 초기 로드
    loadTodos();
});

// To-Do 목록 불러오기
async function loadTodos() {
    const todoList = document.getElementById('todo-list');
    try {
        const res = await fetch('/api/todo');
        if (!res.ok) throw new Error(`GET /api/todo 실패 (${res.status})`);
        const data = await res.json();

        todoList.innerHTML = '';
        data.forEach((todo) => {
            const li = document.createElement('li');
            li.innerHTML = `
                <span class="${todo.done ? 'done' : ''}" onclick="toggleTodo(${todo.id})">
                    ${escapeHtml(todo.task)}
                </span>
                <a onclick="deleteTodo(${todo.id})" style="cursor:pointer;">❌</a>
            `;
            todoList.appendChild(li);
        });
    } catch (err) {
        console.error(err);
        alert('목록 불러오기 중 오류가 발생했습니다.');
    }
}

// 완료 토글
async function toggleTodo(id) {
    try {
        const res = await fetch(`/api/todo/${id}`, { method: 'PUT' });
        if (!res.ok) {
            const err = await checkJson(res);
            throw new Error(err?.error || `PUT /api/todo/${id} 실패 (${res.status})`);
        }
        loadTodos();
    } catch (err) {
        console.error(err);
        alert('완료 처리 중 오류가 발생했습니다.');
    }
}

// To-Do 삭제
async function deleteTodo(id) {
    try {
        const res = await fetch(`/api/todo/${id}`, { method: 'DELETE' });
        if (!res.ok) {
            const err = await checkJson(res);
            throw new Error(err?.error || `DELETE /api/todo/${id} 실패 (${res.status})`);
        }
        loadTodos();
    } catch (err) {
        console.error(err);
        alert('삭제 중 오류가 발생했습니다.');
    }
}

// 안전한 JSON 파싱 (오류 응답 본문이 JSON이 아닐 수 있음)
async function checkJson(res) {
    try { return await res.json(); } catch { return null; }
}

// 간단 XSS 방지
function escapeHtml(str) {
    return String(str)
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#039;');
}
