from pydantic import BaseModel
from typing import Optional


class AgentResponse(BaseModel):
    """
    MCP response schema.
    This is the ONLY valid format the LLM is allowed to return.
    """
    intent: str
    tool_called: bool
    tool_name: Optional[str] = None
    final_response: str
