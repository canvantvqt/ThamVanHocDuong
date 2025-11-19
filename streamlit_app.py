import streamlit as st
from openai import OpenAI
import os

# Hàm đọc file
def rfile(name_file):
    with open(name_file, "r", encoding="utf-8") as file:
        return file.read()

# ============================
#       CSS GIAO DIỆN MỚI
# ============================
st.markdown("""
<style>

body {
    background-color: #0f1116;
}

/* Tổng layout căn giữa */
.main-block {
    max-width: 850px;
    margin: 0 auto;
    text-align: center;
}

/* Title zone */
.header-title {
    text-align: center;
    font-size: 22px;
    font-weight: 700;
    padding: 5px 0 15px 0;
    color: #ffffff;
    line-height: 1.45;
}

/* Mô tả phụ */
.sub-info {
    background: #1c2333;
    color: #d6dcff;
    font-size: 14px;
    padding: 12px 18px;
    border-radius: 14px;
    margin: 0 auto 15px auto;
    max-width: 700px;
}

/* Container chat */
.chat-container {
    max-width: 850px;
    margin: auto;
    padding: 10px 20px;
}

/* Assistant bubble */
.msg-assistant {
    background: #1c2333;
    color: #e8ecff;
    padding: 14px 18px;
    border-radius: 14px;
    margin: 12px 0;
    width: fit-content;
    max-width: 80%;
    box-shadow: 0px 4px 8px rgba(50, 50, 93, 0.35);
    font-size: 16px;
    border-left: 4px solid #4e8cff;
}

/* Prefix "Assistant" */
.msg-assistant::before {
    content: "🧠 TVS - Tham vấn học đường\n";
    font-weight: 700;
    font-size: 14px;
    display: block;
    margin-bottom: 4px;
    opacity: 0.9;
}

/* User bubble */
.msg-user {
    background: #2c3e5c;
    color: #ffffff;
    padding: 14px 18px;
    border-radius: 14px;
    margin: 12px 0;
    width: fit-content;
    max-width: 80%;
    margin-left: auto;
    box-shadow: 0px 4px 8px rgba(50, 50, 93, 0.3);
    font-size: 16px;
    border-right: 4px solid #73d0ff;
}

/* Input chat */
.stChatInputContainer {
    background: #141722 !important;
    border-radius: 14px !important;
}

/* Logo căn giữa */
.logo-zone {
    display: flex;
    justify-content: center;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)


# ============================
#       LOGO + TIÊU ĐỀ
# ============================
try:
    st.markdown('<div class="logo-zone">', unsafe_allow_html=True)
    st.image("logo.png", width=140)
    st.markdown('</div>', unsafe_allow_html=True)
except:
    pass

title_content = rfile("00.xinchao.txt")
st.markdown(f'<div class="header-title">{title_content}</div>', unsafe_allow_html=True)

# ============================
#       INIT OPENAI
# ============================
client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY"))

INITIAL_SYSTEM_MESSAGE = {"role": "system", "content": rfile("01.system_trainning.txt")}
INITIAL_ASSISTANT_MESSAGE = {"role": "assistant", "content": rfile("02.assistant.txt")}

if "messages" not in st.session_state:
    st.session_state.messages = [INITIAL_SYSTEM_MESSAGE, INITIAL_ASSISTANT_MESSAGE]

# ============================
#     Hiển thị lịch sử chat
# ============================
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for m in st.session_state.messages:
    if m["role"] == "assistant":
        st.markdown(f'<div class="msg-assistant">{m["content"]}</div>', unsafe_allow_html=True)
    elif m["role"] == "user":
        st.markdown(f'<div class="msg-user">{m["content"]}</div>', unsafe_allow_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ============================
#       INPUT CHAT
# ============================
prompt = st.chat_input("Bạn muốn được THAM VẤN điều gì nè?...")

if prompt:

    # Lưu tin nhắn người dùng
    st.session_state.messages.append({"role": "user", "content": prompt})

    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="msg-user">{prompt}</div>', unsafe_allow_html=True)

    # Gọi API
    response_text = ""
    stream = client.chat.completions.create(
        model=rfile("module_chatgpt.txt").strip(),
        messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
        stream=True,
    )

    for chunk in stream:
        if chunk.choices:
            response_text += chunk.choices[0].delta.content or ""

    # Hiển thị tin nhắn trợ lý
    st.markdown(f'<div class="msg-assistant">{response_text}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Lưu response vào session
    st.session_state.messages.append({"role": "assistant", "content": response_text})
