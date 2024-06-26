from flask import Flask, render_template
import csv

app = Flask(__name__)

# 전역 변수에 CSV 데이터를 저장
all_csv_data = []

def load_csv_data(filepath):
    # 주어진 파일 경로에서 CSV 데이터를 불러오는 함수.
    global all_csv_data
    
    with open(filepath, newline='', encoding='utf-8') as file:
        csv_data = csv.DictReader(file)
        all_csv_data = list(csv_data)

@app.route('/')
@app.route('/<int:page>')
def index(page=1):
    per_page = 10  # 한 페이지에 보여줄 항목 수

    # 정수 나눗셈(//)을 통해 전체 페이지 개수 구하기
    total_pages = (len(all_csv_data) + per_page - 1) // per_page

    # 시작부터 해당 페이지의 끝까지 인덱스 구하기
    start_index = (page - 1) * per_page
    end_index = start_index + per_page

    # 원하는 페이지 row 정보만을 추출
    current_page_rows = all_csv_data[start_index:end_index]

    return render_template('index.html', data=current_page_rows, page=page, total_pages=total_pages)

if __name__ == '__main__':
    # 서버가 시작될 때 한 번 CSV 데이터를 불러오기
    load_csv_data('data.csv')  # CSV 파일 경로를 여기에 지정
    app.run(debug=True)
