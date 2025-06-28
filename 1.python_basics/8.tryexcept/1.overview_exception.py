# ===================================================================
# 파이썬 10단계: 예외 처리 실습 코드
# ===================================================================

# ===================================================================
# 1. 예외 처리 기본 개념
# ===================================================================

print("=== 예외 처리가 없는 경우 ===")

# 예외가 발생하는 상황들 (주석 처리하여 에러 방지)
print("다음은 에러가 발생할 수 있는 상황들입니다:")

# 1. ZeroDivisionError
# result = 10 / 0  # 0으로 나누기 에러

# 2. ValueError  
# number = int("abc")  # 문자를 숫자로 변환 에러

# 3. IndexError
# my_list = [1, 2, 3]
# item = my_list[10]  # 인덱스 범위 초과 에러

# 4. KeyError
# my_dict = {"name": "김철수"}
# value = my_dict["age"]  # 존재하지 않는 키 에러

# 5. FileNotFoundError
# with open("없는파일.txt", "r") as file:  # 파일이 없는 에러
#     content = file.read()

print("위의 에러들을 예외 처리로 해결해보겠습니다.")

print("\n=== try-except 기본 사용법 ===")

# 기본 try-except 구문
try:
    result = 10 / 0
except ZeroDivisionError:
    print("❌ 0으로 나눌 수 없습니다!")
    result = 0

print(f"결과: {result}")

# 사용자 입력에서의 예외 처리
def safe_input_number():
    """안전한 숫자 입력 함수"""
    while True:
        try:
            # 실제로는 input()을 사용하지만, 예제에서는 시뮬레이션
            user_inputs = ["abc", "12.5", "42"]  # 테스트용 입력들
            
            for user_input in user_inputs:
                print(f"입력값 테스트: '{user_input}'")
                number = int(user_input)
                print(f"✅ 성공! 입력된 숫자: {number}")
                return number
                
        except ValueError:
            print("❌ 올바른 숫자를 입력해주세요.")
    
    # 실제 구현에서는 이렇게 사용:
    # try:
    #     user_input = input("숫자를 입력하세요: ")
    #     number = int(user_input)
    #     return number
    # except ValueError:
    #     print("올바른 숫자를 입력해주세요.")

safe_input_number()

print("\n=== 여러 예외 처리 ===")

def safe_division(a, b):
    """안전한 나눗셈 함수"""
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print("❌ 0으로 나눌 수 없습니다.")
        return None
    except TypeError:
        print("❌ 숫자만 입력할 수 있습니다.")
        return None

# 테스트
test_cases = [
    (10, 2),      # 정상
    (10, 0),      # ZeroDivisionError
    (10, "abc"),  # TypeError
]

for a, b in test_cases:
    print(f"{a} ÷ {b} = {safe_division(a, b)}")

# 여러 예외를 한 번에 처리
def safe_list_access(my_list, index):
    """안전한 리스트 접근 함수"""
    try:
        return my_list[index]
    except (IndexError, TypeError) as e:
        print(f"❌ 리스트 접근 오류: {type(e).__name__}")
        return None

test_list = [1, 2, 3, 4, 5]
print(f"리스트[2]: {safe_list_access(test_list, 2)}")     # 정상
print(f"리스트[10]: {safe_list_access(test_list, 10)}")   # IndexError
print(f"리스트['a']: {safe_list_access(test_list, 'a')}")  # TypeError

# ===================================================================
# 2. try-except-else-finally
# ===================================================================

print("\n=== try-except-else-finally ===")

def file_processor(filename):
    """파일 처리 함수 (모든 절 사용 예제)"""
    file_handle = None
    
    try:
        # 파일이 없을 수 있으므로 예외 처리
        print(f"📁 '{filename}' 파일을 열려고 시도합니다...")
        
        # 실제로는 파일을 열지만, 예제에서는 시뮬레이션
        if filename == "없는파일.txt":
            raise FileNotFoundError("파일을 찾을 수 없습니다")
        
        print(f"✅ '{filename}' 파일이 성공적으로 열렸습니다.")
        file_content = f"'{filename}'의 내용입니다."  # 가상 내용
        
    except FileNotFoundError as e:
        print(f"❌ 파일 오류: {e}")
        file_content = None
        
    except PermissionError:
        print("❌ 파일 접근 권한이 없습니다.")
        file_content = None
        
    else:
        # 예외가 발생하지 않은 경우에만 실행
        print("📖 파일을 성공적으로 읽었습니다.")
        
    finally:
        # 예외 발생 여부와 상관없이 항상 실행
        print("🔒 파일 처리 작업을 마칩니다.")
        if file_handle:
            print("파일을 닫습니다.")
    
    return file_content

