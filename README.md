#  Indian AI Finance Assistant

An intelligent AI-powered assistant designed to help users with queries about the Indian Tax System. It uses Retrieval-Augmented Generation (RAG), memory features, web search, and agentic evaluation to provide contextual, accurate, and insightful responses.

---



##  Features

-  **Short-term memory** – Keeps track of ongoing conversations.
-  **Long-term memory (RAG)** – Retrieves relevant documents for accurate answers.
-  **Tavily Web Search** – Enables the assistant to search the web in real-time for fresh information.
-  **Qdrant Vector Store** – High-performance vector database to store and retrieve embeddings
-  **Summarized Memory** – Provides summaries of past conversations for context preservation.
-  **FastAPI Backend** – Powers the API endpoints and logic.
-  **React Frontend Interface** – Simple, interactive, chat-based UI.
-  **Opik Agentic Flow Tracking** – Evaluates reasoning steps and tracks decisions across interactions.

  
## Tech Stack
- **Programming** - Python
- **Frontend** - React js + Vite
- **Backend** - FastAPI
- **LLM** - llama-4-maverick-17b-128e-instruct
- **LLM framework** - Langchain,Langgraph
- **LLM Provider** - Groq
- **Embedding Model** - sentence-transformers/all-MiniLM-L6-v2
- **Vector Database** - Qdrant
- **Agent Tracking** - Opik
- **Containerization** - Docker
- **Container Orchestration** - Docker Compose
- **Python Package Manager** - uv


## 🔑 Environment Setup

Create a `.env` file inside the `agent-api/` directory:

```env
GROQ_API_KEY=your_groq_api_key
OPIK_API_KEY=your_opik_api_key
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_URL=https://your-qdrant-endpoint.com
TAVILY_API_KEY=your_tavily_api_key
```
**Run With Docker**
 Prerequisites
 - Docker
 - Docker Compose

| Service  | URL                                            |
| -------- | ---------------------------------------------- |
| FastAPI  | [http://localhost:8000](http://localhost:8000) |
| React + Vite | [http://localhost:3000](http://localhost:3000) |

**Run Without Docker**
Backend (FastAPI)
```
cd agent-api
uv sync  # or pip install -r requirements.txt
uvicorn src.infrastructure.api:app --reload --host 0.0.0.0 --port 8000
```

Frontend (React+Vite)
```
cd agent-ui
npm install
npm run dev

```
