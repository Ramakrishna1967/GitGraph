"""Seed database with sample AI/ML repositories."""

from db import pinecone_client, neo4j_client


SEED_REPOS = [
    {
        "full_name": "langchain-ai/langchain",
        "name": "langchain",
        "description": "Build context-aware reasoning applications with LangChain",
        "stars": 75000,
        "language": "Python",
        "url": "https://github.com/langchain-ai/langchain",
        "readme": "LangChain is a framework for developing applications powered by language models.",
        "dependencies": ["pydantic", "openai", "tiktoken"]
    },
    {
        "full_name": "openai/openai-python",
        "name": "openai-python",
        "description": "The official Python library for the OpenAI API",
        "stars": 18000,
        "language": "Python",
        "url": "https://github.com/openai/openai-python",
        "readme": "The OpenAI Python library provides convenient access to the OpenAI REST API.",
        "dependencies": ["httpx", "pydantic", "typing-extensions"]
    },
    {
        "full_name": "Unstructured-IO/unstructured",
        "name": "unstructured",
        "description": "Open source libraries for pre-processing documents for LLM applications",
        "stars": 5200,
        "language": "Python",
        "url": "https://github.com/Unstructured-IO/unstructured",
        "readme": "Unstructured provides tools for ingesting and preprocessing documents.",
        "dependencies": ["langchain", "pypdf", "nltk", "pillow"]
    },
    {
        "full_name": "chroma-core/chroma",
        "name": "chroma",
        "description": "The AI-native open-source embedding database",
        "stars": 12000,
        "language": "Python",
        "url": "https://github.com/chroma-core/chroma",
        "readme": "Chroma is the open-source embedding database for LLM apps.",
        "dependencies": ["pydantic", "fastapi", "numpy"]
    },
    {
        "full_name": "run-llama/llama_index",
        "name": "llama_index",
        "description": "LlamaIndex is a data framework for LLM applications",
        "stars": 28000,
        "language": "Python",
        "url": "https://github.com/run-llama/llama_index",
        "readme": "LlamaIndex provides tools for data ingestion, structuring, and retrieval.",
        "dependencies": ["langchain", "openai", "tiktoken"]
    },
    {
        "full_name": "huggingface/transformers",
        "name": "transformers",
        "description": "State-of-the-art Machine Learning for PyTorch, TensorFlow, and JAX",
        "stars": 120000,
        "language": "Python",
        "url": "https://github.com/huggingface/transformers",
        "readme": "Transformers provides thousands of pretrained models.",
        "dependencies": ["torch", "numpy", "tokenizers"]
    },
    {
        "full_name": "pinecone-io/pinecone-python-client",
        "name": "pinecone-python-client",
        "description": "The Pinecone Python client",
        "stars": 800,
        "language": "Python",
        "url": "https://github.com/pinecone-io/pinecone-python-client",
        "readme": "The Pinecone Python client for vector database operations.",
        "dependencies": ["requests", "urllib3"]
    },
    {
        "full_name": "pydantic/pydantic",
        "name": "pydantic",
        "description": "Data validation using Python type hints",
        "stars": 17000,
        "language": "Python",
        "url": "https://github.com/pydantic/pydantic",
        "readme": "Pydantic is the most widely used data validation library for Python.",
        "dependencies": []
    },
    {
        "full_name": "tiangolo/fastapi",
        "name": "fastapi",
        "description": "FastAPI framework, high performance, ready for production",
        "stars": 68000,
        "language": "Python",
        "url": "https://github.com/tiangolo/fastapi",
        "readme": "FastAPI is a modern web framework for building APIs with Python.",
        "dependencies": ["pydantic", "starlette", "uvicorn"]
    },
    {
        "full_name": "streamlit/streamlit",
        "name": "streamlit",
        "description": "A faster way to build and share data apps",
        "stars": 29000,
        "language": "Python",
        "url": "https://github.com/streamlit/streamlit",
        "readme": "Streamlit turns data scripts into shareable web apps.",
        "dependencies": ["pandas", "numpy", "altair"]
    }
]


def seed_database():
    """Seed both Pinecone and Neo4j with sample data."""
    print("Seeding database with sample repositories...\n")
    
    pinecone_client.create_index()
    neo4j_client.create_constraints()
    
    print("\n" + "="*60)
    
    for i, repo in enumerate(SEED_REPOS, 1):
        print(f"\n[{i}/{len(SEED_REPOS)}] Processing: {repo['full_name']}")
        
        pinecone_client.upsert_repo(
            repo_id=repo['full_name'],
            readme_text=repo['readme'],
            metadata={
                "name": repo['name'],
                "description": repo['description'],
                "stars": repo['stars'],
                "language": repo['language'],
                "url": repo['url']
            }
        )
        
        neo4j_client.create_repo_node(
            full_name=repo['full_name'],
            metadata={
                "name": repo['name'],
                "description": repo['description'],
                "stars": repo['stars'],
                "forks": 0,
                "language": repo['language'],
                "url": repo['url']
            }
        )
        
        if repo['dependencies']:
            for dep in repo['dependencies']:
                dep_repo = next((r for r in SEED_REPOS if r['name'] == dep), None)
                if dep_repo:
                    neo4j_client.create_dependency(
                        from_repo=repo['full_name'],
                        to_repo=dep_repo['full_name']
                    )
        
        print(f"  Done!")
    
    print("\n" + "="*60)
    print("\nDatabase Statistics:")
    
    neo4j_stats = neo4j_client.get_stats()
    print(f"  Neo4j: {neo4j_stats['repos']} repos, {neo4j_stats['dependencies']} dependencies")
    
    pinecone_stats = pinecone_client.get_stats()
    print(f"  Pinecone: {pinecone_stats.get('total_vector_count', 0)} vectors")
    
    print("\nDatabase seeding complete!")
    neo4j_client.close()


if __name__ == "__main__":
    seed_database()
