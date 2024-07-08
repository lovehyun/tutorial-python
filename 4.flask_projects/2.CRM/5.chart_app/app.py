from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get_data():
    data = {
        'labels': ['2023-01', '2023-02', '2023-03', '2023-04', '2023-05', '2023-06', '2023-07', '2023-08', '2023-09', '2023-10', '2023-11', '2023-12'],
        'values': [797500, 401500, 665500, 660000, 566500, 709500, 753500, 814000, 731500, 715000, 621500, 704000]
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
