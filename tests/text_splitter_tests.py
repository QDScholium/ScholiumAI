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
print(f"Query: {search_params.query}")
print(f"Authors: {search_params.authors}")
print(f"Topics: {search_params.topics}")
print(f"Language: {search_params.language}")
print(f"Number of papers: {search_params.n_papers}")
print(f"Time taken: {end_time - start_time:.4f} seconds")

query2 = "Show me 5 recent papers on quantum computing by researchers at MIT in any language"
start_time = time.time()
search_params2 = extract_search_parameters(query2, client)
end_time = time.time()
print("\nTest 2 - Extracted Search Parameters:")
print(f"Query: {search_params2.query}")
print(f"Authors: {search_params2.authors}")
print(f"Topics: {search_params2.topics}")
print(f"Language: {search_params2.language}")
print(f"Number of papers: {search_params2.n_papers}")
print(f"Time taken: {end_time - start_time:.4f} seconds")

query3 = "give me papers on transformers"
start_time = time.time()
search_params3 = extract_search_parameters(query3, client)
end_time = time.time()
print("\nTest 3 - Extracted Search Parameters:")
print(f"Query: {search_params3.query}")
print(f"Authors: {search_params3.authors}")
print(f"Topics: {search_params3.topics}")
print(f"Language: {search_params3.language}")
print(f"Number of papers: {search_params3.n_papers}")
print(f"Time taken: {end_time - start_time:.4f} seconds")

query4 = "Why is the sky blue?"
start_time = time.time()
search_params4 = extract_search_parameters(query4, client)
end_time = time.time()
print("\nTest 4 - Extracted Search Parameters:")
print(f"Query: {search_params4.query}")
print(f"Authors: {search_params4.authors}")
print(f"Topics: {search_params4.topics}")
print(f"Language: {search_params4.language}")
print(f"Number of papers: {search_params4.n_papers}")
print(f"Time taken: {end_time - start_time:.4f} seconds")

query5 = "Hi!"
start_time = time.time()
search_params5 = extract_search_parameters(query5, client)
end_time = time.time()
print("\nTest 5 - Extracted Search Parameters:")
print(f"Query: {search_params5.query}")
print(f"Authors: {search_params5.authors}")
print(f"Topics: {search_params5.topics}")
print(f"Language: {search_params5.language}")
print(f"Number of papers: {search_params5.n_papers}")
print(f"Time taken: {end_time - start_time:.4f} seconds")