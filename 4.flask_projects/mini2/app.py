from flask import Flask, render_template, request
import csv

app = Flask(__name__)

@app.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    per_page = 10
    data = []

    with open('data.csv', 'r', encoding='utf-8') as file:
        csv_data = csv.DictReader(file)
        rows = list(csv_data)
        total_pages = (len(rows) + per_page - 1) // per_page

        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        current_page_rows = rows[start_index:end_index]

        for row in current_page_rows:
            data.append(row)

    return render_template('index.html', data=data, page=page, total_pages=total_pages)

if __name__ == '__main__':
    app.run(debug=True)
