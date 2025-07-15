from flask import Flask, render_template
import database3 as db

app = Flask(__name__)

@app.route('/')
def index():
    stores = db.get_stores()
    # stores = db.get_stores2()
    # stores = db.get_stores3()
    print(stores)
    
    return render_template('index.html', stores=stores)

if __name__ == '__main__':
    app.run(debug=True)
