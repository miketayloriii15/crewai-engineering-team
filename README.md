# 🧠 AI Engineering Crew

An **autonomous AI engineering system** that designs, codes, and tests full-stack applications through coordinated software agents.  
This example demonstrates a **FastAPI + Bootstrap e-commerce web app** automatically created by AI agents working in sequence.

---

## 🚀 Overview

This project showcases how a multi-agent system can plan, implement, and validate software autonomously.  
Each agent specializes in a specific engineering discipline — design, backend, frontend, and testing — and collaborates to produce complete, runnable code.

**Core Components**
- 🧩 `EngineeringTeam`: defines the AI crew (agents + tasks)
- ⚙️ `agents.yaml`: agent definitions (roles, goals, personalities)
- 📋 `tasks.yaml`: task definitions and dependencies
- 🛠️ `custom_tool.py`: example of extending CrewAI with a custom Python tool
- 🧮 `main.py`: orchestrator that kicks off the entire workflow

---

## 🧱 Project Architecture

ai-engineering-crew/
├── config/
│ ├── agents.yaml # Agent roles and prompts
│ ├── tasks.yaml # Task definitions and context
├── engineering_team/
│ ├── crew.py # Crew class binding agents & tasks
│ ├── init.py
├── custom_tool.py # Custom CrewAI tool example
├── main.py # Entry point to run the engineering pipeline
├── output/ # Generated project files (designs, code, tests)
└── requirements.txt # Dependencies (CrewAI, Python libs)

markdown
Copy code

---

## ⚙️ How It Works

1. **Load environment & configs**
   - The `.env`, `agents.yaml`, and `tasks.yaml` files define context and roles.
2. **Kick off the crew**
   - `EngineeringTeam().crew().kickoff(inputs)` initializes all agents.
3. **Sequential collaboration**
   - Agents perform design → backend → frontend → testing in defined order.
4. **Output**
   - Generated project files appear under `/output` (e.g., HTML, CSS, JS, FastAPI code).

---

## 💻 Running the Project

### Prerequisites
- Python 3.10+
- `pip install -r requirements.txt`

### Run
```bash
python main.py
Outputs will be generated in the output/ folder:

shop_backend.py — FastAPI backend

index.html, styles.css, app.js — Frontend files

test_shop_backend.py — Unit tests

🧰 Example Task
The following requirement is automatically passed to the crew:

python
Copy code
Build a simple ecommerce site for Movies & Books:
- FastAPI backend with /health, /products, /cart, /checkout
- In-memory catalog and cart (no DB)
- Frontend: Bootstrap site with search, filters, cart, and checkout
- Tests for all endpoints
🧩 Custom Tool Example
custom_tool.py demonstrates how to build and register your own CrewAI tools.

python
Copy code
class MyCustomTool(BaseTool):
    name = "Name of my tool"
    description = "Description of what this tool does."
    
    def _run(self, argument: str) -> str:
        return "This is an example of a tool output."
Use these to expand your crew’s capabilities (e.g., API calls, file management, data processing).

🧠 Key Features
Modular agent configuration via YAML

Safe code execution in Docker-style sandbox

Autonomous generation of backend, frontend, and test suites

Extensible tool system for custom logic

Great starting point for AI-powered software engineering research

🏗️ Future Enhancements
✅ Add memory and feedback loops for iterative improvement

✅ Integrate vector database for context retention

✅ Expand to microservices & CI/CD pipelines

✅ Implement RAG-based planning for complex projects

🧾 License
MIT License © 2025 Mike Taylor III
