# 웹 애플리케이션 보안 취약점

## 1. SQL 인젝션 (SQL Injection)
- **설명**: 사용자가 입력한 데이터가 SQL 쿼리에 직접 포함되어, 공격자가 쿼리를 조작하여 데이터베이스를 부당하게 읽거나 수정할 수 있는 취약점입니다.
- **예시**: 로그인 폼에서 `username`에 `' OR '1'='1`과 같은 입력값을 주면 비밀번호 없이 인증이 우회됩니다.
- **해결 방법**: Prepared Statements 및 ORM을 사용하여 사용자 입력이 쿼리로 직접 전달되지 않도록 합니다.

---

## 2. XSS (Cross-Site Scripting)
- **설명**: 사용자가 입력한 데이터가 HTML로 렌더링되어 악성 스크립트가 실행될 수 있는 취약점입니다.
- **예시**: 게시판이나 댓글란에 `<script>alert('XSS')</script>`를 삽입하여 다른 사용자가 페이지를 방문할 때 악성 스크립트가 실행됩니다.
- **해결 방법**: 모든 사용자 입력을 HTML로 출력하기 전에 이스케이프 처리하거나, HTML을 필터링하여 스크립트가 실행되지 않도록 합니다.

---

## 3. CSRF (Cross-Site Request Forgery)
- **설명**: 사용자가 의도하지 않은 요청을 악성 사이트에서 보내게 하여, 사용자의 인증된 세션을 악용하는 공격입니다.
- **예시**: 사용자가 로그인된 상태에서 공격자가 만든 사이트를 방문하면 사용자의 의지와 상관없이 특정 요청(예: 비밀번호 변경)이 서버로 전송됩니다.
- **해결 방법**: CSRF 토큰을 사용하여 사용자가 직접 보낸 요청만 유효하도록 합니다.

---

## 4. IDOR (Insecure Direct Object References)
- **설명**: 인증된 사용자가 URL 파라미터나 요청 경로를 통해 다른 사용자의 데이터에 직접 접근할 수 있는 취약점입니다.
- **예시**: `/user_profile?user_id=1`처럼 URL에 파라미터로 사용자 ID를 전달하면, ID 값을 변경하여 다른 사용자의 정보를 조회할 수 있습니다.
- **해결 방법**: 모든 민감한 데이터 접근에 대한 권한 검증을 추가합니다.

---

## 5. 파일 업로드 취약점 (File Upload Vulnerabilities)
- **설명**: 파일 업로드 기능에서 파일의 내용이나 확장자를 검증하지 않아 악성 파일을 서버에 업로드하여 실행할 수 있는 취약점입니다.
- **예시**: `.php`, `.exe` 등 실행 가능한 파일이 업로드되도록 허용해 서버에서 악성 코드를 실행할 수 있습니다.
- **해결 방법**: 업로드된 파일의 확장자를 제한하고, 업로드된 파일을 서버에서 실행 불가능한 위치에 저장해야 합니다.

---

## 6. 약한 비밀번호 정책 (Weak Password Policy)
- **설명**: 비밀번호 정책이 약하게 설정되어 짧거나 예측 가능한 비밀번호를 허용할 경우, 공격자가 쉽게 비밀번호를 추측할 수 있습니다.
- **예시**: 사용자에게 `1234`와 같은 짧은 비밀번호를 허용하여, brute-force 공격에 쉽게 노출됩니다.
- **해결 방법**: 비밀번호 정책을 강화하여 최소 길이, 대소문자, 숫자, 특수문자를 포함하도록 설정합니다.

---

## 7. 검증되지 않은 리디렉션 및 포워드 (Unvalidated Redirects and Forwards)
- **설명**: 사용자가 URL 파라미터에 따라 외부 사이트로 리디렉션될 수 있는 경우, 공격자는 사용자를 피싱 페이지로 유도할 수 있습니다.
- **예시**: 로그인 후 `next` 파라미터에 따른 리디렉션을 허용할 때 `http://malicious-site.com`으로 유도할 수 있습니다.
- **해결 방법**: 리디렉션 시 허용된 URL만 리디렉션할 수 있도록 검증합니다.

---

## 8. 민감한 데이터 노출 (Sensitive Data Exposure)
- **설명**: 암호화되지 않은 민감한 데이터가 전송되거나 저장되어 공격자가 이를 탈취할 수 있는 취약점입니다.
- **예시**: 비밀번호를 평문으로 저장하거나, HTTP로 전송하여 데이터가 암호화되지 않은 상태로 노출됩니다.
- **해결 방법**: HTTPS를 사용해 데이터 전송을 암호화하고, 비밀번호는 해시화하여 저장합니다.

---

## 9. 보안 설정 오류 (Security Misconfiguration)
- **설명**: 서버 설정을 안전하게 구성하지 않거나 기본 설정으로 운영하여, 불필요한 기능이 활성화되어 있는 경우 발생하는 취약점입니다.
- **예시**: 디버그 모드를 활성화한 상태로 운영하거나, 불필요한 엔드포인트가 공개된 경우입니다.
- **해결 방법**: 서버 설정을 주기적으로 점검하여 불필요한 기능이나 디버그 모드를 비활성화합니다.

---

## 10. 인증 및 세션 관리 오류 (Broken Authentication and Session Management)
- **설명**: 세션 토큰이 안전하게 저장되지 않거나, 세션 타임아웃이 설정되지 않아 공격자가 세션을 탈취하여 불법적으로 접근할 수 있는 취약점입니다.
- **예시**: 세션 토큰이 암호화되지 않고 브라우저에 저장되거나, 세션 만료 시간이 설정되지 않아 공격자가 세션 탈취 후 계속 액세스할 수 있습니다.
- **해결 방법**: 세션에 만료 시간을 설정하고, 세션 토큰을 암호화하여 안전하게 저장합니다.

---

이러한 취약점들은 웹 애플리케이션에서 빈번히 발생할 수 있는 보안 문제들로, 각 항목에 대한 사전 예방 및 점검을 통해 보안을 강화하는 것이 중요합니다.
