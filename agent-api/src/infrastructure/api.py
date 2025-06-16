import sys
import os

# Add the parent of `src` to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from contextlib import asynccontextmanager

from fastapi import FastAPI , HTTPException 

from fastapi.middleware.cors import  CORSMiddleware
from opik.integrations.langchain import OpikTracer
from pydantic import BaseModel

from application.conversation_service.reset_conversation import reset_conversation_chain


@asynccontextmanager
async def lifespan(app:FastAPI):
    yield
    opik_tracer = OpikTracer()
    opik_tracer.flush()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"],
)


class ChatMessage(BaseModel):
    message: str



from application.conversation_service.generate_response import GraphBuilding 

obj = None
def create_user_id(id):
    global obj
    obj = GraphBuilding(id)
    return obj

from collections import defaultdict

user_db = []
class Formdata(BaseModel):
    email :str
    username:str  

import uuid


@app.post("/chat")
async def chat(chat_message: ChatMessage):
    try:

        response =  await obj.generate_response(
            messages=chat_message.message
        )

        return {"response": response}
    except Exception as e:
        opik_tracer = OpikTracer()
        opik_tracer.flush()

        raise HTTPException(status_code=500,detail = str(e))

@app.post("/user")
async def user_data(data:Formdata):
    for user in user_db:
        if user["email"] == data.email:
            return {"message": "user Already Exists","id":user["id"]}
    user_id = str(uuid.uuid4)
    new_user = {"id":user_id,"email":data.email,"username":data.username}
    user_db.append(new_user)
    create_user_id(user_id)

    return {"message": "New User Created","id":new_user["id"]}


    
@app.post("/reset-memory")
async def reset_conversation():
    try:
        result = await reset_conversation_chain()
        return result
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
@app.post("/save_docs")
async def save_docs():
    try:
        obj.embed_conversation()
        return {"Sucessfully Saved in Qdrant"}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))


if __name__=="__main__":
    import uvicorn

    uvicorn.run(app,host="0.0.0.0",port = 8000)
    