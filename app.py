import os
import openai
import streamlit as st
from streamlit_chat import message

# Set your OpenAI API key
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    st.warning("OpenAI API key not found. Please set it as an environment variable.")
    st.stop()

openai.api_key = api_key

# Streamlit app config
st.set_page_config(
    page_title="Pātai Bot Aotearoa",
    page_icon=":robot:"
)

st.header("🤖 Pātai Bot Aotearoa")

# --- Select GPT model ---
model_choice = st.selectbox(
    "Kōwhiria he tauira (Choose a model):",
    options=["gpt-3.5-turbo", "gpt-4"],
    index=0
)

# --- Session state setup ---
if 'history' not in st.session_state:
    st.session_state['history'] = [{'role': 'system', 'content': 'You are a helpful assistant from Aotearoa who answers in a kind and knowledgeable way.'}]
if 'past_inputs' not in st.session_state:
    st.session_state['past_inputs'] = []
if 'responses' not in st.session_state:
    st.session_state['responses'] = []

# --- Call OpenAI's API ---
def openai_create(messages, model):
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7
    )
    return response.choices[0].message.content

# --- Chat handler ---
def chatgpt_clone(user_input, history, model):
    history.append({'role': 'user', 'content': user_input})
    reply = openai_create(messages=history, model=model)
    history.append({'role': 'assistant', 'content': reply})
    return history, reply

# --- Text input ---
def get_text():
    return st.text_input("Pātai mai: ", key="input")

user_input = get_text()

# --- Run chat logic ---
if user_input:
    st.session_state['past_inputs'].append(user_input)
    st.session_state['history'], output = chatgpt_clone(user_input, st.session_state['history'], model_choice)
    st.session_state['responses'].append(output)

# --- Display conversation ---
if st.session_state['responses']:
    for i in range(len(st.session_state['responses']) - 1, -1, -1):
        message(st.session_state['responses'][i], key=f"bot_{i}")
        message(st.session_state['past_inputs'][i], is_user=True, key=f"user_{i}")