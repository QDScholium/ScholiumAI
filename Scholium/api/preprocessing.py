from api.openalex import WorksHandler
from api.text_splitter import extract_search_parameters
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

def search_parameters_to_search(query, client):
    params = extract_search_parameters(query, client=client)
    filters= {}
    if params.authors:
        pass
    if params.concepts:
        pass
    if params.institutions:
        pass

    if params.language: filters["language"] = params.language   
    n_papers = params.n_papers if params.n_papers else 10
    print(params)

if __name__ == '__main__':
    query = "Find 15 papers about transformer models by Vaswani and Hinton in English from U of T"
    search_parameters_to_search(client=client, query=query)
