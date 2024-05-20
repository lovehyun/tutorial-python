from person import Person
from car import Car

# Person과 Car 클래스의 인스턴스 생성
person = Person("Alice", 30)
car = Car("Audi", "A4")

# 사람이 차에 타는 것을 표현
person.ride_car(car)

# 차의 주행 거리를 100 미터 증가시킴
car.increment_odometer(100)

# 차의 주행 거리를 50 미터 증가시킴
car.increment_odometer(50)

# 현재 주행 거리 출력
car.read_odometer()
