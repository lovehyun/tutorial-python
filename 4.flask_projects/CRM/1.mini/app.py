from flask import Flask, render_template
import csv

app = Flask(__name__)

@app.route('/')
def index():
    data = []
    with open('data.csv', 'r', encoding='utf-8') as file:
        csv_data = csv.DictReader(file)

        for row in csv_data:
            clean_row = {fieldname.strip(): value.strip() for fieldname, value in row.items()}
            data.append(clean_row)
            # data.append(row)

    print(data)
    return render_template('index.html', data=data)

@app.route('/another')
def another():
    data = []
    with open('data.csv', 'r', encoding='utf-8') as file:
        csv_data = csv.reader(file)

        # Get the header row
        header = next(csv_data)

        for row in csv_data:
            clean_row = {fieldname.strip(): value.strip() for fieldname, value in zip(header, row)}
            data.append(clean_row)

    print(data)
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
