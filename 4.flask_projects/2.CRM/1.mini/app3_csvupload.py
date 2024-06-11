from flask import Flask, render_template, request
import io
import csv

app = Flask(__name__)

# 모든 CSV 데이터를 저장하기 위한 전역 변수
all_csv_data = []

@app.route('/')
def index():
    return render_template('index3.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # 요청 파일이 없을 경우
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    # 파일명이 없을 경우
    if file.filename == '':
        return 'No selected file'
    if file:
        csv_data = []
        # 파일을 텍스트 모드로 읽어오기 위해 StringIO 사용
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_reader = csv.reader(stream)
        # 각 줄을 csv_data에 추가
        for row in csv_reader:
            csv_data.append(row)
        return render_template('table3.html', data=csv_data)

@app.route('/upload2', methods=['POST'])
def upload2_file():
    global all_csv_data  # 글로벌 변수에 데이터 누적

    # 요청 파일이 없을 경우
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    # 파일명이 없을 경우
    if file.filename == '':
        return 'No selected file'
    if file:
        # 파일을 텍스트 모드로 읽어오기 위해 StringIO 사용
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_reader = csv.reader(stream)
        # 새로운 CSV 데이터를 리스트에 추가
        new_csv_data = [row for row in csv_reader]
        if all_csv_data:
            # 헤더가 다를 수 있거나 헤더를 건너뛰고 싶은 경우 처리
            new_csv_data = new_csv_data[1:]  # 헤더 건너뛰기
        all_csv_data.extend(new_csv_data)
        return render_template('table3.html', data=all_csv_data)


if __name__ == '__main__':
    app.run(debug=True)
