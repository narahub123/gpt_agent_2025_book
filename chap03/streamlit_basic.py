import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

with st.sidebar:
    open_api_key = os.getenv("OPENAI_API_KEY")
    st.markdown("[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")
    st.markdown("[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)")
    st.markdown("[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)")

st.title("💬 Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you?"}]

for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

if prompt := st.chat_input():
    if not open_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=open_api_key)

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=st.session_state.messages
    )

    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
