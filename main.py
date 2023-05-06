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
    model_engine = "gpt-3.5-turbo"

    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=[
            {"role": "system", "content": "不能谈任何政治类的问题"},
            {"role": "user", "content": user_input},
        ],
    )

    # get response
    return response.choices[0].message.content.strip()



st.title("SW-ChatBot-中文测试")

# input frame
user_input = st.text_input("输入问题：")

if st.button("发送"):
    # with a waiting icon
    # GPT needs some time to response
    with st.spinner("等待回答..."):
        time.sleep(2)

    # get generate_response
    response = generate_response(user_input)

    # show the anwser
    st.write(response)
