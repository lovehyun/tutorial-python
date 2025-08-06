document.addEventListener('DOMContentLoaded', () => {
    const todoForm = document.getElementById('todo-form');
    const taskInput = document.getElementById('task-input');

    // To-Do 추가
    todoForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const task = taskInput.value.trim();
        if (task) {
            fetch('/api/todo', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ task: task }),
            }).then(() => {
                taskInput.value = '';
                loadTodos();
            });
        }
    });

    // 초기 로드
    loadTodos();
})

// 완료 토글
function toggleTodo(id) {
    fetch(`/api/todo/${id}`, {
        method: 'PUT',
    }).then(() => loadTodos());
}

// To-Do 삭제
function deleteTodo(id) {
    fetch(`/api/todo/${id}`, {
        method: 'DELETE',
    }).then(() => loadTodos());
}

// To-Do 목록 불러오기
function loadTodos() {
    const todoList = document.getElementById('todo-list');

    fetch('/api/todo')
        .then((response) => response.json())
        .then((data) => {
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
        });
}
