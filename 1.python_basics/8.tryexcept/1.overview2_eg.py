############################################################
# 🎯 반드시 연습해야 할 핵심 개념들
############################################################
# 1. 기본 try-except 패턴
# 가장 기본적인 패턴
try:
    risky_operation()
except SpecificError:
    handle_error()

# 여러 예외 처리
try:
    user_input = int(input("숫자 입력: "))
    result = 10 / user_input
except ValueError:
    print("숫자만 입력해주세요")
except ZeroDivisionError:
    print("0은 입력할 수 없습니다")
except Exception as e:
    print(f"예상치 못한 오류: {e}")


############################################################
# 2. 예외 정보 활용
try:
    # 위험한 작업
    process_data()
except Exception as e:
    print(f"오류 타입: {type(e).__name__}")
    print(f"오류 메시지: {e}")
    print(f"오류 발생 위치 정보도 기록할 수 있음")
3. finally 블록으로 리소스 정리
pythonfile_handle = None
try:
    file_handle = open("data.txt", "r")
    data = file_handle.read()
    process_data(data)
except FileNotFoundError:
    print("파일을 찾을 수 없습니다")
except Exception as e:
    print(f"파일 처리 중 오류: {e}")
finally:
    if file_handle:
        file_handle.close()
        print("파일을 닫았습니다")

############################################################
# 💡 실무에서 자주 쓰이는 예외 처리 패턴들
############################################################
# 1. 사용자 입력 검증
def get_user_age():
    """안전한 나이 입력 함수"""
    while True:
        try:
            age = int(input("나이를 입력하세요: "))
            if age < 0 or age > 150:
                raise ValueError("나이는 0~150 사이여야 합니다")
            return age
        except ValueError as e:
            print(f"잘못된 입력: {e}")
            print("다시 입력해주세요.")


############################################################
# 2. API 호출 안전 처리
import requests

def safe_api_call(url, timeout=5):
    """안전한 API 호출"""
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()  # HTTP 오류 확인
        return response.json()
    
    except requests.exceptions.Timeout:
        print("요청 시간 초과")
        return None
    except requests.exceptions.ConnectionError:
        print("네트워크 연결 오류")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP 오류: {e}")
        return None
    except ValueError:
        print("JSON 파싱 오류")
        return None


############################################################
# 3. 데이터 변환 안전 처리
def safe_convert_to_number(value):
    """안전한 숫자 변환"""
    try:
        # 정수 시도
        return int(value)
    except ValueError:
        try:
            # 실수 시도
            return float(value)
        except ValueError:
            print(f"'{value}'는 숫자로 변환할 수 없습니다")
            return None

def parse_csv_safely(csv_line):
    """안전한 CSV 파싱"""
    try:
        fields = csv_line.strip().split(',')
        
        name = fields[0].strip()
        age = safe_convert_to_number(fields[1])
        salary = safe_convert_to_number(fields[2])
        
        if age is None or salary is None:
            raise ValueError("숫자 필드 변환 실패")
            
        return {"name": name, "age": age, "salary": salary}
        
    except IndexError:
        print("CSV 형식이 올바르지 않습니다")
        return None
    except Exception as e:
        print(f"CSV 파싱 오류: {e}")
        return None


############################################################
# 🚨 초보자가 자주 하는 실수들
############################################################
# 1. 너무 광범위한 예외 처리
# 나쁜 예: 모든 예외를 숨김
try:
    complex_operation()
except:  # 모든 예외를 잡아버림
    pass  # 조용히 무시

# 좋은 예: 구체적인 예외만 처리
try:
    complex_operation()
except ValueError as e:
    print(f"값 오류: {e}")
    # 적절한 복구 로직
except FileNotFoundError:
    print("파일을 찾을 수 없습니다")
    # 기본 파일 생성 등


############################################################
# 2. 예외 발생 후 계속 진행
# 위험한 패턴
try:
    important_data = load_critical_data()
except Exception:
    important_data = None  # None으로 설정

# important_data가 None인데 계속 사용
result = important_data.process()  # 오류 발생!

# 안전한 패턴
try:
    important_data = load_critical_data()
except Exception as e:
    print(f"중요한 데이터 로드 실패: {e}")
    return None  # 함수 종료 또는 기본값 제공

if important_data is not None:
    result = important_data.process()


############################################################
# 3. 리소스 정리 누락
# 위험한 패턴
try:
    file = open("data.txt", "w")
    file.write("some data")
    risky_operation()  # 여기서 예외 발생 시 파일이 안 닫힘
    file.close()
except Exception:
    print("오류 발생")

# 안전한 패턴 1: finally 사용
file = None
try:
    file = open("data.txt", "w")
    file.write("some data")
    risky_operation()
except Exception:
    print("오류 발생")
finally:
    if file:
        file.close()

# 안전한 패턴 2: with 문 사용 (더 좋음)
try:
    with open("data.txt", "w") as file:
        file.write("some data")
        risky_operation()
except Exception:
    print("오류 발생")


