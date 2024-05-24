# exception 구조
https://docs.python.org/3/library/exceptions.html#exception-hierarchy

# exception 블록의 역할
1. try 블록: 이 블록 내의 코드는 예외가 발생할 수 있는 코드입니다. 예외가 발생하면 실행이 즉시 except 블록으로 넘어갑니다.
2. except 블록: try 블록에서 예외가 발생하면 이 블록이 실행됩니다. 발생한 예외를 처리하는 코드를 작성합니다.
3. else 블록: try 블록이 성공적으로 완료되었을 때 (즉, 예외가 발생하지 않았을 때) 실행됩니다. 예외가 발생하지 않은 경우에만 실행됩니다.
4. finally 블록: 예외 발생 여부에 상관없이 항상 실행됩니다. 자원을 해제하거나 정리하는 코드를 작성할 때 유용합니다.


```python
def divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError as e:
        print(f"예외 발생: {e}")
    else:
        print(f"결과: {result}")
    finally:
        print("이 문장은 항상 실행됩니다.")

# 예제 1: 예외가 발생하지 않는 경우
divide(10, 2)
# 출력:
# 결과: 5.0
# 이 문장은 항상 실행됩니다.

# 예제 2: 예외가 발생하는 경우
divide(10, 0)
# 출력:
# 예외 발생: division by zero
# 이 문장은 항상 실행됩니다.
```
