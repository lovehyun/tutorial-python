# pip install flask-restx
# http://localhost:5000/api/docs에서 Swagger UI 확인 가능

from flask import Flask, render_template, request, jsonify
from flask_restx import Api, Resource, fields
import math
import database as db

app = Flask(__name__)

# 기본 HTML 페이지
@app.route('/')
def index():
    return render_template('index6.html')

@app.route('/user/<id>')
def user_detail(id):
    user = db.get_user_by_id(id)
    if user:
        return render_template('user_detail3.html', user=user)
    else:
        return "User not found", 404

# REST API 문서 설정
api = Api(app, version='1.0', title='User API', description='A simple User API', doc='/api/docs')
ns = api.namespace('users', path='/api/users', description='User operations')

# API 모델 정의
user_model = api.model('User', {
    'Id': fields.String(required=True, description='The user identifier'),
    'Name': fields.String(required=True, description='The user name'),
    # 다른 필드도 필요하면 추가하세요 (예: Age, Email 등)
})

@ns.route('/')
class UserList(Resource):
    @ns.doc('list_users')
    @ns.param('page', 'The page number')
    @ns.param('name', 'The name to search')
    @ns.param('items_per_page', 'Number of items per page')
    def get(self):
        page = request.args.get('page', default=1, type=int)
        search_name = request.args.get('name', default='', type=str)
        items_per_page = request.args.get('items_per_page', default=10, type=int)

        total_items = db.get_user_count_by_name(search_name)
        total_pages = math.ceil(total_items / items_per_page)
        users = db.get_users_by_name_per_page(page, items_per_page, search_name)

        # dict 변환 + index 추가
        result = []
        for i, row in enumerate(users, start=(page - 1) * items_per_page + 1):
            user_dict = dict(row)
            user_dict["index"] = i
            result.append(user_dict)

        return jsonify({
            'fieldnames': ['index'] + list(users[0].keys()) if users else [],
            'data': result,
            'search_name': search_name,
            'page': page,
            'total_pages': total_pages,
            'items_per_page': items_per_page
        })

@ns.route('/<id>')
@ns.response(404, 'User not found')
@ns.param('id', 'The user identifier')
class User(Resource):
    @ns.doc('get_user')
    @ns.marshal_with(user_model)
    def get(self, id):
        user = db.get_user_by_id(id)
        if user:
            return user
        else:
            api.abort(404, f"User {id} doesn't exist")

if __name__ == '__main__':
    app.run(debug=True)
