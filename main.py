from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from crypto_predictor import get_prediction
from pydantic import BaseModel

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class CoinRequest(BaseModel):
    symbol: str

@app.get("/")
async def root():
    return {"message": "Welcome to the Crypto Prediction API"}

@app.post("/predict")
async def predict_crypto(request: CoinRequest):
    try:
        result = get_prediction(request.symbol)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
