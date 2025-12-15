from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field

from agents.support.state import State
from agents.support.nodes.extractor.prompt import prompt_template

class ContactInfo(BaseModel):
    """Contact information for a person."""
    name: str = Field(description="The name of the person")
    email: str = Field(description="The email address of the person")
    phone: str = Field(description="The phone number of the person")
    age: str = Field(description="The age of the person")

llm_with_structured_output = init_chat_model("openai:gpt-5-nano", temperature=0) # puede ser otro modelo
llm_with_structured_output = llm_with_structured_output.with_structured_output(schema=ContactInfo)

def extractor(state: State):
    history = state["messages"] # historial de mensajes
    customer_name = state.get("customer_name", None)
    new_state: State = {}
    if customer_name is None or len(history) >= 10: # mayor a 10 mensajes, volver a extraer para actualizar datos
        prompt = prompt_template.format()
        schema = llm_with_structured_output.invoke([("system", prompt)] + history)
        new_state["customer_name"] = schema.name
        new_state["phone"] = schema.phone
        new_state["my_age"] = schema.age

    # devolver new_state con los datos extraidos no limpia messages o estado anterior
    # es equivalente a state = {
    #     **state,
    #     **new_state
    # }
    # si quieres controlar el crecimiento del historial, hazlo en un nodo dedicado:
    """
    def trim_history(state: State):
    return {
        "messages": state["messages"][-10:]
    }
    """
    return new_state
