from fastapi import FastAPI
import os
import openai

app = FastAPI()
openai.api_key = os.getenv("OPENAI_API_KEY")

