from pydantic import BaseModel, Field
from typing import Literal
from langchain.chat_models import init_chat_model
from agents.support.state import State
from agents.support.routes.intent.prompt import SYSTEM_PROMPT

# Con BaseModel definimos el esquema de salida esperado como JSON pero es una clase de Python
class RouteIntent(BaseModel):
    # Puede ser conversation o booking
    step: Literal["conversation", "booking"] = Field(
        'conversation', description="The next step in the routing process"
    ) # por defecto retorna conversation con el Field

llm = init_chat_model("openai:gpt-4o", temperature=0)
llm = llm.with_structured_output(schema=RouteIntent)

def intent_route(state: State) -> Literal["conversation", "booking"]:
    # este routing toma toda la conversacion hasta el momento, se podria hacer un resumen o el ultimo mensaje
    history = state["messages"]
    print('*'*100)
    print(history)
    print('*'*100)
    schema = llm.invoke([("system", SYSTEM_PROMPT)] + history)
    print('Ruteo a:', schema.step) # Para ver en consola a donde se rutea
    if schema.step is not None: # por si acaso venga nulo
        return schema.step
    return 'conversation'