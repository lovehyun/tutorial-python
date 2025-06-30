# 기본 생성자
# 메서드
# getter & setter

# 항목                  설명
# __name, __age	        클래스 내부에서만 접근 가능한 private 변수
# get_name, get_age	    값을 읽어오는 getter 메서드
# set_name, set_age	    값을 수정하는 setter 메서드 (검증 포함)
# greet	                단순 출력 메서드

# 목적	            설명
# 데이터 보호	    객체의 속성을 직접 수정하지 못하게 막고, 제어권을 가짐
# 값 검증	        setter에서 잘못된 값을 거를 수 있음 (ex: 나이는 음수가 되면 안 된다)
# 유지보수 편리	    객체 사용법이 바뀌어도 getter/setter 안에서 수정하면 코드 전체가 안 깨짐
# 캡슐화    	    객체지향의 핵심 원칙, 데이터를 안전하게 관리하는 구조


# 직접 접근 비추천
# - person.age = -5  # 누구나 직접 수정할 수 있음 → 데이터 깨짐
#
# getter/setter 사용 추천
# - getter는 값을 읽기만 가능하게 함 (데이터 보호)
# - setter는 값을 변경할 수 있지만, 검증 후에만 허용
# - 외부에서 함부로 값을 바꾸지 못함. 잘못된 데이터 저장을 막음.

class Person:
    def __init__(self, name, age):
        self.__name = name    # private 변수
        self.__age = age      # private 변수
    
    def greet(self):
        print(f"Hello, my name is {self.__name} and I am {self.__age} years old.")
    
    # getter (이름)
    def get_name(self):
        return self.__name

    # setter (이름)
    def set_name(self, name):
        self.__name = name

    # getter (나이)
    def get_age(self):
        return self.__age

    # setter (나이)
    def set_age(self, age):
        if age >= 0:  # 나이는 음수가 될 수 없으니 예외 처리
            self.__age = age
        else:
            print("[Error] 나이는 0 이상이어야 합니다!")

if __name__ == "__main__":
    # 인스턴스 생성
    person1 = Person("Alice", 30)

    # 메서드 호출
    person1.greet()

    # getter 사용
    print("이름:", person1.get_name())
    print("나이:", person1.get_age())

    # setter 사용
    person1.set_name("Alicia")
    person1.set_age(35)

    # 변경 후 확인
    person1.greet()

    # 잘못된 값 입력
    person1.set_age(-5)  # 나이는 음수가 될 수 없으니 에러 출력
