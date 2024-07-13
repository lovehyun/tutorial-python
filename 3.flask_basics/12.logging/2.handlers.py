import logging

# 로거 생성
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)  # 로거의 로그 레벨 설정

# 핸들러 생성 (콘솔 핸들러)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  # 핸들러의 로그 레벨 설정

# 핸들러 생성 (파일 핸들러)
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.INFO)  # 핸들러의 로그 레벨 설정

# 포맷터 생성 및 핸들러에 설정
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# 로거에 핸들러 추가
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# 로그 메시지 생성
logger.debug('This is a debug message')
logger.info('This is an info message')
logger.warning('This is a warning message')
logger.error('This is an error message')
logger.critical('This is a critical message')
