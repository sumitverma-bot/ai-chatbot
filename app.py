import streamlit as st
from groq import Groq
import os

# Connect to AI
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("🤖 Sumit's AI Chatbot")

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    st.write("Model: llama-3.3-70b-versatile")
    st.write("Built by Sumit Verma")

# Clear button
if st.button("🧹 Clear Chat"):
    st.session_state.messages = []

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# User input
user_input = st.chat_input("Type your message...")

if user_input:
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful and professional AI assistant."},
                *st.session_state.messages
            ]
        )

        bot_reply = response.choices[0].message.content

        st.chat_message("assistant").write(bot_reply)
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    except Exception as e:
        st.error(f"Error: {e}")
