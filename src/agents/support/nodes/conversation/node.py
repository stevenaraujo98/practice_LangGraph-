from agents.support.state import State
from langchain.chat_models import init_chat_model
from agents.support.nodes.conversation.tools import tools
# from agents.support.nodes.conversation.prompt import prompt_template
from langchain_core.messages import AIMessage

llm = init_chat_model("openai:gpt-5-nano", temperature=0)
llm = llm.bind_tools(tools)


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
    # prompt = prompt_template.format(name=customer_name)
    prompt = f"You are a helpful assistant that can answer questions about the customer {customer_name}"
    print('*'*100)
    print(last_message.text)
    
    # ai_message = llm.invoke(last_message.text)
    ai_message = llm.invoke([("system", prompt), ("user", last_message.text)])
    ai_message = AIMessage(content=ai_message.text)  # es importante convertir la respuesta a AIMessage y parsear el texto correctamente para que no se pierda el formato
    # o se guarde informacion extraña que no sea solo el contenido del mensaje. Ya que no se parse la respuesta, puede venir con metadatos adicionales.

    # solo se aisló la ultima interaccion para ahorrar tokens.
    new_state["messages"] = [ai_message] # aqui se esta guardando la respuesta del agente, 
    # no es necesario hacer "history + [AIMessage(content="Message from the AI")]" ya que al igualar a una lista nueva, 
    # se extiende el historial automaticamente en el framework del grafo de estados.
    return new_state