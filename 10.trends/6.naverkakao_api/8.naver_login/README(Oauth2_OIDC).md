
# 네이버 로그인 인증 절차 (OAuth2 + OpenID Connect)

본 문서는 네이버 로그인을 내 웹사이트에 연동할 때의 전체 인증 흐름을 **OAuth2 + OpenID Connect** 기준으로 상세히 설명합니다.  
사용자, 내 사이트(클라이언트), 네이버(인증 서버) 간의 상호작용을 단계별로 다룹니다.

---

## 전체 절차 요약

1. 사용자 → 내 사이트 접속
2. 내 사이트 → 사용자 브라우저를 통해 네이버 로그인 페이지로 리디렉션
3. 사용자 → 네이버 로그인
4. 네이버 → 사용자에게 개인정보 제공 동의 요청
5. 네이버 → **사용자 브라우저**에 Authorization Code 포함 리디렉션
6. 사용자 브라우저 → 내 사이트 콜백 URL 접속 (code 전달됨)
7. 내 사이트 → 네이버에 토큰 요청
8. 네이버 → Access Token 응답
9. 내 사이트 → 네이버에 사용자 정보 요청
10. 네이버 → 사용자 정보 응답
11. 내 사이트 → 로그인 처리 완료

---

## 시퀀스 흐름

