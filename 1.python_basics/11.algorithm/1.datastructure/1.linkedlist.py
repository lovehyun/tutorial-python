class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    # 맨 뒤에 추가
    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = new_node

    # 출력
    def print_list(self):
        cur = self.head
        while cur:
            print(cur.data, end=" -> ")
            cur = cur.next
        print("None")


# 테스트
ll = LinkedList()
ll.append(10)
ll.append(20)
ll.append(30)
ll.print_list()
# 출력: 10 -> 20 -> 30 -> None
