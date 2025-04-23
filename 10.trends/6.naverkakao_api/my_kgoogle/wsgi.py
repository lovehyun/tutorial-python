from werkzeug.middleware.dispatcher import DispatcherMiddleware
from app import app
import os

# prefix 설정 (환경변수에서 가져오기)
PREFIX = os.getenv("FLASK_URL_PREFIX", "")

application = DispatcherMiddleware(None, {
    PREFIX: app  # 예: '/kgoogle'
})
