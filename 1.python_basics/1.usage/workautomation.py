# 업무 자동화:
import os
import shutil

# 폴더 내의 파일 복사
source_folder = "source_folder"
destination_folder = "destination_folder"

file_list = os.listdir(source_folder)
for file_name in file_list:
    source = os.path.join(source_folder, file_name)
    destination = os.path.join(destination_folder, file_name)
    shutil.copy(source, destination)

# 스크린샷 찍기
import pyautogui

screenshot = pyautogui.screenshot()
screenshot.save("screenshot.png")

# 웹 페이지 자동화
from selenium import webdriver

driver = webdriver.Chrome("chromedriver.exe")
driver.get("https://www.example.com")

search_box = driver.find_element_by_name("q")
search_box.send_keys("Python")
search_box.submit()
