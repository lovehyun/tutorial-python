import datetime
import json
import os

class TodoManager:
    def __init__(self):
        self.todos = []
        self.next_id = 1
        self.filename = "todos.json"
        self.load_todos()
    
    def add_todo(self, task, priority="normal", due_date=None):
        """
        새로운 할 일 추가
        """
        todo = {
            'id': self.next_id,
            'task': task,
            'completed': False,
            'priority': priority,
            'due_date': due_date,
            'created_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        self.todos.append(todo)
        self.next_id += 1
        print(f"✅ '{task}' 할 일이 추가되었습니다!")
    
    def list_todos(self, show_completed=True):
        """
        할 일 목록 출력
        """
        if not self.todos:
            print("📝 등록된 할 일이 없습니다.")
            return
        
        print("\n" + "="*60)
        print("📋 TODO 리스트")
        print("="*60)
        
        # 우선순위별로 정렬
        priority_order = {'high': 1, 'normal': 2, 'low': 3}
        sorted_todos = sorted(self.todos, key=lambda x: priority_order.get(x['priority'], 2))
        
        for todo in sorted_todos:
            if not show_completed and todo['completed']:
                continue
                
            # 상태 표시
            status = "✅" if todo['completed'] else "❌"
            
            # 우선순위 표시
            priority_symbols = {'high': '🔥', 'normal': '📌', 'low': '💤'}
            priority_symbol = priority_symbols.get(todo['priority'], '📌')
            
            # 마감일 표시
            due_info = ""
            if todo['due_date']:
                due_info = f" (마감: {todo['due_date']})"
                # 마감일이 지났는지 확인
                try:
                    due_date = datetime.datetime.strptime(todo['due_date'], "%Y-%m-%d").date()
                    today = datetime.date.today()
                    if due_date < today and not todo['completed']:
                        due_info += " ⚠️ 지연"
                except ValueError:
                    pass
            
            print(f"{todo['id']:2d}. {status} {priority_symbol} {todo['task']}{due_info}")
        
        print("="*60)
    
    def complete_todo(self, todo_id):
        """
        할 일 완료 처리
        """
        todo = self.find_todo_by_id(todo_id)
        if todo:
            if todo['completed']:
                print(f"❌ ID {todo_id}번 할 일은 이미 완료되었습니다.")
            else:
                todo['completed'] = True
                todo['completed_at'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                print(f"🎉 '{todo['task']}' 할 일을 완료했습니다!")
        else:
            print(f"❌ ID {todo_id}번 할 일을 찾을 수 없습니다.")
    
    def uncomplete_todo(self, todo_id):
        """
        할 일 완료 취소
        """
        todo = self.find_todo_by_id(todo_id)
        if todo:
            if not todo['completed']:
                print(f"❌ ID {todo_id}번 할 일은 완료되지 않은 상태입니다.")
            else:
                todo['completed'] = False
                if 'completed_at' in todo:
                    del todo['completed_at']
                print(f"🔄 '{todo['task']}' 할 일을 미완료로 변경했습니다.")
        else:
            print(f"❌ ID {todo_id}번 할 일을 찾을 수 없습니다.")
    
    def delete_todo(self, todo_id):
        """
        할 일 삭제
        """
        todo = self.find_todo_by_id(todo_id)
        if todo:
            task_name = todo['task']
            self.todos.remove(todo)
            print(f"🗑️ '{task_name}' 할 일이 삭제되었습니다.")
        else:
            print(f"❌ ID {todo_id}번 할 일을 찾을 수 없습니다.")
    
    def edit_todo(self, todo_id, new_task=None, new_priority=None, new_due_date=None):
        """
        할 일 수정
        """
        todo = self.find_todo_by_id(todo_id)
        if todo:
            old_task = todo['task']
            
            if new_task:
                todo['task'] = new_task
            if new_priority:
                todo['priority'] = new_priority
            if new_due_date:
                todo['due_date'] = new_due_date
                
            print(f"✏️ '{old_task}' 할 일이 수정되었습니다.")
        else:
            print(f"❌ ID {todo_id}번 할 일을 찾을 수 없습니다.")
    
    def find_todo_by_id(self, todo_id):
        """
        ID로 할 일 찾기
        """
        for todo in self.todos:
            if todo['id'] == todo_id:
                return todo
        return None
    
    def search_todos(self, keyword):
        """
        할 일 검색
        """
        found_todos = [todo for todo in self.todos if keyword.lower() in todo['task'].lower()]
        
        if not found_todos:
            print(f"🔍 '{keyword}'와 관련된 할 일을 찾을 수 없습니다.")
            return
        
        print(f"\n🔍 '{keyword}' 검색 결과:")
        print("-" * 40)
        for todo in found_todos:
            status = "✅" if todo['completed'] else "❌"
            print(f"{todo['id']:2d}. {status} {todo['task']}")
    
    def show_statistics(self):
        """
        통계 정보 출력
        """
        total = len(self.todos)
        completed = len([todo for todo in self.todos if todo['completed']])
        pending = total - completed
        
        if total == 0:
            completion_rate = 0
        else:
            completion_rate = (completed / total) * 100
        
        print("\n" + "="*40)
        print("📊 TODO 통계")
        print("="*40)
        print(f"전체 할 일: {total}개")
        print(f"완료: {completed}개")
        print(f"미완료: {pending}개")
        print(f"완료율: {completion_rate:.1f}%")
        
        # 우선순위별 통계
        high_priority = len([todo for todo in self.todos if todo['priority'] == 'high'])
        normal_priority = len([todo for todo in self.todos if todo['priority'] == 'normal'])
        low_priority = len([todo for todo in self.todos if todo['priority'] == 'low'])
        
        print(f"\n우선순위별:")
        print(f"🔥 높음: {high_priority}개")
        print(f"📌 보통: {normal_priority}개")
        print(f"💤 낮음: {low_priority}개")
        print("="*40)
    
    def clear_completed(self):
        """
        완료된 할 일들 모두 삭제
        """
        completed_todos = [todo for todo in self.todos if todo['completed']]
        
        if not completed_todos:
            print("❌ 완료된 할 일이 없습니다.")
            return
        
        self.todos = [todo for todo in self.todos if not todo['completed']]
        print(f"🗑️ {len(completed_todos)}개의 완료된 할 일을 삭제했습니다.")
    
    def save_todos(self):
        """
        할 일 목록을 파일에 저장
        """
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump({
                    'todos': self.todos,
                    'next_id': self.next_id
                }, f, ensure_ascii=False, indent=2)
            print("💾 할 일 목록이 저장되었습니다.")
        except Exception as e:
            print(f"❌ 저장 중 오류가 발생했습니다: {e}")
    
    def load_todos(self):
        """
        파일에서 할 일 목록 불러오기
        """
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.todos = data.get('todos', [])
                    self.next_id = data.get('next_id', 1)
                print("📂 저장된 할 일 목록을 불러왔습니다.")
            else:
                print("📝 새로운 TODO 리스트를 시작합니다.")
        except Exception as e:
            print(f"❌ 불러오기 중 오류가 발생했습니다: {e}")
            self.todos = []
            self.next_id = 1

def show_menu():
    """
    메뉴 출력
    """
    print("\n" + "="*50)
    print("📋 TODO 리스트 관리자")
    print("="*50)
    print("1. 할 일 추가")
    print("2. 할 일 목록 보기")
    print("3. 할 일 완료 처리")
    print("4. 할 일 완료 취소")
    print("5. 할 일 수정")
    print("6. 할 일 삭제")
    print("7. 할 일 검색")
    print("8. 통계 보기")
    print("9. 완료된 할 일 모두 삭제")
    print("10. 저장")
    print("0. 종료")
    print("-" * 50)

def get_priority():
    """
    우선순위 입력받기
    """
    while True:
        priority = input("우선순위 (high/normal/low, 기본값: normal): ").lower()
        if priority in ['high', 'normal', 'low', '']:
            return priority if priority else 'normal'
        else:
            print("❌ high, normal, low 중 하나를 입력해주세요.")

def get_due_date():
    """
    마감일 입력받기
    """
    while True:
        due_date = input("마감일 (YYYY-MM-DD 형식, 없으면 엔터): ")
        if not due_date:
            return None
        
        try:
            datetime.datetime.strptime(due_date, "%Y-%m-%d")
            return due_date
        except ValueError:
            print("❌ 올바른 날짜 형식(YYYY-MM-DD)으로 입력해주세요.")

def main():
    """
    메인 함수
    """
    todo_manager = TodoManager()
    
    print("🎉 TODO 리스트 프로그램에 오신 것을 환영합니다!")
    
    while True:
        show_menu()
        choice = input("선택하세요 (0-10): ")
        
        try:
            if choice == '1':
                task = input("할 일을 입력하세요: ")
                if task.strip():
                    priority = get_priority()
                    due_date = get_due_date()
                    todo_manager.add_todo(task, priority, due_date)
                else:
                    print("❌ 할 일을 입력해주세요.")
            
            elif choice == '2':
                show_completed = input("완료된 할 일도 보시겠습니까? (y/n, 기본값: y): ").lower()
                show_completed = show_completed != 'n'
                todo_manager.list_todos(show_completed)
            
            elif choice == '3':
                todo_id = int(input("완료할 할 일의 ID를 입력하세요: "))
                todo_manager.complete_todo(todo_id)
            
            elif choice == '4':
                todo_id = int(input("완료 취소할 할 일의 ID를 입력하세요: "))
                todo_manager.uncomplete_todo(todo_id)
            
            elif choice == '5':
                todo_id = int(input("수정할 할 일의 ID를 입력하세요: "))
                new_task = input("새로운 할 일 (없으면 엔터): ")
                new_priority = input("새로운 우선순위 (high/normal/low, 없으면 엔터): ")
                new_due_date = get_due_date()
                
                todo_manager.edit_todo(
                    todo_id,
                    new_task if new_task else None,
                    new_priority if new_priority else None,
                    new_due_date
                )
            
            elif choice == '6':
                todo_id = int(input("삭제할 할 일의 ID를 입력하세요: "))
                confirm = input(f"정말로 삭제하시겠습니까? (y/n): ").lower()
                if confirm == 'y':
                    todo_manager.delete_todo(todo_id)
                else:
                    print("❌ 삭제가 취소되었습니다.")
            
            elif choice == '7':
                keyword = input("검색할 키워드를 입력하세요: ")
                if keyword.strip():
                    todo_manager.search_todos(keyword)
                else:
                    print("❌ 검색 키워드를 입력해주세요.")
            
            elif choice == '8':
                todo_manager.show_statistics()
            
            elif choice == '9':
                confirm = input("완료된 할 일을 모두 삭제하시겠습니까? (y/n): ").lower()
                if confirm == 'y':
                    todo_manager.clear_completed()
                else:
                    print("❌ 삭제가 취소되었습니다.")
            
            elif choice == '10':
                todo_manager.save_todos()
            
            elif choice == '0':
                todo_manager.save_todos()
                print("👋 TODO 리스트를 저장하고 종료합니다. 안녕히 가세요!")
                break
            
            else:
                print("❌ 올바른 번호를 선택해주세요.")
                
        except ValueError:
            print("❌ 올바른 숫자를 입력해주세요.")
        except Exception as e:
            print(f"❌ 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    main()
