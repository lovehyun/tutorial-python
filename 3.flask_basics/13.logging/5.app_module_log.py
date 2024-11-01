import logging
from flask import Flask
import os

app = Flask(__name__)

# 환경변수로부터 로그 레벨 읽기
log_level = os.getenv('LOG_LEVEL', 'DEBUG').upper()

# 유효한 로그 레벨인지 확인
if not hasattr(logging, log_level):
    log_level = 'DEBUG'

# 기본 로그 레벨을 설정 (기본 핸들러 추가하지 않음)
logging.basicConfig(level=getattr(logging, log_level), handlers=[])

# 현재 모듈의 로거 설정
logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, log_level))

# werkzeug의 로그 레벨 설정
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

# werkzeug 로거에 파일 핸들러 추가
werkzeug_logger.addHandler(file_handler)

# 현재 모듈의 로거에 콘솔 핸들러 추가
logger.addHandler(console_handler)

# app.logger에 기본 핸들러 제거 (기존 핸들러 제거)
for handler in app.logger.handlers[:]:
    app.logger.removeHandler(handler)
# app.logger에 파일 핸들러 추가
app.logger.addHandler(file_handler)

@app.route('/')
def home():
    app.logger.debug("This is a debug message from app.logger")
    app.logger.info("This is an info message from app.logger")
    app.logger.warning("This is a warning message from app.logger")
    app.logger.error("This is an error message from app.logger")
    app.logger.critical("This is a critical message from app.logger")
    
    logger.debug("This is a debug message from custom logger")
    logger.info("This is an info message from custom logger")
    logger.warning("This is a warning message from custom logger")
    logger.error("This is an error message from custom logger")
    logger.critical("This is a critical message from custom logger")
    
    return "Hello, Flask!"

if __name__ == '__main__':
    app.run(debug=True)
