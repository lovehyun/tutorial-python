#                    +------------------+
#                    |      Person      |
#                    |------------------|
#                    |  - name          |
#                    |  - age           |
#                    |------------------|
#                    |  + greet()       |
#                    +---------+--------+
#                              |
#         +--------------------+--------------------+
#         |                    |                    |
# +---------------+    +---------------+    +---------------+
# |    Driver     |    |   Employee    |    |    Student    |
# |---------------|    |---------------|    |---------------|
# | - license_type|    | - company     |    |  - student_id |
# |---------------|    |---------------|    |---------------|
# | + drive()     |    | + work()      |    | + study()     |
# +---------------+    +---------------+    +---------------+

class Person:
    def __init__(self, name, age):
        self._name = name
        self._age = age

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if value >= 0:
            self._age = value
        else:
            print("[Error] 나이는 0 이상이어야 합니다!")

    def greet(self):
        print(f"Hello, my name is {self._name} and I am {self._age} years old.")
