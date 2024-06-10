# 미션. 고객관리시스템 개발
 - 과제1. DB로부터 사용자 정보 로딩 (페이징 처리)
 - 과제2. 검색 기능 추가 (사용자 성, 이름별 검색)
 - 과제3. 사용자 상세 정보 출력 (주문 상품/일자/장소)
 - 과제4. 매장 정보 로딩 (매장별 월간 매출액, 단골 고객 Top10 정보 등)


# DB 내용 확인

```
sqlite3 user-sample.sqlite

sqlite> .schema
CREATE TABLE IF NOT EXISTS "users"(
  "Id" TEXT, 
  "Name" TEXT, 
  "Gender" TEXT, 
  "Age" TEXT,
  "Birthdate" TEXT, 
  "Address" TEXT
);

CREATE TABLE IF NOT EXISTS "stores"(
  "Id" TEXT, 
  "Name" TEXT, 
  "Type" TEXT, 
  "Address" TEXT
);

CREATE TABLE IF NOT EXISTS "items"(
  "Id" TEXT, 
  "Name" TEXT, 
  "Type" TEXT, 
  "UnitPrice" TEXT
);

CREATE TABLE IF NOT EXISTS "orders"(
  "Id" TEXT, 
  "OrderAt" TEXT, 
  "StoreId" TEXT, 
  "UserId" TEXT
);

CREATE TABLE IF NOT EXISTS "order_items"(
  "Id" TEXT, 
  "OrderId" TEXT, 
  "ItemId" TEXT
);
```
