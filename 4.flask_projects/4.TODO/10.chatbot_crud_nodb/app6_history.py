import logging

from flask import Flask
from flask_cors import CORS

from routes.todo_routes5_refactor import todo_bp
from routes.chatbot_routes6_history import chatbot_bp

logging.basicConfig(
    level=logging.DEBUG,  # DEBUG 이상 모두 출력
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

# 외부 라이브러리 로그는 WARN 이상만 출력
logging.getLogger("openai").setLevel(logging.WARN)
logging.getLogger("httpx").setLevel(logging.WARN)
logging.getLogger("httpcore").setLevel(logging.WARN)
logging.getLogger("werkzeug").setLevel(logging.WARN)
logger = logging.getLogger(__name__)  # 내 모듈 전용 로거

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
    # logger.debug("디버그 메시지")    # 상세한 내부 상태 (개발/디버그용)
    # logger.info("정보 메시지")       # 일반 상태 보고
    # logger.warning("경고 메시지")    # 주의해야 할 상황
    # logger.error("에러 메시지")      # 오류 상황
    # logger.critical("치명적 오류")   # 프로그램 중단 수준

    app.run(debug=True)
