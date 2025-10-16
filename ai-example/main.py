import random
from utils import read_secret

from pydantic import BaseModel
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool


model = init_chat_model(
    model="genai-demo",
    model_provider="azure_openai",
    # azure_deployment="your-deployment",
    api_version="2024-12-01-preview",
    azure_endpoint=read_secret('azure-endpoint'),
    api_key=read_secret("azure-key"),
    temperature=0,
)

@tool("get_city")
def get_city() -> str:
    """Get the city."""
    cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Berlin", "London", "Tokyo"]
    return random.choice(cities)

@tool("get_weather")
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

class WeatherResponse(BaseModel):
    conditions: str

agent = create_react_agent(
    model=model,
    tools=[get_weather, get_city],
    response_format=WeatherResponse,
    prompt="You are a helpful assistant that provides weather information for the retrieved city.",
)

# Run the agent
response = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather?"}]}
)

print(response["structured_response"])