# 데이터 분석: 대용량 데이터를 수집, 정제, 분석하여 유용한 정보를 도출하는 작업
import pandas as pd

# CSV 파일 읽기
data = pd.read_csv("data.csv")

# 데이터 정제 및 분석
filtered_data = data[data["age"] >= 18]
mean_height = filtered_data["height"].mean()

print("평균 키:", mean_height)
