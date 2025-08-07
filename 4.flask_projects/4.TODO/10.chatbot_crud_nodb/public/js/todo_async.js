document.addEventListener('DOMContentLoaded', () => {
    const todoForm = document.getElementById('todo-form');
    const taskInput = document.getElementById('task-input');

    // To-Do 추가
    todoForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        const task = taskInput.value.trim();
        if (task) {
            try {
                await fetch('/api/todo', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ task: task }),
                });
                taskInput.value = '';
                await loadTodos();
            } catch (error) {
                console.error('할 일 추가 중 오류 발생:', error);
            }
        }
    });

    // 초기 로드
    loadTodos();
});

// To-Do 목록 불러오기
async function loadTodos() {
    const todoList = document.getElementById('todo-list');

    try {
        const response = await fetch('/api/todo');
        const data = await response.json();

        todoList.innerHTML = '';
        data.forEach((todo) => {
            const li = document.createElement('li');
            li.innerHTML = `
                <span class="${todo.done ? 'done' : ''}" onclick="toggleTodo(${todo.id})">
                    ${todo.task}
                </span>
                <a onclick="deleteTodo(${todo.id})">
                    <i class="bi bi-trash"></i>
                </a>
            `;
            todoList.appendChild(li);
        });
    } catch (error) {
        console.error('할 일 목록 불러오기 중 오류 발생:', error);
    }
}

// 완료 토글
async function toggleTodo(id) {
    try {
        await fetch(`/api/todo/${id}`, {
            method: 'PUT',
        });
        await loadTodos();
    } catch (error) {
        console.error('할 일 완료 토글 중 오류 발생:', error);
    }
}

// To-Do 삭제
async function deleteTodo(id) {
    try {
        await fetch(`/api/todo/${id}`, {
            method: 'DELETE',
        });
        await loadTodos();
    } catch (error) {
        console.error('할 일 삭제 중 오류 발생:', error);
    }
}
