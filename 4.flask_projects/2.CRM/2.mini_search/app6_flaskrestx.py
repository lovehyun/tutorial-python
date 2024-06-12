# pip install flask-restx

from flask import Flask, render_template, request, jsonify
from flask_restx import Api, Resource, fields
import csv
import math

app = Flask(__name__)

# 기존 Flask 라우트
@app.route('/')
def index():
    return render_template('index6.html')

@app.route('/user/<id>')
def user_detail(id):
    user_data = None
    for row in all_csv_data:
        if row['Id'] == id:
            user_data = row
            break

    if user_data:
        return render_template('user_detail3.html', user=user_data)
    else:
        return "User not found", 404

# 기본 라우트 생성 이후 문서 API 정의 및 등록
api = Api(app, version='1.0', title='User API', description='A simple User API', doc='/api/docs')
ns = api.namespace('users', path='/api/users', description='User operations')

# 전역 변수에 CSV 데이터를 저장
all_csv_data = []
fieldnames = []

def load_csv_data(filepath):
    global all_csv_data, fieldnames
    
    with open(filepath, newline='', encoding='utf-8') as file:
        csv_data = csv.DictReader(file)
        all_csv_data = list(csv_data)
        fieldnames = csv_data.fieldnames

# API 모델 정의
user_model = api.model('User', {
    'Id': fields.String(required=True, description='The user identifier'),
    'Name': fields.String(required=True, description='The user name'),
    # 필요한 다른 필드를 추가하세요...
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

        filtered_data = [row for row in all_csv_data if search_name.lower() in row['Name'].lower()]

        total_items = len(filtered_data)
        total_pages = math.ceil(total_items / items_per_page)

        start_index = (page - 1) * items_per_page
        end_index = start_index + items_per_page
        paginated_data = filtered_data[start_index:end_index]

        headers = ['index'] + fieldnames
        for i, item in enumerate(paginated_data, start=start_index + 1):
            item['index'] = i

        return jsonify({
            'fieldnames': headers,
            'data': paginated_data,
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
        user_data = None
        for row in all_csv_data:
            if row['Id'] == id:
                user_data = row
                break

        if user_data:
            return user_data
        else:
            api.abort(404, "User {} doesn't exist".format(id))

if __name__ == '__main__':
    load_csv_data('user.csv')
    app.run(debug=True)
