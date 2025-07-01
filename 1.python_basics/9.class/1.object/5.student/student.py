from person import Person

class Student(Person):
    def __init__(self, name, age, student_id):
        super().__init__(name, age)
        self._student_id = student_id

    def study(self):
        print(f"{self.name} is studying. (ID: {self._student_id})")
