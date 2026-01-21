from fastapi import APIRouter
from pydantic import BaseModel
import httpx
import json

from src.routes.context_manager import ContextManager
from src.routes.llm_client import LLMClient
from src.routes.schemas import AgentResponse



# -------------------------------------------------------------------
# Setup
# -------------------------------------------------------------------

agent_router = APIRouter(prefix="/agent", tags=["agent"])

TOOLS_BASE_URL = "http://localhost:8000/tools"

context_manager = ContextManager()
llm_client = LLMClient(model_name="llama3:latest")


# -------------------------------------------------------------------
# Request model
# -------------------------------------------------------------------

class AgentRequest(BaseModel):
    text: str | None = ""


# -------------------------------------------------------------------
# Tool execution helpers
# -------------------------------------------------------------------

async def call_tool(client: httpx.AsyncClient, tool_name: str, user_text: str):
    """
    Maps tool_name decided by the LLM to your real tool endpoints.
    """
    if tool_name == "echo":
        payload = {"text": user_text}
        r = await client.post(f"{TOOLS_BASE_URL}/echo", json=payload)
        return r.json()

    elif tool_name == "add":
        # Expecting the user text to contain numbers
        import re
        numbers = list(map(int, re.findall(r"-?\d+", user_text)))
        payload = {"a": numbers[0], "b": numbers[1]}
        r = await client.post(f"{TOOLS_BASE_URL}/add", json=payload)
        return r.json()

    elif tool_name == "customer_lookup":
        import re
        match = re.search(r"(cust\d+)", user_text.lower())
        if not match:
            return {"status": "failed", "message": "Customer ID not found"}
        payload = {"customer_id": match.group(1).upper()}
        r = await client.post(f"{TOOLS_BASE_URL}/customer_lookup", json=payload)
        return r.json()

    elif tool_name == "vehicle_info":
        import re
        match = re.search(r"(vin\d+)", user_text.lower())
        if not match:
            return {"status": "failed", "message": "VIN not found"}
        payload = {"vin": match.group(1).upper()}
        r = await client.post(f"{TOOLS_BASE_URL}/vehicle_info", json=payload)
        return r.json()

    elif tool_name == "uppercase":
        payload = {"text": user_text}
        r = await client.post(f"{TOOLS_BASE_URL}/uppercase", json=payload)
        return r.json()

    else:
        return {
            "status": "failed",
            "message": f"Unknown tool requested: {tool_name}"
        }


# -------------------------------------------------------------------
# MCP + LLM governed agent route
# -------------------------------------------------------------------

@agent_router.post("/run")
async def run_agent(request: AgentRequest):
    user_text = (request.text or "").strip()

    if not user_text:
        return {
            "error": "Empty input",
            "message": "Please provide some text"
        }

    # 1. Build MCP prompt
    prompt = context_manager.build_prompt(user_text)

    # 2. Call LLM
    raw_response = llm_client.invoke(prompt)

        # TEMP DEBUG
    print("\n====== RAW LLM OUTPUT ======")
    print(raw_response)
    print("====== END RAW OUTPUT ======\n")

    # 3. Parse and validate against MCP schema
    try:
        parsed = json.loads(raw_response)
        agent_decision = AgentResponse(**parsed)
    except Exception as e:
        return {
            "error": "Invalid LLM response format",
            "raw_output": raw_response,
            "exception": str(e)
        }

    # 4. If LLM says no tool is required → return directly
    if not agent_decision.tool_called:
        return agent_decision.dict()

    # 5. If LLM requests a tool → execute it
    async with httpx.AsyncClient() as client:
        tool_result = await call_tool(
            client,
            agent_decision.tool_name,
            user_text
        )

    # 6. Return a combined response
    return {
        "intent": agent_decision.intent,
        "tool_called": True,
        "tool_name": agent_decision.tool_name,
        "final_response": agent_decision.final_response,
        "tool_result": tool_result
    }
