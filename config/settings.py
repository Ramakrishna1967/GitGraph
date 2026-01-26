"""Configuration settings for GitGraph RAG."""

import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)


class Settings:
    """Application settings from environment variables."""
    
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    GEMINI_MODEL: str = "gemini-2.0-flash"
    EMBEDDING_MODEL: str = "models/text-embedding-004"
    
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY", "")
    PINECONE_INDEX_NAME: str = os.getenv("PINECONE_INDEX_NAME", "gitgraph-index")
    PINECONE_DIMENSION: int = 768
    
    NEO4J_URI: str = os.getenv("NEO4J_URI", "")
    NEO4J_USER: str = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD", "")
    
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    
    PROJECT_NAME: str = "GitGraph RAG"
    VERSION: str = "0.1.0"
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required settings are present."""
        required = [
            ("GOOGLE_API_KEY", cls.GOOGLE_API_KEY),
            ("PINECONE_API_KEY", cls.PINECONE_API_KEY),
            ("NEO4J_URI", cls.NEO4J_URI),
            ("NEO4J_PASSWORD", cls.NEO4J_PASSWORD),
        ]
        
        missing = [name for name, value in required if not value]
        
        if missing:
            print(f"Missing required settings: {', '.join(missing)}")
            return False
        
        print("All required settings loaded")
        return True


settings = Settings()
