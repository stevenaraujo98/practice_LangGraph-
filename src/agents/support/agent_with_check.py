from langgraph.graph import StateGraph, START, END

from agents.support.state import State
from agents.support.routes.intent.route import intent_route
from agents.support.nodes.conversation.node import conversation
from agents.support.nodes.extractor.node import extractor
from agents.support.nodes.booking.node import booking_node

from langgraph.checkpoint.postgres import PostgresSaver
# https://pypi.org/project/langgraph-checkpoint-postgres/

def make_graph(config: dict):
    checkpointer: PostgresSaver = config.get("checkpointer", None)
    builder = StateGraph(State, checkpointer=checkpointer) # especificar el tipo de estado que se va a usar
    builder.add_node("conversation", conversation) # agregar el nodo que actualiza el estado
    builder.add_node("extractor", extractor) # agregar el nodo que actualiza el estado
    builder.add_node("booking", booking_node) 
    # la convexion es el mismo nombre del nodo

    # nodo inicial conectado al nodo 1, y el nodo 1 conectado al nodo final
    builder.add_edge(START, 'extractor')
    builder.add_conditional_edges('extractor', intent_route) # aqui usamos la funcion de ruteo (en la funcion tenemos que va hacia conversation o booking)
    # builder.add_edge('extractor', 'conversation')
    builder.add_edge('conversation', END)
    builder.add_edge('booking', END)

    # compilar el grafo en un agente ejecutable
    agent = builder.compile(checkpointer=checkpointer)
    return agent
