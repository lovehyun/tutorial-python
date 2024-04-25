from openai import OpenAI
import streamlit as st
from streamlit_chat import message

chatgpt_api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=chatgpt_api_key)

# 페이지 기본 셋업
st.set_page_config(page_title="Chatbot", page_icon=":robot_face:")
st.markdown("<h1 style='text-align: center;'>ChatGPT clone</h1>", unsafe_allow_html=True)

# 세션에 담을 변수 초기화
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

if "messages" not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

if 'model_name' not in st.session_state:
    st.session_state['model_name'] = []

if 'cost' not in st.session_state:
    st.session_state['cost'] = []

if 'total_tokens' not in st.session_state:
    st.session_state['total_tokens'] = []

if 'total_cost' not in st.session_state:
    st.session_state['total_cost'] = 0.0


# 사이드바 셋업
st.sidebar.title("GPT models")
model_name = st.sidebar.radio("Choose a model:", ("GPT-3.5", "GPT-4"))
counter_placeholder = st.sidebar.empty()
counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")
clear_button = st.sidebar.button("Clear Conversation", key="clear")

if model_name == "GPT-3.5":
    model = "gpt-3.5-turbo-0613"
else:
    model = "gpt-4-turbo"

# 클리어 버튼
if clear_button:
    st.session_state['generated'] = []
    st.session_state['past'] = []
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    st.session_state['number_tokens'] = []
    st.session_state['model_name'] = []
    st.session_state['cost'] = []
    st.session_state['total_cost'] = 0.0
    st.session_state['total_tokens'] = []
    counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")

# GPT 요청 및 응답처리
def generate_response(prompt):
    st.session_state['messages'].append({"role": "user", "content": prompt})

    completion = client.chat.completions.create(
        model = model,
        messages = st.session_state['messages']
    )

    response = completion.choices[0].message.content
    st.session_state['messages'].append({"role": "assistant", "content": response})

    # print(st.session_state['messages'])
    prompt_tokens = completion.usage.prompt_tokens
    completion_tokens = completion.usage.completion_tokens
    total_tokens = completion.usage.total_tokens

    return response, prompt_tokens, completion_tokens, total_tokens 

# 대화 내용 관리
response_container = st.container()
# 입력 박스
container = st.container()

# 입력 요청
with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("You:", key='input', height=100)
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        output, prompt_tokens, completion_tokens, total_tokens = generate_response(user_input)
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)
        st.session_state['model_name'].append(model_name)
        st.session_state['total_tokens'].append(total_tokens)

        # from https://openai.com/pricing#language-models
        if model_name == "GPT-3.5":
            # gpt-3.5-turbo-0613
            cost = (prompt_tokens * 0.0015 + completion_tokens * 0.002) / 1000
        elif model_name == "GPT-4": 
            # gpt-4-turbo
            cost = (prompt_tokens * 0.01 + completion_tokens * 0.03) / 1000
        else:
            cost = 0.0

        st.session_state['cost'].append(cost)
        st.session_state['total_cost'] += cost

# 응답 결과 출력
if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))
            st.write(f"Model used: {st.session_state['model_name'][i]}, Number of tokens: {st.session_state['total_tokens'][i]}, Cost: ${st.session_state['cost'][i]:.5f}")
            counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")
