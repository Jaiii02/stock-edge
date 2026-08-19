from fastapi import APIRouter


router = APIRouter(tags=["health"])


@router.get("/")
def home():
    return {"message": "StockEdge API is running!"}
