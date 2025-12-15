from dotenv import load_dotenv
load_dotenv() # hay que cargar las variables de entorno antes de cualquier otra cosa

from pydantic import BaseModel

from fastapi import FastAPI
from agents.support.agent_with_check import make_graph
from agents.simple import agent
from langchain_core.messages import HumanMessage
from fastapi.responses import StreamingResponse # esto es para que vaya enviando datos poco a poco
from api.db import lifespan, CheckpointerDep

app = FastAPI(lifespan=lifespan)
# app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}



class Message(BaseModel):
    message: str


@app.post("/chat/{chat_id}") # item sera el body
async def chat(chat_id: str, item: Message):
    human_message = HumanMessage(content=item.message)
    response = agent.invoke({"messages": [human_message]}) # lo recibe como messages ya que el estado del agente es un diccionario con messages
    last_message = response["messages"][-1]
    return last_message.text # o last_message.content
    # return await agent.ainvoke({"messages": [human_message]}) # si es asincrono es ainvoke, si no es solo se pone invoke
    # return {"chat_id": chat_id, "message": item.message}

@app.post("/chat_checkpoint/{chat_id}")
async def chat(chat_id: str, item: Message, checkpointer: CheckpointerDep): # necesita el checkpointer como dependencia
    # CRUD add message
    config = {
        "configurable": {
            "thread_id": chat_id, # saber que estado es
        }
    }
    human_message = HumanMessage(content=item.message)
    agent_check = make_graph(config={"checkpointer": checkpointer})
    state = {"messages": [human_message], "customer_name": "John Doe"}
    response = agent_check.invoke(state, config)
    last_message = response["messages"][-1]
    # CRUD add message
    return response["messages"] # aqui retornamos todo el historial de mensajes completo


# Streaming endpoint
@app.post("/chat/{chat_id}/stream")
async def stream_chat(chat_id: str, message: Message):
    human_message = HumanMessage(content=message.message)
    async def generate_response():
        for message_chunk, metadata in agent.stream({"messages": [human_message]}, stream_mode="messages"):
            if message_chunk.content:
                yield f"data: {message_chunk.content}\n\n"

        print(message_chunk.content, end="|", flush=True)

    return StreamingResponse(generate_response(), media_type="text/event-stream")

# @app.post("/chat/{chat_id}/stream")
# async def stream_chat(chat_id: str, message: Message, checkpointer: CheckpointerDep):
#     human_message = HumanMessage(content=message.message)
#     async def generate_response():
#         agent_check = make_graph(config={"checkpointer": checkpointer})
#         for message_chunk, metadata in agent_check.stream({"messages": [human_message]}, stream_mode="messages"):
#             if message_chunk.content:
#                 yield f"data: {message_chunk.content}\n\n"

#         print(message_chunk.content, end="|", flush=True)

#     return StreamingResponse(generate_response(), media_type="text/event-stream")