# 테스트
print("=== 정상 파일 처리 ===")
content1 = file_processor("정상파일.txt")

print("\n=== 없는 파일 처리 ===")
content2 = file_processor("없는파일.txt")

print("\n=== 데이터베이스 연결 시뮬레이션 ===")

def database_operation():
    """데이터베이스 연결 시뮬레이션"""
    connection = None
    
    try:
        print("🔌 데이터베이스에 연결 중...")
        
        # 연결 실패 시뮬레이션
        import random
        if random.choice([True, False]):
            raise ConnectionError("데이터베이스 연결 실패")
        
        print("✅ 데이터베이스 연결 성공")
        connection = "DB_CONNECTION"
        
        print("📊 데이터 조회 중...")
        data = ["사용자1", "사용자2", "사용자3"]  # 가상 데이터
        
    except ConnectionError as e:
        print(f"❌ 연결 오류: {e}")
        data = []
        
    else:
        print("✅ 데이터 조회 완료")
        
    finally:
        if connection:
            print("🔌 데이터베이스 연결을 종료합니다.")
        print("🏁 데이터베이스 작업 완료")
    
    return data

# 데이터베이스 연결 테스트
db_data = database_operation()
print(f"조회된 데이터: {db_data}")

# ===================================================================
# 3. 예외 정보 활용
# ===================================================================

print("\n=== 예외 정보 활용 ===")

def detailed_error_handling():
    """상세한 예외 정보 처리"""
    
    error_cases = [
        lambda: 10 / 0,
        lambda: int("abc"),
        lambda: [1, 2, 3][10],
        lambda: {"name": "김철수"}["age"],
    ]
    
    for i, error_func in enumerate(error_cases, 1):
        try:
            print(f"\n테스트 케이스 {i}:")
            result = error_func()
            print(f"✅ 결과: {result}")
            
        except Exception as e:
            print(f"❌ 예외 타입: {type(e).__name__}")
            print(f"❌ 예외 메시지: {e}")
            print(f"❌ 예외 발생 위치: {e.__class__.__module__}")

detailed_error_handling()

# 예외 체이닝
def divide_and_log(a, b):
    """나눗셈과 로깅을 함께 수행하는 함수"""
    try:
        result = a / b
        
        # 로깅 시뮬레이션 (파일 쓰기 오류 발생 가능)
        if b == 2:  # 특정 조건에서 로깅 실패 시뮬레이션
            raise IOError("로그 파일 쓰기 실패")
            
        print(f"📝 로그: {a} ÷ {b} = {result}")
        return result
        
    except ZeroDivisionError as original_error:
        print("❌ 나눗셈 오류가 발생했습니다.")
        # 원본 예외 정보 보존하면서 새 예외 발생
        raise ValueError("계산 처리 중 오류 발생") from original_error
        
    except IOError as io_error:
        print(f"❌ 로깅 오류: {io_error}")
        # 계산은 성공했지만 로깅 실패
        return a / b

# 예외 체이닝 테스트
try:
    result = divide_and_log(10, 0)
except ValueError as e:
    print(f"최종 예외: {e}")
    print(f"원인 예외: {e.__cause__}")

# ===================================================================
# 4. 사용자 정의 예외
# ===================================================================

print("\n=== 사용자 정의 예외 ===")

# 커스텀 예외 클래스들
class InvalidAgeError(Exception):
    """나이가 유효하지 않을 때 발생하는 예외"""
    def __init__(self, age, message="나이가 유효하지 않습니다"):
        self.age = age
        self.message = message
        super().__init__(self.message)

class InsufficientFundsError(Exception):
    """잔액이 부족할 때 발생하는 예외"""
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        message = f"잔액 부족: 현재 {balance}원, 요청 {amount}원"
        super().__init__(message)

class InvalidEmailError(Exception):
    """이메일 형식이 잘못되었을 때 발생하는 예외"""
    pass

# 사용자 정의 예외를 사용하는 함수들
def validate_age(age):
    """나이 검증 함수"""
    if not isinstance(age, int):
        raise InvalidAgeError(age, "나이는 정수여야 합니다")
    
    if age < 0:
        raise InvalidAgeError(age, "나이는 0 이상이어야 합니다")
    
    if age > 150:
        raise InvalidAgeError(age, "나이는 150 이하여야 합니다")
    
    return True