############################################################
# 💪 실전 예외 처리 프로젝트
############################################################
# 1. 견고한 계산기
class RobustCalculator:
    def __init__(self):
        self.history = []
    
    def calculate(self, expression):
        """수식을 안전하게 계산"""
        try:
            # 보안상 eval 대신 제한된 연산만 허용
            allowed_chars = set('0123456789+-*/().= ')
            if not all(c in allowed_chars for c in expression):
                raise ValueError("허용되지 않는 문자가 포함되어 있습니다")
            
            # 위험한 함수 호출 방지
            dangerous_keywords = ['import', 'exec', 'eval', '__']
            if any(keyword in expression for keyword in dangerous_keywords):
                raise ValueError("보안상 허용되지 않는 표현식입니다")
            
            result = eval(expression)
            
            # 결과 검증
            if not isinstance(result, (int, float)):
                raise TypeError("계산 결과가 숫자가 아닙니다")
            
            if abs(result) > 10**10:
                raise OverflowError("결과가 너무 큽니다")
            
            # 이력 저장
            self.history.append(f"{expression} = {result}")
            return result
            
        except ZeroDivisionError:
            return "오류: 0으로 나눌 수 없습니다"
        except ValueError as e:
            return f"입력 오류: {e}"
        except TypeError as e:
            return f"타입 오류: {e}"
        except OverflowError as e:
            return f"계산 오류: {e}"
        except Exception as e:
            return f"예상치 못한 오류: {e}"
    
    def get_history(self):
        return self.history.copy()

# 테스트
calc = RobustCalculator()
test_expressions = [
    "2 + 3 * 4",
    "10 / 0",
    "2 ** 100",
    "import os",
    "abc + 123"
]

for expr in test_expressions:
    result = calc.calculate(expr)
    print(f"{expr} → {result}")

############################################################
# 2. 안전한 파일 처리기
class SafeFileProcessor:
    def __init__(self, max_file_size=10*1024*1024):  # 10MB 제한
        self.max_file_size = max_file_size
    
    def read_text_file(self, filepath, encoding='utf-8'):
        """텍스트 파일을 안전하게 읽기"""
        try:
            # 파일 크기 확인
            import os
            if os.path.exists(filepath):
                file_size = os.path.getsize(filepath)
                if file_size > self.max_file_size:
                    raise ValueError(f"파일이 너무 큽니다: {file_size} bytes")
            
            with open(filepath, 'r', encoding=encoding) as file:
                content = file.read()
                return {"success": True, "content": content, "size": len(content)}
                
        except FileNotFoundError:
            return {"success": False, "error": "파일을 찾을 수 없습니다"}
        except PermissionError:
            return {"success": False, "error": "파일 접근 권한이 없습니다"}
        except UnicodeDecodeError:
            return {"success": False, "error": f"{encoding} 인코딩으로 읽을 수 없습니다"}
        except ValueError as e:
            return {"success": False, "error": str(e)}
        except Exception as e:
            return {"success": False, "error": f"예상치 못한 오류: {e}"}
    
    def write_text_file(self, filepath, content, encoding='utf-8', backup=True):
        """텍스트 파일을 안전하게 쓰기"""
        try:
            # 백업 생성
            if backup and os.path.exists(filepath):
                backup_path = filepath + '.backup'
                import shutil
                shutil.copy2(filepath, backup_path)
            
            with open(filepath, 'w', encoding=encoding) as file:
                file.write(content)
                return {"success": True, "message": "파일 저장 완료"}
                
        except PermissionError:
            return {"success": False, "error": "파일 쓰기 권한이 없습니다"}
        except OSError as e:
            return {"success": False, "error": f"파일 시스템 오류: {e}"}
        except Exception as e:
            return {"success": False, "error": f"예상치 못한 오류: {e}"}
    
    def process_csv(self, filepath):
        """CSV 파일을 안전하게 처리"""
        try:
            result = self.read_text_file(filepath)
            if not result["success"]:
                return result
            
            lines = result["content"].strip().split('\n')
            if not lines:
                raise ValueError("빈 파일입니다")
            
            # 헤더와 데이터 분리
            header = [col.strip() for col in lines[0].split(',')]
            data = []
            
            for line_num, line in enumerate(lines[1:], 2):
                try:
                    row_data = [col.strip() for col in line.split(',')]
                    if len(row_data) != len(header):
                        print(f"경고: {line_num}행의 컬럼 수가 맞지 않습니다")
                        continue
                    
                    data.append(dict(zip(header, row_data)))
                    
                except Exception as e:
                    print(f"경고: {line_num}행 처리 중 오류: {e}")
                    continue
            
            return {
                "success": True,
                "header": header,
                "data": data,
                "rows_processed": len(data)
            }
            
        except Exception as e:
            return {"success": False, "error": f"CSV 처리 오류: {e}"}

# 파일 처리기 테스트
processor = SafeFileProcessor()

# 가상 파일 테스트 (실제로는 실제 파일 경로 사용)
test_results = [
    processor.read_text_file("nonexistent.txt"),
    processor.write_text_file("test.txt", "Hello, World!")
]

for result in test_results:
    print(f"결과: {result}")
