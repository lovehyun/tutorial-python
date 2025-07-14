from flask import Flask, jsonify
import sqlite3

app = Flask(__name__, static_folder='static')

def get_stores():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stores")
    stores = cursor.fetchall()
    conn.close()
    return stores

@app.route('/api/stores', methods=['GET'])
def api_stores():
    stores = get_stores()
    return jsonify(stores)

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True)
