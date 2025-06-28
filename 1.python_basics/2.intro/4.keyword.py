import keyword

# 모든 키워드 목록 출력
print(keyword.kwlist)

# 키워드 개수 확인
print(len(keyword.kwlist))

# 특정 단어가 키워드인지 확인
print(keyword.iskeyword('if'))    # True
print(keyword.iskeyword('hello')) # False


# 키워드에 대한 도움말
help('keywords')

# 또는 간단히
help()


# 총 35개의 키워드
# 1. 제어 구조:
# if, elif, else - 조건문
# for, while - 반복문
# break, continue - 반복문 제어
# pass - 빈 블록
#
# 2. 함수 및 클래스:
# def - 함수 정의
# class - 클래스 정의
# return - 값 반환
# yield - 제너레이터
#
# 3. 예외 처리:
# try, except, finally - 예외 처리
# raise - 예외 발생
#
# 논리 연산자:
# 4. and, or, not - 논리 연산
#
# 5. 값과 상수:
# True, False - 불린 값
# None - 빈 값
#
# 6. 모듈 관련:
# import, from, as - 모듈 가져오기
#
# 7. 변수 관련:
# global, nonlocal - 변수 범위 지정
# del - 객체 삭제
#
# 8. 기타:
# in - 멤버십 연산자
# is - 동일성 연산자
# lambda - 익명 함수
# with - 컨텍스트 매니저
# assert - 어서션
