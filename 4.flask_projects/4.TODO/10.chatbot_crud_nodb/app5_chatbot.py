from flask import Flask
from flask_cors import CORS

# from routes.todo_routes import todo_bp
from routes.todo_routes5_refactor import todo_bp
from routes.chatbot_routes import chatbot_bp

app = Flask(__name__, static_folder="public", static_url_path="")
CORS(app, resources={r"/api/*": {"origins": "*"}})
# CORS(app)

# 블루프린트 등록
app.register_blueprint(todo_bp, url_prefix="/api/todo")
app.register_blueprint(chatbot_bp, url_prefix="/api/chat")

@app.route("/")
def home():
    return app.send_static_file("index_restapi.html")

if __name__ == "__main__":
    app.run(debug=True)
