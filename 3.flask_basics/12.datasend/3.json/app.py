from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def json_page():
    return render_template('json_async.html')

@app.route('/submit_json', methods=['POST'])
def submit_json():
    data = request.json
    name = data.get('name')
    age = data.get('age')
    return f"Name: {name}, Age: {age}"

if __name__ == '__main__':
    app.run(debug=True)
