from pyexpat.errors import messages
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

def getResponse(messages):
  response = client.chat.completions.create(
    model="gpt-5-nano",
    messages=messages
  )

  return response.choices[0].message.content

st.title("Chatbot with GPT-5 Nano")
# st.write("Ask anything to the chatbot!")
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt =st.chat_input("whats on your mind?")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    response = getResponse(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

# if prompt:
#   with st.chat_message("user"):
#     st.markdown(prompt)
#     messages = [{"role": "user", "content": prompt}]
#     response = getResponse(messages)
#   with st.chat_message("assistant"):
#     st.markdown(response)
