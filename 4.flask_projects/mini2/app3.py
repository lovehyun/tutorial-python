from flask import Flask, render_template, request
import csv
import math

app = Flask(__name__)

@app.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    items_per_page = 10
    data = []

    with open('data.csv', 'r', encoding='utf-8') as file:
        csv_data = csv.DictReader(file)
        for row in csv_data:
            data.append(row)

    fieldnames = csv_data.fieldnames

    total_items = len(data)
    total_pages = math.ceil(total_items / items_per_page)

    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    paginated_data = data[start_index:end_index]

    return render_template('index3.html', fieldnames=fieldnames, data=paginated_data, page=page, total_pages=total_pages)

@app.route('/user/<id>')
def user_detail(id):
    with open('data.csv', 'r', encoding='utf-8') as file:
        csv_data = csv.DictReader(file)
        for row in csv_data:
            if row['Id'] == id:
                user_data = row
                break

    return render_template('user_detail3.html', user=user_data)


if __name__ == '__main__':
    app.run(debug=True)
