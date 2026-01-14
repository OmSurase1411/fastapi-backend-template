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

# -------UPPERCASE TOOL =----------

class UppercaseRequest(BaseModel):
    text: str

class UppercaseResponse(BaseModel):
    tool: str
    input: str
    output: str

@router.post("/uppercase", response_model=UppercaseResponse)
def uppercase_tool(request: UppercaseRequest):
    logger.info(f"Uppercase tool called with input: {request.text}")
    upper = request.text.upper()
    return UppercaseResponse(
        tool="uppercase",
        input=request.text,
        output=upper
    )

