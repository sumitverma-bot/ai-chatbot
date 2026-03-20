import streamlit as st
from groq import Groq

if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()
    
# Page config
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")

# Title
st.title("🤖 Mimi Cheeku Chatbot")

# Initialize Groq client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
user_input = st.chat_input("Type your message...")

if user_input:
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Display user message
    with st.chat_message("user"):
        st.write(user_input)

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=st.session_state.messages
            )

            bot_reply = response.choices[0].message.content
            st.write(bot_reply)

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply
    })
