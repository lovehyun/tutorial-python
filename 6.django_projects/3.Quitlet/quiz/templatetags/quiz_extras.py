# quiz/templatetags/quiz_extras.py
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

@register.filter
def multiply(value, arg):
    """곱셈 필터 (보너스)"""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def subtract(value, arg):
    """빼기 필터 (보너스)"""
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return 0
