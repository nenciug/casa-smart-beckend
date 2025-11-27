# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

# Dacă folosești OpenAI pentru recomandări AI
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")  # setează cheia în mediu

app = FastAPI()

# Configurare CORS
origins = [
    "https://casasmart-ai.vercel.app",  # domeniul frontend-ului tău
    "http://localhost:3000",            # pentru test local
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # sau ["*"] pentru toate originile
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model pentru request
class RecommendationRequest(BaseModel):
    query: str

# Model pentru response
class RecommendationResponse(BaseModel):
    recommendations: List[str]

@app.post("/recommend", response_model=RecommendationResponse)
async def recommend(data: RecommendationRequest):
    query_text = data.query

    # Exemplu simplu: folosește OpenAI GPT
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ești un consultant pentru case inteligente."},
                {"role": "user", "content": query_text}
            ],
            max_tokens=300
        )

        # Extrage textul recomandării
        answer = response.choices[0].message['content'].strip()
        # Poți împărți răspunsul pe linii dacă vrei lista
        recommendations = [line.strip() for line in answer.split("\n") if line.strip()]
        return RecommendationResponse(recommendations=recommendations)

    except Exception as e:
        print("Eroare OpenAI:", e)
        return RecommendationResponse(recommendations=["Eroare la generarea recomandărilor."])
