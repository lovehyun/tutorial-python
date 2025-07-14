from flask import Flask, jsonify, request
from database3 import get_stores, get_store_by_name

app = Flask(__name__, static_folder='static')

@app.route('/api/stores', methods=['GET'])
def api_stores():
    # stores = get_stores()
    # return jsonify(stores)

    name = request.args.get('name')
    if name:
        stores = get_store_by_name(name)
    else:
        stores = get_stores()
    return jsonify(stores)

@app.route('/')
def index():
    return app.send_static_file('index3.html')

if __name__ == '__main__':
    app.run(debug=True)
