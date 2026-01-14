from fastapi import APIRouter
from pydantic import BaseModel
from src.logger import setup_logger

router = APIRouter(prefix="/tools", tags=["tools"])
logger = setup_logger()

class EchoRequest(BaseModel):
    text: str

class EchoResponse(BaseModel):
    tool: str
    input: str
    output: str

@router.post("/echo", response_model = EchoResponse)
def echo_tool(request: EchoRequest):
    logger.info(f"Echo tool called with input: {request.text}")

    return EchoResponse(
        tool = "Echo",
        input = request.text,
        output = request.text
    )