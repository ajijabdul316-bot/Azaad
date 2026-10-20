
import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="My AI Chatbot",
    page_icon="❤️‍🩹"
)

st.title("Delulu is not solulu")
st.caption("Powered by OpenAI")

# Read API key securely
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except (KeyError, FileNotFoundError):
    st.error("API key set nahi hai. Secrets configure karo.")
    st.stop()

client = OpenAI(api_key=api_key)

# Keep chat history during the session
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi! Main tumhara AI assistant hoon. Kya poochna hai?"
        }
    ]

# Display old messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input box
prompt = st.chat_input("Message type karo...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("AI soch raha hai..."):
                response = client.responses.create(
                    model="gpt-4.1-mini",
                    instructions=(
                        "You are a helpful AI assistant. "
                        "Explain things clearly and simply."
                    ),
                    input=st.session_state.messages,
                    max_output_tokens=800
                )

                answer = response.output_text
                st.markdown(answer)

            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )

        except Exception:
            st.error(
                "Request fail hua. API key, billing, "
                "model access aur internet connection check karo."
            )

if st.sidebar.button("Clear chat"):
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Chat clear ho gayi! Naya question poochho."
        }
    ]
    st.rerun()
  