def withdraw_money(balance, amount):
    """출금 함수"""
    if amount <= 0:
        raise ValueError("출금 금액은 0보다 커야 합니다")
    
    if amount > balance:
        raise InsufficientFundsError(balance, amount)
    
    return balance - amount

def validate_email(email):
    """이메일 검증 함수"""
    if "@" not in email:
        raise InvalidEmailError("이메일에 '@'가 없습니다")
    
    if "." not in email.split("@")[1]:
        raise InvalidEmailError("도메인에 '.'이 없습니다")
    
    return True

# 사용자 정의 예외 테스트
print("=== 나이 검증 테스트 ===")
age_test_cases = [25, -5, 200, "abc"]

for age in age_test_cases:
    try:
        validate_age(age)
        print(f"✅ 나이 {age}: 유효")
    except InvalidAgeError as e:
        print(f"❌ 나이 {e.age}: {e.message}")
    except Exception as e:
        print(f"❌ 나이 {age}: 예상치 못한 오류 - {e}")

print("\n=== 출금 테스트 ===")
withdrawal_test_cases = [
    (100000, 50000),   # 정상
    (100000, 150000),  # 잔액 부족
    (100000, -1000),   # 음수 금액
]

for balance, amount in withdrawal_test_cases:
    try:
        new_balance = withdraw_money(balance, amount)
        print(f"✅ 출금 성공: {amount}원 출금, 잔액: {new_balance}원")
    except InsufficientFundsError as e:
        print(f"❌ {e}")
    except ValueError as e:
        print(f"❌ 입력 오류: {e}")

print("\n=== 이메일 검증 테스트 ===")
email_test_cases = ["test@example.com", "invalid.email", "user@domain", "@domain.com"]

for email in email_test_cases:
    try:
        validate_email(email)
        print(f"✅ 이메일 '{email}': 유효")
    except InvalidEmailError as e:
        print(f"❌ 이메일 '{email}': {e}")

# ===================================================================
# 5. 실습 예제들
# ===================================================================

print("\n=== 실습 예제 1: 안전한 계산기 ===")

class CalculatorError(Exception):
    """계산기 관련 예외의 기본 클래스"""
    pass

class DivisionByZeroError(CalculatorError):
    """0으로 나누기 예외"""
    pass

class InvalidOperationError(CalculatorError):
    """잘못된 연산 예외"""
    pass

def safe_calculator(operation, a, b):
    """안전한 계산기 함수"""
    try:
        # 입력값 검증
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("숫자만 입력할 수 있습니다")
        
        # 연산 수행
        if operation == "+":
            result = a + b
        elif operation == "-":
            result = a - b
        elif operation == "*":
            result = a * b
        elif operation == "/":
            if b == 0:
                raise DivisionByZeroError("0으로 나눌 수 없습니다")
            result = a / b
        elif operation == "**":
            result = a ** b
        elif operation == "%":
            if b == 0:
                raise DivisionByZeroError("0으로 나머지 연산을 할 수 없습니다")
            result = a % b
        else:
            raise InvalidOperationError(f"지원하지 않는 연산: {operation}")
        
        return result
        
    except (TypeError, ValueError) as e:
        print(f"❌ 입력 오류: {e}")
        return None
    except DivisionByZeroError as e:
        print(f"❌ 나눗셈 오류: {e}")
        return None
    except InvalidOperationError as e:
        print(f"❌ 연산 오류: {e}")
        return None
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {e}")
        return None

# 계산기 테스트
calculator_tests = [
    ("+", 10, 5),      # 정상
    ("/", 10, 0),      # 0으로 나누기
    ("*", 10, "abc"),  # 타입 오류
    ("@", 10, 5),      # 잘못된 연산자
    ("**", 2, 10),     # 거듭제곱
]

print("안전한 계산기 테스트:")
for op, x, y in calculator_tests:
    result = safe_calculator(op, x, y)
    if result is not None:
        print(f"✅ {x} {op} {y} = {result}")

print("\n=== 실습 예제 2: 파일 관리 시스템 ===")

class FileManagerError(Exception):
    """파일 관리자 예외 기본 클래스"""
    pass

class FileNotFoundError(FileManagerError):
    """파일을 찾을 수 없는 예외"""
    pass

