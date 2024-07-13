import logging

# 로그 레벨의 우선순위 (낮은 것에서 높은 것 순서)
# DEBUG: 가장 낮은 우선순위로, 매우 상세한 로그 메시지를 출력합니다. 주로 개발 및 디버깅 시에 사용됩니다.
# INFO: 일반적인 정보를 나타냅니다. 애플리케이션의 정상적인 동작을 기록합니다.
# WARNING: 주의가 필요한 상황을 나타냅니다. 심각한 문제는 아니지만 주의해야 할 상황을 기록합니다.
# ERROR: 에러가 발생했음을 나타냅니다. 이 로그 레벨은 애플리케이션의 일부 기능이 실패했음을 기록합니다.
# CRITICAL: 가장 높은 우선순위로, 심각한 문제를 나타냅니다. 애플리케이션이 실행될 수 없는 상태를 기록합니다.

# 기본 로그 레벨을 DEBUG로 설정합니다.
logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.ERROR)
# logging.basicConfig(level=logging.CRITICAL)

# 각 로그 레벨로 메시지를 출력합니다.
logging.debug("This is a debug message")
logging.info("This is an info message")
logging.warning("This is a warning message")
logging.error("This is an error message")
logging.critical("This is a critical message")
