class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        """스택에 항목 추가"""
        self.items.append(item)

    def pop(self):
        """스택에서 항목 제거 및 반환"""
        if not self.is_empty():
            return self.items.pop()
        return None

    def peek(self):
        """스택의 최상단 항목 조회 (제거하지 않음)"""
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self):
        """스택이 비었는지 여부 확인"""
        return len(self.items) == 0

    def size(self):
        """스택의 크기 반환"""
        return len(self.items)

    def __str__(self):
        return f"Stack(bottom → top): {self.items}"

class Browser:
    def __init__(self):
        self.history = Stack()  # 뒤로가기용 스택
        self.current_page = None

    def visit(self, url):
        """새로운 웹 페이지 방문"""
        if self.current_page:
            self.history.push(self.current_page)
        self.current_page = url
        print(f"현재 페이지: {self.current_page}")

    def back(self):
        """뒤로 가기"""
        if self.history.is_empty():
            print("더 이상 뒤로 갈 수 없습니다.")
            return
        self.current_page = self.history.pop()
        print(f"🔙 뒤로 이동 → 현재 페이지: {self.current_page}")

    def show_history(self):
        print(f"방문 기록: {self.history}")
        print(f"현재 페이지: {self.current_page}")


# 테스트
browser = Browser()
browser.visit("google.com")
browser.visit("naver.com")
browser.visit("youtube.com")

browser.show_history()
# 방문 기록: ['google.com', 'naver.com']
# 현재 페이지: youtube.com

browser.back()  # youtube → naver
browser.back()  # naver → google
browser.back()  # 더 이상 없음

browser.show_history()