class PermissionDeniedError(FileManagerError):
    """권한이 없는 예외"""
    pass

def file_manager():
    """파일 관리 시스템"""
    
    # 가상 파일 시스템
    virtual_files = {
        "document.txt": {"content": "문서 내용", "permission": "read"},
        "secret.txt": {"content": "비밀 정보", "permission": "none"},
        "config.json": {"content": '{"setting": "value"}', "permission": "read"}
    }
    
    def read_file(filename):
        """파일 읽기 함수"""
        try:
            if filename not in virtual_files:
                raise FileNotFoundError(f"파일 '{filename}'을 찾을 수 없습니다")
            
            file_data = virtual_files[filename]
            
            if file_data["permission"] == "none":
                raise PermissionDeniedError(f"파일 '{filename}'에 대한 읽기 권한이 없습니다")
            
            return file_data["content"]
            
        except FileNotFoundError as e:
            print(f"❌ {e}")
            return None
        except PermissionDeniedError as e:
            print(f"❌ {e}")
            return None
        except Exception as e:
            print(f"❌ 예상치 못한 오류: {e}")
            return None
    
    def write_file(filename, content):
        """파일 쓰기 함수"""
        try:
            if not content:
                raise ValueError("내용이 비어있습니다")
            
            if filename in virtual_files:
                file_data = virtual_files[filename]
                if file_data["permission"] == "none":
                    raise PermissionDeniedError(f"파일 '{filename}'에 대한 쓰기 권한이 없습니다")
            
            # 파일 생성 또는 업데이트
            virtual_files[filename] = {"content": content, "permission": "read"}
            return True
            
        except ValueError as e:
            print(f"❌ 입력 오류: {e}")
            return False
        except PermissionDeniedError as e:
            print(f"❌ {e}")
            return False
        except Exception as e:
            print(f"❌ 예상치 못한 오류: {e}")
            return False
    
    def list_files():
        """파일 목록 반환"""
        return list(virtual_files.keys())
    
    return {
        "read": read_file,
        "write": write_file,
        "list": list_files
    }

# 파일 관리자 테스트
fm = file_manager()

print("파일 관리 시스템 테스트:")
print(f"📁 파일 목록: {fm['list']()}")

# 파일 읽기 테스트
test_files = ["document.txt", "secret.txt", "nonexistent.txt"]
for filename in test_files:
    print(f"\n📖 '{filename}' 읽기 시도:")
    content = fm["read"](filename)
    if content:
        print(f"✅ 내용: {content}")

# 파일 쓰기 테스트
print(f"\n✏️ 새 파일 'note.txt' 생성:")
success = fm["write"]("note.txt", "새로운 메모 내용")
if success:
    print("✅ 파일 생성 성공")
    print(f"📖 파일 읽기: {fm['read']('note.txt')}")

print("\n=== 실습 예제 3: 웹 API 클라이언트 시뮬레이션 ===")

class APIError(Exception):
    """API 관련 예외 기본 클래스"""
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(f"API Error {status_code}: {message}")

class NetworkError(APIError):
    """네트워크 연결 오류"""
    def __init__(self, message="네트워크 연결 실패"):
        super().__init__(0, message)

class AuthenticationError(APIError):
    """인증 오류"""
    def __init__(self):
        super().__init__(401, "인증 실패")

class NotFoundError(APIError):
    """리소스를 찾을 수 없음"""
    def __init__(self, resource):
        super().__init__(404, f"리소스 '{resource}'를 찾을 수 없습니다")

class RateLimitError(APIError):
    """요청 제한 초과"""
    def __init__(self):
        super().__init__(429, "요청 한도 초과")

