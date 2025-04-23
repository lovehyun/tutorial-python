from flask import Flask, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
from database import Database

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
db = Database()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return send_from_directory('static', 'index2.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/create', methods=['POST'])
def create():
    try:
        title = request.form['title']
        message = request.form['message']
        file = request.files.get('file')
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
        
        # Get the current image filename
        sql = "SELECT image FROM board WHERE id=?"
        current_image = db.execute_fetch(sql, (post_id,))
        
        if current_image and current_image[0][0]: # [(image_filename,)]
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], current_image[0][0])
            if os.path.exists(image_path):
                os.remove(image_path)
        
        # Delete the post
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
        delete_image = data.get('delete_image') == 'true'
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Get the current image filename
        sql = "SELECT image FROM board WHERE id=?"
        result = db.execute_fetch(sql, (post_id,))
        current_image = result[0][0] if result else None

        if delete_image:
            # Delete the existing file if delete_image is true
            if current_image:
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], current_image)
                if os.path.exists(image_path):
                    os.remove(image_path)
            sql = "UPDATE board SET title=?, message=?, image=NULL WHERE id=?"
            db.execute(sql, (title, message, post_id))
        elif filename:
            # Delete the existing file if a new file is uploaded
            if current_image:
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], current_image)
                if os.path.exists(image_path):
                    os.remove(image_path)
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
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(host="0.0.0.0", port=5000, debug=True)
