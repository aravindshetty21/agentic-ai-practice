from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-5-nano")

def get_model():
    return model