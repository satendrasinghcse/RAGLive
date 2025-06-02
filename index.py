import streamlit as st
import requests

st.set_page_config(page_title="RAG Agentic System", layout="centered")

st.markdown(
    """
    <style>
        body {
            background-color: #f0f2f6;
        }
        .stApp {
            background: linear-gradient(135deg, #e8f0ff, #fce4ec);
            color: #333333;
            font-family: 'Segoe UI', sans-serif;
        }
        .message-user {
            background-color: #cce5ff;
            color: #003366;
            padding: 10px 15px;
            border-radius: 10px;
            margin-bottom: 10px;
            max-width: 75%;
            align-self: flex-end;
        }
        .message-bot {
            background-color: #ffe6cc;
            color: #663300;
            padding: 10px 15px;
            border-radius: 10px;
            margin-bottom: 10px;
            max-width: 75%;
            align-self: flex-start;
        }
        .chat-container {
            display: flex;
            flex-direction: column;
        }
        .footer {
            margin-top: 30px;
            text-align: center;
            color: #666666;
            font-size: 0.9em;
        }
        a {
            color: #0066cc;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("RAGLive")


if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.text_input("You:", key="input")

if user_input:
    st.session_state.messages.append(("user", user_input))

    try:
        response = requests.post("http://localhost:8000/chat", json={"user_message": user_input})
        data = response.json()
        bot_reply = data.get("response", "No response found.")
    except Exception as e:
        bot_reply = f"Error: {e}"

    st.session_state.messages.append(("bot", bot_reply))

st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for role, message in st.session_state.messages:
    css_class = "message-user" if role == "user" else "message-bot"
    st.markdown(f'<div class="{css_class}">{message}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="footer">
        Created by <b>Satendra Singh</b> • 
        <a href="https://github.com/satendrasinghcse" target="_blank">GitHub</a>
    </div>
    """,
    unsafe_allow_html=True
)
