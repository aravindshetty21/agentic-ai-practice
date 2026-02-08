from debugpy.common.messaging import InvalidMessageError
from pydantic import BaseModel, Field
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage


class ChatHistory(BaseChatMessageHistory, BaseModel):

    messages: list[BaseMessage] = Field(default_factory=list)

    def add_message(self, message: BaseMessage):
        self.messages.append(message)

    def clear(self):
        self.messages = []

def get_history():
    return ChatHistory()
