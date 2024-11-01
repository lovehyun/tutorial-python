# 기본 개념

## 로거 (Logger)
- 로그 메시지를 생성하는 인터페이스입니다.
- `logging.getLogger(name)`을 통해 생성합니다.
- 애플리케이션 내에서 다양한 로거를 생성하여 모듈별로 로깅을 관리할 수 있습니다.

## 핸들러 (Handler)
- 로그 메시지를 원하는 출력 대상으로 보내는 역할을 합니다.
- 파일, 콘솔, 원격 서버 등으로 로그를 보낼 수 있습니다.
- 일반적인 핸들러: `StreamHandler` (콘솔 출력), `FileHandler` (파일 출력).

## 포맷터 (Formatter)
- 로그 메시지의 출력 형식을 지정합니다.
- 타임스탬프, 로그 레벨, 메시지 등을 포함할 수 있습니다.
- `logging.Formatter(fmt)`를 통해 생성합니다.

## 로그 레벨 (Log Level)
- 로그 메시지의 중요도를 나타냅니다.
- 기본 로그 레벨: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.
- 로거와 핸들러에 로그 레벨을 설정하여, 특정 중요도 이상의 메시지만 처리하도록 할 수 있습니다.


# 예제

## 2.handlers.py

### 설명

1. **기본 로그 레벨 설정**:
   - `logging.basicConfig(level=getattr(logging, log_level))`로 기본 로그 레벨을 설정합니다.

2. **현재 모듈의 로거 설정**:
   - `logger = logging.getLogger(__name__)`로 현재 모듈의 로거를 가져와서, `logger.setLevel(getattr(logging, log_level))`로 로그 레벨을 설정합니다.

3. **werkzeug의 로그 레벨 설정**:
   - `werkzeug_logger = logging.getLogger('werkzeug')`로 `werkzeug` 로거를 가져와서, `werkzeug_logger.setLevel(logging.DEBUG)`로 로그 레벨을 설정합니다.

4. **포맷터 설정**:
   - `formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')`로 로그 메시지 포맷을 설정합니다.
   - 모든 로그 메시지에 대해 타임스탬프, 로거 이름, 로그 레벨, 메시지를 포함합니다.

5. **콘솔 핸들러 설정**:
   - `console_handler = logging.StreamHandler()`로 콘솔 핸들러를 생성합니다.
   - `console_handler.setFormatter(formatter)`로 핸들러에 포맷터를 설정합니다.

6. **파일 핸들러 설정**:
   - `file_handler = logging.FileHandler('app.log')`로 파일 핸들러를 생성합니다.
   - `file_handler.setLevel(getattr(logging, log_level))`로 파일 핸들러의 로그 레벨을 설정합니다.
   - `file_handler.setFormatter(formatter)`로 핸들러에 포맷터를 설정합니다.

7. **werkzeug 로거에 파일 핸들러 추가**:
   - `werkzeug_logger.addHandler(file_handler)`로 `werkzeug` 로거에 파일 핸들러를 추가합니다.

8. **현재 모듈의 로거에 콘솔 핸들러 추가**:
   - `logger.addHandler(console_handler)`로 현재 모듈의 로거에 콘솔 핸들러를 추가합니다.

9. **app.logger의 기본 핸들러 제거 및 파일 핸들러 추가**:
   - `for handler in app.logger.handlers[:]`을 통해 `app.logger`의 모든 기존 핸들러를 제거합니다.
   - `app.logger.addHandler(file_handler)`로 `app.logger`에 파일 핸들러를 추가하여 로그 메시지를 파일로 기록합니다.

### 결과

이 설정을 통해 Flask 애플리케이션의 로그 메시지가 콘솔과 `app.log` 파일에 모두 기록됩니다. `app.log` 파일에는 다음과 같은 포맷으로 로그 메시지가 기록됩니다.


### 추가 팁

- **환경변수 사용**: 환경변수를 통해 로그 레벨을 동적으로 설정할 수 있습니다.
- **다양한 핸들러**: 필요에 따라 `SMTPHandler`, `HTTPHandler`, `SocketHandler` 등을 사용하여 로그 메시지를 다양한 대상에 보낼 수 있습니다.
- **로깅 설정 파일**: `logging.config.fileConfig()`를 사용하여 로깅 설정을 파일로 관리할 수 있습니다.
- **서식 문자열**: 포맷터의 서식 문자열을 사용하여 로그 메시지에 포함될 정보를 세밀하게 조정할 수 있습니다.


## 4.fileiolog.py

### 설명

1. **기본 로그 레벨 설정**:
   - `logging.basicConfig(level=getattr(logging, log_level))`로 기본 로그 레벨을 설정합니다.

2. **현재 모듈의 로그 레벨 설정**:
   - `logger = logging.getLogger(__name__)`로 현재 모듈의 로거를 가져와서, `logger.setLevel(getattr(logging, log_level))`로 로그 레벨을 설정합니다.

3. **werkzeug의 로그 레벨 설정**:
   - `werkzeug_logger = logging.getLogger('werkzeug')`로 `werkzeug` 로거를 가져와서, `werkzeug_logger.setLevel(logging.DEBUG)`로 로그 레벨을 설정합니다.

4. **포맷터 설정**:
   - `formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')`로 로그 메시지 포맷을 설정합니다.
   - 모든 로그 메시지에 대해 타임스탬프, 로거 이름, 로그 레벨, 메시지를 포함합니다.

5. **콘솔 핸들러 설정**:
   - `console_handler = logging.StreamHandler()`로 콘솔 핸들러를 생성합니다.
   - `console_handler.setFormatter(formatter)`로 핸들러에 포맷터를 설정합니다.

6. **파일 핸들러 설정**:
   - `file_handler = logging.FileHandler('app.log')`로 파일 핸들러를 생성합니다.
   - `file_handler.setLevel(getattr(logging, log_level))`로 파일 핸들러의 로그 레벨을 설정합니다.
   - `file_handler.setFormatter(formatter)`로 핸들러에 포맷터를 설정합니다.

7. **werkzeug 로거에 핸들러 추가**:
   - `werkzeug_logger.addHandler(console_handler)`로 `werkzeug` 로거에 콘솔 핸들러를 추가합니다.
   - `werkzeug_logger.addHandler(file_handler)`로 `werkzeug` 로거에 파일 핸들러를 추가합니다.

8. **현재 모듈의 로거에도 파일 핸들러 추가**:
   - `logger.addHandler(file_handler)`로 현재 모듈의 로거에도 파일 핸들러를 추가합니다.


### 결과

이 설정을 통해 Flask 애플리케이션의 로그 메시지가 콘솔과 `app.log` 파일에 모두 기록됩니다. `app.log` 파일에는 다음과 같은 포맷으로 로그 메시지가 기록됩니다.

