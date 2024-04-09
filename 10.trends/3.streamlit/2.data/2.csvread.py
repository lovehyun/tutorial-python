import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# CSV 파일 로드
@st.cache_data
def load_data():
    data = pd.read_csv('your_dataset.csv')
    return data

# 데이터 로드
data = load_data()

# 그래프 그리기
st.title('Graph Example')

# 그래프를 그리기 위한 데이터 선택
column_to_plot = st.selectbox('Select column for plot:', data.columns)

# 선택한 열의 데이터로 선 그래프 그리기
fig, ax = plt.subplots()
plt.plot(data[column_to_plot])
plt.xlabel('Index')
plt.ylabel(column_to_plot)
plt.title(f'{column_to_plot} over Index')
st.pyplot(fig)

# 데이터 테이블 표시
st.subheader('Data Table')
st.write(data)
