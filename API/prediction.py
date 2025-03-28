from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from Scripts.crypto_predictor import get_prediction

router = APIRouter()

class CoinRequest(BaseModel):
    symbol: str

@router.get("/")
async def root():
    return {"message": "Welcome to the Crypto Prediction API"}

@router.post("/predict")
async def predict_crypto(request: CoinRequest):
    try:
        result = get_prediction(request.symbol)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))