from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_stores():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stores")
    stores = cursor.fetchall()
    conn.close()
    return stores

@app.route('/')
def index():
    stores = get_stores()
    return render_template('index.html', stores=stores)

if __name__ == '__main__':
    app.run(debug=True)