\`\`\`plaintext
[사용자] → [내 사이트] : 로그인 페이지 접속  
[내 사이트] → [사용자 브라우저] : 네이버 인증 URL로 리디렉션  
[사용자 브라우저] → [네이버] : 로그인 요청  
[네이버] → [사용자 브라우저] : 동의 화면 표시  
[네이버] → [사용자 브라우저] : Authorization Code 전달 (Redirect)  
[사용자 브라우저] → [내 사이트 콜백 URL] : ?code=...&state=...  
[내 사이트] → [네이버] : 토큰 요청  
[네이버] → [내 사이트] : Access Token 응답  
[내 사이트] → [네이버] : 사용자 정보 요청  
[네이버] → [내 사이트] : 사용자 정보 응답  
[내 사이트] → [사용자] : 로그인 완료  
\`\`\`

---

## 주요 API 호출 요약

### 1. 네이버 인증 요청 (Authorization Request)

\`\`\`
GET https://nid.naver.com/oauth2.0/authorize?
    response_type=code
    &client_id=YOUR_CLIENT_ID
    &redirect_uri=YOUR_CALLBACK_URI
    &state=RANDOM_STRING
\`\`\`

| 파라미터       | 설명                                      |
|----------------|-------------------------------------------|
| response_type  | \`code\` 고정 (Authorization Code 방식)     |
| client_id      | 네이버 앱 등록 시 발급된 클라이언트 ID    |
| redirect_uri   | 인증 후 리디렉션할 내 사이트의 URL        |
| state          | CSRF 방지용 난수 문자열 (검증용)          |

---

### 2. 토큰 요청 (Token Request)

\`\`\`
POST https://nid.naver.com/oauth2.0/token?
    grant_type=authorization_code
    &client_id=YOUR_CLIENT_ID
    &client_secret=YOUR_CLIENT_SECRET
    &code=AUTH_CODE
    &state=RANDOM_STRING
\`\`\`

| 파라미터        | 설명                                      |
|------------------|-------------------------------------------|
| grant_type       | \`authorization_code\` 고정                 |
| client_id        | 클라이언트 ID                             |
| client_secret    | 클라이언트 시크릿                         |
| code             | 콜백 URI로 전달받은 Authorization Code    |
| state            | 최초 요청 시 전달한 값과 동일해야 함     |

---

### 3. 사용자 정보 요청

\`\`\`
GET https://openapi.naver.com/v1/nid/me  
Authorization: Bearer ACCESS_TOKEN
\`\`\`

응답 예:

\`\`\`json
{
  "resultcode": "00",
  "message": "success",
  "response": {
    "id": "abc1234",
    "name": "홍길동",
    "email": "abc@naver.com",
    "profile_image": "https://..."
  }
}
\`\`\`

---

## 참고

- \`redirect_uri\`는 반드시 네이버에 등록된 값과 일치해야 합니다.
- \`state\` 값은 CSRF 보호를 위한 필수 값입니다.
- \`access_token\`은 사용자 정보 요청 시 인증 토큰으로 사용됩니다.

---

## 요약 순서 (한눈에 보기)

| 순번 | 동작 주체         | 설명 |
|------|------------------|------|
| 1    | 사용자            | 내 사이트 접속 |
| 2    | 내 사이트         | 네이버 로그인 URL로 리디렉션 |
| 3    | 사용자            | 네이버 로그인 |
| 4    | 네이버            | 사용자에게 동의 요청 |
| 5    | 네이버            | 사용자 브라우저에 인증 코드 포함 redirect |
| 6    | 사용자 브라우저   | 콜백 URI 접속 (code 포함) |
| 7    | 내 사이트         | 토큰 요청 |
| 8    | 네이버            | 토큰 응답 (access_token 등) |
| 9    | 내 사이트         | 사용자 정보 요청 |
| 10   | 네이버            | 사용자 정보 응답 |
| 11   | 내 사이트         | 로그인 완료 처리 |


---

# OAuth2, OpenID, OpenID Connect 개념 정리

본 문서는 OAuth2, OpenID, OpenID Connect의 개념과 차이를 설명합니다.

---

## 1. OAuth 2.0이란?

OAuth 2.0은 "권한 위임(Authorization Delegation)"을 위한 프로토콜입니다.

### 목적
- 사용자가 직접 비밀번호를 주지 않고 제3자 애플리케이션에게 **자신의 리소스에 접근할 권한을 위임**할 수 있도록 함
- 인증(Authentication)이 아닌 인가(Authorization)에 초점을 둠

### 예시
- A 서비스가 사용자의 구글 드라이브 파일을 읽기 위해 요청
- 사용자는 구글 로그인 후 "허용"을 클릭
- 구글은 A 서비스에 Access Token을 발급
- A 서비스는 해당 토큰으로 사용자의 구글 드라이브 파일에 접근 가능

---

## 2. OpenID란?

OpenID는 하나의 계정으로 여러 사이트에 로그인할 수 있도록 만든 **사용자 인증(Authentication) 시스템**입니다.

- OAuth 등장 이전에 만들어졌으며, URI 기반으로 사용자 식별
- 현재는 거의 사용되지 않으며, OpenID Connect로 대체됨

---

## 3. OpenID Connect (OIDC)란?

OpenID Connect는 OAuth2 위에 **사용자 인증 기능을 추가한 확장 프로토콜**입니다.

### 특징
- OAuth2 기반으로 작동
- 인증이 완료되면 `ID Token`을 발급 (JWT 형식)
- 사용자 이름, 이메일, 프로필 사진 등 다양한 정보를 제공 가능
- 현재 대부분의 소셜 로그인(Google, Naver, Kakao 등)에 사용됨

---

## 4. 세 가지의 관계 요약

| 항목             | OAuth 2.0                      | OpenID              | OpenID Connect                |
|------------------|--------------------------------|----------------------|-------------------------------|
| 목적             | 권한 위임                      | 사용자 인증          | 사용자 인증 + 권한 위임       |
| 인증 기능        | 없음                           | 있음                 | 있음                          |
| 인가 기능        | 있음                           | 없음                 | 있음                          |
| 주요 토큰        | Access Token                   | 없음                 | Access Token + ID Token       |
| 사용 사례        | API 접근 권한 부여             | 초기 싱글사인온       | 네이버/구글/카카오 로그인     |

---

## 5. 비유로 이해하기

| 항목        | 설명                                                              |
|-------------|-------------------------------------------------------------------|
| OAuth2      | "열쇠 위임하기" - 친구에게 내 집의 특정 방만 열 수 있는 열쇠를 줌 |
| OpenID      | "신분증" - 내가 누구인지 증명                                      |
| OIDC        | "신분증 + 열쇠" - 로그인도 하고, 일부 권한도 위임 받음             |

---

## 6. 실제 사례: 네이버 로그인

- 인증: OpenID Connect (`openid` scope 요청 시 `id_token` 포함)
- 인가: OAuth2 (`access_token`을 통해 사용자 정보에 접근)

따라서 네이버 로그인은 OpenID Connect 프로토콜을 사용한 구현 사례입니다.

---

