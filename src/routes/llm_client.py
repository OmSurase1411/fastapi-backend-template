import requests
import json


class LLMClient:
    """
    This class is the ONLY place in the entire project where the LLM is accessed.
    Everything else must go through this client.

    We are using Ollama as a local, free, open-source LLM backend.
    """

    def __init__(self, model_name: str = "llama3"):
        self.model_name = model_name
        self.url = "http://localhost:11434/api/generate"

    def invoke(self, prompt: str) -> str:
        """
        Sends a prompt to Ollama and returns the raw model response.
        MCP guarantees that the prompt is already well-formed.
        """
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(self.url, json=payload)

        if response.status_code != 200:
            raise RuntimeError(f"Ollama error: {response.text}")

        data = response.json()
        return data["response"]
