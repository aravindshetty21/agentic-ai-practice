
from dotenv import load_dotenv
load_dotenv()

from model import get_model
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langgraph.checkpoint.memory import InMemorySaver
from dataclasses import dataclass
from langchain_core.output_parsers import StrOutputParser
from langchain.tools import tool, ToolRuntime


chat_model = get_model()

@dataclass
class ContextSchema:
    '''Location required to fetch weather information.'''
    location: str

@tool
def get_weather_from_location(runtime: ToolRuntime[ContextSchema]) -> str:
    """Fetches weather information for the given location."""
    return f"The weather in {runtime.context.location} is sunny with a high of 75°F."


@dataclass
class ResponseFormat:
    '''The weather report for the specified location.'''
    weather_report: str

checkpointer = InMemorySaver()

weather_report_agent = create_agent(
    model=chat_model,
    tools=[get_weather_from_location],
    context_schema=ContextSchema,
    response_format=ToolStrategy(ResponseFormat),
    checkpointer=checkpointer
)

# `thread_id` is a unique identifier for a given conversation.
config = {"configurable": {"thread_id": "1"}}

while(True):
    try:
        ipt = input()
        if str(ipt).lower() == "exit":
            break
        elif str(ipt).strip() == "":
            continue
        print("Fetching weather report...")
        response = weather_report_agent.invoke(
            {"messages": [{"role": "user", "content": str(ipt)}]},
            config=config,
            context=ContextSchema(location="India")
        )
        print(response["structured_response"].weather_report)
    except Exception as e:
        print(f"Error occurred: {e}. Retrying...")