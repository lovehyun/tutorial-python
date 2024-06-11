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
    # GET 파라미터를 통한 인자 처리
    page = request.args.get('page', default=1, type=int)
    items_per_page = 10
    
    # 정수 나눗셈(//) 대신 math.ceil 통해서 올림함수로 계산하기
    total_items = len(all_csv_data)
    total_pages = math.ceil(total_items / items_per_page)

    # 시작부터 해당 페이지의 끝까지 인덱스 구하기
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page

    # 원하는 데이터만 추출
    paginated_data = all_csv_data[start_index:end_index]

    return render_template('index2.html', fieldnames=fieldnames, data=paginated_data, page=page, total_pages=total_pages)

if __name__ == '__main__':
    # 서버가 시작될 때 한 번 CSV 데이터를 불러오기
    load_csv_data('data.csv')  # CSV 파일 경로를 여기에 지정
    app.run(debug=True)
