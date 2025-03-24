from api.text_splitter import extract_search_parameters
from dotenv import load_dotenv
import time
from openai import OpenAI
import os

load_dotenv()

client = OpenAI()

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


query2 = "give me papers on transformers"
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