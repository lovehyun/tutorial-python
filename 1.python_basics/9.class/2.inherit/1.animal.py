class Animal:
    def speak(self):
        print("This animal makes a sound.")

class Dog(Animal):
    def speak(self):
        print("The dog barks.")

class Cat(Animal):
    def speak(self):
        print("The cat meows.")

animals = [Dog(), Cat(), Animal()]

for animal in animals:
    animal.speak()
