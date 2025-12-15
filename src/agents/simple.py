# from typing import TypedDict
from langgraph.graph import MessagesState
from langchain_core.messages import AIMessage
import random
from langchain.chat_models import init_chat_model

# llm = init_chat_model("openai:gpt-4o", temperature=1)
llm = init_chat_model("google_genai:gemini-2.5-flash", temperature=0)

# compartir datos o estados entre los agentes, memoria rapida
# class State(TypedDict):
#     customer_name: str
#     my_age: int

class State(MessagesState): # gracias a MessagesState ya tiene messages como clave y parte del estado
    customer_name: str
    my_age: int


# la funcion principal de un nodo es actualizar el estado
def node_1(state: State):
    # # Puedo obtener el historial de mensajes si es necesario
    # history = state["messages"]

    # nuevo estado que se va a devolver
    new_state: State = {}

    if state.get("customer_name") is None:
        # # devolver solo lo que se actualiza en el estado
        # return {
        #     "customer_name": "John Doe"
        # }
        new_state["customer_name"] = "John Doe"
    # return {
    #     "my_age": 30
    # }
    # else:
    #     ai_msg = AIMessage(content=f"Hello, {state.get('customer_name')}! How can I assist you today?")
    #     return {
    #         "messages": [ai_msg] # agrega mensaje AI al estado o como un append, solo se retorna el mensaje que se va a agregar
    #     }
    else:
        new_state["my_age"] = random.randint(20, 30)

    history = state["messages"]
    ai_message = llm.invoke(history)
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