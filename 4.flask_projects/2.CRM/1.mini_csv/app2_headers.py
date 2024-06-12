from flask import Flask, render_template
import csv

app = Flask(__name__)

# 모든 CSV 데이터를 저장하기 위한 전역 변수
all_csv_data = []
fieldnames = []

def load_csv_data(filepath):    
    with open(filepath, newline='', encoding='UTF8') as file:
        global fieldnames

        csv_data = csv.DictReader(file)

        # 공백을 제거한 fieldnames 생성
        fieldnames = [fieldname.strip() for fieldname in csv_data.fieldnames]
        for row in csv_data:
            clean_row = {fieldname.strip(): value.strip() for fieldname, value in row.items()}
            all_csv_data.append(clean_row)

@app.route('/')
def index():
    return render_template('index2.html', data=all_csv_data, fieldnames=fieldnames)

if __name__ == '__main__':
    # 서버가 시작될 때 한 번 CSV 데이터를 불러오기
    load_csv_data('./data.csv')
    app.run(debug=True)
