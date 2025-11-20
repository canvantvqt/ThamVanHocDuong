import streamlit as st
from openai import OpenAI
import os

# ============================
#       HÀM ĐỌC FILE
# ============================
def rfile(name_file):
    with open(name_file, "r", encoding="utf-8") as file:
        return file.read()

# ============================
#       CSS GIAO DIỆN MỚI
# ============================
st.markdown("""
<style>

/* --- BASE STYLES (Dành cho mọi màn hình, chủ yếu là Desktop) --- */

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

/* Mô tả phụ (Sub-info) - Giữ nguyên vì nó đã responsive tốt */
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
    /* Giảm padding ngang mặc định để có thêm không gian trên di động */
    padding: 10px 10px; 
}

/* Assistant bubble */
.msg-assistant {
    background: #1c2333;
    color: #e8ecff;
    padding: 14px 18px;
    border-radius: 14px;
    margin: 12px 0;
    width: fit-content;
    max-width: 85%; /* Tăng max-width lên một chút cho di động */
    box-shadow: 0px 4px 8px rgba(50, 50, 93, 0.35);
    font-size: 16px;
    border-left: 4px solid #4e8cff;
}

/* Prefix "Assistant" */
.msg-assistant::before {
    content: "🧠 TVS - Tham vấn học đường\\A";
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
    max-width: 85%; /* Tăng max-width lên một chút cho di động */
    margin-left: auto;
    box-shadow: 0px 4px 8px rgba(50, 50, 93, 0.3);
    font-size: 16px;
    border-right: 4px solid #73d0ff;
}

/* Logo căn giữa */
.logo-zone {
    display: flex;
    justify-content: center;
    margin-bottom: 10px;
}

/* Tùy chỉnh thanh Input chat của Streamlit */
/* Selector này nhắm vào container bao quanh st.chat_input */
.stChatInput {
    /* Đảm bảo nó chiếm toàn bộ chiều rộng có thể */
    width: 100%; 
    /* Dùng !important để ghi đè CSS mặc định của Streamlit */
}
/* Selector cho hộp input */
.stChatInput > div > div > textarea {
    background: #141722 !important;
    border-radius: 14px !important;
    color: #ffffff !important; /* Đảm bảo màu chữ hiển thị tốt */
}
/* Selector cho container ngoài cùng của input */
[data-testid="stChatInputContainer"] {
    position: fixed; /* Cố định thanh input ở cuối màn hình */
    bottom: 0;
    left: 0;
    right: 0;
    padding: 10px; /* Thêm padding xung quanh */
    background: #0f1116; /* Màu nền giống màu body để che đi phần dưới */
    box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.5); /* Thêm bóng để tách biệt */
    z-index: 1000;
}
/* Thêm khoảng trống ở cuối trang để nội dung không bị thanh input che mất */
.stApp {
    padding-bottom: 90px; /* Tạo khoảng trống bằng chiều cao thanh input cố định */
}


/* --- MEDIA QUERY CHO DI ĐỘNG (Màn hình nhỏ hơn 600px) --- */
@media (max-width: 600px) {
    
    /* Điều chỉnh tiêu đề */
    .header-title {
        font-size: 18px; /* Giảm kích thước chữ tiêu đề */
        padding: 5px 10px 10px 10px;
    }
    
    /* Điều chỉnh logo */
    .logo-zone {
        margin-bottom: 5px;
    }
    
    /* Giảm kích thước chữ của bong bóng chat */
    .msg-assistant, .msg-user {
        font-size: 15px; 
        padding: 12px 16px;
        max-width: 95%; /* Tăng tối đa để tận dụng không gian màn hình nhỏ */
    }
    
    /* Điều chỉnh prefix */
    .msg-assistant::before {
        font-size: 13px;
    }

    /* Điều chỉnh container chat */
    .chat-container {
        padding: 5px 5px; /* Giảm padding ngang tối đa */
    }

    /* Điều chỉnh thanh input cố định */
    [data-testid="stChatInputContainer"] {
        padding: 8px 5px; /* Giảm padding trên điện thoại */
    }
    .stApp {
        padding-bottom: 80px; /* Giảm padding để phù hợp với thanh input nhỏ hơn */
    }
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
st.markdown(f'<div class="header-title">{str(title_content)}</div>', unsafe_allow_html=True)

# ============================
#       INIT OPENAI
# ============================
client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY"))

INITIAL_SYSTEM_MESSAGE = {"role": "system", "content": rfile("01.system_trainning.txt")}
INITIAL_ASSISTANT_MESSAGE = {"role": "assistant", "content": rfile("02.assistant.txt")}

if "messages" not in st.session_state:
    st.session_state.messages = [INITIAL_SYSTEM_MESSAGE, INITIAL_ASSISTANT_MESSAGE]

# ============================
#     HIỂN THỊ LỊCH SỬ CHAT
# ============================
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for m in st.session_state.messages:
    content = str(m.get("content", ""))
    role = m.get("role", "")
    if role == "assistant":
        st.markdown(f'<div class="msg-assistant">{content}</div>', unsafe_allow_html=True)
    elif role == "user":
        st.markdown(f'<div class="msg-user">{content}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ============================
#       INPUT CHAT
# ============================
prompt = st.chat_input("Bạn muốn được THAM VẤN điều gì nè?...")

if prompt:
    # Lưu tin nhắn người dùng
    st.session_state.messages.append({"role": "user", "content": prompt})

    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="msg-user">{str(prompt)}</div>', unsafe_allow_html=True)

    # Gọi API
    response_text = ""
    stream = client.chat.completions.create(
        model=rfile("module_chatgpt.txt").strip(),
        messages=[{"role": m["role"], "content": str(m["content"])} for m in st.session_state.messages],
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
