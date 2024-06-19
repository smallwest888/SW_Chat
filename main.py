import os
import openai
import streamlit as st
import random
import hashlib

base = "light"

st.set_page_config(page_title="SW-Chatbot公开版", page_icon="SW-CHAT.png", layout="wide")
all_example_questions = [
    "你能告诉我一个笑话吗？",
    "如何制作蛋糕？",
    "附近有什么好吃的餐馆？",
    "你喜欢什么样的音乐？",
    "如何减肥？",
    "推荐一些好看的电影。",
    "如何学好英语？",
    "如何管理时间？"
]

st.markdown(
    """
    <style>
        .stChatFloatingInputContainer {
            bottom: -50px;
            background-color: rgba(0, 0, 0, 0)
        }
    </style>
    """,
    unsafe_allow_html=True,
)

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

html_code = """
    <div style="position: relative; center: 100px; left: 0px; z-index: 9999;display: flex; align-items: center; background-color: #CCE1E9; ">
        <span style="margin-left: 10px; font-size: 30px; color: black;">SW-Chat公开版</span>
    </div>
"""

st.markdown(html_code, unsafe_allow_html=True)


def generate_key(question, index):
    """ Generate a unique key for each button based on the question text. """
    hash_object = hashlib.md5(question.encode())
    return hash_object.hexdigest() + str(index)

def add_bg():
    st.markdown(
        f"""
         <style>
         .stApp {{
             background-color: #CCE1E9;
             background-attachment: fixed;
             background-size: cover;
         }}
         </style>
         """,
        unsafe_allow_html=True
    )


add_bg()


def set_info_style():
    style = """
        <style>
            .stAlert {
                background-color: #9CC4CC;  
                border-radius: 15px;  
            }
        </style>
        """
    st.markdown(style, unsafe_allow_html=True)


# 应用自定义样式
set_info_style()


# Function to set the background color for areas not covered by the image
def set_background_color(color):
    st.markdown(f"""
    <style>
    .stApp {{
        background-color: {color};
    }}
    </style>
    """, unsafe_allow_html=True)


def set_button_style():
    button_style = """
        <style>
            .stButton > button {
                color: white;  
                background-color: #003B5F; 
                border: none;  
                padding: 10px 20px; 
                border-radius: 30px; 
                font-size: 16px;  
            }
            .stButton > button:hover {
                color: white;
                background-color: #9CC4CC;  
            }
            .stButton > button:active {
                color: #3E5565;  
                background-color: #9CC4CC;  
            }
        </style>
        """
    st.markdown(button_style, unsafe_allow_html=True)


set_button_style()


# Not Working
def set_chat_message_style():
    style = """
        <style>
            .chat-message.user:before {
                content: '';
                background-image: url('User.jpeg');  /* user icon */
            }
            .chat-message.bot:before {
                content: '';
                background-image: url('Bot.jpeg');  /* Chatbot icon */
            }
        </style>
        """
    st.markdown(style, unsafe_allow_html=True)


# Set Style
set_chat_message_style()

# Initialize the OpenAI client with the API key
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.Client()


def generate_response(user_input):
    # GPT-3 and other parameters
    model_engine = "gpt-4o"
    temperature = 0.7
    qa_template = """
    Answer in the language of the question. 

    previous conversation:
    {previous_conversation}
    question: {question}
    ======
    """

    # Ensure the 'messages' list exists in the session state
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

    # Build the string of previous conversation, including past Q&A
    previous_conversation = "\n".join(
        f"{msg['role']}: {msg['content']}" for msg in st.session_state['messages']
    )

    response = client.chat.completions.create(
        model=model_engine,
        messages=[
            {"role": "system",
             "content": qa_template.format(previous_conversation=previous_conversation,
                                           question=user_input)},
            {"role": "user", "content": user_input},
        ],
        temperature=temperature,
    )

    # Add the generated answer to the conversation history
    st.session_state['messages'].append(
        {"role": "assistant", "content": response.choices[0].message.content.strip()}
    )

    return response.choices[0].message.content.strip()


# Initialize chat history in session state if it doesn't exist
if 'messages' not in st.session_state:
    st.session_state.messages = []


def handle_example_question(question):
    # Add user input to the session state
    st.session_state.messages.append({"role": "user", "content": question})

    # Generate a response
    generate_response(question)


# Streamlit part of the code
if 'displayed_questions' not in st.session_state:
    st.session_state.displayed_questions = random.sample(all_example_questions, 3)

cols = st.columns(3)
for i, example_question in enumerate(st.session_state.displayed_questions):
    with cols[i]:
        if st.button(example_question, key=f"example_question_{i}"):
            handle_example_question(example_question)

st.info(
    "本项目属于Hochschule Emden/Leer IPRO-Chat项目的衍生。可能不是最新版本的代码，如果要是寻找最新版本的代码请前往IPRO-Chat的页面"
)

# React to user input
user_input = st.chat_input("请输入你的问题：")

if user_input:
    # Check if the user input was already processed
    if ('last_input' not in st.session_state or
            st.session_state.last_input != user_input):
        # Store the current user input to prevent processing it again
        st.session_state.last_input = user_input

        # Add user input to the session state
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Generate a response
        response = generate_response(user_input)

# Display the chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Add a button to clear chat history
if st.button("清除聊天记录"):
    # Clear chat history and last input to reset the chat
    st.session_state.messages = []
    if 'last_input' in st.session_state:
        del st.session_state.last_input
