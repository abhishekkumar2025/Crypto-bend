from fastapi import APIRouter
from API.prediction import router as prediction_router

api_router = APIRouter()

api_router.include_router(prediction_router, tags=["prediction"])