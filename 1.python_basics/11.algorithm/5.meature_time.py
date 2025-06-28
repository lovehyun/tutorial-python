import time

def my_function():
    # 여기에 측정하고 싶은 코드를 작성합니다.
    for i in range(1000000):
        pass

start_time = time.time()
my_function()
end_time = time.time()

execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")


import timeit

def my_function():
    num = 0
    # 여기에 측정하고 싶은 코드를 작성합니다.
    for i in range(1_000_000):
        num *= i
        pass

execution_time = timeit.timeit(my_function, number=10)
print(f"Execution time: {execution_time} seconds")

