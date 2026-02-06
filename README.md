# 🧠 GitGraph RAG

> **Hybrid Search Engine for GitHub Repository Discovery**  


[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🎯 The Problem

GitHub's search is broken for developers:
- ❌ **Semantic Blindness**: Keyword matching only, no concept understanding
- ❌ **Structural Blindness**: Repos are isolated islands, no relationship data
- ❌ **Decision Paralysis**: 500+ results, manual README inspection required

## 💡 The Solution

**GitGraph RAG** combines three powerful technologies:

```
🧠 Vector Search (Pinecone + Gemini) → Understands MEANING
🕸️ Graph Database (Neo4j)           → Knows RELATIONSHIPS  
🤖 AI Agent (Gemini 1.5 Flash)      → Intelligent FUSION
```

### Example Queries:
- *"PDF parser for langchain"* → Finds repos that work with LangChain
- *"works with pydantic"* → Graph traversal for dependencies
- *"data validation library"* → Semantic understanding

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- API Keys (all free):
  - [Google Gemini](https://aistudio.google.com)
  - [Pinecone](https://www.pinecone.io)
  - [Neo4j Aura](https://neo4j.com/cloud/aura)

### Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/gitgraph-rag.git
cd gitgraph-rag

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your API keys

# Seed database
python seed_database.py

# Run the app
streamlit run app/main.py
```


---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USER QUERY                           │
│                  "PDF parser for langchain"                 │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   GEMINI 1.5 FLASH                          │
│              Understands Intent & Entities                  │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
        ▼                             ▼
┌──────────────────┐          ┌──────────────────┐
│  VECTOR SEARCH   │          │  GRAPH SEARCH    │
│    (Pinecone)    │          │    (Neo4j)       │
│                  │          │                  │
│ Semantic matches │          │ Dependency links │
└────────┬─────────┘          └────────┬─────────┘
         │                             │
         └──────────────┬──────────────┘
                        │
                        ▼
         ┌──────────────────────────┐
         │   FUSION & RANKING       │
         │   (Gemini Intelligence)  │
         └──────────────┬───────────┘
                        │
                        ▼
         ┌──────────────────────────┐
         │    TOP 5 RESULTS         │
         │  with explanations       │
         └──────────────────────────┘
```

---

## 🛠 Tech Stack

| Component | Technology | Cost |
|-----------|------------|------|
| **Frontend** | Streamlit Community Cloud 
| **LLM** | Gemini 1.5 Flash (15 RPM) 
| **Vector DB** | Pinecone Serverless (100K vectors)
| **Graph DB** | Neo4j Aura (200K nodes) 
| **Embeddings** | Gemini text-embedding-004 
| **Total** |

---

## 📊 Project Structure

```
GITGRAPH/
├── app/
│   └── main.py              # Streamlit frontend
├── agent/
│   └── search.py            # Hybrid search logic
├── db/
│   ├── pinecone_client.py   # Vector search
│   ├── neo4j_client.py      # Graph queries
│   └── schemas.py           # Pydantic models
├── config/
│   └── settings.py          # Environment config
├── seed_database.py         # Initial data load
├── test_connections.py      # Connection tests
└── requirements.txt         # Dependencies
```

---

## 🎯 Features

- ✅ **Semantic Search**: Understands concepts, not just keywords
- ✅ **Dependency Awareness**: Finds repos that work together
- ✅ **AI Explanations**: Gemini explains why results match
- ✅ **Hybrid Strategy**: Combines vector + graph intelligently
- ✅ **Real-time**: Sub-3-second response time

---

## 📈 Performance

| Metric | Value |
|--------|-------|
| Query Response Time | < 3 seconds |
| Repositories Indexed | 10 (MVP) |
| Dependency Relationships | 70 |
| Search Accuracy | High (semantic + structural) |

---

## 🔮 Future Enhancements






---


---


