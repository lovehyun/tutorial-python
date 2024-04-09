import streamlit as st
import cv2

# 웹 페이지 제목 설정
st.title('Real-time Camera Feed')

run = st.checkbox('Run')
FRAME_WINDOW = st.image([])

# 카메라 열기
cap = cv2.VideoCapture(0)

# Streamlit 앱 루프
while run:
    _, frame = cap.read()  # 카메라에서 프레임 읽기

    # 프레임을 RGB로 변환하여 Streamlit에 표시
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # st.image(frame_rgb, channels='RGB')
    FRAME_WINDOW.image(frame_rgb)
else:
    st.write('Stopped')

# 카메라 닫기
cap.release()
