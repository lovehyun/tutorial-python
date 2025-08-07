from flask import Flask, request, redirect, render_template

app = Flask(__name__)

# 메모리 내 To-Do 리스트 (딕셔너리 구조로 담김)
todos = []

# READ = GET
@app.route('/')
def index():
    return render_template('index_ssr.html', todos=todos)

# CREATE = POST
@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    if task:
        todos.append({'task': task, 'done': False})
    return redirect('/')

# UPDATE = GET
@app.route('/toggle/<int:task_id>')
def toggle(task_id): 
    if 0 <= task_id < len(todos):
        todos[task_id]['done'] = not todos[task_id]['done']
    return redirect('/')

# DELETE = GET
@app.route('/delete/<int:task_id>')
def delete(task_id):
    if 0 <= task_id < len(todos):
        todos.pop(task_id)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
