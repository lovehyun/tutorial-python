from flask import Flask, render_template, request
import csv
import math

app = Flask(__name__)

@app.route('/')
def index():
    data = []
    with open('data.csv', 'r', encoding='utf-8') as file:
        csv_data = csv.DictReader(file)

        for row in csv_data:
            data.append(row)

    fieldnames = csv_data.fieldnames

    items_per_page = 10  # 한 페이지에 보여줄 항목 수
    total_items = len(data)
    total_pages = math.ceil(total_items / items_per_page)

    page = request.args.get('page', default=1, type=int)
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    paginated_data = data[start_index:end_index]

    return render_template('index2.html', fieldnames=fieldnames, data=paginated_data, current_page=page, max_pages=total_pages)

if __name__ == '__main__':
    app.run(debug=True)
