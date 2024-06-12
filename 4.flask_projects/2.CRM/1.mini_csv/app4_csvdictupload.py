from flask import Flask, render_template, request, redirect, url_for
import io
import csv

app = Flask(__name__)

# 모든 CSV 데이터를 저장하기 위한 전역 변수
all_csv_data = []

@app.route('/')
def index():
    if not all_csv_data:
        return redirect(url_for('upload'))
    
    return render_template('index4.html', data=all_csv_data)

@app.route('/upload')
def upload():
    return render_template('upload3.html')

# CSV 파일을 처리하고 데이터를 반환
def process_csv(file):
    if not file or file.filename == '':
        return 'No selected file', None
    
    csv_data = []
    # 파일을 텍스트 모드로 읽어오기 위해 StringIO 사용
    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    csv_reader = csv.DictReader(stream)
    for row in csv_reader:
        csv_data.append(row)
    
    return None, csv_data

@app.route('/upload_overwrite', methods=['POST'])
def upload_file():
    error, csv_data = process_csv(request.files.get('file'))
    if error:
        return error
    
    if csv_data:
        global all_csv_data
        all_csv_data = csv_data

    return render_template('index4.html', data=all_csv_data)

@app.route('/upload_append', methods=['POST'])
def upload2_file():
    error, csv_data = process_csv(request.files.get('file'))
    if error:
        return error

    if csv_data:
        all_csv_data.extend(csv_data)
    
    return render_template('index4.html', data=all_csv_data)

if __name__ == '__main__':
    app.run(debug=True)
