# 미션. 고객관리시스템 개발
 - 과제1. DB로부터 사용자 정보 로딩 (페이징 처리)
 - 과제2. 검색 기능 추가 (사용자 성, 이름별 검색)
 - 과제3. 사용자 상세 정보 출력 (주문 상품/일자/장소)
 - 과제4. 매장 정보 로딩 (매장별 월간 매출액, 단골 고객 Top10 정보 등)


# DB 내용 확인

SQLite에서 지원하는 데이터 타입은 다른 관계형 데이터베이스 시스템(RDBMS)과 다소 다를 수 있습니다. SQLite는 동적 타입 시스템을 사용하여 컬럼에 저장되는 실제 데이터 타입에 대해서는 큰 제약이 없습니다. 그러나 SQLite는 다섯 가지의 저장 클래스(storage class)를 사용합니다:

1. NULL - NULL 값.
2. INTEGER - 부호 있는 정수.
3. REAL - 부동 소수점 숫자.
4. TEXT - 텍스트 문자열.
5. BLOB - 정확히 입력된 그대로 저장된 데이터(바이너리).

따라서 SQLite에 적합한 타입으로 다시 설정한 스키마는 다음과 같습니다:

```
sqlite3 user-sample.sqlite

sqlite> .schema
CREATE TABLE IF NOT EXISTS "users"(
  "Id" TEXT PRIMARY KEY, 
  "Name" TEXT, 
  "Gender" TEXT, 
  "Age" INTEGER,
  "Birthdate" TEXT, 
  "Address" TEXT
);

CREATE TABLE IF NOT EXISTS "stores"(
  "Id" TEXT PRIMARY KEY, 
  "Name" TEXT, 
  "Type" TEXT, 
  "Address" TEXT
);

CREATE TABLE IF NOT EXISTS "items"(
  "Id" TEXT PRIMARY KEY, 
  "Name" TEXT, 
  "Type" TEXT, 
  "UnitPrice" REAL
);

CREATE TABLE IF NOT EXISTS "orders"(
  "Id" TEXT PRIMARY KEY, 
  "OrderAt" TEXT, 
  "StoreId" TEXT, 
  "UserId" TEXT,
  FOREIGN KEY ("StoreId") REFERENCES "stores" ("Id"),
  FOREIGN KEY ("UserId") REFERENCES "users" ("Id")
);

CREATE TABLE IF NOT EXISTS "order_items"(
  "Id" TEXT PRIMARY KEY, 
  "OrderId" TEXT, 
  "ItemId" TEXT,
  FOREIGN KEY ("OrderId") REFERENCES "orders" ("Id"),
  FOREIGN KEY ("ItemId") REFERENCES "items" ("Id")
);

```

# 변경된 컬럼 타입 설명
- users 테이블
  - Id: TEXT (PRIMARY KEY)
  - Name: TEXT
  - Gender: TEXT
  - Age: INTEGER
  - Birthdate: TEXT (DATE 형식의 텍스트)
  - Address: TEXT
  
- stores 테이블
  - Id: TEXT (PRIMARY KEY)
  - Name: TEXT
  - Type: TEXT
  - Address: TEXT

- items 테이블
  - Id: TEXT (PRIMARY KEY)
  - Name: TEXT
  - Type: TEXT
  - UnitPrice: REAL

- orders 테이블
  - Id: TEXT (PRIMARY KEY)
  - OrderAt: TEXT (TIMESTAMP 형식의 텍스트)
  - StoreId: TEXT (FOREIGN KEY)
  - UserId: TEXT (FOREIGN KEY)

- order_items 테이블
  - Id: TEXT (PRIMARY KEY)
  - OrderId: TEXT (FOREIGN KEY)
  - ItemId: TEXT (FOREIGN KEY)

이 스키마는 SQLite의 타입 시스템에 맞추어 적절한 데이터 유형을 사용하여 정의되었습니다. Birthdate와 OrderAt 필드는 날짜와 시간을 나타내는 텍스트 형식으로 저장됩니다. SQLite는 이러한 텍스트 필드에 대해 비교 및 정렬 작업을 수행할 수 있습니다.
