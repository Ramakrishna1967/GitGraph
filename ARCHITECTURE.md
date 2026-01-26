# 🧠 GitGraph RAG: Complete Architecture & Deployment Guide

> **A $0 Hybrid Search Engine for GitHub Repository Discovery**  
> Built for 2026 | Free Tier Only | Production Ready

---

## 📋 Table of Contents

1. [The Problem](#-the-problem)
2. [The Solution](#-the-solution)
3. [Tech Stack ($0 Budget)](#-tech-stack-0-budget)
4. [System Architecture](#-system-architecture)
5. [Data Flow](#-data-flow)
6. [Agent Workflow](#-agent-workflow-langgraph)
7. [Database Design](#-database-design)
8. [Deployment Strategy](#-deployment-strategy)
9. [Implementation Roadmap](#-implementation-roadmap)
10. [Cost Breakdown](#-cost-breakdown)

---

## 🎯 The Problem

```mermaid
mindmap
  root((GitHub Search<br/>Is Broken))
    Semantic Blindness
      Keyword matching only
      No concept understanding
      "async HTTP" ≠ "non-blocking requests"
    Structural Blindness
      Repos as isolated islands
      No dependency awareness
      No compatibility signals
    Decision Paralysis
      100+ results per search
      Manual README inspection
      No stack compatibility filter
```

### Real Example:
> **User Query:** "PDF parser that works with LangChain in Python"
> 
> **GitHub Search Result:** 500+ repos with "PDF" or "Python" in name
> 
> **What User Actually Needs:** Repos that `import langchain` AND handle PDFs

---

## 💡 The Solution

### GitGraph RAG = Vector Search + Graph Traversal

```mermaid
graph LR
    subgraph "Traditional Search"
        A[Query] --> B[Keyword Match]
        B --> C[Ranked by Stars]
    end
    
    subgraph "GitGraph RAG"
        D[Query] --> E[Gemini: Understand Intent]
        E --> F{Search Strategy}
        F -->|Semantic| G[Pinecone Vector Search]
        F -->|Compatibility| H[Neo4j Graph Traversal]
        F -->|Hybrid| G & H
        G --> I[Fusion + Rerank]
        H --> I
        I --> J[Context-Aware Results]
    end
    
    style J fill:#00ff00,stroke:#333,stroke-width:2px
```

### What Makes This Different:

| Aspect | GitHub Search | GitGraph RAG |
|--------|---------------|--------------|
| Query Understanding | Literal keywords | Semantic intent |
| "works with X" |  Not possible |  Graph traversal |
| "alternatives to X" |  Manual search | ✅ `ALTERNATIVE_TO` edges |
| Stack compatibility | ❌ Read every README | ✅ Dependency graph filter |

---

## � How We Solve Each Problem (Detailed)

### Problem 1: Semantic Blindness

> **The Issue:** GitHub only matches exact keywords. "async HTTP client" won't find "non-blocking request library"

```mermaid
flowchart TB
    subgraph "❌ GitHub's Approach"
        Q1["Query: async HTTP client"] --> KW[Keyword Matcher]
        KW --> R1["Results: repos with 'async' OR 'HTTP' in name"]
        R1 --> MISS["❌ Misses: aiohttp, httpx, asks"]
    end
    
    subgraph "✅ GitGraph's Solution"
        Q2["Query: async HTTP client"] --> EMB[Gemini Embedding]
        EMB --> VEC["Vector: [0.23, 0.87, ...]"]
        VEC --> PC[(Pinecone)]
        PC --> SEM["Semantic Similarity Search"]
        SEM --> HIT["✅ Finds: aiohttp, httpx, asks, treq"]
    end
    
    style MISS fill:#ff6b6b
    style HIT fill:#4ade80
```

#### The Solution Flow:

```mermaid
sequenceDiagram
    participant U as User
    participant G as Gemini
    participant P as Pinecone
    
    Note over U,P: Semantic Understanding Pipeline
    
    U->>G: "async HTTP client for Python"
    
    G->>G: Understand CONCEPT not keywords
    Note right of G: Concepts extracted:<br/>- Asynchronous I/O<br/>- HTTP requests<br/>- Python ecosystem
    
    G->>P: Embed query → [0.23, 0.87, 0.12, ...]
    
    P->>P: Cosine similarity with README embeddings
    Note right of P: Top matches by MEANING:<br/>1. httpx (0.94)<br/>2. aiohttp (0.91)<br/>3. asks (0.88)
    
    P-->>U: Returns conceptually similar repos
```

---

### Problem 2: Structural Blindness

> **The Issue:** GitHub treats repos as isolated. Can't answer "what works with LangChain?"

```mermaid
flowchart TB
    subgraph "❌ GitHub's View"
        R1[langchain] --- ISLAND1["Isolated Island"]
        R2[chromadb] --- ISLAND2["Isolated Island"]
        R3[unstructured] --- ISLAND3["Isolated Island"]
        ISLAND1 -.- NO["❌ No connections visible"]
        ISLAND2 -.- NO
        ISLAND3 -.- NO
    end
    
    subgraph "✅ GitGraph's Knowledge Graph"
        LC((langchain))
        CH((chromadb))
        UN((unstructured))
        PP((pypdf))
        OA((openai))
        
        CH -->|INTEGRATES_WITH| LC
        UN -->|DEPENDS_ON| LC
        PP -->|USED_BY| UN
        LC -->|DEPENDS_ON| OA
        
        style LC fill:#e91e63
        style CH fill:#2196f3
        style UN fill:#4caf50
        style PP fill:#ff9800
        style OA fill:#9c27b0
    end
```

#### The Solution Flow:

```mermaid
sequenceDiagram
    participant U as User
    participant A as Agent
    participant N as Neo4j
    
    Note over U,N: Graph Traversal for Compatibility
    
    U->>A: "PDF parser that works with LangChain"
    
    A->>N: Cypher Query
    Note right of A: MATCH (r:Repository)<br/>-[:DEPENDS_ON]-><br/>(lc:Repository {name: 'langchain'})<br/>WHERE r.topics CONTAINS 'pdf'
    
    N->>N: Graph Traversal (O(1) hop)
    Note right of N: Traverses dependency edges<br/>Not scanning all repos!
    
    N-->>A: [unstructured, langchain-pdf, docarray]
    
    A-->>U: "These repos import langchain AND handle PDFs"
```

#### Example Cypher Queries:

```mermaid
graph LR
    subgraph "Query: Works with LangChain"
        Q1["MATCH (r)-[:DEPENDS_ON]->(lc {name:'langchain'})<br/>RETURN r"]
    end
    
    subgraph "Query: Alternatives to Pandas"
        Q2["MATCH (r)-[:ALTERNATIVE_TO]->(p {name:'pandas'})<br/>RETURN r, r.reason"]
    end
    
    subgraph "Query: Popular in ML ecosystem"
        Q3["MATCH (r)-[:TAGGED_WITH]->(t:Topic)<br/>WHERE t.name IN ['ml', 'deep-learning']<br/>AND r.stars > 1000<br/>RETURN r"]
    end
```

---

### Problem 3: Decision Paralysis

> **The Issue:** 500 results, no way to filter by YOUR specific stack

```mermaid
flowchart TB
    subgraph "❌ GitHub Experience"
        SEARCH["Search: 'PDF parser Python'"] --> RESULTS["500+ Results"]
        RESULTS --> MANUAL["Manual inspection of each README"]
        MANUAL --> HOURS["⏰ Hours of research"]
        HOURS --> MAYBE["Maybe find the right one?"]
        
        style MAYBE fill:#ff6b6b
    end
    
    subgraph "✅ GitGraph Experience"
        QUERY["Query: 'PDF parser for my LangChain + FastAPI stack'"] --> AGENT["LangGraph Agent"]
        AGENT --> HYBRID["Hybrid Search"]
        HYBRID --> FILTER["Stack-aware filtering"]
        FILTER --> TOP3["Top 3 recommendations with reasons"]
        TOP3 --> DONE["✅ Decision in 3 seconds"]
        
        style DONE fill:#4ade80
    end
```

#### The Intelligent Filtering Pipeline:

```mermaid
flowchart LR
    subgraph "Step 1: Understand User Stack"
        INPUT["User: I use LangChain, FastAPI, Python 3.11"]
        INPUT --> EXTRACT["Extract stack components"]
        EXTRACT --> STACK["Stack Profile:<br/>- LangChain ✓<br/>- FastAPI ✓<br/>- Python 3.11 ✓"]
    end
    
    subgraph "Step 2: Multi-Signal Search"
        STACK --> VS["Vector: Semantic match on 'PDF'"]
        STACK --> GS["Graph: repos → DEPENDS_ON → langchain"]
        VS --> CANDIDATES["50 candidates"]
        GS --> COMPATIBLE["20 compatible repos"]
    end
    
    subgraph "Step 3: Intersection + Rank"
        CANDIDATES --> INTERSECT{Intersection}
        COMPATIBLE --> INTERSECT
        INTERSECT --> MATCHED["12 repos match BOTH"]
        MATCHED --> RANK["Rank by: stars, recency, compatibility score"]
        RANK --> FINAL["Top 3 with explanations"]
    end
    
    style FINAL fill:#4ade80,stroke:#333,stroke-width:2px
```

---

### The Complete Problem → Solution Mapping

```mermaid
graph TB
    subgraph "PROBLEMS"
        P1["🔴 Semantic Blindness<br/>Keywords ≠ Concepts"]
        P2["🔴 Structural Blindness<br/>No relationship awareness"]
        P3["🔴 Decision Paralysis<br/>Too many results"]
    end
    
    subgraph "SOLUTIONS"
        S1["🟢 Vector Embeddings<br/>Pinecone + Gemini"]
        S2["🟢 Knowledge Graph<br/>Neo4j relationships"]
        S3["🟢 Intelligent Agent<br/>LangGraph fusion"]
    end
    
    subgraph "TECHNIQUES"
        T1["Cosine similarity<br/>on README text"]
        T2["Graph traversal<br/>DEPENDS_ON, ALTERNATIVE_TO"]
        T3["Reciprocal Rank Fusion<br/>Multi-signal ranking"]
    end
    
    P1 --> S1 --> T1
    P2 --> S2 --> T2
    P3 --> S3 --> T3
    
    style P1 fill:#ff6b6b
    style P2 fill:#ff6b6b
    style P3 fill:#ff6b6b
    style S1 fill:#4ade80
    style S2 fill:#4ade80
    style S3 fill:#4ade80
```

---

### End-to-End Query Resolution

```mermaid
flowchart TB
    subgraph "1️⃣ User Input"
        USER["Developer asks:<br/>'PDF parser for LangChain in Python'"]
    end
    
    subgraph "2️⃣ Intent Understanding (Gemini)"
        USER --> PARSE["Parse Query"]
        PARSE --> INTENT["Intent: compatibility"]
        PARSE --> ENTITIES["Entities: PDF, LangChain, Python"]
        PARSE --> CONSTRAINTS["Constraints: DEPENDS_ON langchain"]
    end
    
    subgraph "3️⃣ Dual Search Strategy"
        INTENT --> DECISION{Strategy}
        DECISION -->|Semantic| VECTOR["Pinecone Search<br/>'PDF parser Python'"]
        DECISION -->|Structural| GRAPH["Neo4j Query<br/>repos → langchain"]
        
        VECTOR --> V_RESULTS["pypdf, pdfplumber,<br/>pymupdf, camelot"]
        GRAPH --> G_RESULTS["unstructured, langchain-pdf,<br/>docarray, llama-index"]
    end
    
    subgraph "4️⃣ Fusion & Ranking"
        V_RESULTS --> FUSION["Reciprocal Rank Fusion"]
        G_RESULTS --> FUSION
        FUSION --> RERANK["Gemini Reranking<br/>by query relevance"]
        RERANK --> FINAL["Final Ranked List:<br/>1. unstructured<br/>2. pypdf<br/>3. langchain-pdf"]
    end
    
    subgraph "5️⃣ Response Generation"
        FINAL --> RESPONSE["Gemini generates explanation:<br/>'Based on your LangChain stack,<br/>I recommend unstructured because...'"]
        RESPONSE --> OUTPUT["✅ Actionable Answer"]
    end
    
    style OUTPUT fill:#4ade80,stroke:#333,stroke-width:3px
```

---

### Why This Architecture Works

```mermaid
graph LR
    subgraph "Traditional RAG"
        A[Query] --> B[Vector Search Only]
        B --> C[Results lack context]
    end
    
    subgraph "GitGraph RAG (Hybrid)"
        D[Query] --> E[Vector Search]
        D --> F[Graph Traversal]
        E --> G[Semantic matches]
        F --> H[Structural matches]
        G --> I[Fusion Layer]
        H --> I
        I --> J[Context-rich results]
    end
    
    style C fill:#ff6b6b
    style J fill:#4ade80
```

| Approach | Strength | Weakness | GitGraph Combines Both |
|----------|----------|----------|------------------------|
| **Vector Only** | Finds similar concepts | Can't verify compatibility | ✅ Semantic understanding |
| **Graph Only** | Perfect for relationships | Can't handle fuzzy queries | ✅ Structural awareness |
| **Hybrid (Ours)** | Best of both worlds | Complexity | ✅ Managed by LangGraph |

---

## �🛠 Tech Stack ($0 Budget)

```mermaid
graph TB
    subgraph "Frontend - FREE"
        ST[Streamlit Community Cloud]
    end
    
    subgraph "AI/LLM - FREE"
        GM[Google Gemini 1.5 Flash<br/>Free Tier: 15 RPM]
        EMB[text-embedding-004<br/>Free Tier]
    end
    
    subgraph "Databases - FREE"
        PC[Pinecone Serverless<br/>Starter: 100K vectors]
        N4J[Neo4j Aura<br/>Free: 200K nodes]
    end
    
    subgraph "Orchestration - FREE"
        LG[LangGraph<br/>Open Source]
    end
    
    subgraph "Data Source - FREE"
        GH[GitHub API<br/>5000 req/hr authenticated]
    end
    
    subgraph "Deployment - FREE"
        STC[Streamlit Cloud]
        GHA[GitHub Actions<br/>2000 min/month]
    end
    
    ST --> LG
    LG --> GM
    LG --> PC
    LG --> N4J
    GH --> N4J
    GH --> PC
```

### Why These Specific Tools?

| Tool | Why Not Alternatives? |
|------|----------------------|
| **Gemini 1.5 Flash** | 1M token context (vs GPT-4o's 128K). Can process entire sub-graphs. |
| **Neo4j Aura** | Native graph traversal. SQL/Mongo can't do O(1) relationship hops. |
| **Pinecone** | Serverless = no cold starts. Weaviate/Qdrant need self-hosting. |
| **LangGraph** | Cyclic workflows. LangChain is linear, can't retry/switch strategies. |
| **Streamlit** | Python-native. Next.js would need separate backend. |

---

## 🏗 System Architecture

```mermaid
graph TB
    subgraph "User Layer"
        U[Developer] --> UI[Streamlit UI]
    end
    
    subgraph "Application Layer"
        UI --> API[FastAPI Endpoints]
        API --> AGENT[LangGraph Agent]
    end
    
    subgraph "Intelligence Layer"
        AGENT --> QP[Query Parser Node]
        AGENT --> VS[Vector Search Node]
        AGENT --> GT[Graph Traversal Node]
        AGENT --> FR[Fusion & Rerank Node]
        AGENT --> RG[Response Generator]
        
        QP --> GM1[Gemini: Intent Extraction]
        FR --> GM2[Gemini: Reranking]
        RG --> GM3[Gemini: Response]
    end
    
    subgraph "Memory Layer"
        VS --> PC[(Pinecone<br/>README Embeddings)]
        GT --> N4J[(Neo4j<br/>Dependency Graph)]
    end
    
    subgraph "Data Layer"
        INGESTION[Ingestion Pipeline] --> PC
        INGESTION --> N4J
        GH[GitHub API] --> INGESTION
    end
    
    style AGENT fill:#ff6b6b,stroke:#333,stroke-width:2px
    style PC fill:#1e88e5,stroke:#333,stroke-width:2px
    style N4J fill:#7cb342,stroke:#333,stroke-width:2px
```

---

## 🔄 Data Flow

### Query Processing Flow

```mermaid
sequenceDiagram
    participant U as User
    participant UI as Streamlit
    participant A as LangGraph Agent
    participant G as Gemini
    participant P as Pinecone
    participant N as Neo4j
    
    U->>UI: "PDF parser for LangChain"
    UI->>A: process_query()
    
    A->>G: Extract intent & entities
    G-->>A: {intent: "compatibility", entities: ["PDF", "LangChain"]}
    
    par Vector Search
        A->>P: Semantic search "PDF parser"
        P-->>A: [pypdf, pdfplumber, ...]
    and Graph Search
        A->>N: MATCH (r)-[:DEPENDS_ON]->(langchain)
        N-->>A: [langchain-pdf, unstructured, ...]
    end
    
    A->>G: Rerank & fuse results
    G-->>A: Ranked results with explanations
    
    A->>UI: Final response
    UI->>U: "Based on your stack, I recommend..."
```

### Data Ingestion Flow

```mermaid
flowchart LR
    subgraph "Data Sources"
        GH[GitHub API]
        BQ[BigQuery Public Dataset<br/>github_repos]
    end
    
    subgraph "Processing"
        F[Fetcher<br/>Rate Limited] --> P[Parser]
        P --> E[Embedder<br/>text-embedding-004]
        P --> G[Graph Builder]
    end
    
    subgraph "Storage"
        E --> PC[(Pinecone)]
        G --> N4J[(Neo4j)]
    end
    
    GH --> F
    BQ --> F
```

---

## 🤖 Agent Workflow (LangGraph)

```mermaid
stateDiagram-v2
    [*] --> ReceiveQuery
    
    ReceiveQuery --> ParseIntent: User query received
    
    ParseIntent --> DecideStrategy: Gemini extracts intent
    
    DecideStrategy --> VectorSearch: intent = "semantic"
    DecideStrategy --> GraphTraversal: intent = "compatibility"
    DecideStrategy --> ParallelSearch: intent = "hybrid"
    
    state ParallelSearch {
        [*] --> VS: Vector
        [*] --> GT: Graph
        VS --> Merge
        GT --> Merge
    }
    
    VectorSearch --> EvaluateResults
    GraphTraversal --> EvaluateResults
    ParallelSearch --> EvaluateResults
    
    EvaluateResults --> GenerateResponse: confidence > 0.7
    EvaluateResults --> RetryWithDifferentStrategy: confidence < 0.7
    
    RetryWithDifferentStrategy --> VectorSearch: retry_count < 2
    RetryWithDifferentStrategy --> GenerateResponse: retry_count >= 2
    
    GenerateResponse --> [*]
    
    note right of RetryWithDifferentStrategy
        LangGraph's cyclic capability
        allows dynamic strategy switching
    end note
```

### Agent State

```python
class GitGraphState(TypedDict):
    # Input
    query: str
    
    # Extracted
    intent: Literal["semantic", "compatibility", "alternative", "hybrid"]
    entities: list[str]
    constraints: dict
    
    # Search Results
    vector_results: list[RepoResult]
    graph_results: list[RepoResult]
    
    # Control Flow
    strategy_attempts: int
    current_strategy: str
    confidence_score: float
    
    # Output
    final_response: str
    recommended_repos: list[RepoResult]
```

---

## 🗄 Database Design

### Neo4j Graph Schema

```mermaid
graph LR
    R1((Repository)) -->|DEPENDS_ON| R2((Repository))
    R1 -->|TAGGED_WITH| T((Topic))
    R1 -->|USES_LANGUAGE| L((Language))
    R1 -->|OWNED_BY| O((Owner))
    R1 -->|SIMILAR_TO| R3((Repository))
    R1 -->|ALTERNATIVE_TO| R4((Repository))
    O -->|MEMBER_OF| ORG((Organization))
    
    style R1 fill:#e91e63
    style R2 fill:#e91e63
    style R3 fill:#e91e63
    style R4 fill:#e91e63
    style T fill:#2196f3
    style L fill:#4caf50
    style O fill:#ff9800
    style ORG fill:#9c27b0
```

### Node Properties

| Node | Properties |
|------|------------|
| `Repository` | `name`, `full_name`, `description`, `stars`, `forks`, `last_updated`, `readme_vector_id`, `license` |
| `Topic` | `name`, `count`, `category` |
| `Language` | `name`, `ecosystem` |
| `Owner` | `login`, `type`, `followers`, `repos_count` |

### Relationship Properties

| Relationship | Properties |
|--------------|------------|
| `DEPENDS_ON` | `version`, `is_dev`, `is_optional` |
| `SIMILAR_TO` | `similarity_score` (cosine), `method` |
| `ALTERNATIVE_TO` | `reason`, `confidence`, `source` |

### Pinecone Index Schema

```python
{
    "id": "owner/repo-name",
    "values": [0.1, 0.2, ...],  # 768-dim embedding
    "metadata": {
        "name": "repo-name",
        "owner": "owner",
        "stars": 1500,
        "language": "Python",
        "topics": ["machine-learning", "nlp"],
        "chunk_index": 0,
        "chunk_text": "First 500 chars of README..."
    }
}
```

---

## 🚀 Deployment Strategy

```mermaid
graph TB
    subgraph "Development"
        DEV[Local Development]
        DEV --> GIT[GitHub Repository]
    end
    
    subgraph "CI/CD - FREE"
        GIT --> GHA[GitHub Actions]
        GHA --> TEST[Run Tests]
        GHA --> LINT[Linting]
    end
    
    subgraph "Deployment - FREE"
        GHA --> STC[Streamlit Community Cloud]
    end
    
    subgraph "Databases - FREE Tier"
        STC --> PC[Pinecone Serverless<br/>us-east-1]
        STC --> N4J[Neo4j Aura<br/>Free Instance]
    end
    
    subgraph "Scheduled Jobs - FREE"
        GHA --> CRON[Scheduled Ingestion<br/>Daily @ 2 AM UTC]
        CRON --> PC
        CRON --> N4J
    end
    
    style STC fill:#ff4b4b,stroke:#333,stroke-width:3px
```

### Deployment Platforms (All $0)

| Component | Platform | Free Tier Limits |
|-----------|----------|-----------------|
| **Frontend + Backend** | Streamlit Community Cloud | Unlimited public apps |
| **Vector DB** | Pinecone Serverless | 100K vectors, 1 index |
| **Graph DB** | Neo4j Aura | 200K nodes, 400K relationships |
| **LLM API** | Google AI Studio | 15 RPM, 1M TPM |
| **CI/CD** | GitHub Actions | 2000 min/month |
| **Data Refresh** | GitHub Actions CRON | Free with repo |

### Environment Variables (Secrets)

```bash
# .streamlit/secrets.toml (for Streamlit Cloud)
GOOGLE_API_KEY = "your-gemini-api-key"
PINECONE_API_KEY = "your-pinecone-key"
NEO4J_URI = "neo4j+s://xxxxx.databases.neo4j.io"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "your-password"
GITHUB_TOKEN = "ghp_xxxxx"  # For API rate limits
```

---

## 📅 Implementation Roadmap

```mermaid
gantt
    title GitGraph RAG - 2 Week Sprint
    dateFormat  YYYY-MM-DD
    section Phase 1: Foundation
    Project Setup & Configs     :a1, 2026-01-27, 1d
    Neo4j Schema Design         :a2, after a1, 1d
    Pinecone Index Setup        :a3, after a1, 1d
    
    section Phase 2: Data Pipeline
    GitHub Fetcher              :b1, after a2, 2d
    Embedding Pipeline          :b2, after b1, 1d
    Graph Builder               :b3, after b1, 1d
    Initial Data Load           :b4, after b2, 1d
    
    section Phase 3: Agent Core
    LangGraph Skeleton          :c1, after b4, 1d
    Query Parser Node           :c2, after c1, 1d
    Vector Search Node          :c3, after c2, 1d
    Graph Traversal Node        :c4, after c2, 1d
    Fusion & Rerank Node        :c5, after c3, 1d
    
    section Phase 4: Frontend
    Streamlit UI                :d1, after c5, 2d
    Results Visualization       :d2, after d1, 1d
    
    section Phase 5: Deploy
    Streamlit Cloud Deploy      :e1, after d2, 1d
    GitHub Actions CI/CD        :e2, after e1, 1d
```

### Phase Breakdown

#### Phase 1: Foundation (Days 1-2)
```
□ Initialize project structure
□ Set up virtual environment
□ Create Neo4j Aura instance
□ Create Pinecone index
□ Configure environment variables
□ Set up Git repository
```

#### Phase 2: Data Pipeline (Days 3-5)
```
□ Build GitHub API client with rate limiting
□ Parse requirements.txt / pyproject.toml / package.json
□ Create README embedding pipeline
□ Build Cypher queries for graph population
□ Load initial dataset (1000 popular repos)
```

#### Phase 3: Agent Core (Days 6-9)
```
□ Define LangGraph state schema
□ Implement query parser (Gemini)
□ Implement vector search node
□ Implement graph traversal node
□ Implement fusion logic (RRF)
□ Implement response generator
□ Add retry/fallback logic
```

#### Phase 4: Frontend (Days 10-11)
```
□ Build Streamlit layout
□ Create search input component
□ Build results cards
□ Add graph visualization (optional)
□ Style with custom CSS
```

#### Phase 5: Deployment (Days 12-14)
```
□ Push to GitHub
□ Connect Streamlit Cloud
□ Configure secrets
□ Set up GitHub Actions for data refresh
□ Write README documentation
□ Create demo video
```

---

## 💰 Cost Breakdown

```mermaid
pie title Monthly Operating Cost
    "Streamlit Cloud" : 0
    "Pinecone Starter" : 0
    "Neo4j Aura Free" : 0
    "Gemini Free Tier" : 0
    "GitHub Actions" : 0
    "Domain (Optional)" : 0
```

### Detailed Cost Analysis

| Service | Free Tier Limit | Our Usage | Monthly Cost |
|---------|-----------------|-----------|--------------|
| Streamlit Cloud | Unlimited public apps | 1 app | **$0** |
| Pinecone Serverless | 100K vectors | ~50K | **$0** |
| Neo4j Aura | 200K nodes | ~100K | **$0** |
| Gemini 1.5 Flash | 15 RPM, 1M TPM | ~10 RPM avg | **$0** |
| GitHub Actions | 2000 min/month | ~100 min | **$0** |
| Custom Domain | Optional | - | **$0-12/yr** |
| **TOTAL** | | | **$0** |

### Scaling Path (If Needed Later)

| Trigger | Upgrade Path | New Cost |
|---------|--------------|----------|
| >100K vectors | Pinecone Standard | $70/mo |
| >200K nodes | Neo4j Aura Pro | $65/mo |
| >15 RPM sustained | Gemini Pay-as-you-go | ~$0.001/query |
| Custom domain | Namecheap/Cloudflare | $12/year |

---

## 🎯 Success Metrics

```mermaid
graph LR
    subgraph "User Metrics"
        A[Query to Result: < 3s]
        B[Result Relevance: > 80%]
        C[User Retention: Daily Active]
    end
    
    subgraph "Technical Metrics"
        D[API Latency: < 500ms]
        E[Error Rate: < 1%]
        F[Uptime: 99%]
    end
    
    subgraph "Portfolio Metrics"
        G[GitHub Stars]
        H[Demo Views]
        I[Interview Mentions]
    end
```

---

## 📁 Final Project Structure

```
GITGRAPH/
├── .streamlit/
│   └── secrets.toml          # API keys (gitignored)
├── .github/
│   └── workflows/
│       ├── ci.yml            # Test & lint
│       └── data-refresh.yml  # Daily ingestion
├── app/
│   ├── main.py               # Streamlit entry
│   ├── components/
│   │   ├── search_bar.py
│   │   ├── result_card.py
│   │   └── graph_viz.py
│   └── styles/
│       └── custom.css
├── agent/
│   ├── graph.py              # LangGraph definition
│   ├── state.py              # State schema
│   └── nodes/
│       ├── query_parser.py
│       ├── vector_search.py
│       ├── graph_traversal.py
│       ├── fusion.py
│       └── response_gen.py
├── db/
│   ├── neo4j_client.py
│   ├── pinecone_client.py
│   └── schemas.py
├── ingestion/
│   ├── github_fetcher.py
│   ├── dependency_parser.py
│   ├── embedder.py
│   └── graph_builder.py
├── tests/
│   ├── test_agent.py
│   └── test_ingestion.py
├── requirements.txt
├── README.md
└── ARCHITECTURE.md           # This file
```

---

## 🔗 Quick Links

| Resource | URL |
|----------|-----|
| Streamlit Cloud | https://streamlit.io/cloud |
| Neo4j Aura | https://neo4j.com/cloud/aura/ |
| Pinecone | https://www.pinecone.io/ |
| Google AI Studio | https://aistudio.google.com/ |
| LangGraph Docs | https://langchain-ai.github.io/langgraph/ |

---

> **Built with Ramakrishna | 2026**  
> *Proving that $0 budget ≠ $0 value*
