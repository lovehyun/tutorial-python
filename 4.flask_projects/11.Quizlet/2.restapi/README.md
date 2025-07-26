# Flask 퀴즈 REST API 실행 및 사용 가이드

## 실행 방법

### 1. 패키지 설치
```bash
pip install Flask Flask-CORS openpyxl
```

### 2. 앱 실행
```bash
python app.py
```

### 3. 브라우저에서 접속
```
http://localhost:5000
```

## API 엔드포인트 정리

| 메소드 | URL | 설명 | 요청 형태 | 응답 형태 |
|--------|-----|------|-----------|-----------|
| GET | `/` | 메인 HTML 페이지 | - | HTML 파일 |
| GET | `/static/<filename>` | 정적 파일 (CSS, JS) | - | 정적 파일 |
| GET | `/api/download-template` | Excel 템플릿 다운로드 | - | Excel 파일 |
| POST | `/api/upload` | Excel 파일 업로드 | FormData | JSON |
| GET | `/api/questions` | 문제 목록 (공부 모드, 정답 포함) | - | JSON |
| GET | `/api/quiz` | 퀴즈 문제 (시험 모드, 정답 제외) | - | JSON |
| POST | `/api/submit-quiz` | 퀴즈 제출 및 채점 | JSON | JSON |
| GET | `/api/status` | 현재 상태 확인 | - | JSON |

## API 상세 설명

### 1. 파일 업로드 API
**POST** `/api/upload`

**요청:**
```javascript
const formData = new FormData();
formData.append('file', file);

fetch('/api/upload', {
    method: 'POST',
    body: formData
});
```

**응답 (성공):**
```json
{
    "success": true,
    "message": "파일이 성공적으로 업로드되었습니다! (3문제)",
    "question_count": 3
}
```

**응답 (실패):**
```json
{
    "error": "Excel 파일만 업로드 가능합니다."
}
```

### 2. 문제 목록 조회 API (공부 모드)
**GET** `/api/questions`

**응답:**
```json
{
    "questions": [
        {
            "id": 1,
            "question": "Python에서 리스트를 정의하는 기호는?",
            "choice1": "()",
            "choice2": "[]",
            "choice3": "{}",
            "choice4": "\"\"",
            "answer": 2,
            "explanation": "대괄호 []를 사용합니다."
        }
    ]
}
```

### 3. 퀴즈 문제 조회 API (시험 모드)
**GET** `/api/quiz`

**응답:**
```json
{
    "questions": [
        {
            "id": 1,
            "question": "Python에서 리스트를 정의하는 기호는?",
            "choice1": "()",
            "choice2": "[]",
            "choice3": "{}",
            "choice4": "\"\""
        }
    ]
}
```
*주의: 정답(answer)과 해설(explanation) 제외*

### 4. 퀴즈 제출 API
**POST** `/api/submit-quiz`

**요청:**
```json
{
    "answers": {
        "1": 2,
        "2": 1,
        "3": 4
    }
}
```

**응답:**
```json
{
    "results": [
        {
            "question": {
                "id": 1,
                "question": "Python에서 리스트를 정의하는 기호는?",
                "choice1": "()",
                "choice2": "[]",
                "choice3": "{}",
                "choice4": "\"\"",
                "answer": 2,
                "explanation": "대괄호 []를 사용합니다."
            },
            "user_answer": 2,
            "is_correct": true
        }
    ],
    "correct_count": 2,
    "total_questions": 3,
    "score_percentage": 66.7
}
```

### 5. 상태 확인 API
**GET** `/api/status`

**응답:**
```json
{
    "has_questions": true,
    "question_count": 3,
    "filename": "my_quiz.xlsx"
}
```

## 주요 변경사항

### 템플릿 엔진에서 REST API로
- **이전**: Flask 템플릿 엔진 (Jinja2) 사용
- **현재**: REST API + JavaScript fetch 사용

### 페이지 구조 변화
- **이전**: 여러 HTML 페이지 (index.html, study.html, quiz.html, result.html)
- **현재**: 단일 페이지 애플리케이션 (SPA)

### 데이터 흐름
```
브라우저 → JavaScript fetch → Flask API → JSON 응답 → JavaScript DOM 조작
```

## 프론트엔드 주요 기능

### 1. 파일 업로드
```javascript
async uploadFile() {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData
    });
    
    const data = await response.json();
    // 결과 처리
}
```

### 2. 공부 모드 렌더링
```javascript
async loadStudyMode() {
    const response = await fetch('/api/questions');
    const data = await response.json();
    
    this.questions = data.questions;
    this.renderStudyMode(); // DOM 조작으로 화면 생성
}
```

### 3. 시험 제출
```javascript
async submitQuiz() {
    const response = await fetch('/api/submit-quiz', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ answers: this.userAnswers })
    });
    
    const data = await response.json();
    this.renderResult(data); // 결과 화면 생성
}
```

## 세션 관리

### 서버사이드 세션
```python
# 문제 저장
session['questions'] = questions
session['filename'] = filename

# 문제 조회
questions = session.get('questions')
```

### 클라이언트사이드 상태 관리
```javascript
class QuizApp {
    constructor() {
        this.questions = [];      // 현재 문제들
        this.userAnswers = {};    // 사용자 답안
    }
}
```

## 에러 처리

### 서버사이드
```python
try:
    # 작업 수행
    return jsonify({'success': True})
except Exception as e:
    return jsonify({'error': str(e)}), 500
```

### 클라이언트사이드
```javascript
try {
    const response = await fetch('/api/endpoint');
    if (!response.ok) {
        const error = await response.json();
        this.showAlert(error.error, 'danger');
    }
} catch (error) {
    this.showAlert('네트워크 오류가 발생했습니다.', 'danger');
}
```

## Excel 파일 형식

### 필수 컬럼 순서
1. **문제** - 질문 내용
2. **선택지1** - 첫 번째 선택지
3. **선택지2** - 두 번째 선택지
4. **선택지3** - 세 번째 선택지
5. **선택지4** - 네 번째 선택지
6. **정답** - 1, 2, 3, 4 중 하나의 숫자
7. **해설** - 정답 설명 (선택사항)

### 예시 데이터
| 문제 | 선택지1 | 선택지2 | 선택지3 | 선택지4 | 정답 | 해설 |
|------|---------|---------|---------|---------|------|------|
| Python에서 리스트를 정의하는 기호는? | () | [] | {} | "" | 2 | 대괄호 []를 사용합니다. |

## 브라우저 호환성

### 필요한 기능들
- **Fetch API** (모던 브라우저)
- **ES6 Classes** (IE 미지원)
- **Async/Await** (IE 미지원)

### 지원 브라우저
- Chrome 55+
- Firefox 52+
- Safari 10.1+
- Edge 79+

### IE 지원이 필요한 경우
Babel 트랜스파일링과 Fetch polyfill 필요

## 개발 팁

### 1. CORS 설정
```python
from flask_cors import CORS
CORS(app)  # 모든 도메인에서 접근 허용
```

### 2. 디버깅
```javascript
// 브라우저 개발자 도구에서 API 테스트
fetch('/api/status').then(r => r.json()).then(console.log);
```

### 3. 파일 업로드 제한
```python
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
```

## 확장 가능성

### 1. 데이터베이스 연동
세션 대신 SQLite, PostgreSQL 등 데이터베이스 사용

### 2. 사용자 인증
JWT 토큰 기반 인증 시스템 추가

### 3. 실시간 기능
WebSocket을 이용한 실시간 퀴즈 기능

### 4. 모바일 앱
React Native, Flutter 등으로 모바일 앱 개발
