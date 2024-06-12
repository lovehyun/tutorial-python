from flask import Flask, render_template, request
import csv
import math

app = Flask(__name__)

# 전역 변수에 CSV 데이터를 저장
all_csv_data = []
fieldnames = []

def load_csv_data(filepath):
    # 주어진 파일 경로에서 CSV 데이터를 불러오는 함수.
    global all_csv_data, fieldnames
    
    with open(filepath, newline='', encoding='utf-8') as file:
        csv_data = csv.DictReader(file)
        all_csv_data = list(csv_data)
        fieldnames = csv_data.fieldnames

@app.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    search_name = request.args.get('name', default='', type=str)
    items_per_page = 10  # 한 페이지에 보여줄 항목 수

    # 검색어가 포함된 데이터만 필터링
    filtered_data = [row for row in all_csv_data if search_name.lower() in row['Name'].lower()]

    total_items = len(filtered_data)
    total_pages = math.ceil(total_items / items_per_page)

    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    paginated_data = filtered_data[start_index:end_index]

    # 'index' 값을 각 딕셔너리에 추가 (원본 데이터는 수정하지 않음)
    headers = ['index'] + fieldnames
    for i, item in enumerate(paginated_data, start=start_index + 1):
        item['index'] = i

    return render_template('index4.html', fieldnames=headers, data=paginated_data, search_name=search_name, page=page, total_pages=total_pages)

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

if __name__ == '__main__':
    # 서버가 시작될 때 한 번 CSV 데이터를 불러오기
    load_csv_data('data.csv')  # CSV 파일 경로를 여기에 지정
    app.run(debug=True)
