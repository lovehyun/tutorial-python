# Playwright 주요 문법 정리

## 0. 배경

| Selenium 시대         | Playwright |
| ------------------- | ---------- |
| webdriver 설치        | 자동         |
| driver 버전 충돌        | 거의 없음      |
| wait 지옥             | 자동 wait    |
| find_element 반복     | locator 통합 |
| iframe/window 처리 복잡 | 상대적으로 간단   |
| stale element 오류 많음 | 적음         |
| API 오래되고 복잡         | 현대적        |

### Selenium 스타일 

```python 
driver.find_element(By.ID, ...)
driver.find_elements(By.CLASS_NAME, ...)
WebDriverWait(...)
expected_conditions(...)
```

### Playwright 스타일

```python
page.locator(".title").click()
```

## 1. 브라우저 실행

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto("https://example.com")
```

---

## 2. 요소 찾기 (가장 중요)

### CSS 선택자

```python
page.locator("h1")
page.locator(".title")
page.locator("#main")
```

---

## 3. 텍스트 가져오기

```python
text = page.locator("h1").inner_text()

print(text)
```

---

## 4. 속성(attribute) 가져오기

```python
href = page.locator("a").get_attribute("href")

print(href)
```

---

## 5. 여러 개 요소 가져오기

```python
items = page.locator("li")

print(items.count())
```

---

## 6. 특정 순서 요소 선택

```python
first_item = items.nth(0)

print(first_item.inner_text())
```

---

## 7. 반복문 처리

```python
items = page.locator("li")

for i in range(items.count()):

    item = items.nth(i)

    print(item.inner_text())
```

---

## 8. 클릭

```python
page.locator("button").click()
```

---

## 9. 입력창 입력

```python
page.locator("input").fill("hello")
```

---

## 10. 엔터 입력

```python
page.locator("input").press("Enter")
```

---

## 11. 대기(wait)

### 특정 요소 나올 때까지

```python
page.wait_for_selector(".result")
```

---

## 12. 스크린샷

```python
page.screenshot(path="capture.png")
```

---

## 13. 현재 HTML 가져오기

```python
html = page.content()

print(html)
```

---

## 14. 페이지 제목

```python
print(page.title())
```

---

## 15. 현재 URL

```python
print(page.url)
```

---

# 실무에서 가장 많이 쓰는 패턴

```python
cards = page.locator(".card")

for i in range(cards.count()):

    card = cards.nth(i)

    title = card.locator(".title").inner_text()

    price = card.locator(".price").inner_text()

    print(title, price)
```

---

# Playwright의 핵심 장점

| 특징 | 설명 |
|---|---|
| 자동 wait | 요소 뜰 때까지 자동 대기 |
| JS 렌더링 | React/Vue 가능 |
| 실제 브라우저 | 로그인/클릭 가능 |
| CSS 선택자 강력 | 매우 직관적 |
| Selenium보다 현대적 | API 깔끔 |

---

# 가장 중요한 개념 하나

거의 모든 게 이것입니다:

```python
page.locator()
```

그리고 그 뒤에:

```python
.inner_text()
.click()
.fill()
.get_attribute()
```

붙는 구조입니다.
