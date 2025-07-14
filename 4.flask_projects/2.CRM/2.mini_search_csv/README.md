# 6.app6_flaskrestx

## 개요
- Flask 애플리케이션에서 Swagger 문서화를 하기 위해 가장 많이 사용되는 라이브러리는 Flask-RESTPlus(이제 Flask-RESTX로 유지 관리됨)입니다.
- Flask-RESTX는 Swagger UI를 통해 API 문서를 자동으로 생성하고 쉽게 관리할 수 있도록 도와줍니다.

## 동작방식
- 위의 요청 방식은 AJAX 요청을 통해 RESTful API와 상호 작용하는 방식입니다.
- RESTful API는 특정 규칙을 따르는 API로, 리소스(URL로 식별되는 데이터)와 상호 작용하기 위해 HTTP 메서드(GET, POST, PUT, DELETE 등)를 사용하는 것을 의미합니다.

### 요약
1. **RESTful API**:
   - 리소스를 URL로 식별합니다.
   - HTTP 메서드를 사용하여 리소스와 상호 작용합니다.
   - JSON 형식의 데이터를 주고받는 것이 일반적입니다.

2. **AJAX**:
   - 비동기적으로 서버와 통신하기 위해 사용됩니다.
   - JavaScript를 사용하여 서버로 요청을 보내고 응답을 처리합니다.

### 예시
위의 HTML/JavaScript 코드는 RESTful API 엔드포인트(/api/users)로 AJAX 요청을 보내고, 응답 데이터를 사용하여 테이블과 페이지네이션을 렌더링합니다. 이것이 RESTful API와 AJAX의 사용 방식입니다.

1. **예시 RESTful API 엔드포인트**:
   - `GET /api/users`: 사용자 목록을 가져오는 엔드포인트입니다.
   - `GET /api/users/<id>`: 특정 사용자의 정보를 가져오는 엔드포인트입니다.

2. **AJAX 요청**:
   - `fetch(/api/users?page=${page}&name=${searchName}&items_per_page=${itemsPerPage})`: JavaScript `fetch` API를 사용하여 `GET` 요청을 보냅니다.
