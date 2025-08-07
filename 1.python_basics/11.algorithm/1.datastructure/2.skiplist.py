import random

# 각 노드는 여러 레벨의 forward 포인터를 가짐
class SkipNode:
    def __init__(self, data, level):
        self.data = data
        self.forward = [None] * (level + 1)  # 레벨 0부터 시작하므로 +1

class SkipList:
    MAX_LEVEL = 4  # 최대 레벨 수 (log(n) 보다 충분히 큰 값)
    P = 0.5        # 노드가 다음 레벨로 올라갈 확률 (50%)

    def __init__(self):
        self.head = SkipNode(None, self.MAX_LEVEL)  # 헤드 노드는 데이터 없음
        self.level = 0  # 현재 스킵리스트에서 가장 높은 레벨

    # 레벨을 무작위로 생성
    def random_level(self):
        lvl = 0
        # 확률적으로 레벨 결정
        while random.random() < self.P and lvl < self.MAX_LEVEL:
            lvl += 1
        return lvl

    # 데이터 삽입
    def insert(self, data):
        update = [None] * (self.MAX_LEVEL + 1)  # 레벨별 갱신용 포인터
        current = self.head

        # 가장 높은 레벨부터 순차적으로 탐색하며 삽입 위치 찾기
        for i in reversed(range(self.level + 1)):
            while current.forward[i] and current.forward[i].data < data:
                current = current.forward[i]
            update[i] = current  # 나중에 포인터 연결을 위해 저장

        # 새로 추가할 노드의 레벨을 랜덤으로 결정
        lvl = self.random_level()

        # 현재 레벨보다 높은 경우, 헤드로 초기화
        if lvl > self.level:
            for i in range(self.level + 1, lvl + 1):
                update[i] = self.head
            self.level = lvl

        # 새 노드 생성 및 forward 포인터 연결
        new_node = SkipNode(data, lvl)
        for i in range(lvl + 1):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node

    # 기본 검색 함수
    def search(self, data):
        current = self.head
        node_count = 0  # 거친 노드 수를 세기 위한 변수

        # 가장 높은 레벨부터 내려오며 검색
        for i in reversed(range(self.level + 1)):
            while current.forward[i] and current.forward[i].data < data:
                current = current.forward[i]
                node_count += 1  # 노드 하나를 거쳤음

        current = current.forward[0]  # 레벨 0에서 최종 비교
        node_count += 1  # 마지막 노드도 비교

        if current and current.data == data:
            print(f"[검색 성공] {data} 찾음 - 거친 노드 수: {node_count}")
            return True
        else:
            print(f"[검색 실패] {data} 없음 - 거친 노드 수: {node_count}")
            return False
    
    # 검색 경로를 시각적으로 출력
    def search_visual(self, data, column_width=6):
        current = self.head
        node_count = 0
        path_map = {lvl: set() for lvl in range(self.level + 1)}

        print(f"\n[시각적 경로 출력] {data} 찾기\n")

        # 각 레벨에서 우측 이동한 노드 기록
        for lvl in reversed(range(self.level + 1)):
            while current.forward[lvl] and current.forward[lvl].data < data:
                current = current.forward[lvl]
                path_map[lvl].add(current.data)
                node_count += 1

        # 마지막 비교 노드 처리 (Level 0)
        current = current.forward[0]
        node_count += 1
        found = current and current.data == data
        if current:
            final_compare_node = current.data

        # 시각화 출력 (path_map + 최종 노드 강조 포함)
        self._print_path_structure(path_map, final_compare_node, column_width)
    
        # 결과 출력
        print("\n검색 결과")
        if found:
            print(f"[검색 성공] {data} 찾음 - 비교 횟수: {node_count}")
        else:
            print(f"[검색 실패] {data} 없음 - 비교 횟수: {node_count}")

    # 특정 레벨에 존재하는 노드 집합 반환
    def _get_level_nodes(self, lvl):
        node = self.head.forward[lvl]
        result = set()
        while node:
            result.add(node.data)
            node = node.forward[lvl]
        return result

    # 시각화 출력 함수 (탐색 경로 강조 포함)
    def _print_path_structure(self, path_map, final_compare_node=None, column_width=6):
        # 전체 노드 순서 (레벨 0 기준)
        all_nodes = []
        node = self.head.forward[0]
        while node:
            all_nodes.append(node.data)
            node = node.forward[0]

        # 각 노드가 속한 레벨 기록
        node_levels = {data: [] for data in all_nodes}
        for lvl in range(self.level + 1):
            node = self.head.forward[lvl]
            while node:
                node_levels[node.data].append(lvl)
                node = node.forward[lvl]

        # 상위 레벨부터 출력
        print("Skip List 시각적 경로 (레벨 4 → 0)")
        for lvl in reversed(range(self.level + 1)):
            line = f"Level {lvl}: "
            for data in all_nodes:
                if lvl in node_levels[data]:
                    if data in path_map[lvl]:
                        # 실제 우측 이동한 노드
                        cell = f"[{str(data).zfill(2)}]".center(column_width)
                    elif lvl == 0 and data == final_compare_node:
                        # Level 0에서 최종 비교된 노드
                        cell = f"[{str(data).zfill(2)}]".center(column_width)
                    else:
                        # 단순히 존재하는 노드
                        cell = f" {str(data).zfill(2)} ".center(column_width)
                else:
                    # 존재하지 않는 칸은 빈칸 처리
                    cell = "------".center(column_width)
                line += cell
            print(line)

    def search_animated(self, data):
        current = self.head
        compare_count = 0  # 총 비교 횟수

        print(f"\n[Skip List 애니메이션 검색] {data} 찾기")

        for lvl in reversed(range(self.level + 1)):
            print(f"\nLevel {lvl}")
            while current.forward[lvl]:
                next_node = current.forward[lvl]
                compare_count += 1

                # 현재 비교 내용과 방향
                cur_val = "HEAD" if current.data is None else str(current.data)
                next_val = str(next_node.data)
                cond = f"{next_node.data} < {data}" if next_node.data < data else f"{next_node.data} ≥ {data}"
                direction = "→ 오른쪽" if next_node.data < data else "→ 아래로 이동"

                # 줄별로 한줄에 비교 번호 표시
                print(f"  [비교 #{compare_count}] {cur_val} → {next_val} | 조건: {cond} {direction}")

                if next_node.data < data:
                    current = next_node
                else:
                    break
                
        # 마지막 비교
        print("\nLevel 0 최종 비교")
        if current.forward[0]:
            final = current.forward[0]
            compare_count += 1
            result = "==" if final.data == data else "!="
            print(f"  [비교 #{compare_count}] {final.data} {result} {data}")
            if final.data == data:
                print(f"{data} 을(를) 찾았습니다!")
            else:
                print(f"{data} 은(는) 존재하지 않습니다.")
        else:
            print("  더 이상 노드가 없습니다. 검색 실패.")

        print(f"\n총 비교 횟수: {compare_count}")

    # 텍스트 기반 구조 출력
    def print_list(self):
        print("Skip List 구조:")
        for i in range(self.level + 1):
            current = self.head.forward[i]
            print(f"Level {i}: ", end="")
            while current:
                print(current.data, end=" -> ")
                current = current.forward[i]
            print("None")
    
    # 전체 수직 구조 출력
    def print_vertical_structure(self, highlight_nodes=None, column_width=6):
        """세로 정렬 구조 출력 (------로 빈칸 채우고 정렬 보정)"""
        if highlight_nodes is None:
            highlight_nodes = set()

        # 정렬 기준이 되는 전체 데이터 수집 (레벨 0 기준)
        all_nodes = []
        node = self.head.forward[0]
        while node:
            all_nodes.append(node.data)
            node = node.forward[0]

        # 각 노드가 포함된 레벨 수집
        node_levels = {data: [] for data in all_nodes}
        for lvl in range(self.level + 1):
            node = self.head.forward[lvl]
            while node:
                node_levels[node.data].append(lvl)
                node = node.forward[lvl]

        # 출력
        print("\nSkip List 세로 구조 (레벨 4 → 0)")
        for lvl in reversed(range(self.level + 1)):
            line = f"Level {lvl}: "
            for data in all_nodes:
                if lvl in node_levels[data]:
                    if data in highlight_nodes:
                        cell = f"*{str(data).zfill(2)}*".center(column_width)
                    else:
                        cell = f"{str(data).zfill(2)}".center(column_width)
                else:
                    cell = "------".center(column_width)
                line += cell
            print(line)


# 테스트
random.seed(42)  # 시드 고정으로 항상 같은 결과 재현 가능

sl = SkipList()
for num in range(10, 81, 5):
    sl.insert(num)

# 구조 출력
sl.print_list()
sl.print_vertical_structure()

# 일반 검색
sl.search(30)
sl.search(52)

# 시각화된 검색 경로
sl.search_visual(30)
sl.search_animated(30)

sl.search_visual(52)
sl.search_animated(52)
