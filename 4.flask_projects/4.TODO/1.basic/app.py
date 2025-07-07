from flask import Flask, request, redirect, render_template

app = Flask(__name__)

# 메모리 내 To-Do 리스트 (딕셔너리 구조로 변경)
todo_list = []

@app.route('/')
def index():
    return render_template('index.html', todos=todo_list)

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    if task:
        todo_list.append({'task': task, 'done': False})
    return redirect('/')

@app.route('/toggle/<int:task_id>')
def toggle(task_id):
    if 0 <= task_id < len(todo_list):
        todo_list[task_id]['done'] = not todo_list[task_id]['done']
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete(task_id):
    if 0 <= task_id < len(todo_list):
        todo_list.pop(task_id)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
