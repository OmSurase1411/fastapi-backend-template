# Agentic AI Tool Server – MCP Governed Agent


This project is a fully MCP (Model Context Protocol) governed AI Agent system built using FastAPI and a local LLM (Ollama).
It demonstrates how to convert an LLM from a chatbot into a deterministic system controller that decides when and how tools should be executed.


This repository is part of a 12-week Agentic AI enablement plan.
Weeks 1–5 focus on protocol design, tool orchestration, and LLM governance.


---


## 🔥 What This Project Does


The agent can:


- Understand user intent  
- Decide whether a tool is required  
- Call backend tools when needed  
- Return structured, deterministic responses  
- Handle user mistakes politely (missing VIN / Customer ID)  
- Explain concepts when no tool is required  
- Enforce strict JSON contracts between the LLM and the backend  


This is not a chatbot.  
This is a **governed decision-making AI agent**.


---


## 🧠 Core Concept: Model Context Protocol (MCP)


MCP is a strict contract that controls LLM behavior.


Every LLM response must follow:


```json
{
  "intent": "string",
  "tool_called": true or false,
  "tool_name": "string or null",
  "final_response": "string"
}
```


Rules enforced:


- JSON only output  
- No markdown  
- No trailing commas  
- No hallucinated tool names  
- Only whitelisted tools allowed  
- `final_response` must always be a non-empty string  
- Output must be directly parsable by `json.loads()`  


This transforms the LLM from a chatbot into a deterministic **decision engine**.

---


## 🏗️ System Architecture


```
User → MCP Prompt → LLM → JSON Decision → Tool Execution → Unified Response → UI
```


| Component | Role |
|--------|------|
| ContextManager | Enforces MCP and controls LLM behavior |
| LLMClient | Communicates with Ollama |
| Agent Router | Orchestrates tool decisions |
| Tools Layer | Deterministic APIs |
| Frontend | Interprets and formats agent responses |

---



## 🛠️ Available Tools


| Tool | Description |
|------|-----------|
| `add` | Adds two numbers |
| `echo` | Echoes user input |
| `customer_lookup` | Fetches customer details |
| `vehicle_info` | Fetches vehicle details using VIN |
| `uppercase` | Converts text to uppercase |


---


## 🖥️ Frontend Behavior


The frontend UI:


- Shows explanations when no tool is needed  
- Shows explanation + polite correction when IDs are missing  
- Formats tool results professionally  
- Never exposes raw JSON or backend errors  


---


## 🚀 How to Run


1. Start Ollama:
```bash
ollama serve
```


2. Pull the model:
```bash
ollama pull llama3
```


3. Start backend:
```bash
uvicorn src.main:app --reload
```


4. Open frontend:
Open your HTML file directly in the browser.


---


## 📁 Project Structure


```
src/
 ├── routes/
 │   ├── agent.py
 │   ├── context_manager.py
 │   ├── llm_client.py
 │   ├── schemas.py
 │   └── tools.py
docs/
 ├── MCP.md
 └── ARCHITECTURE.md
```

---


## 🧭 Project Status


| Week | Focus | Status |
|------|------|------|
| Week 1–2 | Tools + FastAPI Foundation | ✅ |
| Week 3–4 | Rule-Based Agent Logic | ✅ |
| Week 5 | MCP Governance & LLM Orchestration | ✅ |

---


## 🎯 Why This Project Matters


This project demonstrates:


- Protocol-driven LLM governance  
- Deterministic agent design  
- Enterprise-grade AI architecture  
- Separation between decision and execution  
- Real-world agent orchestration patterns  


This is how modern AI agents are built in production environments.



