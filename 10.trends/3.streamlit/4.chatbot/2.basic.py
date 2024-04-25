from openai import OpenAI
import streamlit as st

# API 키 로딩 (환경변수파일)
chatgpt_api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=chatgpt_api_key)

st.title("ChatGPT clone")

# 세션에 담을 변수 초기화
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

# 대화 내용 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 입력값 처리
if prompt := st.chat_input("무엇이든 물어보세요"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # API 요청
        stream = client.chat.completions.create(
            model = st.session_state["openai_model"],
            messages = [
                { "role": m["role"], "content": m["content"] }
                for m in st.session_state.messages
            ],
            stream = True,
        )
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})
