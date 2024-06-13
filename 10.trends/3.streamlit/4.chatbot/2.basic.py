# 설정파일:
#   .streamlit/secrets.toml 파일생성 (사용자 홈)
#   [secrets]
#   OPENAI_API_KEY = "your_openai_api_key_here"
# 실행:
#   streamlit run app.py

import openai
import streamlit as st

# secrets에서 API 키 로드
chatgpt_api_key = st.secrets["OPENAI_API_KEY"]
openai.api_key = chatgpt_api_key

# OpenAI 클라이언트 초기화
client = openai.OpenAI(api_key=chatgpt_api_key)

st.title("ChatGPT 클론")

# 세션 상태 변수 초기화
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

# 채팅 메시지 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 처리
if prompt := st.chat_input("무엇이든 물어보세요"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        collected_chunks = []
        collected_messages = []

        # API 요청
        response = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # 스트리밍된 응답 처리
        for chunk in response:
            collected_chunks.append(chunk)  # 이벤트 응답 저장
            if hasattr(chunk.choices[0].delta, 'content'):
                chunk_message = chunk.choices[0].delta.content  # 메시지 추출
                if chunk_message:
                    collected_messages.append(chunk_message)  # 메시지 저장
                    full_response += chunk_message
                    response_placeholder.markdown(full_response)
                    
    st.session_state.messages.append({"role": "assistant", "content": full_response})