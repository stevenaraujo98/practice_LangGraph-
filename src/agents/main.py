from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

@tool
async def get_weather(city: str) -> str:
    """Devuelve el clima para la ciudad dada."""
    return f"It's always sunny in {city}!"

model_g = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", #"gemini-3-pro-preview",
    temperature=1.0,  # Gemini 3.0+ defaults to 1.0
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

agent = create_agent(
    model=model_g,
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)
