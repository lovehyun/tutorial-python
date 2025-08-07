import time
import threading

class Queue:
    def __init__(self):
        self.items = []
        self.lock = threading.Lock()  # 큐 접근 동기화

    def enqueue(self, item):
        with self.lock:
            self.items.append(item)

    def dequeue(self):
        with self.lock:
            if self.items:
                return self.items.pop(0)
            return None

    def peek(self):
        with self.lock:
            return self.items[0] if self.items else None

    def is_empty(self):
        with self.lock:
            return len(self.items) == 0

    def __str__(self):
        with self.lock:
            return f"Queue(front → back): {self.items[:]}"

# 프린터 작업 처리 쓰레드 (2초 소요)
def printer_worker(printer_queue):
    while True:
        if not printer_queue.is_empty():
            job = printer_queue.dequeue()
            print(f"[처리 시작] {job}")
            time.sleep(3)  # 인쇄 작업 시간
            print(f"[처리 완료] {job}")
        else:
            time.sleep(0.1)  # 큐가 비었으면 잠깐 쉼

# 큐 상태 확인 루프 (1초마다 확인)
def monitor_worker(printer_queue):
    while True:
        print(f"[대기열 상태 확인] {printer_queue}")
        time.sleep(1)

# 실행
if __name__ == "__main__":
    printer_queue = Queue()

    # 작업 추가
    printer_queue.enqueue("문서1.pdf")
    printer_queue.enqueue("문서2.docx")
    printer_queue.enqueue("사진.png")
    printer_queue.enqueue("이력서.pdf")

    # 백그라운드 스레드 시작
    threading.Thread(target=printer_worker, args=(printer_queue,), daemon=True).start()
    threading.Thread(target=monitor_worker, args=(printer_queue,), daemon=True).start()

    # 메인 스레드는 대기
    while True:
        time.sleep(10)
