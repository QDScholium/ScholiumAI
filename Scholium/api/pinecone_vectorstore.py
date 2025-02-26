'''
My own wrapper for a Pinecone index because the Langchain one only works for documents
'''
import ast

class ScholiumPineconeVectorStore():
    """
    A wrapper class for Pinecone vector database operations.
    
    This class provides an interface for embedding queries and performing similarity searches
    using a Pinecone vector index. It is designed to work with OpenAI embeddings.

    Attributes:
        client: The embedding client (typically OpenAIEmbeddings) used to generate embeddings
        index: The Pinecone index instance to perform vector searches against

    Args:
        embedding_client: An embedding client that provides embedding generation functionality
        index: A Pinecone index instance for vector storage and retrieval
    """
    def __init__(self, embedding_client, index) -> None:
        self.client = embedding_client
        self.index = index

    def _openAI_embed_query(self,query):
        return self.client.embeddings.create(
            input= query,
            model= "text-embedding-3-small"
        ).data[0].embedding
    
    def _filter_results(self, responses:list, score_cutoff = 0.8):
        '''
        This exists because, for some stupid reason, pinecone doesn't have a builtin way to cutoff low similarity responses
        '''
        return([
            response for response in responses if response['score'] >= score_cutoff
        ])
    
    def _parse_authors(self, author_strings):
        return [f"{lastname}, {firstname}" for lastname, firstname, _ in (ast.literal_eval(entry)[:3] for entry in author_strings)]
    

    def similarity_search(self, query, top_k = 10):
        embedded_query = self._openAI_embed_query(query)
        results = self.index.query(
            namespace="",
            vector=embedded_query,
            top_k = top_k,
            include_metadata = True
        )['matches']
        for result in results:
            result['metadata']["authors"] = self._parse_authors(result['metadata']["authors"])
        return results 
    
    def similarity_search_with_score_cutoff(self, query, top_k, score_cutoff):
        return self._filter_results(self.similarity_search(query, top_k), score_cutoff)
    
if __name__ == "__main__":
    import os
    from openai import OpenAI
    from pinecone import Pinecone
    from dotenv import load_dotenv

    load_dotenv()

    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    pinecone_api_key = os.environ.get("PINECONE_API_KEY")


    index_name = "arxiv-index"
    pc = Pinecone(api_key= pinecone_api_key)
    index = pc.Index(index_name)
    client = OpenAI(api_key=OPENAI_API_KEY)
    vector_store = ScholiumPineconeVectorStore(embedding_client= client, index = index)

    # print(vector_store._parse_authors((["['Chalkidis', 'Ilias', '']", "['Fergadiotis', 'Manos', '']", "['Malakasiotis', 'Prodromos', '']", "['Aletras', 'Nikolaos', '']", "['Androutsopoulos', 'Ion', '']"])))
    results = vector_store.similarity_search("BERT algorithm overview", 5)
    print(results)