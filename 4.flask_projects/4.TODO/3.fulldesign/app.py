from flask import Flask, render_template, request, jsonify
import datetime

app = Flask(__name__)

# 메모리에 저장할 간단한 데이터
todos = [
    {"id": 1, "task": "Flask 학습하기", "completed": False},
    {"id": 2, "task": "웹 애플리케이션 만들기", "completed": True}
]

@app.route('/')
def home():
    """홈페이지"""
    return render_template('index.html', todos=todos)

@app.route('/about')
def about():
    """소개 페이지"""
    return render_template('about.html')

@app.route('/api/todos', methods=['GET'])
def get_todos():
    """모든 할 일 목록 반환 (API)"""
    return jsonify(todos)

@app.route('/api/todos', methods=['POST'])
def add_todo():
    """새로운 할 일 추가 (API)"""
    data = request.get_json()
    if not data or 'task' not in data:
        return jsonify({"error": "Task is required"}), 400
    
    new_todo = {
        "id": len(todos) + 1,
        "task": data['task'],
        "completed": False
    }
    todos.append(new_todo)
    return jsonify(new_todo), 201

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """할 일 상태 업데이트 (API)"""
    todo = next((t for t in todos if t['id'] == todo_id), None)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    
    data = request.get_json()
    if 'completed' in data:
        todo['completed'] = data['completed']
    if 'task' in data:
        todo['task'] = data['task']
    
    return jsonify(todo)

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """할 일 삭제 (API)"""
    global todos
    todos = [t for t in todos if t['id'] != todo_id]
    return jsonify({"message": "Todo deleted"}), 200

@app.route('/api/time')
def get_time():
    """현재 시간 반환 (API)"""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({"current_time": current_time})

@app.route('/hello/<name>')
def hello(name):
    """동적 라우트 예제"""
    return f"<h1>안녕하세요, {name}님!</h1>"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
