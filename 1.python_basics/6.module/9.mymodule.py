# mymodule.py
def greet(name):
    return f"Hello, {name}!"


# 다른 파일에서...
# # main.py
# import mymodule
# import mymodule as mm
# from mymodule import greet
# from mymodule import greet as gt

# # mymodule의 greet 함수 호출
# greeting = mymodule.greet("Alice")
# print(greeting)
