#!/usr/bin/env python
# coding: utf-8

import os
import streamlit as st
import time
import openai

def generate_response(user_input):
    # OpenAI API
    openai.api_key = os.getenv("OPENAI_API_KEY")
    # GPT-3 and other parameter

    model_engine = "gpt-4"

    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=[
            {"role": "system", "content": "不能谈任何政治类的问题，如果被问及是否可以理解文件，回答https://smallwest888-sw-chat-filesreader-filereader-bot-j0o50d.streamlit.app/"},
            {"role": "user", "content": user_input},
        ],
    )

    # get response
    return response.choices[0].message.content.strip()

st.title("SW-ChatBot-中文测试")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.text_input("输入问题："):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.spinner("等待回答..."):
        time.sleep(2)
        # get generate_response
        response = generate_response(prompt)
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

# Add a button to clear chat history
if st.button("Clear Chat History"):
    st.session_state['chat_history'] = []
