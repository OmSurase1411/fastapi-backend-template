from fastapi import APIRouter
from pydantic import BaseModel
import httpx
import re
from datetime import datetime


agent_router = APIRouter(prefix="/agent", tags=["agent"])

TOOLS_BASE_URL = "http://localhost:8000/tools"


class AgentRequest(BaseModel):
    text: str | None = ""


@agent_router.post("/run")
async def run_agent(request: AgentRequest):
    user_text = (request.text or "").strip()

    async with httpx.AsyncClient() as client:

        # 1️⃣ Empty input → time tool
        if not user_text:
            now = datetime.now()
            return {
                "status": "success",
                "output": f"Please enter some text 🙂\nToday: {now.date()}\nTime: {now.strftime('%H.%M')}"
            }
        # 2️⃣ Echo command (explicit)
        if user_text.lower().startswith("echo "):
            payload = {"text": user_text[5:]}
            r = await client.post(f"{TOOLS_BASE_URL}/echo", json=payload)
            return r.json()

        # 3️⃣ Extract numbers → ADD tool
        numbers = list(map(int, re.findall(r"-?\d+", user_text)))
        if len(numbers) >= 2:
            payload = {"a": numbers[0], "b": numbers[1]}
            r = await client.post(f"{TOOLS_BASE_URL}/add", json=payload)
            return r.json()

        # 4️⃣ Customer lookup
        if "cust" in user_text.lower():
            match = re.search(r"(cust\d+)", user_text.lower())
            if match:
                r = await client.post(
                    f"{TOOLS_BASE_URL}/customer_lookup",
                    json={"customer_id": match.group(1).upper()},
                )
                return r.json()

        # 5️⃣ Vehicle lookup
        if "vin" in user_text.lower():
            match = re.search(r"(vin\d+)", user_text.lower())
            if match:
                r = await client.post(
                    f"{TOOLS_BASE_URL}/vehicle_info",
                    json={"vin": match.group(1).upper()},
                )
                return r.json()

        # 6️⃣ Default → Uppercase
        r = await client.post(
            f"{TOOLS_BASE_URL}/uppercase",
            json={"text": user_text},
        )
        return r.json()
