# SQLite 및 CSV 파일 import 방법

## CSV 파일 불러오기

SQLite의 커맨드 라인 도구를 사용하여 CSV 파일을 import하는 방법을 안내해 드리겠습니다.

1. 터미널 또는 명령 프롬프트에서 SQLite 커맨드 라인 도구를 실행합니다. 아래와 같이 명령어를 입력합니다:

    ```sql
    sqlite3
    ```

2. SQLite 데이터베이스 파일을 엽니다:

    ```sql
    .open database.db
    ```

    위의 명령에서 **`database.db`**는 SQLite 데이터베이스 파일의 경로 및 파일 이름입니다. 필요에 따라 해당 경로를 수정하여 사용하세요.

3. CSV 파일을 import할 테이블을 생성합니다:

    ```sql
    CREATE TABLE table_name (column1 DATATYPE, column2 DATATYPE, ...);
    ```

    위의 명령에서 **`table_name`**은 생성할 테이블의 이름입니다. **`column1`**, **`column2`** 등은 테이블의 각 열(column) 이름과 데이터 유형을 나타냅니다. 필요에 따라 열 이름과 데이터 유형을 적절히 수정하여 사용하세요.

4. CSV 파일을 import합니다:

    ```sql
    .mode csv
    .import data.csv table_name
    ```

    위의 명령에서 **`data.csv`**는 import할 CSV 파일의 경로입니다. **`table_name`**은 데이터를 import할 SQLite 테이블의 이름입니다. 적절한 파일 경로와 테이블 이름으로 명령어를 수정하여 사용하세요.

### 우리 CRM 솔루션 예제

```sql
CREATE TABLE users(id TEXT PRIMARY KEY, name TEXT, gender TEXT, age INTEGER, birthdate TEXT, address TEXT);
.mode csv
.import user.csv users
```

### import 주의사항

CSV 파일의 포맷과 **`table_name`**의 스키마가 일치하지 않는 경우, SQLite는 데이터를 import하는 동안 오류를 발생시킵니다. 일치하지 않는 열 수, 데이터 유형 불일치 등과 같은 이유로 오류가 발생할 수 있습니다.

SQLite의 **`IMPORT`** 명령어는 CSV 파일의 열 수와 스키마의 열 수를 일치시키고, 각 열의 데이터 유형도 일치시켜야 합니다. 데이터 유형이 일치하지 않을 경우 SQLite는 데이터를 삽입하지 않고 오류를 발생시킵니다.

따라서, CSV 파일의 포맷과 **`table_name`**의 스키마를 일치시켜야 합니다. 만약 일치하지 않는 경우, CSV 파일의 내용을 수정하거나 테이블 스키마를 조정하여 일치시킨 후 다시 시도해야 합니다. 데이터 유형도 맞춰주어야 하며, 필요에 따라 데이터를 변환해야 할 수도 있습니다.

일치하지 않는 스키마와 데이터 유형 오류를 해결하기 위해 다음과 같은 절차를 수행할 수 있습니다:

1. CSV 파일의 포맷을 확인하고, 필요한 경우 수정합니다. CSV 파일의 열 수와 데이터 유형을 **`table_name`**의 스키마에 맞게 맞춰줍니다.
2. **`table_name`**의 스키마를 수정하여 일치시킵니다. 필요에 따라 열의 수와 데이터 유형을 조정합니다.
3. 데이터를 import하기 전에 CSV 파일과 **`table_name`**의 스키마가 일치하는지 다시 한번 확인합니다.
4. 수정된 CSV 파일과 스키마를 기반으로 import를 수행합니다. SQLite는 일치하는 데이터를 import하고, 일치하지 않는 데이터에 대해서는 오류를 발생시킵니다.

일치하지 않는 스키마와 데이터 유형 오류를 예방하기 위해, 데이터를 import하기 전에 CSV 파일의 구조와 **`table_name`**의 스키마를 신중하게 검토하는 것이 중요합니다. 데이터의 일관성을 유지하기 위해 데이터베이스 스키마와 데이터 소스를 일치시키는 것이 좋습니다.

## 테이블 컬럼 속성 변경하기

SQLite는 **`ALTER TABLE`** 문을 사용하여 기존 테이블의 컬럼을 수정하는 **`MODIFY COLUMN`** 구문을 지원하지 않습니다. 대신에, 컬럼을 변경하려면 다음과 같은 절차를 따라야 합니다:

1. 새로운 테이블을 생성하고 기존 데이터를 복사합니다.

    ```sql
    CREATE TABLE new_users (
      id INTEGER PRIMARY KEY,
      uuid TEXT,
      name TEXT,
      age INTEGER,
      birthdate DATETIME
    );

    INSERT INTO new_users (uuid, name, age, birthdate)
    SELECT id, name, CAST(age AS INTEGER), datetime(birthdate) FROM users;

    -- 이후 내용 확인
    SELECT id, name, age, strftime('%y-%m-%d', birthdate) FROM users;
    ```

2. 기존 테이블을 삭제하고 새로운 테이블의 이름을 변경합니다.

    ```sql
    DROP TABLE users;

    ALTER TABLE new_users RENAME TO users;
    ```

위의 예제에서는 **`users`** 테이블의 **`age`** 컬럼의 데이터 유형을 **`INTEGER`**로 변경하기 위해 새로운 테이블인 **`new_users`**를 생성하고, 기존 데이터를 복사한 후에 기존 테이블을 삭제하고 이름을 변경합니다.

이렇게 하면 **`users`** 테이블의 **`age`** 컬럼의 데이터 유형을 **`INTEGER`**로 변경할 수 있습니다. 단, 데이터를 복사하고 테이블을 삭제하는 과정에서 데이터의 손실이 발생할 수 있으므로, 작업을 수행하기 전에 데이터의 백업을 권장합니다.

## 쿼리구문 파일로 실행하기

다음과 같이 SQL 파일을 실행하여 결과를 확인할 수 있습니다.

```sql
sqlite3 users.db < show_10users.sql
```

# 참고

- SQLite에서 처리 가능한 데이터의 갯수는 실제로는 테이블당 레코드의 갯수나 데이터베이스 파일의 크기에 제한되지 않습니다. SQLite는 대용량의 데이터를 처리할 수 있도록 설계되었으며, 거의 무제한의 레코드를 처리할 수 있습니다.
- SQLite의 제한은 주로 하드웨어 및 운영 체제의 제약에 의해 결정됩니다. 테이블당 수천, 수백만 또는 억 개의 레코드를 가질 수 있으며, 데이터베이스 파일의 크기도 기기의 파일 시스템의 제한에 따라 다릅니다.
- 또한 SQLite는 대규모 데이터베이스 작업에 대한 효율성을 향상시키기 위해 색인(indexing)과 같은 기능을 제공합니다. 이를 통해 데이터의 검색과 정렬 속도를 향상시킬 수 있습니다.
- 따라서 SQLite를 사용할 때는 실제 하드웨어 및 운영 체제의 제약을 고려하여 데이터베이스 디자인을 계획하는 것이 좋습니다.

