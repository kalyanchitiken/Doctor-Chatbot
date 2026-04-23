import streamlit as st
import time
import uuid
from groq_llm import get_response

st.set_page_config(page_title="AI Doctor", page_icon="👩‍⚕️", layout="wide")

# ───── SESSION STATE ─────
if "chats" not in st.session_state:
    st.session_state.chats = {}

if "current_chat" not in st.session_state:
    chat_id = str(uuid.uuid4())
    st.session_state.current_chat = chat_id
    st.session_state.chats[chat_id] = []

# ───── SIDEBAR ─────
with st.sidebar:
    st.title("🩺 AI Doctor")

    # New chat
    if st.button("➕ New Chat"):
        chat_id = str(uuid.uuid4())
        st.session_state.current_chat = chat_id
        st.session_state.chats[chat_id] = []
        st.rerun()

    st.markdown("### 💬 Chats")

    for chat_id in list(st.session_state.chats.keys()):
        messages = st.session_state.chats[chat_id]

        title = "New Chat"
        for msg in messages:
            if msg["role"] == "user":
                title = msg["content"][:30]
                break

        col1, col2 = st.columns([4, 1])

        if col1.button(title, key=chat_id):
            st.session_state.current_chat = chat_id
            st.rerun()

        if col2.button("❌", key=f"del_{chat_id}"):
            del st.session_state.chats[chat_id]

            if st.session_state.current_chat == chat_id:
                new_id = str(uuid.uuid4())
                st.session_state.current_chat = new_id
                st.session_state.chats[new_id] = []

            st.rerun()

# ───── MAIN UI ─────
st.title("👩‍⚕️ Doctor Chatbot")

messages = st.session_state.chats[st.session_state.current_chat]

# Greeting
if len(messages) == 0:
    messages.append({
        "role": "assistant",
        "content": "Hello 👩‍⚕️ I'm your AI Doctor.\n\nHow are you feeling today?"
    })

# Show chat
for msg in messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input
user_input = st.chat_input("Describe your symptoms...")

if user_input:
    messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    conversation_text = "\n".join(
        [f"{m['role']}: {m['content']}" for m in messages]
    )

    # Streaming response
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_text = ""

        with st.spinner("👩‍⚕️ Doctor is thinking..."):
            reply = get_response(conversation_text)

        for word in reply.split():
            full_text += word + " "
            placeholder.markdown(full_text)
            time.sleep(0.04)

    messages.append({"role": "assistant", "content": reply})