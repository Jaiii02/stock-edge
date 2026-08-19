import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from analyzer import analyze_stock
from app.core.config import DATA_PATH, FRONTEND_ORIGINS


app = FastAPI()

df = pd.read_csv(DATA_PATH)

app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "StockEdge API is running!"}


@app.get("/symbols")
def get_symbols():
    return df["Symbol"].tolist()


@app.get("/analyze/{symbol}")
def analyze(symbol: str):
    return analyze_stock(symbol.upper())
