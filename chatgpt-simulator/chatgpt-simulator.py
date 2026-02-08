import uuid

from dotenv import load_dotenv
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory, ConfigurableFieldSpec
from langchain_openai import ChatOpenAI


load_dotenv()

model = ChatOpenAI(model="gpt-5-nano")

prompt = ChatPromptTemplate.from_messages(
    [
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)

chain = prompt | model

import streamlit as st

st.title("Chatgpt-simulator")

if "store" not in st.session_state:
    st.session_state.store = {}

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "conversation_list" not in st.session_state:
    st.session_state.conversation_list = [st.session_state.session_id]


def createConversation():
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.conversation_list.append(st.session_state.session_id)


def get_session_history(session_id: str) -> FileChatMessageHistory:
    if session_id not in st.session_state.store:
        st.session_state.store[session_id] = FileChatMessageHistory("../chat-files/" + session_id)
    return st.session_state.store[session_id]


chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history",
)

with st.sidebar:
    if st.button("New Conversation"):
        createConversation()

    selected_conversation = st.selectbox(options=list(st.session_state.conversation_list), label="Choose a conversation",
                            index=st.session_state.conversation_list.index(st.session_state.session_id))

    if selected_conversation != st.session_state.session_id:
        st.session_state.session_id = selected_conversation



prompt = st.chat_input("Ask a question")
config = {"configurable": {"session_id": st.session_state.session_id}}
history = get_session_history(st.session_state.session_id).messages


def getRole(message):
    if type(message) == AIMessage:
        return "assistant"
    if type(message) == HumanMessage:
        return "user"
    return "system"
for message in history:
    with st.chat_message(getRole(message)):
        st.markdown(message.content)

if(prompt):
    with st.chat_message("user"):
        st.markdown(prompt)
    response = chain_with_history.invoke({"question": prompt}, config=config)
    with st.chat_message("assistant"):
        st.markdown(response.content)


