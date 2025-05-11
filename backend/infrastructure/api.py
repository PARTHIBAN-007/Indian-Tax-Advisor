from contextlib import asynccontextmanager

from fastapi import FastAPI , HTTPException 

from fastapi.middleware.cors import  CORSMiddleware
from opik.integrations.langchain import OpikTracer
from pydantic import BaseModel

from conversation.generate_response import get_response
from conversation.reset_conversation import reset_conversation_chain


@asynccontextmanager
async def lifespan(app:FastAPI):
    yield
    opik_tracer = OpikTracer()
    opik_tracer.flush()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_cridentials = ["*"],
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
    

if __name__=="__main__":
    import uvicorn

    uvicorn.run(app,host="0.0.0.0",port = 8000)
    