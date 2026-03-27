import streamlit as st
from chatbot import answer

st.set_page_config(page_title="TechDocs Solutions", page_icon="💬")

st.title("💬 TechDocs Solutions - Atendimento Automatizado")
st.write("Faça uma pergunta sobre os produtos e serviços.")

if "history" not in st.session_state:
    st.session_state.history = []

question = st.chat_input("Digite sua pergunta...")

if question:
    response = answer(question)

    st.session_state.history.append(("user", question))
    st.session_state.history.append(("bot", response))

for role, message in st.session_state.history:
    with st.chat_message("user" if role == "user" else "assistant"):
        st.write(message)