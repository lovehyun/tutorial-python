import logging
from flask import Flask
import os

app = Flask(__name__)

# 환경변수로부터 로그 레벨 읽기
log_level = os.getenv('LOG_LEVEL', 'DEBUG').upper()

# 유효한 로그 레벨인지 확인
if not hasattr(logging, log_level):
    log_level = 'DEBUG'

# 기본 로그 레벨을 설정
logging.basicConfig(level=getattr(logging, log_level))

# 현재 모듈의 로그 레벨 설정
logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, log_level))

# werkzeug의 로그 레벨을 DEBUG로 설정하여 부팅 로그가 출력되도록 함
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.DEBUG)

# 포맷터 설정
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 콘솔 핸들러 설정
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# 파일 핸들러 설정
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(getattr(logging, log_level))
file_handler.setFormatter(formatter)

# werkzeug 로거에 핸들러 추가
werkzeug_logger.addHandler(console_handler)
werkzeug_logger.addHandler(file_handler)

# 현재 모듈의 로거에도 파일 핸들러 추가
logger.addHandler(file_handler)

@app.route('/')
def home():
    app.logger.debug("This is a debug message")
    app.logger.info("This is an info message")
    app.logger.warning("This is a warning message")
    app.logger.error("This is an error message")
    app.logger.critical("This is a critical message")
    return "Hello, Flask!"

if __name__ == '__main__':
    app.run(debug=True)
