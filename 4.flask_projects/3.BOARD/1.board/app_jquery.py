from flask import Flask, render_template
from flask import request, jsonify
from database import Database

app = Flask(__name__)
db = Database()

@app.route('/')
def index():
    return render_template('index_jquery.html')

@app.route('/create', methods=['POST'])
def create():
    # contentType: 'application/json', 으로 보냈으면,
    # data = request.get_json()  # JSON 데이터를 가져옴
    # title = data['title']
    # message = data['message']

    # contentType: 'application/x-www-form-urlencoded', 으로 보냈으면 (기본값),
    title = request.form['title']
    message = request.form['message']
    sql = "INSERT INTO board(title, message) VALUES('{}', '{}')".format(title, message)
    db.execute(sql)
    db.commit()
    return jsonify({'result': 'success'})

@app.route('/list', methods=['GET'])
def list():
    tuple_keys = ("id", "title", "message")

    sql = "SELECT * FROM board"
    result = db.execute_fetch(sql)
    print(result)
    
    dict_list = []
    for r in result:
        # dict_value = {k: v for k, v in zip(tuple_keys, r)}
        dict_value = dict(zip(tuple_keys, r))
        dict_list.append(dict_value)

    print(dict_list)
    return jsonify(dict_list)

@app.route('/delete', methods=['POST'])
def delete():
    id = request.form['id']
    print("id:", id)

    sql = "DELETE FROM board WHERE id={}".format(id)
    db.execute(sql)
    db.commit()
    return jsonify({'result': 'success'})

@app.route('/modify', methods=['POST'])
def modify():
    title = request.form['title']
    message = request.form['message']
    id = request.form['id']
    
    sql = "UPDATE board SET title='{}', message='{}' WHERE id={}".format(title, message, id)
    db.execute(sql)
    db.commit()
    return jsonify({'result': 'success'})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
