# 1. defaultdict 사용
# defaultdict는 collections 모듈에서 제공하는 딕셔너리의 서브 클래스입니다. 기본값이 자동으로 할당된다는 점이 일반 딕셔너리와 다릅니다.

from collections import defaultdict

# defaultdict 생성
dd = defaultdict(int)
dd['a'] += 1
dd['b'] += 2
print(dd)  # defaultdict(<class 'int'>, {'a': 1, 'b': 2})

# defaultdict 기본값 설정
dd = defaultdict(lambda: "default_value")
print(dd['a'])  # default_value
print(dd['b'])  # default_value
print(dd)  # defaultdict(<function <lambda> at 0x...>, {'a': 'default_value', 'b': 'default_value'})


# 2. Counter 사용
# Counter는 collections 모듈에서 제공하는 딕셔너리의 서브 클래스입니다. 해시 가능한 객체를 세는 데 유용합니다.

from collections import Counter

# Counter 생성
counter = Counter(['a', 'b', 'c', 'a', 'b', 'a'])
print(counter)  # Counter({'a': 3, 'b': 2, 'c': 1})

# 요소 개수 추가
counter.update(['a', 'b', 'd'])
print(counter)  # Counter({'a': 4, 'b': 3, 'c': 1, 'd': 1})

# 가장 흔한 요소 찾기
print(counter.most_common(2))  # [('a', 4), ('b', 3)]


# 3. OrderedDict 사용
# OrderedDict는 collections 모듈에서 제공하며, 삽입된 순서대로 항목을 기억하는 딕셔너리입니다.

from collections import OrderedDict

# OrderedDict 생성
od = OrderedDict()
od['a'] = 1
od['b'] = 2
od['c'] = 3
print(od)  # OrderedDict([('a', 1), ('b', 2), ('c', 3)])

# 삽입된 순서 유지
for key, value in od.items():
    print(f"{key}: {value}")
# 출력:
# a: 1
# b: 2
# c: 3
