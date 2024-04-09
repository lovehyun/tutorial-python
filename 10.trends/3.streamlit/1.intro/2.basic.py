import streamlit as st

# 웹 페이지 제목 설정
st.title('My First Streamlit App')

# 웹 페이지에 텍스트 표시
st.write('Hello, Streamlit!')

# 사용자가 선택할 수 있는 사이드바 위젯 추가
number = st.sidebar.slider('Select a number', 0, 10, 5)

# 선택된 숫자의 제곱을 계산하여 텍스트로 표시
st.write(f'The square of {number} is {number ** 2}')
