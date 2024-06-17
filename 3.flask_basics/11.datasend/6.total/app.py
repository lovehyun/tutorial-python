from flask import Flask, request, render_template
from datetime import timedelta
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.permanent_session_lifetime = timedelta(days=1)

app.config['UPLOAD_FOLDER'] = 'uploads/'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    name = request.form.get('name')
    age = request.form.get('age')
    return f"Name: {name}, Age: {age}"

@app.route('/json')
def json_page():
    return render_template('json.html')

@app.route('/submit_json', methods=['POST'])
def submit_json():
    data = request.json
    name = data.get('name')
    age = data.get('age')
    return f"Name: {name}, Age: {age}"

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/upload_file', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return f"File uploaded successfully: {file.filename}"
    return "No file uploaded"

@app.route('/query')
def query_page():
    return render_template('query.html')

@app.route('/submit_query', methods=['GET'])
def submit_query():
    name = request.args.get('name')
    age = request.args.get('age')
    return f"Name: {name}, Age: {age}"

@app.route('/multipart')
def multipart_page():
    return render_template('multipart.html')

@app.route('/submit_multipart', methods=['POST'])
def submit_multipart():
    name = request.form.get('name')
    file = request.files['file']
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return f"Name: {name}, File uploaded successfully: {file.filename}"
    return "No file uploaded"


if __name__ == '__main__':
    app.run(debug=True)
