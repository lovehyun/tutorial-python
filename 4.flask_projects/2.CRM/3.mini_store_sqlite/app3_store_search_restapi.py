from flask import Flask, jsonify, request
import database3 as db

app = Flask(__name__, static_folder='static')

@app.route('/api/stores', methods=['GET'])
def api_stores():
    name = request.args.get('name')
    if name:
        stores = db.get_store_by_name(name)
    else:
        stores = db.get_stores()
    return jsonify(stores)

@app.route('/')
def index():
    return app.send_static_file('index3.html')

if __name__ == '__main__':
    app.run(debug=True)
