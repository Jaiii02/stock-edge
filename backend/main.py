from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from analyzer import analyze_stock
import pandas as pd

app = FastAPI()

df = pd.read_csv("./data/nifty500nse.csv")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
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


