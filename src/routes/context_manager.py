class ContextManager:
    """
    Model Context Protocol (MCP) implementation.
    This class controls exactly what the LLM sees and how it must behave.
    """

    def __init__(self):
        self.system_message = """
You are an enterprise-grade AI agent controller.

Rules you must follow strictly:
1. You must respond with valid JSON only.
2. Your response must follow this exact schema:

{
  "intent": "string",
  "tool_called": true or false,
  "tool_name": "string or null",
  "final_response": "string"
}

3. Do not add any text outside JSON.
4. Do not use markdown.
5. Do not hallucinate tool names.
6. If no tool is required, set:
   - tool_called: false
   - tool_name: null
7. Think like a system controller, not a chatbot.
"""

    def build_prompt(self, user_input: str) -> str:
        """
        Builds an MCP-compliant prompt.
        Only system rules and the current user input are passed to the LLM.
        """
        prompt = f"""
SYSTEM:
{self.system_message}

USER:
{user_input}

ASSISTANT:
Return ONLY the JSON object that follows the schema.
"""
        return prompt.strip()
