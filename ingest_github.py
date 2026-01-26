"""Ingest repos from GitHub into Pinecone and Neo4j."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from ingestion import github_fetcher
from db import pinecone_client, neo4j_client


def ingest_repo(full_name: str) -> bool:
    """Ingest a single repo into both databases."""
    parts = full_name.split("/")
    if len(parts) != 2:
        print(f"Invalid repo name: {full_name}")
        return False
    
    owner, repo = parts
    print(f"\nIngesting: {full_name}")
    
    # Fetch repo data
    print("  Fetching metadata...")
    repo_data = github_fetcher.fetch_repo(owner, repo)
    if not repo_data:
        return False
    
    # Fetch README
    print("  Fetching README...")
    readme = github_fetcher.fetch_readme(owner, repo)
    if not readme:
        readme = repo_data.get("description", "")
    
    # Fetch dependencies
    print("  Fetching dependencies...")
    deps = github_fetcher.fetch_dependencies(owner, repo)
    
    # Add to Pinecone
    print("  Adding to Pinecone...")
    pinecone_client.upsert_repo(
        repo_id=full_name,
        readme_text=readme,
        metadata={
            "name": repo_data["name"],
            "description": repo_data["description"],
            "stars": repo_data["stars"],
            "language": repo_data["language"],
            "url": repo_data["url"]
        }
    )
    
    # Add to Neo4j
    print("  Adding to Neo4j...")
    neo4j_client.create_repo_node(
        full_name=full_name,
        metadata=repo_data
    )
    
    # Add dependencies
    if deps:
        print(f"  Adding {len(deps)} dependencies...")
        for dep in deps:
            neo4j_client.create_dependency(full_name, dep)
    
    print(f"  Done!")
    return True


def ingest_from_search(query: str, limit: int = 20):
    """Ingest repos from a GitHub search."""
    print(f"\nSearching GitHub for: {query}")
    repos = github_fetcher.search_repos(query, limit=limit)
    
    print(f"Found {len(repos)} repos")
    
    success = 0
    for repo in repos:
        if ingest_repo(repo):
            success += 1
    
    print(f"\nIngested {success}/{len(repos)} repos")


def main():
    print("=" * 60)
    print("GitGraph RAG - GitHub Ingestion")
    print("=" * 60)
    
    # Initialize databases
    print("\nInitializing databases...")
    pinecone_client.create_index()
    neo4j_client.create_constraints()
    
    # Ingest popular AI/ML repos
    queries = [
        "langchain",
        "llm framework",
        "vector database python",
        "rag retrieval"
    ]
    
    for query in queries:
        ingest_from_search(query, limit=10)
    
    # Show stats
    print("\n" + "=" * 60)
    print("Final Statistics:")
    neo4j_stats = neo4j_client.get_stats()
    print(f"  Neo4j: {neo4j_stats['repos']} repos, {neo4j_stats['dependencies']} dependencies")
    
    pinecone_stats = pinecone_client.get_stats()
    print(f"  Pinecone: {pinecone_stats.get('total_vector_count', 0)} vectors")
    
    neo4j_client.close()
    print("\nDone!")


if __name__ == "__main__":
    main()
