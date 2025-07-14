from flask import Flask, render_template
import database as db

app = Flask(__name__)

@app.route('/')
def index():
    chart_data = db.get_monthly_revenue()
    print(chart_data)
    return render_template('index3.html', data=chart_data)

if __name__ == '__main__':
    app.run(debug=True)
