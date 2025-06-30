# Animal 클래스 (부모 클래스)
class Animal:
    def speak(self):
        # 부모 클래스의 기본 동작 (자식 클래스에서 오버라이딩할 예정)
        print("This animal makes a sound.")

# Dog 클래스 (Animal을 상속받음)
class Dog(Animal):
    def speak(self):
        # 부모의 speak 메서드를 오버라이딩 (재정의)
        print("The dog barks.")

# Cat 클래스 (Animal을 상속받음)
class Cat(Animal):
    def speak(self):
        # 부모의 speak 메서드를 오버라이딩 (재정의)
        print("The cat meows.")

# Dog, Cat, Animal 객체를 리스트로 생성 (다형성)
# **다형성 (Polymorphism)**은 "하나의 코드가 여러 객체에서 서로 다르게 동작하는 것".
animals = [Dog(), Cat(), Animal()]

# 각 동물 객체의 speak 메서드 호출
for animal in animals:
    animal.speak()  # 각 클래스에서 오버라이딩된 메서드가 호출됨
