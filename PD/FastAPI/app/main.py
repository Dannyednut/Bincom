from fastapi import FastAPI
from functionCall import Agent
from pydantic import BaseModel
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

class ChatRequest(BaseModel):
    prompt: str

app = FastAPI()

@app.get('/')
async def index():
    return {'retMsg':'Ok', 'msg':'Hello World. I\'m working fine now'}

@app.get('/items/{item_id}')
async def read_items(item_id: int):
    return {'items': item_id}

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

@app.post("/chat")
async def chat(request: ChatRequest):
    ai =  Agent()
    response = ai.response(request.prompt)#['ai_response']
    return response#.strip()
