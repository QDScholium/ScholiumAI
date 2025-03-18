from openai import OpenAI
import json
import os
from dotenv import load_dotenv
import langchain
from pydantic import BaseModel, Field

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class SearchParameters(BaseModel):
    """
    Structured parameters for academic search queries.
    
    This model defines the parameters that can be extracted from a natural language
    search query to facilitate structured academic paper searches.
    """
    authors: list[str] = Field(
        description="List of author names to filter search results"
    )
    concepts: list[str] = Field(
        description="List of key topics or concepts to search for"
    )
    language: str = Field(
        description="Language of the papers to search for"
    )
    n_papers: int = Field(
        description="Number of papers to retrieve",
    )
    institutions: list[str] = Field(
        description="List of research institutions or universities to filter search results"
    )
    
def extract_search_parameters(query: str, client) -> SearchParameters:
    """
    Extract structured search parameters from a natural language query.
    
    Args:
        query (str): The natural language search query
        
    Returns:
        SearchParameters: Structured parameters extracted from the query
    """
    return client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Extract academic search parameters from the user's query."},
            {"role": "user", "content": query},
        ],
        response_format=SearchParameters,
        max_tokens=100,
        temperature=0.0,
    ).choices[0].message.parsed

# Example usage
if __name__ == "__main__":

    import time
    
    query = "Find 15 papers about transformer models by Vaswani and Hinton in English from U of T"
    start_time = time.time()
    search_params = extract_search_parameters(query, client)
    end_time = time.time()
    print("Test 1 - Extracted Search Parameters:")
    print(f"Authors: {search_params.authors}")
    print(f"Concepts: {search_params.concepts}")
    print(f"Language: {search_params.language}")
    print(f"Number of papers: {search_params.n_papers}")
    print(f"Institutions: {search_params.institutions}")
    print(f"Time taken: {end_time - start_time:.4f} seconds")
    
    query2 = "Show me 5 recent papers on quantum computing by researchers at MIT in any language"
    start_time = time.time()
    search_params2 = extract_search_parameters(query2, client)
    end_time = time.time()
    print("\nTest 2 - Extracted Search Parameters:")
    print(f"Authors: {search_params2.authors}")
    print(f"Concepts: {search_params2.concepts}")
    print(f"Language: {search_params2.language}")
    print(f"Number of papers: {search_params2.n_papers}")
    print(f"Institutions: {search_params2.institutions}")
    print(f"Time taken: {end_time - start_time:.4f} seconds")