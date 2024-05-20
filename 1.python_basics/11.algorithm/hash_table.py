# 해시 테이블(Hash Table) 검색
class HashTable:
    def __init__(self):
        self.table = [None] * 10

    def hash_func(self, key):
        return key % 10

    def insert(self, key, value):
        index = self.hash_func(key)
        self.table[index] = value

    def search(self, key):
        index = self.hash_func(key)
        return self.table[index]

# 해시 테이블 사용 예제
hash_table = HashTable()
hash_table.insert(5, "Apple")
hash_table.insert(2, "Banana")
hash_table.insert(9, "Cherry")

key = 2
result = hash_table.search(key)
if result is not None:
    print("키 {}에 해당하는 값: {}".format(key, result))
else:
    print("키 {}에 해당하는 값이 없습니다.".format(key))