def api_client():
    """웹 API 클라이언트 시뮬레이션"""
    
    # API 상태 시뮬레이션
    import random
    
    def make_request(endpoint, auth_token=None):
        """API 요청 함수"""
        try:
            print(f"🌐 API 요청: {endpoint}")
            
            # 네트워크 연결 실패 시뮬레이션 (10% 확률)
            if random.random() < 0.1:
                raise NetworkError("서버에 연결할 수 없습니다")
            
            # 인증 확인
            if endpoint.startswith("/private") and not auth_token:
                raise AuthenticationError()
            
            # 잘못된 토큰 (20% 확률)
            if auth_token == "invalid_token" and random.random() < 0.2:
                raise AuthenticationError()
            
            # 존재하지 않는 리소스
            if endpoint == "/users/999":
                raise NotFoundError("사용자")
            
            # 요청 제한 (5% 확률)
            if random.random() < 0.05:
                raise RateLimitError()
            
            # 성공적인 응답 시뮬레이션
            if endpoint == "/users":
                return {"users": ["김철수", "이영희", "박민수"]}
            elif endpoint == "/private/data":
                return {"secret": "기밀 정보"}
            else:
                return {"message": "성공"}
                
        except NetworkError as e:
            print(f"❌ 네트워크 오류: {e.message}")
            return None
            
        except AuthenticationError as e:
            print(f"❌ 인증 오류: {e.message}")
            return None
            
        except NotFoundError as e:
            print(f"❌ 리소스 오류: {e.message}")
            return None
            
        except RateLimitError as e:
            print(f"❌ 제한 오류: {e.message}")
            print("잠시 후 다시 시도해주세요.")
            return None
            
        except APIError as e:
            print(f"❌ API 오류: {e}")
            return None
            
        except Exception as e:
            print(f"❌ 예상치 못한 오류: {e}")
            return None
    
    def retry_request(endpoint, auth_token=None, max_retries=3):
        """재시도 기능이 있는 API 요청"""
        for attempt in range(max_retries + 1):
            try:
                if attempt > 0:
                    print(f"🔄 재시도 {attempt}/{max_retries}")
                
                response = make_request(endpoint, auth_token)
                if response is not None:
                    return response
                
                # NetworkError나 RateLimitError인 경우 재시도
                if attempt < max_retries:
                    import time
                    time.sleep(1)  # 1초 대기
                    
            except (NetworkError, RateLimitError):
                if attempt < max_retries:
                    print("🕐 잠시 후 재시도합니다...")
                    continue
                else:
                    print("❌ 최대 재시도 횟수를 초과했습니다.")
            except Exception:
                # 다른 종류의 예외는 재시도하지 않음
                break
        
        return None
    
    return {
        "request": make_request,
        "retry_request": retry_request
    }

# API 클라이언트 테스트
api = api_client()

print("웹 API 클라이언트 테스트:")

# 일반적인 요청들
test_requests = [
    ("/users", None),
    ("/private/data", "valid_token"),
    ("/private/data", None),  # 인증 토큰 없음
    ("/users/999", None),     # 존재하지 않는 사용자
]

for endpoint, token in test_requests:
    print(f"\n🚀 요청: {endpoint}")
    response = api["request"](endpoint, token)
    if response:
        print(f"✅ 응답: {response}")

# 재시도 요청 테스트
print(f"\n🔄 재시도 기능 테스트:")
response = api["retry_request"]("/users")
if response:
    print(f"✅ 최종 응답: {response}")

print("\n=== 10단계 완료! ===")
print("예외 처리를 모두 배웠습니다.")
print("다음 단계에서는 파일 입출력을 배워보겠습니다!")

# ===================================================================
# 추가 팁
# ===================================================================

"""
10단계에서 기억해야 할 중요한 점들:

1. 예외 처리 기본 구조:
   try:
       # 예외가 발생할 수 있는 코드
   except SpecificError:
       # 특정 예외 처리
   except Exception as e:
       # 모든 예외 처리
   else:
       # 예외가 없을 때 실행
   finally:
       # 항상 실행 (정리 작업)

2. 주요 내장 예외:
   - ValueError: 잘못된 값
   - TypeError: 잘못된 타입
   - IndexError: 인덱스 범위 초과
   - KeyError: 존재하지 않는 키
   - FileNotFoundError: 파일 없음
   - ZeroDivisionError: 0으로 나누기

3. 사용자 정의 예외:
   - Exception 클래스를 상속
   - 의미 있는 예외명 사용
   - 적절한 메시지 제공

4. 예외 처리 모범 사례:
   - 구체적인 예외부터 처리
   - 예외 정보 활용 (as e)
   - 리소스 정리 (finally 블록)
   - 적절한 로깅

5. 언제 예외 처리를 사용할까:
   - 사용자 입력 검증
   - 파일/네트워크 작업
   - 외부 API 호출
   - 데이터 변환 작업

실습할 때 꼭 해보세요:
- 다양한 예외 상황 만들어보기
- 사용자 정의 예외 클래스 작성하기
- try-except-else-finally 모든 블록 사용해보기
- 실제 프로젝트에서 발생할 수 있는 예외들 처리하기
"""
