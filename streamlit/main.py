import streamlit as st
import requests
import os
from streamlit_javascript import st_javascript
from dotenv import load_dotenv

load_dotenv(override=True)

API_URL = os.getenv("API_URL")

def register_user(username, password):
    response = requests.post(f"{API_URL}/auth/register", json={"username": username, "password": password})
    return response

def login_user(username, password):
    response = requests.post(f"{API_URL}/auth/token", data={"username": username, "password": password})
    if response.status_code == 200:
        return response.json().get("access_token")
    return None

def send_question(token, question):
    print(f"question=={question}")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {"question": question}
    print("Enviando dados:", data)
    response = requests.post(f"{API_URL}/chat/chat", headers=headers, json=data)
    return response.json()

def set_token_local(token):
    st_javascript(f"localStorage.setItem('authToken', '{token}');")

def get_token_local():
    token = st_javascript("localStorage.getItem('authToken');")
    return token

def register_screen():
    st.subheader("Registrar novo usuário")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    if st.button("Registrar"):
        response = register_user(username, password)
        if response.status_code == 200:
            st.success("Usuário registrado com sucesso! Faça login para continuar.")
        else:
            st.error("Erro ao registrar. Nome de usuário pode já estar em uso.")

def login_screen():
    st.subheader("Login de Usuário")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    if st.button("Login"):
        token = login_user(username, password)
        if token:
            st.session_state["token"] = token
            set_token_local(token)
            st.success("Login realizado com sucesso!")
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos.")

def chat_screen():
    st.subheader("Chat")
    question = st.text_input("Digite sua pergunta")
    if st.button("Enviar"):
        if question:
            response = send_question(st.session_state["token"], question)
            st.write("Resposta:", response.get("text", "Erro ao obter resposta."))
        else:
            st.error("Por favor, insira uma pergunta.")
    if st.button("Sair"):
        st.session_state["token"] = None
        st.rerun()

def main():
    st.title("Chat com Autenticação")

    if "token" not in st.session_state:
        st.session_state["token"] = get_token_local()
        print(f'token if == {st.session_state["token"]}')
    else:
        print(f'token else == {st.session_state["token"]}')

    if not st.session_state["token"]:
        menu = ["Login", "Registrar"]
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Registrar":
            register_screen()
        else:
            login_screen()
    else:
        chat_screen()

if __name__ == "__main__":
    main()
