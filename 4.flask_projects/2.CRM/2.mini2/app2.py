from flask import Flask, render_template, request
import csv
import math

app = Flask(__name__)

@app.route('/')
def index():
    # GET 파라미터를 통한 인자 처리
    page = request.args.get('page', default=1, type=int)
    items_per_page = 10
    data = []
    
    with open('data.csv', 'r', encoding='utf-8') as file:
        csv_data = csv.DictReader(file)
        for row in csv_data:
            data.append(row)

    # 필드 헤더값 별도로 전달
    fieldnames = csv_data.fieldnames

    # 정수 나눗셈(//) 대신 math.ceil 통해서 올림함수로 계산하기
    total_items = len(data)
    total_pages = math.ceil(total_items / items_per_page)

    # 시작부터 해당 페이지의 끝까지 인덱스 구하기
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page

    # 원하는 데이터만 추출
    paginated_data = data[start_index:end_index]

    return render_template('index2.html', fieldnames=fieldnames, data=paginated_data, page=page, total_pages=total_pages)


if __name__ == '__main__':
    app.run(debug=True)
