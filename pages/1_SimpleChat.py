import streamlit as st
import json

from openai import OpenAI
from mongdb_connect import insert_one_data

st.title("💬 聊天机器人")
st.caption("🚀 在这里，模型只会给出一个回答，请您在侧边栏给出反馈，以便我们改进模型")


def copy_answer_and_question():
    if st.session_state.get("messages"):
        data = st.session_state['messages']
        if len(data) >= 2:
            data = data[-2:]
            if data[0].get("role") == "user" and data[1].get("role") == 'assistant':
                st.session_state.copy_problem = data[0]['content']
                st.session_state.copy_answer = data[1]['content']
                # print(st.session_state.copy_problem, st.session_state.copy_answer)


def update_chat(client):
    # 如果输入框输入信息了
    if prompt := st.chat_input("请问我问题"):
        # 用户提问也存入问答历史中
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)  # 显示用户输入

        # 得到模型的回答并写入网页对话框
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],  # messages: 上下文信息，所有的聊天记录都传进去
                stream=True,
            )
            response = st.write_stream(stream)  # 得到回答
            # print("response: ", response)

        # 这里的response是一个字符串，是模型对当前问题的回答，将其存入问答历史中
        st.session_state.messages.append({"role": "assistant", "content": response})
        # write_files()


def chat_with_gpt():
    key = 'sk-SFXiex2MCespk9H83d766aE49cCd4cFd8a5b4dEbAb728507'
    client = OpenAI(api_key=key, base_url="https://free.gpt.ge/v1/", default_headers={"x-foo": "true"})

    # 初始化聊天使用的模型
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo-0125"

    # 初始化聊天记录
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 每次都刷新当前的聊天记录显示
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    update_chat(client)


def write_files():
    with open('history.json', 'w', encoding='utf-8') as file:
        json.dump(st.session_state.to_dict(), file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    with st.form('feedback'):
        with st.sidebar:
            st.subheader("**提交反馈**")

            quick_copy = st.sidebar.button("复制当前问题及答案", on_click=copy_answer_and_question)

            is_correct = st.sidebar.selectbox('模型回答准确吗', ['准确', '不准确'])
            problem = st.sidebar.text_area(label="输入原问题", key='copy_problem')
            answer = st.sidebar.text_area(label="输入原问题的答案", key='copy_answer')
            improve = st.sidebar.text_area(label="输入你认为正确的回答")

            submitted = st.form_submit_button('提交')

    chat_with_gpt()

    if submitted:
        if insert_one_data(is_correct, problem, answer, improve):
            st.success('上传成功，感谢您的反馈', icon="✅")
        else:
            st.error('上传失败了，请再试一次', icon="🚨")
    else:
        with st.sidebar:
            st.write('☝️ 提交您的反馈!')
