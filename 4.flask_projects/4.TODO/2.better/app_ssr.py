from flask import Flask, request, redirect, render_template

app = Flask(__name__)

todos = []
next_id = 1

@app.route('/')
def index():
    return render_template('index_ssr.html', todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    global next_id
    task = request.form.get('task')
    if task:
        todos.append({'id': next_id, 'task': task, 'done': False})
        next_id += 1
    return redirect('/')

@app.route('/toggle/<int:todo_id>', methods=['POST'])
def toggle_todo(todo_id):
    for todo in todos:
        if todo['id'] == todo_id:
            todo['done'] = not todo['done']
            break
    return redirect('/')

@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    for todo in todos:
        if todo['id'] == todo_id:
            todos.remove(todo)
            break
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
