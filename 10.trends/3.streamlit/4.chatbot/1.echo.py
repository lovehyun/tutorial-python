import streamlit as st

st.title("Echo Bot")

# 세션에 담을 변수 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 대화 내용 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 입력값 처리
if prompt := st.chat_input("메세지를 입력하세요"):
    # 사용자 입력 표시
    with st.chat_message("user"):
        st.markdown(prompt)

    # 대화 기록 저장
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 응답 결과 생성
    response = f"{prompt.swapcase()}"
    
    # 응답 결과 표시
    with st.chat_message("assistant"):
        st.markdown(response)
        
    # 대화 기록 저장
    st.session_state.messages.append({"role": "assistant", "content": response})
