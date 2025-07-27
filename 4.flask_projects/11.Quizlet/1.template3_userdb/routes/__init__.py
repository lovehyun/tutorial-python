# routes/__init__.py
# Blueprint 패키지 초기화 파일

from .user_routes import user_bp
from .quiz_routes import quiz_bp
from .result_routes import result_bp

__all__ = ['user_bp', 'quiz_bp', 'result_bp']
