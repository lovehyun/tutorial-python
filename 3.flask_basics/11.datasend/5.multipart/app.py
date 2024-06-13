from flask import Flask, request, render_template
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
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
