from flask import Flask, render_template
import csv

app = Flask(__name__)

# 모든 CSV 데이터를 저장하기 위한 전역 변수
all_csv_data = []

def load_csv_data(filepath):
    global all_csv_data
    
    with open(filepath, newline='', encoding='UTF8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            all_csv_data.append(row)

@app.route('/')
def index():
    return render_template('table3.html', data=all_csv_data)

if __name__ == '__main__':
    # 서버가 시작될 때 한 번 CSV 데이터를 불러오기
    load_csv_data('./data.csv')  # CSV 파일 경로를 여기에 지정
    app.run(debug=True)
