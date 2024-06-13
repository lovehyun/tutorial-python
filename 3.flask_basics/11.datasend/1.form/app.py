from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    name = request.form.get('name')
    age = request.form.get('age')
    return f"Name: {name}, Age: {age}"

if __name__ == '__main__':
    app.run(debug=True)
