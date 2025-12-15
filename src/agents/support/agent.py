from langgraph.graph import StateGraph, START, END

from agents.support.state import State
from agents.support.routes.intent.route import intent_route
from agents.support.nodes.conversation.node import conversation
from agents.support.nodes.extractor.node import extractor
from agents.support.nodes.booking.node import booking_node
# from agents.support.nodes.booking.node import booking_node_f


builder = StateGraph(State) # especificar el tipo de estado que se va a usar
builder.add_node("conversation", conversation) # agregar el nodo que actualiza el estado
builder.add_node("extractor", extractor) # agregar el nodo que actualiza el estado
builder.add_node("booking", booking_node) 
# builder.add_node("booking_node_f", booking_node_f) 
# la convexion es el mismo nombre del nodo

# nodo inicial conectado al nodo 1, y el nodo 1 conectado al nodo final
builder.add_edge(START, 'extractor')
builder.add_conditional_edges('extractor', intent_route) # aqui usamos la funcion de ruteo (en la funcion tenemos que va hacia conversation o booking)
# builder.add_edge('extractor', 'conversation')
builder.add_edge('conversation', END)
builder.add_edge('booking', END)
# builder.add_edge('booking_node_f', END)

# compilar el grafo en un agente ejecutable
agent = builder.compile()