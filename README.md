# Flight Deals & Tracker MCP Server

A Model Context Protocol (MCP) server that searches live flights via Google Flights and tracks deals in MongoDB Atlas. Includes an agent script to run tool-assisted workflows with a local Ollama model (`qwen2.5:3b`).

---

## 🛠️ Tech Stack
- **Protocol:** FastMCP / Model Context Protocol (stdio)
- **Flight Data:** `fast-flights` (Google Flights scraper)
- **Database:** MongoDB Atlas (`pymongo`)
- **LLM Agent:** Local Ollama (`qwen2.5:3b`)

---

## 🚀 Setup & Installation

1. **Clone & Create Virtual Environment:**
   ```bash
   git clone <repo-url>
   cd flight-mcp-server
   python -m venv venv
   .\venv\Scripts\activate   # Windows
   pip install -r requirements.txt