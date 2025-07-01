from person import Person

class Employee(Person):
    def __init__(self, name, age, company):
        super().__init__(name, age)
        self._company = company

    def greet(self):  # 메서드 오버라이딩
        print(f"Hello, my name is {self.name}, I work at {self._company}.")

    def work(self):
        print(f"Employee {self.name} is working at {self._company}")
