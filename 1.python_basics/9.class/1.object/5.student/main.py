from student import Student
from employee import Employee
from driver import Driver

# Student 테스트
student = Student("Tom", 20, "S1234")
student.greet()
student.study()

print()

# Employee 테스트
employee = Employee("Jane", 28, "CompanyA")
employee.greet()
employee.work()

print()

# Driver 테스트
driver = Driver("Bob", 40, "Type A")
driver.greet()
driver.drive()
