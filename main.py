import streamlit as st

st.title("💬 聊天机器人")
st.caption("🚀 请给我们反馈，我们会持续改进模型")

st.page_link("main.py", label="Home", icon="🏠")
st.page_link("pages/1_SimpleChat.py", label="获取单个回答病给我们反馈", icon="1️⃣")
st.page_link("pages/2_ChatWithFeedback.py", label="获取多个回答并给我们反馈", icon="2️⃣")

