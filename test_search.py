"""
Test the search agent with sample queries.
"""

from agent.search import search_repos, format_results


def test_search():
    """Test different types of queries."""
    
    test_queries = [
        "PDF parser for Python",
        "works with langchain",
        "data validation library",
        "web framework",
    ]
    
    for query in test_queries:
        print("\n" + "="*70)
        response = search_repos(query, top_k=3)
        print(format_results(response))
        print("="*70)


if __name__ == "__main__":
    test_search()
