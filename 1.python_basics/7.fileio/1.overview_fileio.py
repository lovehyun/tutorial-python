# ===================================================================
# 파이썬 11단계: 파일 입출력 실습 코드
# ===================================================================

# ===================================================================
# 1. 파일 읽기와 쓰기 기본
# ===================================================================

print("=== 파일 입출력 기초 ===")

# 텍스트 파일 쓰기
def create_sample_file():
    """샘플 파일들을 생성하는 함수"""
    
    # 1. 기본 텍스트 파일 생성
    try:
        with open("sample.txt", "w", encoding="utf-8") as file:
            file.write("안녕하세요!\n")
            file.write("파이썬 파일 처리를 배우고 있습니다.\n")
            file.write("이것은 샘플 텍스트 파일입니다.\n")
        print("✅ sample.txt 파일이 생성되었습니다.")
    except Exception as e:
        print(f"❌ 파일 생성 오류: {e}")
    
    # 2. 학생 데이터 파일 생성
    student_data = """김철수,20,컴퓨터공학,85
이영희,21,경영학,92
박민수,19,수학,78
최영수,22,물리학,95
한지민,20,화학,88"""
    
    try:
        with open("students.csv", "w", encoding="utf-8") as file:
            file.write("이름,나이,전공,성적\n")
            file.write(student_data)
        print("✅ students.csv 파일이 생성되었습니다.")
    except Exception as e:
        print(f"❌ CSV 파일 생성 오류: {e}")
    
    # 3. 설정 파일 생성
    config_data = """[Database]
host=localhost
port=5432
username=admin
password=secret123

[Application]
debug=True
max_users=1000
timeout=30"""
    
    try:
        with open("config.ini", "w", encoding="utf-8") as file:
            file.write(config_data)
        print("✅ config.ini 파일이 생성되었습니다.")
    except Exception as e:
        print(f"❌ 설정 파일 생성 오류: {e}")

# 샘플 파일들 생성
create_sample_file()

print("\n=== 파일 읽기 방법들 ===")

# 1. 전체 파일 읽기
def read_entire_file(filename):
    """파일 전체를 한 번에 읽는 함수"""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"❌ 파일 '{filename}'을 찾을 수 없습니다.")
        return None
    except Exception as e:
        print(f"❌ 파일 읽기 오류: {e}")
        return None

# 전체 파일 읽기 테스트
print("sample.txt 전체 내용:")
content = read_entire_file("sample.txt")
if content:
    print(content)

# 2. 줄 단위로 읽기
def read_lines(filename):
    """파일을 줄 단위로 읽는 함수"""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
            return lines
    except Exception as e:
        print(f"❌ 파일 읽기 오류: {e}")
        return []

print("\nsample.txt 줄별 내용:")
lines = read_lines("sample.txt")
for i, line in enumerate(lines, 1):
    print(f"{i}: {line.strip()}")

# 3. 한 줄씩 처리하기 (메모리 효율적)
def process_file_line_by_line(filename):
    """파일을 한 줄씩 처리하는 함수 (큰 파일에 적합)"""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, 1):
                # 각 줄을 처리
                cleaned_line = line.strip()
                if cleaned_line:  # 빈 줄이 아닌 경우만
                    print(f"라인 {line_number}: {cleaned_line}")
    except Exception as e:
        print(f"❌ 파일 처리 오류: {e}")

print("\nsample.txt 한 줄씩 처리:")
process_file_line_by_line("sample.txt")

# ===================================================================
# 2. with 문 사용법
# ===================================================================

print("\n=== with 문의 중요성 ===")

# 좋지 않은 방법 (파일이 제대로 닫히지 않을 수 있음)
def bad_file_handling():
    """권장하지 않는 파일 처리 방법"""
    try:
        file = open("sample.txt", "r", encoding="utf-8")
        content = file.read()
        # 예외가 발생하면 파일이 닫히지 않을 수 있음
        file.close()
        return content
    except Exception as e:
        print(f"오류: {e}")
        return None

# 좋은 방법 (with 문 사용)
def good_file_handling():
    """권장하는 파일 처리 방법"""
    try:
        with open("sample.txt", "r", encoding="utf-8") as file:
            content = file.read()
            # with 블록을 벗어나면 자동으로 파일이 닫힘
            return content
    except Exception as e:
        print(f"오류: {e}")
        return None

print("with 문을 사용한 안전한 파일 처리:")
safe_content = good_file_handling()
if safe_content:
    print("파일이 안전하게 처리되었습니다.")

# 여러 파일 동시 처리
def process_multiple_files():
    """여러 파일을 동시에 처리하는 함수"""
    try:
        with open("sample.txt", "r", encoding="utf-8") as input_file, \
             open("output.txt", "w", encoding="utf-8") as output_file:
            
            # 입력 파일 읽기
            lines = input_file.readlines()
            
            # 처리된 내용을 출력 파일에 쓰기
            for i, line in enumerate(lines, 1):
                processed_line = f"[{i}] {line}"
                output_file.write(processed_line)
        
        print("✅ 여러 파일 처리 완료")
        
    except Exception as e:
        print(f"❌ 다중 파일 처리 오류: {e}")

