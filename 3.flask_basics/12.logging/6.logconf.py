import logging
import logging.config

# 로깅 설정 파일 불러오기
logging.config.fileConfig('logging.conf')

# 로거 생성
logger = logging.getLogger('myapp')
module1_logger = logging.getLogger('myapp.module1')

# 로그 메시지 생성
logger.debug('This is a debug message from myapp logger')
logger.info('This is an info message from myapp logger')
logger.warning('This is a warning message from myapp logger')
logger.error('This is an error message from myapp logger')
logger.critical('This is a critical message from myapp logger')

module1_logger.debug('This is a debug message from myapp.module1 logger')
module1_logger.info('This is an info message from myapp.module1 logger')
module1_logger.warning('This is a warning message from myapp.module1 logger')
module1_logger.error('This is an error message from myapp.module1 logger')
module1_logger.critical('This is a critical message from myapp.module1 logger')
