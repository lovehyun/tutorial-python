def function_a1():
    print("module_a.py: function_a1 호출됨")
    function_a2()

def function_a2():
    print("module_a.py: function_a2 호출됨")
    function_a3()

def function_a3():
    print("module_a.py: function_a3 호출됨")
    helper_function()

def helper_function():
    print("module_a.py: helper_function 호출됨")
    deep_call_1()

def deep_call_1():
    print("module_a.py: deep_call_1 호출됨")
    deep_call_2()

def deep_call_2():
    print("module_a.py: deep_call_2 호출됨")
    raise RuntimeError("🔥 의도적으로 예외를 발생시킵니다!")

def function_b1(value: int):
    print("module_a.py: function_b1 호출됨")
    function_b2(value + 10)

def function_b2(value: int):
    print("module_a.py: function_b2 호출됨")
    function_b3(value * 2)

def function_b3(value: int):
    print("module_a.py: function_b3 호출됨")
    wrong_value = str(value)
    result = wrong_value * "x"
    print("최종 계산 결과:", result)
