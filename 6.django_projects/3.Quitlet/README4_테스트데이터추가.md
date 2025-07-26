# 관리자 페이지 테스트 데이터 추가 가이드

## 1. 관리자 페이지 접속

```bash
# 개발 서버 실행
python manage.py runserver

# 브라우저에서 접속
http://127.0.0.1:8000/admin/
```

슈퍼유저 계정으로 로그인하세요.

## 2. 데이터 추가 순서

### 📁 1단계: 카테고리 추가
**Quiz → Categories → Add Category**

```
카테고리 1:
- Name: 영어
- Description: 영어 어휘 및 문법 문제

카테고리 2:
- Name: 수학
- Description: 기초 수학 및 계산 문제

카테고리 3:
- Name: 과학
- Description: 일반 과학 상식 문제

카테고리 4:
- Name: 역사
- Description: 한국사 및 세계사 문제
```

### 📚 2단계: 문제집 추가
**Quiz → Question sets → Add Question set**

```
문제집 1:
- Title: 기초 영어 단어
- Description: 중학교 수준의 기본 영어 단어 문제집
- Category: 영어
- Creator: (현재 로그인한 사용자)
- Is public: ✅ 체크

문제집 2:
- Title: 수학 기초 연산
- Description: 사칙연산과 기본 수학 개념
- Category: 수학
- Creator: (현재 로그인한 사용자)
- Is public: ✅ 체크

문제집 3:
- Title: 과학 상식
- Description: 일반적인 과학 지식과 상식
- Category: 과학
- Creator: (현재 로그인한 사용자)
- Is public: ✅ 체크
```

### ❓ 3단계: 문제 및 선택지 추가

#### 문제집 1: 기초 영어 단어

**문제 1**
- Question set: 기초 영어 단어
- Question text: "Apple"의 한국어 뜻은?
- Order: 1

선택지:
1. 사과 (정답: ✅)
2. 바나나
3. 오렌지  
4. 포도

**문제 2**
- Question set: 기초 영어 단어
- Question text: "Book"의 한국어 뜻은?
- Order: 2

선택지:
1. 연필
2. 책 (정답: ✅)
3. 가방
4. 책상

**문제 3**
- Question set: 기초 영어 단어
- Question text: "Water"의 한국어 뜻은?
- Order: 3

선택지:
1. 불
2. 물 (정답: ✅)
3. 공기
4. 땅

#### 문제집 2: 수학 기초 연산

**문제 1**
- Question set: 수학 기초 연산
- Question text: 5 + 3 = ?
- Order: 1

선택지:
1. 7
2. 8 (정답: ✅)
3. 9
4. 6

**문제 2**
- Question set: 수학 기초 연산
- Question text: 12 ÷ 3 = ?
- Order: 2

선택지:
1. 3
2. 4 (정답: ✅)
3. 5
4. 6

**문제 3**
- Question set: 수학 기초 연산
- Question text: 7 × 8 = ?
- Order: 3

선택지:
1. 54
2. 55
3. 56 (정답: ✅)
4. 57

#### 문제집 3: 과학 상식

**문제 1**
- Question set: 과학 상식
- Question text: 지구에서 가장 큰 포유동물은?
- Order: 1

선택지:
1. 코끼리
2. 기린
3. 흰긴수염고래 (정답: ✅)
4. 하마

**문제 2**
- Question set: 과학 상식
- Question text: 물의 화학 기호는?
- Order: 2

선택지:
1. CO2
2. H2O (정답: ✅)
3. NaCl
4. O2

## 3. 빠른 데이터 추가 팁

### 💡 문제 추가 시 주의사항
1. **Question set 선택** - 어떤 문제집에 속할지 먼저 선택
2. **Order 번호** - 문제 순서를 1, 2, 3... 순으로 설정
3. **선택지는 정확히 4개** - 그 중 하나만 정답으로 체크
4. **Choice order** - 선택지 순서도 1, 2, 3, 4로 설정

### 🔥 효율적인 입력 방법
1. **카테고리 먼저 모두 추가**
2. **문제집 먼저 모두 추가**  
3. **문제는 하나씩 추가하면서 바로 선택지도 함께 입력**

## 4. 확인해볼 페이지들

데이터 추가 후 다음 URL들을 확인해보세요:

```
홈페이지: http://127.0.0.1:8000/
문제집 목록: http://127.0.0.1:8000/sets/
특정 문제집: http://127.0.0.1:8000/sets/1/
퀴즈 시작: http://127.0.0.1:8000/sets/1/quiz/start/
```

## 5. 추가 테스트 데이터 (선택사항)

더 많은 데이터가 필요하다면:

- 각 문제집당 5-10문제 추가
- 역사 카테고리용 문제집도 생성
- 다양한 난이도의 문제 추가
- 설명(explanation) 필드도 활용

## 6. 문제 발생 시 체크리스트

- [ ] 슈퍼유저 계정으로 로그인했는가?
- [ ] accounts, quiz 앱이 INSTALLED_APPS에 있는가?
- [ ] 마이그레이션이 모두 적용되었는가?
- [ ] 선택지는 정확히 4개이고 하나만 정답인가?
- [ ] Order 번호가 중복되지 않았는가?


## 7. 데이터베이스 백업 TODO

# Django 데이터베이스 백업 가이드

## 백업이 필요한 이유

- **실수 방지**: 코드 수정하다가 실수로 데이터 날릴 수 있음
- **테스트 데이터 보존**: 다시 처음부터 입력하는 번거로움 방지
- **버전 관리**: 좋은 상태의 데이터를 보관
- **안전한 개발**: 언제든 이전 상태로 복원 가능

## 백업 방법

### 방법 1: 파일 복사 (가장 간단)

