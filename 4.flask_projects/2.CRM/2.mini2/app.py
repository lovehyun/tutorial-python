from flask import Flask, render_template, request
import csv

app = Flask(__name__)

@app.route('/')
@app.route('/<int:page>')
def index(page=1):
    per_page = 10 # 한 페이지에 보여줄 항목 수
    data = []

    with open('data.csv', 'r', encoding='utf-8') as file:
        csv_data = csv.DictReader(file)
        data = list(csv_data)
        
    # 정수 나눗셈(//) 을 통해 전체 페이지 개수 구하기
    total_pages = (len(data) + per_page - 1) // per_page

    # 시작부터 해당 페이지의 끝까지 인덱스 구하기
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    
    # 원하는 페이지 row 정보만을 추출
    current_page_rows = data[start_index:end_index]

    return render_template('index.html', data=current_page_rows, page=page, total_pages=total_pages)

if __name__ == '__main__':
    app.run(debug=True)
