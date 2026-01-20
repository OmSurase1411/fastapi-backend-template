from fastapi import APIRouter
from pydantic import BaseModel
from src.logger import setup_logger
from typing import Any, Optional
from datetime import datetime, timezone


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

FAKE_VEHICLES = {
    "VIN123": {
        "model": "BMW X5",
        "year": 2023,
        "status": "In Service"
    },
    "VIN456": {
        "model": "BMW 3 Series",
        "year": 2021,
        "status": "Out of Service"
    },
    "VIN789": {
        "model": "BMW i4",
        "year": 2024,
        "status": "In Production"
    }
}

class ToolResponse(BaseModel):
    tool: str
    status: str
    input: Any = None
    output: Any = None
    message: Optional [str] | None = None


class EchoRequest(BaseModel):
    text: str

class EchoResponse(BaseModel):
    tool: str
    input: str
    output: str

@router.post("/echo", response_model = ToolResponse)
def echo_tool(request: EchoRequest):
    logger.info(f"Echo tool called with input: {request.text}")

    return ToolResponse(
        tool = "echo",
        status="success",
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

@router.post("/uppercase", response_model=ToolResponse)
def uppercase_tool(request: UppercaseRequest):
    logger.info(f"Uppercase tool called with input: {request.text}")
    upper = request.text.upper()
    return ToolResponse(
        tool="uppercase",
        status="success",
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

@router.post("/customer_lookup", response_model=ToolResponse)
def customer_lookup_tool(request: CustomerLookupRequest):
    logger.info(f"Customer lookup called for ID: {request.customer_id}")

    customer = FAKE_CUSTOMERS.get(request.customer_id)

    if not customer:
        return ToolResponse(
            tool="customer_lookup",
            status="failed",
            input=request.customer_id,
            output= None,
            message="Customer Not Found"
        )

    return ToolResponse(
        tool="customer_lookup",
        status="success",
        input=request.customer_id,
        output=customer
    )


#--------VEHICLE INFO TOOL---------
class VehicleInfoRequest(BaseModel):
    vin: str


class VehicleInfoResponse(BaseModel):
    tool: str
    input: str
    output: dict


@router.post("/vehicle_info", response_model=ToolResponse)
def vehicle_info_tool(request: VehicleInfoRequest):
    logger.info(f"Vehicle info lookup called for VIN: {request.vin}")

    vehicle = FAKE_VEHICLES.get(request.vin)

    if not vehicle:
        return ToolResponse(
            tool="vehicle_info",
            status="failed",
            input=request.vin,
            output= None, 
            message="Vehicle not found"
        )

    return ToolResponse(
        tool="vehicle_info",
        status="success",
        input=request.vin,
        output=vehicle
    )

#-------------TIME TOOL_--------------
@router.post("/time", response_model=ToolResponse)
def time_tool():
    now = datetime.now(timezone.utc).isoformat()

    logger.info("Time tool called")

    return ToolResponse(
        tool="time",
        status="success",
        input=None,
        output=now,
        message=None
    )

class AddRequest(BaseModel):
    a: float
    b: float

@router.post("/add", response_model= ToolResponse)
def add_tool(request: AddRequest):
    logger.info(f"Add tool called with a={request.a},b={request.b}")

    result = request.a + request.b

    return ToolResponse(
        tool = "add",
        status = "success",
        input = [request.a, request.b],
        output = result,
        message = None
    )

