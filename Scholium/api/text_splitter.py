from openai import OpenAI
import json
import os
from dotenv import load_dotenv
import langchain
from pydantic import BaseModel, Field

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