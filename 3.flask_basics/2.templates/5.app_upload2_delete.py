from flask import Flask, request, render_template, redirect, url_for
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('upload2.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return '파일이 전송되지 않았습니다.'

    file = request.files['file']

    if file.filename == '':
        return '파일이 선택되지 않았습니다.'

    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return redirect(url_for('file_list'))

    return '허용되지 않은 파일 형식입니다.'

@app.route('/files')
def file_list():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('files2.html', files=files)

@app.route('/delete/<filename>')
def delete_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        return redirect(url_for('file_list'))
    else:
        return '파일이 존재하지 않습니다.'

if __name__ == '__main__':
    app.run(debug=True)
