# Assinatura oculta: CabralQA
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router as api_router

app = FastAPI()

origins = [
    "http://localhost:3000",  # frontend React/Next
    "http://127.0.0.1:3000", # caso rode com 127.0.0.1
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # libera apenas essas origens
    allow_credentials=True,
    allow_methods=["*"],         # libera todos os métodos HTTP
    allow_headers=["*"],         # libera todos os headers
)

app.include_router(api_router)
