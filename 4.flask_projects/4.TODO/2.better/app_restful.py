# 요청	        설명	    HTTP Method	요청 데이터
# /api/todo	    전체 조회	GET	없음
# /api/todo	    항목 추가	POST { "task": "Study Flask" }
# /api/todo	    완료 토글	PUT { "id": 1 }
# /api/todo	    항목 삭제	DELETE { "id": 1 }

from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# 메모리 내 To-Do 리스트
todos = []
next_id = 1

@app.route('/')
def home():
    return render_template('index_restapi.html')

@app.route('/api/todo', methods=['GET'])
def get_todos():
    return jsonify(todos)

@app.route('/api/todo', methods=['POST'])
def add_todo():
    global next_id
    data = request.get_json()
    task = data.get('task')
    if not task:
        return jsonify({'error': 'Task is required'}), 400

    new_todo = {'id': next_id, 'task': task, 'done': False}
    todos.append(new_todo)
    next_id += 1
    return jsonify(new_todo), 201

@app.route('/api/todo/<int:todo_id>', methods=['PUT'])
def toggle_todo(todo_id):
    for todo in todos:
        if todo['id'] == todo_id:
            todo['done'] = not todo['done']
            return jsonify(todo)
    return jsonify({'error': 'Todo not found'}), 404

@app.route('/api/todo/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    for todo in todos:
        if todo['id'] == todo_id:
            todos.remove(todo)
            return jsonify({'message': 'Todo deleted successfully'})
    return jsonify({'error': 'Todo not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
