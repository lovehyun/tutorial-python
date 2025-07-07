# Flask 예제 애플리케이션

간단한 할 일 관리 시스템을 통해 Flask 웹 프레임워크의 기본 기능을 학습할 수 있는 예제 애플리케이션입니다.

## 주요 기능

- ✅ 할 일 추가, 수정, 삭제
- ✅ 할 일 완료 상태 관리
- ✅ RESTful API 제공
- ✅ 반응형 웹 디자인 (Bootstrap 5)
- ✅ 실시간 시간 표시

## 기술 스택

### 백엔드
- Python 3.x
- Flask 웹 프레임워크
- Jinja2 템플릿 엔진

### 프론트엔드
- HTML5
- CSS3
- JavaScript (ES6+)
- Bootstrap 5

## 설치 및 실행

### 1. 저장소 클론 또는 파일 다운로드

### 2. 가상환경 생성 (권장)
```bash
python -m venv venv
```

### 3. 가상환경 활성화
**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

### 5. 애플리케이션 실행
```bash
python app.py
```

### 6. 브라우저에서 접속
```
http://localhost:5000
```

## API 엔드포인트

| 메서드 | 엔드포인트 | 설명 |
|--------|------------|------|
| GET | `/api/todos` | 모든 할 일 목록 조회 |
| POST | `/api/todos` | 새로운 할 일 추가 |
| PUT | `/api/todos/<id>` | 특정 할 일 수정 |
| DELETE | `/api/todos/<id>` | 특정 할 일 삭제 |
| GET | `/api/time` | 현재 시간 조회 |

## API 사용 예제

### 할 일 목록 조회
```bash
curl -X GET http://localhost:5000/api/todos
```

### 새 할 일 추가
```bash
curl -X POST http://localhost:5000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"task": "새로운 할 일"}'
```

### 할 일 완료 상태 변경
```bash
curl -X PUT http://localhost:5000/api/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

### 할 일 삭제
```bash
curl -X DELETE http://localhost:5000/api/todos/1
```

## 프로젝트 구조

```
flask_example/
├── app.py                 # 메인 애플리케이션 파일
├── requirements.txt       # 필요한 패키지 목록
├── README.md             # 프로젝트 설명서
└── templates/            # HTML 템플릿 디렉토리
    ├── base.html         # 기본 레이아웃 템플릿
    ├── index.html        # 홈페이지 템플릿
    └── about.html        # 소개 페이지 템플릿
```

## 학습 포인트

이 예제를 통해 다음과 같은 Flask 개념들을 학습할 수 있습니다:

1. **라우팅**: URL과 함수를 연결하는 방법
2. **템플릿 렌더링**: Jinja2를 사용한 동적 HTML 생성
3. **RESTful API**: HTTP 메서드를 활용한 API 설계
4. **JSON 처리**: 요청과 응답에서 JSON 데이터 다루기
5. **정적 파일**: CSS, JavaScript 파일 서빙
6. **에러 처리**: 기본적인 에러 핸들링

## 확장 아이디어

이 기본 예제를 바탕으로 다음과 같은 기능들을 추가해볼 수 있습니다:

- 데이터베이스 연동 (SQLite, PostgreSQL 등)
- 사용자 인증 및 세션 관리
- 파일 업로드 기능
- 페이지네이션
- 검색 기능
- 실시간 업데이트 (WebSocket)

## 라이선스

이 프로젝트는 교육 목적으로 만들어졌으며 자유롭게 사용하실 수 있습니다.
