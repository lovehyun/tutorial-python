from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/query')
def query_page():
    return render_template('query.html')

@app.route('/submit_query', methods=['GET'])
def submit_query():
    name = request.args.get('name')
    age = request.args.get('age')
    return f"Name: {name}, Age: {age}"

if __name__ == '__main__':
    app.run(debug=True)
