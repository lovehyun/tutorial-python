# Google API Key 발급 가이드

## 1. Google Cloud API Key 공식 문서

공식 문서:
https://docs.cloud.google.com/docs/authentication/api-keys

이 문서에서는 다음 절차를 안내합니다.

1. Google Cloud Console 접속
2. 프로젝트 생성
3. API 활성화
4. Credentials(사용자 인증 정보) 이동
5. API Key 생성

---

## 2. Google Cloud Console

공식 사이트:
https://console.cloud.google.com/

일반적인 생성 경로:

```text
API 및 서비스
→ 사용자 인증 정보(Credentials)
→ 사용자 인증 정보 만들기(Create Credentials)
→ API Key
```

---

## 3. Google Maps Platform 시작 페이지

공식 문서:
https://developers.google.com/maps/get-started

여기서는 다음 내용을 함께 안내합니다.

- Billing 연결
- Maps API 활성화
- API Key 생성
- API Key 제한(Restriction)

---

## 4. API Key 보안 설정(중요)

실무에서는 API Key 생성 직후 반드시 제한을 설정합니다.

대표적인 제한 방식:

- HTTP referrer 제한
- IP 주소 제한
- 특정 API만 허용

예시:

```text
이 키는 Maps JavaScript API만 허용
```

---

## 5. 서비스별 일반적인 발급 위치

### Gemini API
https://aistudio.google.com/

### Google Maps API
https://console.cloud.google.com/

### YouTube Data API
https://console.cloud.google.com/

### Gmail API
https://console.cloud.google.com/

---

## 6. 참고 공식 문서 링크

- Google Cloud API Keys
  https://docs.cloud.google.com/docs/authentication/api-keys

- Google Maps Platform Getting Started
  https://developers.google.com/maps/get-started

- Google Cloud Console
  https://console.cloud.google.com/
