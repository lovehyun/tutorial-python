from driver import Driver
from car import Car

# Driver와 Car 객체 생성
driver = Driver("Bob", 40, "Type A")
car = Car("Hyundai", "Sonata")

# 차량 소유
driver.assign_car(car)

# 차량 주행
driver.drive(50)
driver.drive(100)

# 차량 주행 거리 직접 확인
car.read_odometer()

driver.drive(30)
car.read_odometer()
