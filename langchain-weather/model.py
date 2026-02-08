from langchain.chat_models import init_chat_model

model = init_chat_model("gpt-5-nano", max_tokens=1000)

def get_model():
    return model