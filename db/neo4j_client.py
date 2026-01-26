"""Neo4j client for graph database operations."""

from typing import List, Dict, Any, Optional
from neo4j import GraphDatabase

from config import settings
from db.schemas import RepoResult


class Neo4jClient:
    """Wrapper for Neo4j graph database."""
    
    def __init__(self):
        self.driver = GraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
        )
        
    def close(self):
        """Close driver connection."""
        self.driver.close()
        
    def test_connection(self) -> bool:
        """Test Neo4j connection."""
        try:
            with self.driver.session() as session:
                result = session.run("RETURN 1 as test")
                return result.single()["test"] == 1
        except Exception as e:
            print(f"Neo4j connection failed: {e}")
            return False
    
    def create_constraints(self):
        """Create uniqueness constraints."""
        with self.driver.session() as session:
            session.run("""
                CREATE CONSTRAINT repo_name IF NOT EXISTS
                FOR (r:Repository) REQUIRE r.full_name IS UNIQUE
            """)
            print("Neo4j constraints created")
    
    def create_repo_node(self, full_name: str, metadata: Dict[str, Any]) -> None:
        """Create or update a repository node."""
        with self.driver.session() as session:
            session.run("""
                MERGE (r:Repository {full_name: $full_name})
                SET r.name = $name,
                    r.description = $description,
                    r.stars = $stars,
                    r.forks = $forks,
                    r.language = $language,
                    r.url = $url
            """, 
                full_name=full_name,
                name=metadata.get("name", ""),
                description=metadata.get("description", ""),
                stars=metadata.get("stars", 0),
                forks=metadata.get("forks", 0),
                language=metadata.get("language", ""),
                url=metadata.get("url", "")
            )
    
    def create_dependency(self, from_repo: str, to_repo: str, version: Optional[str] = None) -> None:
        """Create a DEPENDS_ON relationship between repos."""
        with self.driver.session() as session:
            session.run("""
                MATCH (from:Repository {full_name: $from_repo})
                MERGE (to:Repository {full_name: $to_repo})
                MERGE (from)-[d:DEPENDS_ON]->(to)
                SET d.version = $version
            """,
                from_repo=from_repo,
                to_repo=to_repo,
                version=version or ""
            )
    
    def find_repos_depending_on(self, dependency: str, limit: int = 10) -> List[RepoResult]:
        """Find repositories that depend on a specific package."""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (r:Repository)-[:DEPENDS_ON]->(dep:Repository)
                WHERE dep.full_name CONTAINS $dependency 
                   OR dep.name = $dependency
                RETURN r.full_name as full_name,
                       r.name as name,
                       r.description as description,
                       r.stars as stars,
                       r.language as language,
                       r.url as url
                ORDER BY r.stars DESC
                LIMIT $limit
            """,
                dependency=dependency,
                limit=limit
            )
            
            repos = []
            for record in result:
                repos.append(RepoResult(
                    name=record["name"],
                    full_name=record["full_name"],
                    description=record["description"],
                    stars=record["stars"],
                    language=record["language"],
                    score=1.0,
                    url=record["url"]
                ))
            
            return repos
    
    def find_popular_repos(self, language: Optional[str] = None, min_stars: int = 100, limit: int = 10) -> List[RepoResult]:
        """Find popular repositories."""
        with self.driver.session() as session:
            query = """
                MATCH (r:Repository)
                WHERE r.stars >= $min_stars
            """
            
            if language:
                query += " AND r.language = $language"
            
            query += """
                RETURN r.full_name as full_name,
                       r.name as name,
                       r.description as description,
                       r.stars as stars,
                       r.language as language,
                       r.url as url
                ORDER BY r.stars DESC
                LIMIT $limit
            """
            
            result = session.run(
                query,
                min_stars=min_stars,
                language=language,
                limit=limit
            )
            
            repos = []
            for record in result:
                repos.append(RepoResult(
                    name=record["name"],
                    full_name=record["full_name"],
                    description=record["description"],
                    stars=record["stars"],
                    language=record["language"],
                    score=1.0,
                    url=record["url"]
                ))
            
            return repos
    
    def get_stats(self) -> Dict[str, int]:
        """Get database statistics."""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (r:Repository)
                OPTIONAL MATCH ()-[d:DEPENDS_ON]->()
                RETURN count(DISTINCT r) as repo_count,
                       count(d) as dependency_count
            """)
            
            record = result.single()
            return {
                "repos": record["repo_count"],
                "dependencies": record["dependency_count"]
            }


neo4j_client = Neo4jClient()
