from flask import Flask, send_file, send_from_directory

app = Flask(__name__)

@app.route('/')
def home():
    return send_file('static/index.html')
    # return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
