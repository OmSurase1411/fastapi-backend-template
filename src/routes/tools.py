from fastapi import APIRouter
from pydantic import BaseModel
from src.logger import setup_logger


router = APIRouter(prefix="/tools", tags=["tools"])
logger = setup_logger()

FAKE_CUSTOMERS = {
    "CUST123": {
        "name": "Om Surase",
        "email": "om@example.com",
        "status": "Active"
    },
    "CUST456": {
        "name": "Nidhi Chaubey",
        "email": "nidhi@example.com",
        "status": "Inactive"
    },
    "CUST789": {
        "name": "Karen",
        "email": "karen@example.com",
        "status": "Active"
    }
}

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


# -------CustomerLookup TOOL ----------
class CustomerLookupRequest(BaseModel):
    customer_id: str

class CustomerLookupResponse(BaseModel):
    tool: str
    input: str
    output: dict

@router.post("/customer_lookup", response_model=CustomerLookupResponse)
def customer_lookup_tool(request: CustomerLookupRequest):
    logger.info(f"Customer lookup called for ID: {request.customer_id}")

    customer = FAKE_CUSTOMERS.get(request.customer_id)

    if not customer:
        return CustomerLookupResponse(
            tool="customer_lookup",
            input=request.customer_id,
            output={"error": "Customer not found"}
        )

    return CustomerLookupResponse(
        tool="customer_lookup",
        input=request.customer_id,
        output=customer
    )