process_multiple_files()

# ===================================================================
# 3. CSV 파일 다루기
# ===================================================================

print("\n=== CSV 파일 처리 ===")

import csv

def read_csv_manual():
    """수동으로 CSV 파일 읽기"""
    try:
        with open("students.csv", "r", encoding="utf-8") as file:
            lines = file.readlines()
            
            if not lines:
                print("빈 파일입니다.")
                return
            
            # 헤더 분리
            header = lines[0].strip().split(",")
            print(f"헤더: {header}")
            
            # 데이터 처리
            students = []
            for line in lines[1:]:
                data = line.strip().split(",")
                if len(data) == len(header):
                    student = dict(zip(header, data))
                    students.append(student)
            
            return students
            
    except Exception as e:
        print(f"❌ CSV 수동 읽기 오류: {e}")
        return []

# 수동 CSV 읽기
print("수동 CSV 읽기:")
students_manual = read_csv_manual()
for student in students_manual[:3]:  # 처음 3명만 출력
    print(student)

def read_csv_with_module():
    """csv 모듈을 사용한 CSV 파일 읽기"""
    try:
        with open("students.csv", "r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            students = []
            
            for row in csv_reader:
                students.append(row)
            
            return students
            
    except Exception as e:
        print(f"❌ CSV 모듈 읽기 오류: {e}")
        return []

print("\ncsv 모듈을 사용한 읽기:")
students_module = read_csv_with_module()
for student in students_module[:3]:
    print(student)

def write_csv_file():
    """CSV 파일 쓰기"""
    try:
        # 새로운 학생 데이터
        new_students = [
            {"이름": "정수진", "나이": "23", "전공": "영어교육", "성적": "89"},
            {"이름": "조민호", "나이": "24", "전공": "체육교육", "성적": "91"},
            {"이름": "윤서연", "나이": "22", "전공": "미술", "성적": "87"}
        ]
        
        with open("new_students.csv", "w", newline="", encoding="utf-8") as file:
            fieldnames = ["이름", "나이", "전공", "성적"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            # 헤더 쓰기
            writer.writeheader()
            
            # 데이터 쓰기
            for student in new_students:
                writer.writerow(student)
        
        print("✅ new_students.csv 파일이 생성되었습니다.")
        
    except Exception as e:
        print(f"❌ CSV 쓰기 오류: {e}")

write_csv_file()

def analyze_csv_data():
    """CSV 데이터 분석"""
    try:
        students = read_csv_with_module()
        
        if not students:
            print("분석할 데이터가 없습니다.")
            return
        
        print(f"\n=== 학생 데이터 분석 ===")
        print(f"총 학생 수: {len(students)}명")
        
        # 성적 분석
        scores = [int(student["성적"]) for student in students]
        average_score = sum(scores) / len(scores)
        highest_score = max(scores)
        lowest_score = min(scores)
        
        print(f"평균 성적: {average_score:.1f}점")
        print(f"최고 성적: {highest_score}점")
        print(f"최저 성적: {lowest_score}점")
        
        # 전공별 분석
        majors = {}
        for student in students:
            major = student["전공"]
            if major not in majors:
                majors[major] = []
            majors[major].append(int(student["성적"]))
        
        print(f"\n전공별 평균 성적:")
        for major, scores in majors.items():
            avg = sum(scores) / len(scores)
            print(f"  {major}: {avg:.1f}점 ({len(scores)}명)")
            
    except Exception as e:
        print(f"❌ 데이터 분석 오류: {e}")

analyze_csv_data()

# ===================================================================
# 4. 파일 시스템 작업
# ===================================================================

print("\n=== 파일 시스템 작업 ===")

import os
import shutil
from datetime import datetime

def file_system_operations():
    """파일 시스템 관련 작업들"""
    
    # 현재 디렉토리 확인
    current_dir = os.getcwd()
    print(f"현재 디렉토리: {current_dir}")
    
    # 디렉토리 생성
    test_dir = "test_directory"
    try:
        if not os.path.exists(test_dir):
            os.makedirs(test_dir)
            print(f"✅ '{test_dir}' 디렉토리 생성됨")
        else:
            print(f"'{test_dir}' 디렉토리가 이미 존재함")
    except Exception as e:
        print(f"❌ 디렉토리 생성 오류: {e}")
    
    # 파일 존재 확인
    files_to_check = ["sample.txt", "students.csv", "nonexistent.txt"]
    print(f"\n파일 존재 확인:")
    for filename in files_to_check:
        exists = os.path.exists(filename)
        print(f"  {filename}: {'존재함' if exists else '존재하지 않음'}")
    
    # 파일 정보 조회
    if os.path.exists("sample.txt"):
        stat_info = os.stat("sample.txt")
        file_size = stat_info.st_size
        modified_time = datetime.fromtimestamp(stat_info.st_mtime)
        
        print(f"\nsample.txt 정보:")
        print(f"  크기: {file_size} bytes")
        print(f"  수정 시간: {modified_time}")
    
    # 디렉토리 내용 확인
    print(f"\n현재 디렉토리 내용:")
    try:
        for item in os.listdir("."):
            if os.path.isfile(item):
                size = os.path.getsize(item)
                print(f"  📄 {item} ({size} bytes)")
            elif os.path.isdir(item):
                print(f"  📁 {item}/")
    except Exception as e:
        print(f"❌ 디렉토리 조회 오류: {e}")

file_system_operations()

def backup_files():
    """파일 백업 시스템"""
    backup_dir = "backup"
    
    try:
        # 백업 디렉토리 생성
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        # 백업할 파일들
        files_to_backup = ["sample.txt", "students.csv", "config.ini"]
        
        print(f"\n=== 파일 백업 ===")
        for filename in files_to_backup:
            if os.path.exists(filename):
                # 타임스탬프 추가
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                name, ext = os.path.splitext(filename)
                backup_filename = f"{name}_{timestamp}{ext}"
                backup_path = os.path.join(backup_dir, backup_filename)
                
                # 파일 복사
                shutil.copy2(filename, backup_path)
                print(f"✅ {filename} → {backup_path}")
            else:
                print(f"❌ {filename} 파일이 존재하지 않음")
                
    except Exception as e:
        print(f"❌ 백업 오류: {e}")

backup_files()

# ===================================================================
# 5. JSON 파일 처리
# ===================================================================

print("\n=== JSON 파일 처리 ===")

import json

def json_file_operations():
    """JSON 파일 읽기/쓰기 작업"""
    
    # JSON 데이터 생성
    student_records = {
        "school_name": "파이썬 대학교",
        "semester": "2025-1학기",
        "students": [
            {
                "id": "2024001",
                "name": "김철수",
                "age": 20,
                "major": "컴퓨터공학",
                "grades": {
                    "python": 95,
                    "database": 88,
                    "algorithm": 92
                },
                "active": True
            },
            {
                "id": "2024002", 
                "name": "이영희",
                "age": 21,
                "major": "경영학",
                "grades": {
                    "marketing": 91,
                    "finance": 87,
                    "management": 94
                },
                "active": True
            },
            {
                "id": "2024003",
                "name": "박민수", 
                "age": 19,
                "major": "수학",
                "grades": {
                    "calculus": 96,
                    "statistics": 89,
                    "algebra": 93
                },
                "active": False
            }
        ]
    }
    
    # JSON 파일 쓰기
    try:
        with open("student_records.json", "w", encoding="utf-8") as file:
            json.dump(student_records, file, ensure_ascii=False, indent=2)
        print("✅ student_records.json 파일이 생성되었습니다.")
    except Exception as e:
        print(f"❌ JSON 쓰기 오류: {e}")
    
    # JSON 파일 읽기
    try:
        with open("student_records.json", "r", encoding="utf-8") as file:
            loaded_data = json.load(file)
        
        print(f"\n=== JSON 데이터 읽기 ===")
        print(f"학교명: {loaded_data['school_name']}")
        print(f"학기: {loaded_data['semester']}")
        print(f"학생 수: {len(loaded_data['students'])}명")
        
        # 학생별 정보 출력
        for student in loaded_data['students']:
            name = student['name']
            major = student['major']
            grades = student['grades']
            average = sum(grades.values()) / len(grades)
            status = "재학" if student['active'] else "휴학"
            
            print(f"\n학생: {name} ({major})")
            print(f"  상태: {status}")
            print(f"  성적: {grades}")
            print(f"  평균: {average:.1f}점")
            
    except Exception as e:
        print(f"❌ JSON 읽기 오류: {e}")

json_file_operations()

def update_json_data():
    """JSON 파일 데이터 업데이트"""
    try:
        # 기존 데이터 읽기
        with open("student_records.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        
        # 새 학생 추가
        new_student = {
            "id": "2024004",
            "name": "최영수",
            "age": 22,
            "major": "물리학",
            "grades": {
                "physics": 97,
                "quantum": 91,
                "relativity": 95
            },
            "active": True
        }
        
        data['students'].append(new_student)
        
        # 기존 학생의 성적 업데이트
        for student in data['students']:
            if student['name'] == "김철수":
                student['grades']['web_development'] = 90
                break
        
        # 업데이트된 데이터 저장
        with open("student_records.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        
        print("✅ JSON 데이터가 업데이트되었습니다.")
        
    except Exception as e:
        print(f"❌ JSON 업데이트 오류: {e}")

update_json_data()

# ===================================================================
# 6. 로그 파일 처리
# ===================================================================

print("\n=== 로그 파일 처리 ===")

def create_log_system():
    """간단한 로그 시스템"""
    
    def write_log(level, message):
        """로그 메시지를 파일에 기록"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] {level}: {message}\n"
            
            with open("application.log", "a", encoding="utf-8") as file:
                file.write(log_entry)
                
        except Exception as e:
            print(f"❌ 로그 쓰기 오류: {e}")
    
    def read_logs(level_filter=None):
        """로그 파일 읽기 및 필터링"""
        try:
            if not os.path.exists("application.log"):
                print("로그 파일이 존재하지 않습니다.")
                return
            
            with open("application.log", "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if level_filter:
                        if level_filter.upper() in line:
                            print(line)
                    else:
                        print(line)
                        
        except Exception as e:
            print(f"❌ 로그 읽기 오류: {e}")
    
    # 로그 시스템 테스트
    print("로그 시스템 테스트:")
    
    # 다양한 로그 메시지 작성
    write_log("INFO", "애플리케이션이 시작되었습니다.")
    write_log("DEBUG", "사용자 로그인 시도: admin")
    write_log("INFO", "사용자 admin이 로그인했습니다.")
    write_log("WARNING", "비정상적인 접근 시도가 감지되었습니다.")
    write_log("ERROR", "데이터베이스 연결에 실패했습니다.")
    write_log("INFO", "데이터베이스 연결이 복구되었습니다.")
    write_log("INFO", "애플리케이션이 종료되었습니다.")
    
    print("\n전체 로그:")
    read_logs()
    
    print("\n에러 로그만:")
    read_logs("ERROR")
    
    print("\n경고 로그만:")
    read_logs("WARNING")

create_log_system()

# ===================================================================
# 7. 실습 예제들
# ===================================================================

print("\n=== 실습 예제 1: 텍스트 파일 분석기 ===")

def text_file_analyzer():
    """텍스트 파일 분석 도구"""
    
    # 분석용 샘플 텍스트 파일 생성
    sample_text = """Python is a high-level programming language.
It is widely used for web development, data analysis, and artificial intelligence.
Python's syntax is clean and readable, making it perfect for beginners.
Many companies like Google, Netflix, and Instagram use Python.
Learning Python opens up many career opportunities in technology.
Python has a large community and extensive libraries.
Data science and machine learning are popular applications of Python."""

    with open("text_to_analyze.txt", "w", encoding="utf-8") as file:
        file.write(sample_text)
    
    def analyze_text_file(filename):
        """텍스트 파일 분석"""
        try:
            with open(filename, "r", encoding="utf-8") as file:
                content = file.read()
            
            # 기본 통계
            char_count = len(content)
            char_count_no_spaces = len(content.replace(" ", ""))
            word_count = len(content.split())
            line_count = len(content.split("\n"))
            
            # 단어 빈도 분석
            words = content.lower().replace(".", "").replace(",", "").split()
            word_frequency = {}
            for word in words:
                word_frequency[word] = word_frequency.get(word, 0) + 1
            
            # 가장 빈번한 단어들
            sorted_words = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)
            
            # 결과 출력
            print(f"=== '{filename}' 분석 결과 ===")
            print(f"총 문자 수: {char_count}")
            print(f"공백 제외 문자 수: {char_count_no_spaces}")
            print(f"단어 수: {word_count}")
            print(f"줄 수: {line_count}")
            print(f"고유 단어 수: {len(word_frequency)}")
            
            print(f"\n가장 빈번한 단어 (상위 10개):")
            for word, count in sorted_words[:10]:
                print(f"  '{word}': {count}회")
            
            # 분석 결과를 파일로 저장
            analysis_filename = f"{filename}_analysis.txt"
            with open(analysis_filename, "w", encoding="utf-8") as file:
                file.write(f"텍스트 파일 분석 결과\n")
                file.write(f"분석 대상: {filename}\n")
                file.write(f"분석 시간: {datetime.now()}\n")
                file.write(f"="*50 + "\n")
                file.write(f"총 문자 수: {char_count}\n")
                file.write(f"공백 제외 문자 수: {char_count_no_spaces}\n")
                file.write(f"단어 수: {word_count}\n")
                file.write(f"줄 수: {line_count}\n")
                file.write(f"고유 단어 수: {len(word_frequency)}\n\n")
                
                file.write("단어 빈도:\n")
                for word, count in sorted_words:
                    file.write(f"{word}: {count}\n")
            
            print(f"✅ 분석 결과가 '{analysis_filename}'에 저장되었습니다.")
            
        except Exception as e:
            print(f"❌ 파일 분석 오류: {e}")
    
    analyze_text_file("text_to_analyze.txt")

text_file_analyzer()

print("\n=== 실습 예제 2: 데이터 백업 시스템 ===")

def data_backup_system():
    """데이터 백업 및 복원 시스템"""
    
    def create_backup():
        """전체 데이터 백업 생성"""
        try:
            # 백업할 파일들 찾기
            files_to_backup = []
            for file in os.listdir("."):
                if file.endswith(('.txt', '.csv', '.json', '.ini')):
                    files_to_backup.append(file)
            
            if not files_to_backup:
                print("백업할 파일이 없습니다.")
                return
            
            # 백업 메타데이터
            backup_metadata = {
                "backup_time": datetime.now().isoformat(),
                "files": {},
                "total_files": len(files_to_backup)
            }
            
            # 백업 디렉토리 생성
            backup_dir = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.makedirs(backup_dir, exist_ok=True)
            
            # 파일들 백업
            for filename in files_to_backup:
                try:
                    # 파일 정보 수집
                    file_stat = os.stat(filename)
                    file_info = {
                        "size": file_stat.st_size,
                        "modified": datetime.fromtimestamp(file_stat.st_mtime).isoformat(),
                        "backup_path": os.path.join(backup_dir, filename)
                    }
                    
                    # 파일 복사
                    shutil.copy2(filename, os.path.join(backup_dir, filename))
                    backup_metadata["files"][filename] = file_info
                    
                    print(f"✅ {filename} 백업 완료")
                    
                except Exception as e:
                    print(f"❌ {filename} 백업 실패: {e}")
            
            # 백업 메타데이터 저장
            metadata_file = os.path.join(backup_dir, "backup_metadata.json")
            with open(metadata_file, "w", encoding="utf-8") as file:
                json.dump(backup_metadata, file, ensure_ascii=False, indent=2)
            
            print(f"✅ 백업 완료: {backup_dir}")
            print(f"백업된 파일 수: {len(backup_metadata['files'])}")
            
        except Exception as e:
            print(f"❌ 백업 생성 오류: {e}")
    
    def list_backups():
        """사용 가능한 백업 목록 표시"""
        try:
            backup_dirs = [d for d in os.listdir(".") if d.startswith("backup_")]
            
            if not backup_dirs:
                print("사용 가능한 백업들:")
            for i, backup_dir in enumerate(sorted(backup_dirs), 1):
                try:
                    metadata_file = os.path.join(backup_dir, "backup_metadata.json")
                    if os.path.exists(metadata_file):
                        with open(metadata_file, "r", encoding="utf-8") as file:
                            metadata = json.load(file)
                        
                        backup_time = metadata.get("backup_time", "알 수 없음")
                        file_count = metadata.get("total_files", 0)
                        print(f"  {i}. {backup_dir}")
                        print(f"     시간: {backup_time}")
                        print(f"     파일 수: {file_count}")
                    else:
                        print(f"  {i}. {backup_dir} (메타데이터 없음)")
                        
                except Exception as e:
                    print(f"  {i}. {backup_dir} (오류: {e})")
            
            return backup_dirs
            
        except Exception as e:
            print(f"❌ 백업 목록 조회 오류: {e}")
            return []
    
    def restore_backup(backup_dir):
        """백업 복원"""
        try:
            if not os.path.exists(backup_dir):
                print(f"백업 디렉토리 '{backup_dir}'가 존재하지 않습니다.")
                return
            
            metadata_file = os.path.join(backup_dir, "backup_metadata.json")
            if not os.path.exists(metadata_file):
                print("백업 메타데이터를 찾을 수 없습니다.")
                return
            
            # 메타데이터 읽기
            with open(metadata_file, "r", encoding="utf-8") as file:
                metadata = json.load(file)
            
            print(f"백업 복원 중: {backup_dir}")
            print(f"백업 시간: {metadata.get('backup_time')}")
            
            # 파일들 복원
            restored_count = 0
            for filename, file_info in metadata["files"].items():
                try:
                    backup_file_path = os.path.join(backup_dir, filename)
                    if os.path.exists(backup_file_path):
                        # 기존 파일이 있다면 백업 생성
                        if os.path.exists(filename):
                            backup_name = f"{filename}.backup_{datetime.now().strftime('%H%M%S')}"
                            shutil.copy2(filename, backup_name)
                            print(f"  기존 {filename}을 {backup_name}으로 백업")
                        
                        # 파일 복원
                        shutil.copy2(backup_file_path, filename)
                        print(f"✅ {filename} 복원 완료")
                        restored_count += 1
                    else:
                        print(f"❌ {filename} 백업 파일을 찾을 수 없음")
                        
                except Exception as e:
                    print(f"❌ {filename} 복원 실패: {e}")
            
            print(f"✅ 백업 복원 완료: {restored_count}개 파일")
            
        except Exception as e:
            print(f"❌ 백업 복원 오류: {e}")
    
    # 백업 시스템 테스트
    print("데이터 백업 시스템 테스트:")
    
    print("\n1. 백업 생성:")
    create_backup()
    
    print("\n2. 백업 목록:")
    available_backups = list_backups()
    
    print("\n3. 백업 복원 시뮬레이션:")
    if available_backups:
        # 가장 최근 백업 복원 (실제로는 사용자가 선택)
        print(f"최신 백업 '{available_backups[-1]}' 복원 시뮬레이션...")
        # restore_backup(available_backups[-1])  # 실제 복원은 주석 처리

data_backup_system()

print("\n=== 실습 예제 3: 설정 파일 관리자 ===")

def config_file_manager():
    """설정 파일 관리 시스템"""
    
    class ConfigManager:
        def __init__(self, config_file="app_config.json"):
            self.config_file = config_file
            self.config = self.load_config()
        
        def load_config(self):
            """설정 파일 로드"""
            try:
                if os.path.exists(self.config_file):
                    with open(self.config_file, "r", encoding="utf-8") as file:
                        return json.load(file)
                else:
                    # 기본 설정 생성
                    default_config = {
                        "database": {
                            "host": "localhost",
                            "port": 5432,
                            "username": "admin",
                            "password": "secret",
                            "database_name": "myapp"
                        },
                        "application": {
                            "debug": False,
                            "max_users": 1000,
                            "timeout": 30,
                            "log_level": "INFO"
                        },
                        "ui": {
                            "theme": "light",
                            "language": "ko",
                            "auto_save": True
                        }
                    }
                    self.save_config(default_config)
                    return default_config
                    
            except Exception as e:
                print(f"❌ 설정 로드 오류: {e}")
                return {}
        
        def save_config(self, config=None):
            """설정 파일 저장"""
            try:
                config_to_save = config if config else self.config
                with open(self.config_file, "w", encoding="utf-8") as file:
                    json.dump(config_to_save, file, ensure_ascii=False, indent=2)
                print(f"✅ 설정이 {self.config_file}에 저장되었습니다.")
                
            except Exception as e:
                print(f"❌ 설정 저장 오류: {e}")
        
        def get_setting(self, key_path):
            """점 표기법으로 설정값 가져오기 (예: 'database.host')"""
            try:
                keys = key_path.split('.')
                value = self.config
                
                for key in keys:
                    value = value[key]
                
                return value
                
            except KeyError:
                print(f"❌ 설정 키 '{key_path}'를 찾을 수 없습니다.")
                return None
            except Exception as e:
                print(f"❌ 설정 조회 오류: {e}")
                return None
        
        def set_setting(self, key_path, value):
            """점 표기법으로 설정값 변경하기"""
            try:
                keys = key_path.split('.')
                config_ref = self.config
                
                # 마지막 키를 제외하고 경로 따라가기
                for key in keys[:-1]:
                    if key not in config_ref:
                        config_ref[key] = {}
                    config_ref = config_ref[key]
                
                # 마지막 키에 값 설정
                config_ref[keys[-1]] = value
                
                # 변경사항 저장
                self.save_config()
                print(f"✅ '{key_path}' = {value} 설정 완료")
                
            except Exception as e:
                print(f"❌ 설정 변경 오류: {e}")
        
        def print_config(self):
            """전체 설정 출력"""
            print("현재 설정:")
            print(json.dumps(self.config, ensure_ascii=False, indent=2))
        
        def create_backup(self):
            """설정 파일 백업"""
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_filename = f"{self.config_file}.backup_{timestamp}"
                shutil.copy2(self.config_file, backup_filename)
                print(f"✅ 설정 백업 생성: {backup_filename}")
                
            except Exception as e:
                print(f"❌ 설정 백업 오류: {e}")
        
        def validate_config(self):
            """설정 유효성 검사"""
            errors = []
            
            # 데이터베이스 설정 검사
            if "database" in self.config:
                db_config = self.config["database"]
                
                if not isinstance(db_config.get("port"), int):
                    errors.append("데이터베이스 포트는 정수여야 합니다")
                
                if not db_config.get("host"):
                    errors.append("데이터베이스 호스트가 비어있습니다")
                
                if not db_config.get("username"):
                    errors.append("데이터베이스 사용자명이 비어있습니다")
            
            # 애플리케이션 설정 검사
            if "application" in self.config:
                app_config = self.config["application"]
                
                if not isinstance(app_config.get("max_users"), int):
                    errors.append("최대 사용자 수는 정수여야 합니다")
                
                if app_config.get("log_level") not in ["DEBUG", "INFO", "WARNING", "ERROR"]:
                    errors.append("로그 레벨이 유효하지 않습니다")
            
            return errors
    
    # 설정 관리자 테스트
    print("설정 파일 관리자 테스트:")
    
    # 설정 관리자 생성
    config_mgr = ConfigManager()
    
    print("\n1. 초기 설정:")
    config_mgr.print_config()
    
    print("\n2. 설정값 조회:")
    print(f"데이터베이스 호스트: {config_mgr.get_setting('database.host')}")
    print(f"애플리케이션 디버그 모드: {config_mgr.get_setting('application.debug')}")
    print(f"UI 테마: {config_mgr.get_setting('ui.theme')}")
    
    print("\n3. 설정값 변경:")
    config_mgr.set_setting('application.debug', True)
    config_mgr.set_setting('ui.theme', 'dark')
    config_mgr.set_setting('database.port', 3306)
    
    print("\n4. 설정 유효성 검사:")
    validation_errors = config_mgr.validate_config()
    if validation_errors:
        print("설정 오류:")
        for error in validation_errors:
            print(f"  ❌ {error}")
    else:
        print("✅ 모든 설정이 유효합니다.")
    
    print("\n5. 설정 백업:")
    config_mgr.create_backup()

config_file_manager()

print("\n=== 실습 예제 4: 파일 동기화 시스템 ===")

def file_sync_system():
    """간단한 파일 동기화 시스템"""
    
    def calculate_file_hash(filepath):
        """파일의 해시값 계산 (변경 감지용)"""
        import hashlib
        
        try:
            with open(filepath, "rb") as file:
                file_hash = hashlib.md5()
                chunk = file.read(8192)
                while chunk:
                    file_hash.update(chunk)
                    chunk = file.read(8192)
                return file_hash.hexdigest()
                
        except Exception as e:
            print(f"❌ 해시 계산 오류: {e}")
            return None
    
    def create_file_index(directory):
        """디렉토리의 파일 인덱스 생성"""
        file_index = {}
        
        try:
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                
                if os.path.isfile(filepath):
                    stat_info = os.stat(filepath)
                    file_hash = calculate_file_hash(filepath)
                    
                    file_index[filename] = {
                        "size": stat_info.st_size,
                        "modified": stat_info.st_mtime,
                        "hash": file_hash
                    }
            
            return file_index
            
        except Exception as e:
            print(f"❌ 파일 인덱스 생성 오류: {e}")
            return {}
    
    def save_file_index(index, index_file):
        """파일 인덱스를 JSON 파일로 저장"""
        try:
            with open(index_file, "w", encoding="utf-8") as file:
                json.dump(index, file, ensure_ascii=False, indent=2)
            
        except Exception as e:
            print(f"❌ 인덱스 저장 오류: {e}")
    
    def load_file_index(index_file):
        """저장된 파일 인덱스 로드"""
        try:
            if os.path.exists(index_file):
                with open(index_file, "r", encoding="utf-8") as file:
                    return json.load(file)
            else:
                return {}
                
        except Exception as e:
            print(f"❌ 인덱스 로드 오류: {e}")
            return {}
    
    def detect_changes(old_index, new_index):
        """파일 변경사항 감지"""
        changes = {
            "added": [],      # 새로 추가된 파일
            "modified": [],   # 수정된 파일
            "deleted": []     # 삭제된 파일
        }
        
        # 새로 추가되거나 수정된 파일 확인
        for filename, file_info in new_index.items():
            if filename not in old_index:
                changes["added"].append(filename)
            elif old_index[filename]["hash"] != file_info["hash"]:
                changes["modified"].append(filename)
        
        # 삭제된 파일 확인
        for filename in old_index:
            if filename not in new_index:
                changes["deleted"].append(filename)
        
        return changes
    
    # 동기화 시스템 테스트
    print("파일 동기화 시스템 테스트:")
    
    # 테스트 디렉토리 생성
    test_sync_dir = "sync_test"
    if not os.path.exists(test_sync_dir):
        os.makedirs(test_sync_dir)
    
    # 테스트 파일들 생성
    test_files = {
        "document1.txt": "첫 번째 문서 내용",
        "document2.txt": "두 번째 문서 내용",
        "config.txt": "설정 파일 내용"
    }
    
    for filename, content in test_files.items():
        filepath = os.path.join(test_sync_dir, filename)
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)
    
    # 초기 인덱스 생성
    print(f"\n1. 초기 파일 인덱스 생성:")
    initial_index = create_file_index(test_sync_dir)
    index_file = os.path.join(test_sync_dir, "file_index.json")
    save_file_index(initial_index, index_file)
    
    print(f"초기 파일 수: {len(initial_index)}")
    for filename in initial_index:
        print(f"  📄 {filename}")
    
    # 파일 변경 시뮬레이션
    print(f"\n2. 파일 변경 시뮬레이션:")
    
    # 파일 수정
    modified_file = os.path.join(test_sync_dir, "document1.txt")
    with open(modified_file, "w", encoding="utf-8") as file:
        file.write("첫 번째 문서의 수정된 내용")
    print("  ✏️ document1.txt 수정됨")
    
    # 새 파일 추가
    new_file = os.path.join(test_sync_dir, "new_document.txt")
    with open(new_file, "w", encoding="utf-8") as file:
        file.write("새로 추가된 문서")
    print("  ➕ new_document.txt 추가됨")
    
    # 파일 삭제
    deleted_file = os.path.join(test_sync_dir, "config.txt")
    os.remove(deleted_file)
    print("  🗑️ config.txt 삭제됨")
    
    # 변경사항 감지
    print(f"\n3. 변경사항 감지:")
    current_index = create_file_index(test_sync_dir)
    old_index = load_file_index(index_file)
    changes = detect_changes(old_index, current_index)
    
    if changes["added"]:
        print(f"  ➕ 추가된 파일: {changes['added']}")
    
    if changes["modified"]:
        print(f"  ✏️ 수정된 파일: {changes['modified']}")
    
    if changes["deleted"]:
        print(f"  🗑️ 삭제된 파일: {changes['deleted']}")
    
    if not any(changes.values()):
        print("  변경사항이 없습니다.")
    
    # 새 인덱스 저장
    save_file_index(current_index, index_file)
    print(f"\n✅ 파일 인덱스가 업데이트되었습니다.")

file_sync_system()

# ===================================================================
# 8. 고급 파일 처리 기법
# ===================================================================

print("\n=== 고급 파일 처리 기법 ===")

def advanced_file_techniques():
    """고급 파일 처리 기법들"""
    
    # 1. 대용량 파일 처리
    def process_large_file(filename, chunk_size=1024):
        """대용량 파일을 청크 단위로 처리"""
        try:
            with open(filename, "r", encoding="utf-8") as file:
                chunk_count = 0
                while True:
                    chunk = file.read(chunk_size)
                    if not chunk:
                        break
                    
                    chunk_count += 1
                    # 여기서 청크를 처리 (예: 단어 수 세기, 패턴 찾기 등)
                    
                print(f"파일이 {chunk_count}개 청크로 처리되었습니다.")
                
        except Exception as e:
            print(f"❌ 대용량 파일 처리 오류: {e}")
    
    # 2. 파일 압축 및 해제
    def compress_files():
        """파일들을 압축"""
        import zipfile
        
        try:
            files_to_compress = ["sample.txt", "students.csv"]
            
            with zipfile.ZipFile("archive.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
                for filename in files_to_compress:
                    if os.path.exists(filename):
                        zipf.write(filename)
                        print(f"  📦 {filename} 압축됨")
            
            print("✅ 파일 압축 완료: archive.zip")
            
        except Exception as e:
            print(f"❌ 파일 압축 오류: {e}")
    
    def extract_files():
        """압축 파일 해제"""
        import zipfile
        
        try:
            extract_dir = "extracted"
            
            with zipfile.ZipFile("archive.zip", "r") as zipf:
                zipf.extractall(extract_dir)
                extracted_files = zipf.namelist()
                
                print(f"✅ 파일 해제 완료: {extract_dir}/")
                for filename in extracted_files:
                    print(f"  📄 {filename}")
                    
        except Exception as e:
            print(f"❌ 파일 해제 오류: {e}")
    
    # 3. 임시 파일 사용
    def use_temporary_files():
        """임시 파일 사용 예제"""
        import tempfile
        
        try:
            # 임시 파일 생성
            with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as temp_file:
                temp_filename = temp_file.name
                temp_file.write("임시 파일의 내용입니다.")
                temp_file.write("\n이 파일은 임시로 생성되었습니다.")
            
            print(f"✅ 임시 파일 생성: {temp_filename}")
            
            # 임시 파일 읽기
            with open(temp_filename, "r") as temp_file:
                content = temp_file.read()
                print(f"임시 파일 내용:\n{content}")
            
            # 임시 파일 삭제
            os.remove(temp_filename)
            print(f"✅ 임시 파일 삭제됨")
            
        except Exception as e:
            print(f"❌ 임시 파일 처리 오류: {e}")
    
    # 4. 파일 락킹 (간단한 버전)
    def file_locking_example():
        """파일 락킹 예제"""
        lock_file = "process.lock"
        
        try:
            # 락 파일 확인
            if os.path.exists(lock_file):
                print("❌ 다른 프로세스가 실행 중입니다.")
                return
            
            # 락 파일 생성
            with open(lock_file, "w") as lock:
                lock.write(f"프로세스 시작: {datetime.now()}")
            
            print("🔒 프로세스 락 획득")
            
            # 실제 작업 시뮬레이션
            import time
            time.sleep(1)
            print("💼 중요한 작업 수행 중...")
            
            # 락 파일 삭제
            os.remove(lock_file)
            print("🔓 프로세스 락 해제")
            
        except Exception as e:
            print(f"❌ 파일 락킹 오류: {e}")
            # 락 파일이 남아있다면 삭제
            if os.path.exists(lock_file):
                os.remove(lock_file)
    
    # 고급 기법들 테스트
    print("고급 파일 처리 기법 테스트:")
    
    print("\n1. 파일 압축:")
    compress_files()
    
    print("\n2. 파일 해제:")
    extract_files()
    
    print("\n3. 임시 파일 사용:")
    use_temporary_files()
    
    print("\n4. 파일 락킹:")
    file_locking_example()

advanced_file_techniques()

print("\n=== 11단계 완료! ===")
print("파일 입출력을 모두 배웠습니다.")
print("다음 단계에서는 모듈과 패키지를 배워보겠습니다!")

# ===================================================================
# 추가 팁
# ===================================================================

"""
11단계에서 기억해야 할 중요한 점들:

1. 파일 처리 기본:
   - with 문 사용으로 안전한 파일 처리
   - 인코딩 지정 (encoding="utf-8")
   - 예외 처리로 견고한 파일 작업

2. 파일 모드:
   - "r": 읽기, "w": 쓰기, "a": 추가
   - "b": 바이너리 모드
   - "x": 배타적 생성 (파일이 이미 있으면 실패)

3. 다양한 파일 형식:
   - 텍스트 파일: 일반적인 텍스트 데이터
   - CSV 파일: 표 형태 데이터, csv 모듈 활용
   - JSON 파일: 구조화된 데이터, json 모듈 활용

4. 파일 시스템 작업:
   - os 모듈: 파일/디렉토리 존재 확인, 정보 조회
   - shutil 모듈: 파일 복사, 이동, 삭제
   - pathlib 모듈: 경로 처리 (Python 3.4+)

5. 성능 고려사항:
   - 대용량 파일은 청크 단위로 처리
   - 메모리 사용량 고려
   - 파일 락킹으로 동시 접근 제어

6. 보안 고려사항:
   - 사용자 입력으로 파일 경로 만들 때 검증
   - 파일 권한 확인
   - 임시 파일 안전하게 처리

실습할 때 꼭 해보세요:
- 다양한 파일 형식 읽기/쓰기
- CSV와 JSON 데이터 처리
- 파일 백업/복원 시스템 구현
- 로그 파일 분석
- 설정 파일 관리 시스템
- 대용량 파일 처리 최적화
"""
