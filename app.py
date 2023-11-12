import os
import openai
import streamlit as st
from streamlit_chat import message

# Set your OpenAI GPT-3 API key
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    st.warning("OpenAI API key not found. Please set it as an environment variable.")
    st.stop()

openai.api_key = api_key

# Define the ChatOpenAI class (assuming it is defined somewhere in your code)
class ChatOpenAI:
    def __init__(self, model, prompt, temperature, max_tokens, top_p, frequency_penalty, presence_penalty, stop):
        # Define the initialization logic for ChatOpenAI
        pass

# Your openai_create function
def openai_create(prompt):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        prompt=prompt,
        temperature=0.9,
        max_tokens=110,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )
    # Perform any necessary processing using the chat instance
    # ...

# Your chatgpt_clone function
def chatgpt_clone(input, history):
    # Assuming the logic for openai_create is correct, use it here
    output = openai_create(input)
    history.append((input, output))
    return history, history

# Streamlit App
st.set_page_config(
    page_title="Streamlit Chat - Demo",
    page_icon=":robot:"
)

st.header("Pātai Bot Aotearoa")

history_input = []

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def get_text():
    input_text = st.text_input("Pātai mai: ", key="input")
    return input_text

user_input = get_text()

if user_input:
    output = chatgpt_clone(user_input, history_input)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output[0])

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
