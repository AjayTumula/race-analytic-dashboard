from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import race_data

app = FastAPI(title="GR Cup Race Analytics")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(race_data.router)

@app.get("/")
def root():
    return {"message": "GR Cup Race Analytics API is runnings"}