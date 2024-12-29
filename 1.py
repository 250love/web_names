import streamlit as st
from http import HTTPStatus
from dashscope import Application
import datetime

# 设置 API Key 和 App ID
api_key = "sk-e2492dea19b945059a9a05abb4d0fc0b"
app_id = 'ac10b1136ce24175a8289b00bb27ad0b'

# Streamlit 页面设置
st.set_page_config(page_title="webname_creator", page_icon="🤖")
st.title("rwebname_creator")

# 初始化会话历史
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# 自动介绍自己
if len(st.session_state.chat_history) == 0:
    # 发送初始问题
    initial_prompt = "你是谁？"
    response = Application.call(
        api_key=api_key,
        app_id=app_id,
        prompt=initial_prompt
    )

    if response.status_code == HTTPStatus.OK:
        response_text = response.output.text
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.chat_history.append({"role": "assistant", "content": response_text, "timestamp": timestamp})
    else:
        st.error(f"请求失败: {response.message}")
        st.write(f"请求ID: {response.request_id}")
        st.write(f"状态码: {response.status_code}")
        st.write(f"请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")

# 显示聊天历史
for record in st.session_state.chat_history:
    with st.chat_message(record['role']):
        st.write(f"{record['content']} [{record['timestamp']}]")

# 用户输入
user_input = st.chat_input("You: ")

if user_input:
    # 获取当前时间戳
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 添加用户问题到历史记录
    st.session_state.chat_history.append({"role": "user", "content": user_input, "timestamp": timestamp})

    # 调用 DashScope API
    response = Application.call(
        api_key=api_key,
        app_id=app_id,
        prompt=user_input
    )

    if response.status_code == HTTPStatus.OK:
        response_text = response.output.text
        # 添加模型回答到历史记录
        st.session_state.chat_history.append({"role": "assistant", "content": response_text, "timestamp": timestamp})
    else:
        st.error(f"请求失败: {response.message}")
        st.write(f"请求ID: {response.request_id}")
        st.write(f"状态码: {response.status_code}")
        st.write(f"请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")

    # 重新渲染页面以显示新的聊天记录
    st.rerun()