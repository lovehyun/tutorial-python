from flask import Flask, render_template
import csv

app = Flask(__name__)

@app.route('/')
def index():
    data = []
    with open('data.csv', 'r', encoding='utf-8') as file:
        csv_data = csv.DictReader(file)

        # 공백을 제거한 fieldnames 생성
        fieldnames = [fieldname.strip() for fieldname in csv_data.fieldnames]
        for row in csv_data:
            clean_row = {fieldname.strip(): value.strip() for fieldname, value in row.items()}
            data.append(clean_row)
        
    print(data)
    return render_template('index2.html', data=data, fieldnames=fieldnames)

if __name__ == '__main__':
    app.run(debug=True)
