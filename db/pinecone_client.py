"""Pinecone client for vector search operations."""

from typing import List, Dict, Any, Optional
from pinecone import Pinecone, ServerlessSpec
import google.generativeai as genai

from config import settings
from db.schemas import RepoResult


class PineconeClient:
    """Wrapper for Pinecone vector database."""
    
    def __init__(self):
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.index_name = settings.PINECONE_INDEX_NAME
        self.index = None
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        
    def create_index(self):
        """Create Pinecone index if it doesn't exist."""
        if self.index_name not in self.pc.list_indexes().names():
            print(f"Creating index: {self.index_name}")
            self.pc.create_index(
                name=self.index_name,
                dimension=settings.PINECONE_DIMENSION,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )
            print(f"Index created: {self.index_name}")
        else:
            print(f"Index already exists: {self.index_name}")
        
        self.index = self.pc.Index(self.index_name)
        
    def embed_text(self, text: str) -> List[float]:
        """Convert text to vector embedding."""
        result = genai.embed_content(
            model=settings.EMBEDDING_MODEL,
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']
    
    def upsert_repo(self, repo_id: str, readme_text: str, metadata: Dict[str, Any]) -> None:
        """Add or update a repository in the vector database."""
        if not self.index:
            self.create_index()
        
        vector = self.embed_text(readme_text)
        self.index.upsert(vectors=[(repo_id, vector, metadata)])
        
    def search(self, query: str, top_k: int = 10, filter_dict: Optional[Dict] = None) -> List[RepoResult]:
        """Semantic search for repositories."""
        if not self.index:
            self.create_index()
        
        query_vector = self.embed_text(query)
        
        results = self.index.query(
            vector=query_vector,
            top_k=top_k,
            include_metadata=True,
            filter=filter_dict
        )
        
        repo_results = []
        for match in results.matches:
            repo_results.append(RepoResult(
                name=match.metadata.get("name", ""),
                full_name=match.id,
                description=match.metadata.get("description"),
                stars=match.metadata.get("stars", 0),
                language=match.metadata.get("language"),
                score=match.score,
                url=match.metadata.get("url", "")
            ))
        
        return repo_results
    
    def get_stats(self) -> Dict[str, Any]:
        """Get index statistics."""
        if not self.index:
            self.create_index()
        return self.index.describe_index_stats()


pinecone_client = PineconeClient()
