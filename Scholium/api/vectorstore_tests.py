import os
from openai import OpenAI
from dotenv import load_dotenv
from pinecone.grpc import PineconeGRPC as Pinecone

from api.pinecone_vectorstore import ScholiumPineconeVectorStore

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
pinecone_api_key = os.environ.get("PINECONE_API_KEY")


index_name = "arxiv-index"
pc = Pinecone(api_key= pinecone_api_key)
index = pc.Index(index_name)
client = OpenAI(api_key=OPENAI_API_KEY)
vector_store = ScholiumPineconeVectorStore(embedding_client= client, index = index)

def test_accuracy():
    for _ in range(10):
        results = vector_store.similarity_search("BERT algorithm overview", 5)
        for result in results:
            assert "BART" not in result['metadata']["summary"]
            assert "Bayesian" not in result['metadata']["summary"]
    print("Accuracy test passed!")


def run_tests():
    test_accuracy()

if __name__ == "__main__":
    run_tests()