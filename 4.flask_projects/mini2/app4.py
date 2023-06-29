from flask import Flask, render_template, request
import csv
import math

app = Flask(__name__)

@app.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    search_name = request.args.get('name', default='', type=str)
    items_per_page = 10  # 한 페이지에 보여줄 항목 수
    data = []

    with open('data.csv', 'r', encoding='utf-8') as file:
        csv_data = csv.DictReader(file)
        for row in csv_data:
            if search_name not in row['Name']:
                continue  # 검색어가 포함되어 있지 않으면 생략
            data.append(row)

    fieldnames = csv_data.fieldnames

    total_items = len(data)
    total_pages = math.ceil(total_items / items_per_page)

    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    paginated_data = data[start_index:end_index]

    return render_template('index4.html', fieldnames=fieldnames, data=paginated_data, search_name=search_name, page=page, total_pages=total_pages)

@app.route('/user/<id>')
def user_detail(id):
    with open('data.csv', 'r', encoding='utf-8') as file:
        csv_data = csv.DictReader(file)
        for row in csv_data:
            if row['Id'] == id:
                user_data = row
                break

    return render_template('user_detail3.html', user=user_data)

if __name__ == '__main__':
    app.run(debug=True)
