# Django div, mod 필터 문제 해결

## 문제 상황

Django 템플릿에서 수학 연산을 위해 `div`와 `mod` 필터를 사용하려고 했지만 다음과 같은 에러가 발생:

```
TemplateSyntaxError: Invalid filter: 'div'
TemplateSyntaxError: Invalid filter: 'mod'
```

**원인:** Django에는 기본적으로 `div`(나눗셈)와 `mod`(나머지) 필터가 제공되지 않음

## 해결 방법

### 방법 1: 커스텀 필터 생성 (권장)

#### 1단계: templatetags 폴더 구조 생성

```
quiz/
├── templatetags/
│   ├── __init__.py        # 빈 파일
│   └── math_filters.py    # 수학 필터들
├── models.py
├── views.py
└── ...
```

#### 2단계: 필터 파일 생성

**quiz/templatetags/__init__.py**
```python
# 빈 파일 (내용 없음)
```

**quiz/templatetags/math_filters.py**
```python
from django import template

register = template.Library()

@register.filter
def div(value, arg):
    """나눗셈 필터 - 정수 결과 반환"""
    try:
        return int(value) // int(arg)
    except (ValueError, ZeroDivisionError):
        return 0

@register.filter
def mod(value, arg):
    """나머지 필터"""
    try:
        return int(value) % int(arg)
    except (ValueError, ZeroDivisionError):
        return 0
```

#### 3단계: 템플릿에서 사용

```html
{% load math_filters %}

<!-- 예시: 150초를 분으로 변환 -->
{{ 150|div:60 }}분  <!-- 결과: 2분 -->

<!-- 예시: 150초에서 나머지 초 계산 -->
{{ 150|mod:60 }}초  <!-- 결과: 30초 -->

<!-- 복합 사용: 시간 형태로 표시 -->
{% if quiz.time_taken.seconds >= 3600 %}
    {{ quiz.time_taken.seconds|div:3600 }}시간 
{% endif %}
{{ quiz.time_taken.seconds|mod:3600|div:60 }}분 
{{ quiz.time_taken.seconds|mod:60 }}초
```

#### 4단계: 서버 재시작

```bash
# 서버 중지 후 재시작 (필수!)
python manage.py runserver
```

### 방법 2: widthratio 태그 사용

Django 기본 제공 `widthratio` 태그로 나눗셈 구현:

```html
<!-- div 필터 대신 -->
{% widthratio value 60 1 %}  <!-- value를 60으로 나눈 결과 -->

<!-- 예시 -->
{% widthratio quiz.time_taken.seconds 60 1 %}분
```

**단점:** 나머지 연산은 불가능하고, 복잡한 계산에는 부적합

### 방법 3: 뷰에서 미리 계산

템플릿에서 계산하지 말고 views.py에서 미리 계산해서 전달:

**quiz/views.py**
```python
def quiz_complete(request, quiz_id):
    # 기존 코드...
    
    # 시간 계산
    time_display = None
    if quiz.time_taken:
        total_seconds = int(quiz.time_taken.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        time_display = {
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds,
            'total_minutes': total_seconds // 60
        }
    
    context = {
        'quiz': quiz,
        'time_display': time_display,
        # 기타...
    }
    return render(request, 'quiz/quiz_complete.html', context)
```

**템플릿에서 사용**
```html
{% if time_display %}
    {% if time_display.hours > 0 %}{{ time_display.hours }}시간 {% endif %}
    {% if time_display.minutes > 0 %}{{ time_display.minutes }}분 {% endif %}
    {{ time_display.seconds }}초
{% endif %}
```

## 실제 적용 예시

### 원본 문제 코드
```html
<!-- 에러 발생 -->
{{ quiz.time_taken.seconds|div:60 }}분
{{ quiz.time_taken.seconds|mod:60 }}초
```

### 해결된 코드

**커스텀 필터 사용**
```html
{% load math_filters %}
{{ quiz.time_taken.seconds|div:60 }}분
{{ quiz.time_taken.seconds|mod:60 }}초
```

**widthratio 사용 (div만 가능)**
```html
{% widthratio quiz.time_taken.seconds 60 1 %}분
```

**views.py 계산 사용**
```html
{{ time_display.minutes }}분
{{ time_display.seconds }}초
```

## 각 방법의 장단점

### 커스텀 필터
- **장점:** 재사용 가능, 템플릿에서 직관적, Django스러운 방식
- **단점:** 초기 설정 필요, 서버 재시작 필요

### widthratio 태그
- **장점:** Django 기본 제공, 추가 설정 불필요
- **단점:** 나누기만 가능, 나머지 연산 불가

### views.py 계산
- **장점:** 복잡한 로직 처리 가능, 템플릿 단순화
- **단점:** 뷰 코드 복잡해짐, 재사용성 떨어짐

## 권장사항

1. **간단한 수학 연산:** 커스텀 필터 (방법 1)
2. **복잡한 계산 로직:** views.py에서 계산 (방법 3)
3. **임시 해결책:** widthratio 사용 (방법 2)

대부분의 경우 **커스텀 필터를 만드는 것이 가장 좋은 해결책**입니다.
