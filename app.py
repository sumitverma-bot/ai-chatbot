import streamlit as st

with st.sidebar:
    st.title("⚙️ Settings")
    st.write("Model: llama-3.3-70b-versatile")
    st.write("Built by Sumit Verma")

if st.button("🧹 Clear Chat"):
    st.session_state.messages = []

import streamlit as st
from groq import Groq

# 🔑 Add your API key
client = Groq(api_key="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")

st.title("🤖 Sumit's AI Chatbot")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# User input
user_input = st.chat_input("Type your message...")

if user_input:
    # Show user message
    st.chat_message("user").write(user_input)

    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        # AI response
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages
        )

        bot_reply = response.choices[0].message.content

        # Show bot reply
        st.chat_message("assistant").write(bot_reply)

        # Save bot reply
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    except Exception as e:
        st.error(f"Error: {e}")