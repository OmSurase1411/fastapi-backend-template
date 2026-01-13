from fastapi import APIRouter
from src.logger import setup_logger

router = APIRouter()
logger = setup_logger()

@router.get("/ping")
def ping():
    logger.info("ping endpoint called")
    return {"message":"pong"}

