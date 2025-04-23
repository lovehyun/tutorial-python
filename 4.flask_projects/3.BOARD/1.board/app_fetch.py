from flask import Flask, send_from_directory, request, jsonify
from database import Database

app = Flask(__name__)
db = Database()

@app.route('/')
def index():
    return send_from_directory('static', 'index_fetch.html')

@app.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    title = data.get('title')
    message = data.get('message')
    sql = "INSERT INTO board (title, message) VALUES (?, ?)"
    db.execute(sql, (title, message))
    db.commit()
    return jsonify({'result': 'success'})

@app.route('/list', methods=['GET'])
def list():
    sql = "SELECT id, title, message FROM board"
    result = db.execute_fetch(sql)
    
    dict_list = [{'id': r[0], 'title': r[1], 'message': r[2]} for r in result]
    return jsonify(dict_list)

@app.route('/delete', methods=['POST'])
def delete():
    data = request.get_json()
    post_id = data.get('id')
    sql = "DELETE FROM board WHERE id=?"
    db.execute(sql, (post_id,))
    db.commit()
    return jsonify({'result': 'success'})

@app.route('/modify', methods=['POST'])
def modify():
    data = request.get_json()
    post_id = data.get('id')
    title = data.get('title')
    message = data.get('message')
    sql = "UPDATE board SET title=?, message=? WHERE id=?"
    db.execute(sql, (title, message, post_id))
    db.commit()
    return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
