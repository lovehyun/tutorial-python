Selenium을 사용하여 다양한 웹 자동화를 수행하는 몇 가지 예제를 추가해보겠습니다. 이 예제들은 웹 페이지에서 요소를 찾고 조작하는 방법, 버튼 클릭, 드롭다운 메뉴 선택, 스크롤 등의 다양한 기능을 포함합니다.

# 예제 1: 페이지에서 특정 요소 찾기 및 조작
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Chrome 드라이버 초기화
driver = webdriver.Chrome()

# 웹 페이지 열기
driver.get('https://www.google.com')

# 요소 찾기
search_box = driver.find_element(By.NAME, 'q')

# 키 입력하기
search_box.send_keys('Selenium')
search_box.send_keys(Keys.RETURN)

# 검색 결과 중 첫 번째 링크 클릭하기
first_result = driver.find_element(By.CSS_SELECTOR, 'h3')
first_result.click()

# 브라우저 닫기
driver.quit()
```

# 예제 2: 버튼 클릭 및 텍스트 입력
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get('https://example.com/login')

# 사용자명 입력
username = driver.find_element(By.ID, 'username')
username.send_keys('your_username')

# 비밀번호 입력
password = driver.find_element(By.ID, 'password')
password.send_keys('your_password')

# 로그인 버튼 클릭
login_button = driver.find_element(By.ID, 'loginButton')
login_button.click()

driver.quit()
```

# 예제 3: 드롭다운 메뉴 선택
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

driver = webdriver.Chrome()
driver.get('https://example.com/dropdown')

# 드롭다운 메뉴 요소 찾기
dropdown = Select(driver.find_element(By.ID, 'dropdownMenu'))

# 드롭다운에서 항목 선택
dropdown.select_by_visible_text('Option 1')

driver.quit()
예제 4: 체크박스 및 라디오 버튼 조작
python
코드 복사
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get('https://example.com/form')

# 체크박스 선택
checkbox = driver.find_element(By.ID, 'checkbox')
checkbox.click()

# 라디오 버튼 선택
radio_button = driver.find_element(By.ID, 'radioButton')
radio_button.click()

driver.quit()
```

# 예제 5: 스크롤 조작
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome()
driver.get('https://example.com/longpage')

# 페이지 하단으로 스크롤
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# 특정 요소로 스크롤
element = driver.find_element(By.ID, 'targetElement')
actions = ActionChains(driver)
actions.move_to_element(element).perform()

driver.quit()
```

# 예제 6: 프레임 전환
```python
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get('https://example.com/iframe')

# 프레임으로 전환
driver.switch_to.frame('iframeName')

# 프레임 내에서 요소 찾기
element_in_frame = driver.find_element(By.ID, 'elementInFrame')
element_in_frame.click()

# 기본 콘텐츠로 돌아오기
driver.switch_to.default_content()

driver.quit()
```

# 예제 7: 알림창 처리
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert

driver = webdriver.Chrome()
driver.get('https://example.com/alert')

# 버튼 클릭하여 알림창 띄우기
alert_button = driver.find_element(By.ID, 'alertButton')
alert_button.click()

# 알림창 전환
alert = Alert(driver)

# 알림창 텍스트 출력
print(alert.text)

# 알림창 수락
alert.accept()

driver.quit()
```

이 예제들은 Selenium을 사용하여 웹 페이지와 상호작용하는 다양한 방법을 보여줍니다. 이러한 기본적인 기능들을 활용하여 복잡한 웹 자동화 작업을 수행할 수 있습니다.
