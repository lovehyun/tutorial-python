# app.py

from flask import Flask, render_template
from data import get_seoul_population_data

app = Flask(__name__)

# Flask 라우트 정의
@app.route('/')
def index():
    seoul_data = get_seoul_population_data()
    return render_template('population_map.html', seoul_data=seoul_data)

if __name__ == '__main__':
    app.run(debug=True)
