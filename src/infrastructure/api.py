import sys
import os

# Add the parent of `src` to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from application.conversation_service.generate_response import get_response

from contextlib import asynccontextmanager

from fastapi import FastAPI , HTTPException 

from fastapi.middleware.cors import  CORSMiddleware
from opik.integrations.langchain import OpikTracer
from pydantic import BaseModel

from application.conversation_service.generate_response import get_response
from application.conversation_service.reset_conversation import reset_conversation_chain
from application.conversation_service.embed_conversation import embed_conversation


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


@app.post("/chat")
async def chat(chat_message: ChatMessage):
    try:
        response = await get_response(
            messages=chat_message.message
        )

        return {"response": response}
    except Exception as e:
        opik_tracer = OpikTracer()
        opik_tracer.flush()

        raise HTTPException(status_code=500,detail = str(e))
    
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
        embed_conversation()
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    

if __name__=="__main__":
    import uvicorn

    uvicorn.run(app,host="0.0.0.0",port = 8000)
    