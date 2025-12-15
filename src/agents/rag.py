from langgraph.graph import MessagesState
from langchain.chat_models import init_chat_model
import random

llm = init_chat_model("openai:gpt-5-nano", temperature=0)
file_search_tool = {
    "type": "file_search",
    "vector_store_ids": ["vs_693dfbd8a488819194da68c87493f8bc"],
}
llm = llm.bind_tools([file_search_tool])

class State(MessagesState):
    customer_name: str
    my_age: str
    phone: str


# Structure for extracted contact info
from pydantic import BaseModel, Field

class ContactInfo(BaseModel):
    """Contact information for a person."""
    name: str = Field(description="The name of the person")
    email: str = Field(description="The email address of the person")
    phone: str = Field(description="The phone number of the person")
    age: str = Field(description="The age of the person") # si inicia como int puede dar error al inicio porque no hay valor


llm_with_structured_output = init_chat_model("openai:gpt-5-nano", temperature=0) # puede ser otro modelo
llm_with_structured_output = llm_with_structured_output.with_structured_output(schema=ContactInfo)

def extractor(state: State):
    history = state["messages"] # historial de mensajes
    customer_name = state.get("customer_name", None)
    new_state: State = {}
    if customer_name is None or len(history) >= 10: # mayor a 10 mensajes, volver a extraer para actualizar datos
        schema = llm_with_structured_output.invoke(history)
        new_state["customer_name"] = schema.name
        new_state["phone"] = schema.phone
        new_state["my_age"] = schema.age
    return new_state

def conversation(state: State):
    new_state: State = {}

    # if state.get("customer_name") is None:
    #     new_state["customer_name"] = "John Doe"
    # else:
    #     new_state["my_age"] = random.randint(20, 30)

    history = state["messages"]
    # SOLO ENVIARLE EL ULTIMO PARA NO GASTAR TOKENS
    last_message = history[-1] if history else None
    
    customer_name = state.get("customer_name", 'John Doe')
    system_message = f"You are a helpful assistant that can answer questions about the customer {customer_name}"
    # ai_message = llm.invoke(last_message.text)
    ai_message = llm.invoke([("system", system_message), ("user", last_message.text)])
    new_state["messages"] = [ai_message] # aqui se esta guardando solo la respuesta del agente, como formateo del estado messages
    # para concatenar todo el historial, se tendria que hacer un append del historial anterior + la nueva respuesta o solo un mas como 
    # "history + [AIMessage(content="Message from the AI")]"
    return new_state



from langgraph.graph import StateGraph, START, END

builder = StateGraph(State) # especificar el tipo de estado que se va a usar
builder.add_node("conversation", conversation) # agregar el nodo que actualiza el estado
builder.add_node("extractor", extractor) # agregar el nodo que actualiza el estado
# la convexion es el mismo nombre del nodo

# nodo inicial conectado al nodo 1, y el nodo 1 conectado al nodo final
builder.add_edge(START, 'extractor')
builder.add_edge('extractor', 'conversation')
builder.add_edge('conversation', END)

# compilar el grafo en un agente ejecutable
agent = builder.compile()