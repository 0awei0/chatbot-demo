import streamlit as st
import json

from openai import OpenAI
from mongdb_connect import insert_one_choice
from streamlit_feedback import streamlit_feedback

st.title("💬 聊天机器人")
st.caption("🚀 在这里，模型会给出多个回答，请您选择最好的一个答案，以便我们改进模型")


def update_chat(client):
    # 如果输入框输入信息了
    if prompt := st.chat_input("请问我问题"):
        st.session_state['answer_complete'] = False

        # 用户提问也存入问答历史中
        st.session_state.messages_multiple.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)  # 显示用户输入

        # 得到模型的回答并写入网页对话框
        with st.chat_message("assistant"):
            messages_multiple = []
            for message in st.session_state['messages_multiple']:
                if message['role'] == 'user':
                    messages_multiple.append({"role": "user", "content": message['content']})
                else:
                    messages_multiple.append({"role": "assistant", "content": message['content'][0]})

            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=messages_multiple,
                stream=True,
            )

            st.markdown("A \n")
            response = st.write_stream(stream)  # 得到回答

            st.markdown("B \n")
            st.write(response)  # 得到回答

            st.markdown("C \n")
            st.write(response)  # 得到回答
            responses = [response, response, response]

        st.session_state['answer_complete'] = True
        # 这里的response是一个字符串，是模型对当前问题的回答，将其存入问答历史中
        st.session_state.messages_multiple.append({"role": "assistant", "content": responses})
        # write_files()


def chatgpt_with_multiple_answers():
    key = 'sk-SFXiex2MCespk9H83d766aE49cCd4cFd8a5b4dEbAb728507'
    # client = OpenAI(api_key=key, base_url="https://free.gpt.ge/v1/", default_headers={"x-foo": "true"})
    client = OpenAI(api_key="sk-770a1b142cb24646ac6cc9f49c744b4c", base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",)
    # 初始化聊天使用的模型
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "qwen-max"

    # 初始化聊天记录
    if "messages_multiple" not in st.session_state:
        st.session_state.messages_multiple = []

    # 每次都刷新当前的聊天记录显示
    for message in st.session_state.messages_multiple:
        with st.chat_message(message["role"]):
            if isinstance(message['content'], list):
                for index, content in enumerate(message['content']):
                    st.write(chr(ord("A") + index) + " \n" + content)
            else:
                st.write(message["content"])

    update_chat(client)


def get_data():
    if st.session_state.get("messages_multiple"):
        data = st.session_state['messages_multiple']
        if len(data) >= 2:
            data = data[-2:]
            if data[0].get("role") == "user" and data[1].get("role") == 'assistant':
                return data[0]['content'], data[1]['content']


def upload_feedback():
    question, answers = get_data()
    choice = ord(st.session_state['choice']) - ord("A")
    upload_state = insert_one_choice(question, answers, choice)
    if upload_state:
        st.session_state['answer_complete'] = False
        st.toast("上传成功，感谢您的反馈!", icon="📝")
    else:
        st.toast("上传失败了，请再试一次!", icon="🚨")

    return upload_state


def get_feedback():
    # 如果当前已经获取到了回答，则显示一个复选框
    if st.session_state['answer_complete']:
        option = st.selectbox(
            "上面三个回答，您认为哪个更好?",
            ("A", "B", "C"),
        )

        st.write("您的选择: ", option)
        st.session_state['choice'] = option
        st.button("提交反馈", on_click=upload_feedback)


def init_vars():
    if not st.session_state.get("answer_complete"):
        st.session_state['answer_complete'] = False


if __name__ == '__main__':
    init_vars()
    chatgpt_with_multiple_answers()
    get_feedback()
