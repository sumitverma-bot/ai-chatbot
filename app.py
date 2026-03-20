import streamlit as st
from groq import Groq
from pypdf import PdfReader

st.set_page_config(page_title="Business Chatbot", page_icon="🤖")

# Sidebar (branding + settings)
with st.sidebar:
    st.title("⚙️ Settings")

    company_name = st.text_input("Verma Enterprises Pvt. Ltd", "My Business")

    system_prompt = st.text_area(
        "Bot Instructions",
        f"You are a helpful assistant for {company_name}. Answer customer questions clearly."
    )

    st.markdown("---")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Groq client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# PDF Upload
uploaded_file = st.file_uploader("📄 Upload Company PDF (optional)", type="pdf")

pdf_text = ""
if uploaded_file:
    reader = PdfReader(uploaded_file)
    for page in reader.pages:
        pdf_text += page.extract_text()
    st.success("✅ PDF loaded")

# Title
st.title(f"🤖 {company_name} Assistant")

# Show messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input
user_input = st.chat_input("Ask something...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            messages = [
                {
                    "role": "system",
                    "content": system_prompt + "\n\nUse this data if available:\n" + pdf_text
                }
            ] + st.session_state.messages

            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages
            )

            reply = response.choices[0].message.content
            st.write(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
