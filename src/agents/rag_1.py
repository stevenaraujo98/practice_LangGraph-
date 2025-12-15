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


# la funcion principal de un nodo es actualizar el estado
def node_1(state: State):
    new_state: State = {}

    if state.get("customer_name") is None:
        new_state["customer_name"] = "John Doe"
    else:
        new_state["my_age"] = random.randint(20, 30)

    history = state["messages"]
    # SOLO ENVIARLE EL ULTIMO PARA NO GASTAR TOKENS
    last_message = history[-1] if history else None
    ai_message = llm.invoke(last_message.text)
    new_state["messages"] = [ai_message]
    return new_state


from langgraph.graph import StateGraph, START, END

builder = StateGraph(State) # especificar el tipo de estado que se va a usar
builder.add_node("node_1", node_1) # agregar el nodo que actualiza el estado
# la convexion es el mismo nombre del nodo

# nodo inicial conectado al nodo 1, y el nodo 1 conectado al nodo final
builder.add_edge(START, 'node_1')
builder.add_edge('node_1', END)

# compilar el grafo en un agente ejecutable
agent = builder.compile()