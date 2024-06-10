from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///board.db'
db = SQLAlchemy(app)

class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create():
    title = request.form['title']
    message = request.form['message']

    new_board = Board(title=title, message=message)
    db.session.add(new_board)
    db.session.commit()

    return jsonify({'result': 'success'})

@app.route('/list', methods=['GET'])
def list():
    boards = Board.query.all()
    dict_list = [{'id': board.id, 'title': board.title, 'message': board.message} for board in boards]

    return jsonify(dict_list)

@app.route('/delete', methods=['POST'])
def delete():
    id = request.form['id']
    board = Board.query.get(id)

    if board:
        db.session.delete(board)
        db.session.commit()

        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'failure', 'message': '게시글이 존재하지 않습니다.'})

@app.route('/modify', methods=['POST'])
def modify():
    id = request.form['id']
    board = Board.query.get(id)
    # 위 함수가 deprecated 되어서, 권장방식은 아래
    # board = Board.query.filter_by(id=id).first()

    if board:
        title = request.form['title']
        message = request.form['message']
        board.title = title
        board.message = message

        db.session.commit()

        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'failure', 'message': '게시글이 존재하지 않습니다.'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
