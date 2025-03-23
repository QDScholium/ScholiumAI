from api.openalex import WorksHandler, IDHandler
from api.text_splitter import extract_search_parameters
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()


def search_parameters_to_search(query: str, client: OpenAI, idhandler: IDHandler, workshandler = WorksHandler):
    params = extract_search_parameters(query, client=client)
    filters= {}
    if params.authors:
        authors = [idhandler.get_author_id(author) for author in params.authors]
        filters["author"] = ",".join(authors)
        
    if params.concepts:
        concepts = [idhandler.get_topic_id(concept) for concept in params.concepts]
        filters["concept"] = ",".join(concepts)
        
    if params.institutions:
        institutions = [idhandler.get_institution_id(institution) for institution in params.institutions]
        filters["institution"] = ",".join(institutions)

    if params.language: filters["language"] = params.language  

    n_papers = params.n_papers if params.n_papers else 10
    
    results = workshandler.search(query=query,filters=filters, n_results= n_papers)
    print(results)

if __name__ == '__main__':
    idhandler = IDHandler("sunny@scholium.ai")
    wh = WorksHandler("sunny@scholium.ai")
    query = "Find 15 papers about transformer models by Vaswani and Hinton in English from U of T"
    search_parameters_to_search(client=client, query=query, idhandler=idhandler, workshandler=wh)
