import module_a

def start_program():
    print("main.py: start_program 호출됨")
    module_a.function_a1()
    module_a.function_b1(5)
    
    # try:
    #     module_a.function_b1(5)
    # except Exception as e:
    #     print("[main.py] 예외 발생:", type(e).__name__, "-", e)
        
if __name__ == '__main__':
    start_program()
