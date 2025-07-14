from flask import Flask, render_template, request
import database3 as db

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    """
    이름(query string: ?name=xxx) 유무에 따라
    매장 목록을 필터링하거나 전체 조회합니다.
    """
    name = request.args.get("name", "").strip()
    if name:
        stores = db.get_store_by_name(name)
    else:
        stores = db.get_stores()
        
    # 템플릿에 검색어와 결과 전달
    return render_template("index3.html", stores=stores, search=name)

if __name__ == "__main__":
    app.run(debug=True)