```bash
# 현재 디렉토리에서 파일 복사
copy db.sqlite3 db_backup_20250726.sqlite3

# 백업 폴더 만들어서 관리
mkdir backup
copy db.sqlite3 backup\db_backup_20250726.sqlite3

# 날짜별 백업 (권장)
copy db.sqlite3 backup\db_working_$(date +%Y%m%d).sqlite3
```

### 방법 2: Django 명령어 사용 (더 안전)

```bash
# 전체 데이터를 JSON 형태로 백업
python manage.py dumpdata > backup_data.json

# 특정 앱만 백업
python manage.py dumpdata quiz > quiz_backup.json
python manage.py dumpdata accounts > accounts_backup.json

# 날짜가 포함된 백업 파일명
python manage.py dumpdata > backup\full_backup_20250726.json

# 예쁘게 포맷된 JSON (용량 더 큼)
python manage.py dumpdata --indent 2 > backup_formatted.json
```

## 권장 백업 루틴

### 지금 당장 실행할 명령어

```bash
# 1. 백업 폴더 생성
mkdir backup

# 2. 파일 백업 (빠르고 간단)
copy db.sqlite3 backup\db_working_20250726.sqlite3

# 3. JSON 백업 (안전하고 이식성 좋음)
python manage.py dumpdata > backup\full_backup_20250726.json

# 4. 특정 앱별 백업 (선택사항)
python manage.py dumpdata quiz > backup\quiz_20250726.json
python manage.py dumpdata accounts > backup\accounts_20250726.json
```

### 정기적 백업 명령어

```bash
# 중요한 작업 전 백업
copy db.sqlite3 backup\db_before_feature_$(date +%Y%m%d_%H%M).sqlite3

# 일일 백업
python manage.py dumpdata > backup\daily_backup_$(date +%Y%m%d).json

# 주요 마일스톤 백업
python manage.py dumpdata > backup\milestone_v1_complete.json
```

## 복원 방법

### 파일 복사 백업 복원

```bash
# 기존 데이터베이스 백업 (안전장치)
copy db.sqlite3 db_current_backup.sqlite3

# 백업 파일로 복원
copy backup\db_backup_20250726.sqlite3 db.sqlite3

# 서버 재시작
python manage.py runserver
```

### JSON 백업 복원

```bash
# 1. 기존 데이터베이스 초기화
del db.sqlite3

# 2. 새 데이터베이스 생성 및 마이그레이션
python manage.py migrate

# 3. 백업 데이터 로드
python manage.py loaddata backup\full_backup_20250726.json

# 4. 슈퍼유저 계정 확인 (필요시 재생성)
python manage.py createsuperuser
```

## 백업 파일 관리

### 추천 폴더 구조

```
프로젝트/
├── backup/
│   ├── daily/
│   │   ├── db_20250726.sqlite3
│   │   └── full_20250726.json
│   ├── milestones/
│   │   ├── v1_auth_complete.json
│   │   ├── v2_quiz_complete.json
│   │   └── v3_final.json
│   └── emergency/
│       └── before_major_change.sqlite3
├── db.sqlite3
└── manage.py
```

### 백업 파일 명명 규칙

```bash
# 날짜 기반
db_20250726.sqlite3
full_backup_20250726_1430.json

# 기능 기반
db_after_auth_setup.sqlite3
quiz_models_complete.json

# 버전 기반
v1_0_complete.json
milestone_beta.sqlite3
```

## 주의사항

### ✅ 좋은 백업 습관

- **중요한 작업 전 반드시 백업**
- **정기적으로 백업 (일일/주간)**
- **백업 파일에 명확한 날짜/설명 포함**
- **여러 백업 방법 병행 사용**
- **백업 파일의 복원 테스트**

### ❌ 피해야 할 실수

- **백업 없이 큰 변경사항 적용**
- **백업 파일 덮어쓰기**
- **단일 백업 방법에만 의존**
- **오래된 백업 파일 방치**

## 자동화 스크립트 (선택사항)

### Windows 배치 파일 (backup.bat)

```batch
@echo off
set TIMESTAMP=%date:~10,4%%date:~4,2%%date:~7,2%_%time:~0,2%%time:~3,2%
set TIMESTAMP=%TIMESTAMP: =0%

echo Creating backup...
copy db.sqlite3 backup\db_%TIMESTAMP%.sqlite3
python manage.py dumpdata > backup\full_%TIMESTAMP%.json
echo Backup completed: %TIMESTAMP%
```

### 사용법

```bash
# 실행 권한 부여 후
backup.bat
```

## 복원 테스트

### 백업이 제대로 되었는지 확인

```bash
# 1. 현재 DB 임시 이동
move db.sqlite3 db_temp.sqlite3

# 2. 백업으로 복원 테스트
copy backup\db_backup_20250726.sqlite3 db.sqlite3

# 3. 서버 실행해서 데이터 확인
python manage.py runserver

# 4. 확인 후 원본 복구
del db.sqlite3
move db_temp.sqlite3 db.sqlite3
```

## 언제 백업해야 하나?

### 🔥 필수 백업 타이밍

- **새로운 기능 개발 시작 전**
- **데이터베이스 구조 변경 전**
- **대량의 테스트 데이터 추가 후**
- **배포 전**
- **큰 코드 리팩토링 전**

### 📅 정기 백업 일정

- **매일**: 개발 작업 후
- **주간**: 주요 기능 완성 후  
- **마일스톤**: 프로젝트 단계별 완료 후

---

> **💡 팁**: 지금이 백업하기 좋은 타이밍입니다!
> - 기본 데이터 구조 완성
> - 테스트 데이터 추가 완료  
> - 다음 단계(퀴즈 응시 페이지)로 넘어가기 전
