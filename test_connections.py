"""Test database connections and basic operations."""

import sys
from config import settings
from db import pinecone_client, neo4j_client


def test_settings():
    """Test settings are loaded."""
    print("\nTesting Settings...")
    if settings.validate():
        print("All settings loaded correctly")
        return True
    else:
        print("Settings validation failed")
        return False


def test_neo4j():
    """Test Neo4j connection."""
    print("\nTesting Neo4j Connection...")
    try:
        if neo4j_client.test_connection():
            print("Neo4j connection successful")
            neo4j_client.create_constraints()
            stats = neo4j_client.get_stats()
            print(f"   Repos: {stats['repos']}, Dependencies: {stats['dependencies']}")
            return True
        else:
            print("Neo4j connection failed")
            return False
    except Exception as e:
        print(f"Neo4j error: {e}")
        return False


def test_pinecone():
    """Test Pinecone connection."""
    print("\nTesting Pinecone Connection...")
    try:
        pinecone_client.create_index()
        stats = pinecone_client.get_stats()
        print(f"Pinecone connection successful")
        print(f"Index: {settings.PINECONE_INDEX_NAME}")
        print(f"Vectors: {stats.get('total_vector_count', 0)}")
        return True
    except Exception as e:
        print(f"Pinecone error: {e}")
        return False


def test_embedding():
    """Test embedding generation."""
    print("\nTesting Gemini Embeddings...")
    try:
        test_text = "LangChain is a framework for building LLM applications"
        vector = pinecone_client.embed_text(test_text)
        print(f"Embedding generated successfully")
        print(f"Dimension: {len(vector)}")
        return True
    except Exception as e:
        print(f"Embedding error: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("GitGraph RAG - Connection Tests")
    print("=" * 60)
    
    results = {
        "Settings": test_settings(),
        "Neo4j": test_neo4j(),
        "Pinecone": test_pinecone(),
        "Embeddings": test_embedding(),
    }
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "PASS" if passed else "FAIL"
        print(f"{test_name:15} {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("All tests passed! Ready to build.")
    else:
        print("Some tests failed. Check your configuration.")
    print("=" * 60)
    
    neo4j_client.close()
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
