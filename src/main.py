from fastapi import FastAPI
from src.logger import setup_logger
from src.config import settings

logger = setup_logger()

app = FastAPI(title=settings.APP_NAME)

@app.get("/health")
def health_check():
    logger.info("Health check endpoint called")
    return {
        "status": "ok",
        "app": settings.APP_NAME
    }
