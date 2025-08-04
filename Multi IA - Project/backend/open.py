import markdown2
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import OpenAI

from dotenv import load_dotenv

# from .utils import Utils


app = FastAPI()

# CORS: Permitir llamadas desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Modelo del JSON que recibes
class Prompt(BaseModel):
    prompt: str

@app.post("/api/fake")
async def recibir_dato(data: Prompt):


    #OPEN AI
    client = OpenAI( api_key= os.getenv('OPENAI_API_KEY'))

    response = client.responses.create(
    model="gpt-4o-mini",
    input=data.prompt,
    store=True,
    )


    return {
        "openai": f"{markdown2.markdown(response.output_text)}",
    }
  