from flask import Flask, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
from database import Database

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
db = Database()

# 모든 CSV 데이터를 저장하기 위한 전역 변수
all_csv_data = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/create', methods=['POST'])
def create():
    try:
        title = request.form['title']
        message = request.form['message']
        file = request.files['file']
        filename = None
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        sql = "INSERT INTO board (title, message, image) VALUES (?, ?, ?)"
        db.execute(sql, (title, message, filename))
        db.commit()
        
        return jsonify({'result': 'success'})
    except Exception as e:
        return jsonify({'result': 'error', 'message': str(e)}), 500
    
@app.route('/list', methods=['GET'])
def list():
    try:
        sql = "SELECT id, title, message, image FROM board"
        result = db.execute_fetch(sql)
        
        dict_list = [{'id': r[0], 'title': r[1], 'message': r[2], 'image': r[3]} for r in result]
        return jsonify(dict_list)
    except Exception as e:
        return jsonify({'result': 'error', 'message': str(e)}), 500

@app.route('/delete', methods=['POST'])
def delete():
    try:
        data = request.get_json()
        post_id = data.get('id')
        sql = "DELETE FROM board WHERE id=?"
        db.execute(sql, (post_id,))
        db.commit()
        return jsonify({'result': 'success'})
    except Exception as e:
        return jsonify({'result': 'error', 'message': str(e)}), 500

@app.route('/modify', methods=['POST'])
def modify():
    try:
        data = request.form
        title = data.get('title')
        message = data.get('message')
        post_id = data.get('id')
        file = request.files.get('file')
        filename = None
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        if filename:
            sql = "UPDATE board SET title=?, message=?, image=? WHERE id=?"
            db.execute(sql, (title, message, filename, post_id))
        else:
            sql = "UPDATE board SET title=?, message=? WHERE id=?"
            db.execute(sql, (title, message, post_id))
        
        db.commit()
        return jsonify({'result': 'success'})
    except Exception as e:
        return jsonify({'result': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
