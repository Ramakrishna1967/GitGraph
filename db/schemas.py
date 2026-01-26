"""Pydantic models for data validation."""

from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class RepoMetadata(BaseModel):
    """Repository metadata."""
    name: str
    full_name: str
    description: Optional[str] = None
    stars: int = 0
    forks: int = 0
    language: Optional[str] = None
    topics: List[str] = Field(default_factory=list)
    owner: str = ""
    url: str = ""


class RepoResult(BaseModel):
    """Search result for a repository."""
    name: str
    full_name: str
    description: Optional[str] = None
    stars: int = 0
    language: Optional[str] = None
    score: float = 0.0
    reason: Optional[str] = None
    url: str = ""


class GitGraphState(BaseModel):
    """State for LangGraph agent."""
    query: str
    intent: Literal["semantic", "compatibility", "alternative", "hybrid"] = "hybrid"
    entities: List[str] = Field(default_factory=list)
    constraints: dict = Field(default_factory=dict)
    vector_results: List[RepoResult] = Field(default_factory=list)
    graph_results: List[RepoResult] = Field(default_factory=list)
    strategy_attempts: int = 0
    current_strategy: str = "hybrid"
    confidence_score: float = 0.0
    final_response: str = ""
    recommended_repos: List[RepoResult] = Field(default_factory=list)
    
    class Config:
        arbitrary_types_allowed = True
