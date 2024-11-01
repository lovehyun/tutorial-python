from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def json_page():
    return render_template('json2_async.html')

@app.route('/submit_json', methods=['POST', 'PUT', 'DELETE'])
def submit_json():
    # request.json은 요청 본문이 JSON 형식일 경우, 이를 자동으로 파싱하여 반환합니다.
    # request.get_json()은 JSON 데이터를 파싱하여 반환하는 메서드입니다.
    # data = request.get_json(silent=True) 유효하지 않은 JSON 데이터가 있을 때 예외를 발생시킵니다.
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')
    
    if request.method == 'POST':
        # POST 요청 처리
        return jsonify({"message": "POST request received", "name": name, "age": age})
    elif request.method == 'PUT':
        # PUT 요청 처리
        return jsonify({"message": "PUT request received", "name": name, "age": age})
    elif request.method == 'DELETE':
        # DELETE 요청 처리
        return jsonify({"message": "DELETE request received", "name": name, "age": age})

if __name__ == '__main__':
    app.run(debug=True)
