# 주요 컴포넌트
## 버튼 예제:
- btn btn-primary: 파란색의 주 버튼 스타일을 적용합니다.
- btn btn-secondary: 회색의 보조 버튼 스타일을 적용합니다.
- btn btn-success: 초록색의 성공 버튼 스타일을 적용합니다.
- btn btn-danger: 빨간색의 위험 버튼 스타일을 적용합니다.
- btn btn-warning: 노란색의 경고 버튼 스타일을 적용합니다.
- btn btn-info: 하늘색의 정보 버튼 스타일을 적용합니다.
- btn btn-light: 흰색의 라이트 버튼 스타일을 적용합니다.
- btn btn-dark: 검은색의 다크 버튼 스타일을 적용합니다.

## 폼 예제:
- form-control: 입력 필드의 스타일을 적용합니다.
- form-check-input: 체크박스 입력 필드의 스타일을 적용합니다.
- form-check-label: 체크박스의 라벨 스타일을 적용합니다.

## 카드 예제:
- card: 카드 컴포넌트를 생성합니다.
- card-img-top: 카드 상단의 이미지를 스타일링합니다.
- card-body: 카드 본문을 스타일링합니다.
- card-title: 카드 제목을 스타일링합니다.
- card-text: 카드 텍스트를 스타일링합니다.
- btn btn-primary: 카드 내의 버튼을 스타일링합니다.

## 모달 예제:
- modal: 모달 컴포넌트를 생성합니다.
- modal-dialog: 모달 다이얼로그를 스타일링합니다.
- modal-content: 모달의 콘텐츠를 스타일링합니다.
- modal-header: 모달 헤더를 스타일링합니다.
- modal-title: 모달 제목을 스타일링합니다.
- modal-body: 모달 본문을 스타일링합니다.
- modal-footer: 모달 푸터를 스타일링합니다.
- btn-close: 모달 닫기 버튼을 스타일링합니다.

## 그리드 시스템 예제:
- row: 행을 생성합니다.
- col-md-4: 중간 크기 이상의 화면에서 12칸 중 4칸을 차지하는 열을 생성합니다.


# 반응형을 위한 주요 속성
## Grid System
- container, container-fluid, container-{breakpoint}: 그리드 컨테이너를 정의합니다. {breakpoint}는 sm, md, lg, xl, xxl 등의 브레이크포인트를 지정할 수 있습니다.
- row: 그리드 행을 정의합니다.
- col, col-{breakpoint}, col-{breakpoint}-{number}, col-auto: 그리드 열을 정의합니다. {number}는 1부터 12까지의 숫자를 지정할 수 있습니다.

## Display Utility Classes
- d-none, d-{breakpoint}-none: 요소를 숨깁니다.
- d-block, d-{breakpoint}-block: 블록 요소로 표시합니다.
- d-inline, d-{breakpoint}-inline: 인라인 요소로 표시합니다.
- d-inline-block, d-{breakpoint}-inline-block: 인라인 블록 요소로 표시합니다.
- d-flex, d-{breakpoint}-flex: Flexbox 컨테이너로 표시합니다.

## Flexbox Utilities
- flex-row, flex-{breakpoint}-row: 가로 방향으로 정렬합니다.
- flex-column, flex-{breakpoint}-column: 세로 방향으로 정렬합니다.
- justify-content-start, justify-content-{breakpoint}-start: Flexbox 컨테이너의 항목들을 시작점에 정렬합니다.
- justify-content-center, justify-content-{breakpoint}-center: 가운데 정렬합니다.
- justify-content-end, justify-content-{breakpoint}-end: 끝점에 정렬합니다.
- align-items-start, align-items-{breakpoint}-start: Flexbox 컨테이너의 항목들을 시작점에 맞춥니다.
- align-items-center, align-items-{breakpoint}-center: 가운데 맞춥니다.
- align-items-end, align-items-{breakpoint}-end: 끝점에 맞춥니다.

## Spacing Utilities
- m-{number}, mt-{number}, mr-{number}, mb-{number}, ml-{number}, mx-{number}, my-{number}: 여백(Margin)을 지정합니다. {number}는 0부터 5까지 지정할 수 있습니다.
- p-{number}, pt-{number}, pr-{number}, pb-{number}, pl-{number}, px-{number}, py-{number}: 패딩(Padding)을 지정합니다. {number}는 0부터 5까지 지정할 수 있습니다.

## Text Utilities
- text-left, text-{breakpoint}-left: 왼쪽 정렬합니다.
- text-center, text-{breakpoint}-center: 가운데 정렬합니다.
- text-right, text-{breakpoint}-right: 오른쪽 정렬합니다.
- text-uppercase: 모든 문자를 대문자로 표시합니다.
- text-lowercase: 모든 문자를 소문자로 표시합니다.
- text-capitalize: 각 단어의 첫 문자를 대문자로 표시합니다.
- text-muted: 회색 톤의 텍스트로 표시합니다.
- text-primary, text-secondary, text-success, text-danger, text-warning, text-info, - text-light, text-dark: 텍스트 색상을 지정합니다.

## Background Utilities
- bg-primary, bg-secondary, bg-success, bg-danger, bg-warning, bg-info, bg-light, bg-dark, bg-white, bg-transparent: 배경 색상을 지정합니다.

## Borders
- border, border-top, border-right, border-bottom, border-left: 테두리를 지정합니다.
- border-0, border-top-0, border-right-0, border-bottom-0, border-left-0: 테두리를 제거합니다.
- rounded, rounded-top, rounded-right, rounded-bottom, rounded-left, rounded-circle, - rounded-pill: 테두리를 둥글게 만듭니다.

## Buttons
- btn, btn-primary, btn-secondary, btn-success, btn-danger, btn-warning, btn-info, btn-light, btn-dark, btn-link: 버튼 스타일을 지정합니다.
- btn-lg, btn-sm: 버튼 크기를 지정합니다.
- btn-block: 블록 레벨 버튼을 만듭니다.

## 기타 유틸리티 클래스
- w-100: 너비를 100%로 설정합니다.
- h-100: 높이를 100%로 설정합니다.
- mw-100: 최대 너비를 100%로 설정합니다.
- mh-100: 최대 높이를 100%로 설정합니다.
- overflow-auto, overflow-hidden, overflow-visible, overflow-scroll: 요소의 오버플로우(overflow) 속성을 설정합니다.
- position-static, position-relative, position-absolute, position-fixed, position-sticky: 요소의 위치 속성을 설정합니다.
- top-0, right-0, bottom-0, left-0: 위치를 지정합니다.
