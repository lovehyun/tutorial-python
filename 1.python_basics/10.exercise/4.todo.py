# 간단한 TODO 리스트 프로그램

todos = []  # 할 일 목록을 저장할 리스트

def show_todos():
    """할 일 목록 보기"""
    if not todos:
        print("할 일이 없습니다.")
        return
    
    print("\n=== 할 일 목록 ===")
    for i, todo in enumerate(todos, 1):
        status = "✅" if todo['done'] else "❌"
        print(f"{i}. {status} {todo['task']}")
    print()

def add_todo():
    """할 일 추가"""
    task = input("새로운 할 일: ")
    if task:
        todos.append({'task': task, 'done': False})
        print(f"'{task}' 추가완료!")
    else:
        print("할 일을 입력해주세요.")

def complete_todo():
    """할 일 완료 처리"""
    show_todos()
    if not todos:
        return
    
    try:
        num = int(input("완료할 할 일 번호: "))
        if 1 <= num <= len(todos):
            todos[num-1]['done'] = True
            print(f"'{todos[num-1]['task']}' 완료!")
        else:
            print("올바른 번호를 입력하세요.")
    except ValueError:
        print("숫자를 입력하세요.")

def delete_todo():
    """할 일 삭제"""
    show_todos()
    if not todos:
        return
    
    try:
        num = int(input("삭제할 할 일 번호: "))
        if 1 <= num <= len(todos):
            task = todos.pop(num-1)
            print(f"'{task['task']}' 삭제완료!")
        else:
            print("올바른 번호를 입력하세요.")
    except ValueError:
        print("숫자를 입력하세요.")

def main():
    """메인 프로그램"""
    print("📝 간단한 TODO 리스트")
    
    while True:
        print("\n1. 목록보기")
        print("2. 추가하기") 
        print("3. 완료하기")
        print("4. 삭제하기")
        print("5. 종료")
        
        choice = input("\n선택: ")
        
        if choice == '1':
            show_todos()
        elif choice == '2':
            add_todo()
        elif choice == '3':
            complete_todo()
        elif choice == '4':
            delete_todo()
        elif choice == '5':
            print("종료합니다!")
            break
        else:
            print("1~5 중에서 선택하세요.")

# 프로그램 실행
if __name__ == "__main__":
    main()
