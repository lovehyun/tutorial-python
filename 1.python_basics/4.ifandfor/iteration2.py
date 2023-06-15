import time

def nested_loops_example():
    n = 10
    count = 0

    for i in range(n):  # O(n)
        for j in range(n):  # O(n)
            for k in range(n):  # O(n)
                for l in range(n):  # O(n)
                    count += 1

    return count

# 실행 시간 측정
start_time = time.time()

result = nested_loops_example()

end_time = time.time()

execution_time = end_time - start_time


print("Result:", result)
print("Execution Time:", execution_time, "seconds")
