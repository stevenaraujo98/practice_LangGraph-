from langchain.agents import create_agent

from agents.support.nodes.booking.tools import tools
from agents.support.nodes.booking.prompt import prompt_template
from langchain_google_genai import ChatGoogleGenerativeAI


model_g = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", #"gemini-3-pro-preview",
    temperature=1.0,  # Gemini 3.0+ defaults to 1.0
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# a este agente se le comparte todo el historial de la conversacion
# no es recomendable para conversaciones largas, ya que se pueden gastar muchos tokens
# langchain ejecuta agentes
booking_node = create_agent(
    model=model_g,
    tools=tools,
    system_prompt=prompt_template.format(),
)


######
from typing import TypedDict, List
from langchain_core.messages import AIMessage
from agents.support.state import State

def booking_node_f(state: State):
    # Solo enviamos el último mensaje al agente
    # last_message = state["messages"][-1]
    history = state["messages"]


    # El agente devuelve texto plano
    response = booking_node.invoke({"messages": history}) # gracias al response_format="text",
    last_message = response["messages"][-1]

    # Actualizamos el estado manteniendo el historial
    return {
        "messages": [AIMessage(content=last_message)]
    }

    # lo siguiente esta mal porque
    # Esto toma la lista vieja y le pega el mensaje nuevo.
    # Resultado en el estado: [Mensaje1, Mensaje2, Mensaje1, Mensaje2, MensajeNuevo]
    # ¡DUPLICAS TODO EL HISTORIAL!
    # return {
    #     "messages": state["messages"] + [
    #         AIMessage(content=response_text)
    #     ]
    # }
