import streamlit as st
import os
from openai import OpenAI

st.title("🤖 TVS-ChatBot AI - Tham vấn học đường")

api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
if not api_key:
    st.error("⚠️ Không có API key! Hãy thêm OPENAI_API_KEY trong Streamlit → Secrets.")
    st.stop()

client = OpenAI(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

prompt = st.chat_input("Hỏi ChatBot điều gì đó...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages,
            stream=True,
        )
        response = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                response += chunk.choices[0].delta.content
                st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
