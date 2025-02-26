import os
import logging

from langchain_core.tools import tool
from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableConfig
from pinecone import Pinecone

from langgraph.graph import END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import MessagesState, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI

from openai import OpenAI
from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field


from api.pinecone_vectorstore import ScholiumPineconeVectorStore

from copilotkit.langgraph import copilotkit_customize_config

load_dotenv()


logger = logging.getLogger('uvicorn.error')

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
pinecone_api_key = os.environ.get("PINECONE_API_KEY")
model = ChatOpenAI(
    model="gpt-4o",
    temperature=1,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

index_name = "arxiv-index"
pc = Pinecone(api_key= pinecone_api_key)
index = pc.Index(index_name)
client = OpenAI(api_key=OPENAI_API_KEY)
vector_store = ScholiumPineconeVectorStore(embedding_client= client, index = index)

class ResearchState(MessagesState):
    """
    This is the state of the agent.
    It is a subclass of the MessagesState class from langgraph.
    """
    answer: Optional[str]
    citations: Optional[list[str]]

@tool(response_format="content_and_artifact")
def retrieve(query: str):
    """Retrieve information related to a query."""
    retrieved_docs = vector_store.similarity_search(query= query, top_k= 10)
    logger.debug(retrieved_docs)
    serialized_docs = [
        f"Source: {doc["metadata"]} \n Content: {doc["metadata"]["summary"]}" 
        for doc in retrieved_docs
    ]

    retrieved_metadata = {
        doc['metadata']['title']: doc['metadata']
        for doc in retrieved_docs
    }
    serialized = "\n\n".join(serialized_docs)
    return serialized, retrieved_metadata

async def query_or_respond(state: MessagesState):
    """Generate tool call for retrieval or respond."""
    tool_model = model.bind_tools([retrieve])
    response = tool_model.invoke(state["messages"])
    return {"messages": [response]}

tools = ToolNode([retrieve])

class Metadata(BaseModel):
    """Model for a reference"""
    title: str = Field(description="The title of the paper")
    authors: str = Field(description="The authors of the paper ")
    publish_date: str = Field(description="The publish date of the paper")

class SummaryInput(BaseModel):
    """Input for the summarize tool"""
    markdown: str = Field(description="""
                          The markdown formatted summary of the final result.
                          If you add any headings, make sure to start at the top level (#).
                          """)
    metadata: list[Metadata] = Field(description="""
                                    A list of all The metadata of the papers used in generating the response. 
                                    """)

@tool(args_schema=SummaryInput)
def PaperSummaryTool(summary: str):
    """
    Summarize the summary of each paper from the retrieved context. Make sure that each summary is one paragraph long and 
    includes all relevant information, including the paper title. 
    """

async def generate_summary_node(state: ResearchState, config: RunnableConfig):
    """
    The generate summary node is responsible for summarizing the retrieved papers.
    """
    config = copilotkit_customize_config(
        config,
        emit_intermediate_state=[
            {
                "state_key": "answer",
                "tool": "PaperSummaryTool",
            }
        ]
    )
    recent_tool_messages = []
    for message in reversed(state["messages"]):
        if message.type == "tool":
            recent_tool_messages.append(message)
        else:
            break
    tool_messages = recent_tool_messages[::-1]

    docs_content = "\n\n".join(doc.content for doc in tool_messages)


    # Dealing with an out of context question
    if len(docs_content)==0:
        return {"answer": "Sorry, this query seems to be outside of our corpus. If you have suggestions for papers that should be included, please email: sunnywan2020@gmail.com and let me know what papers/topics I should include!", "paper_metadata": {}}

    system_message_content = (
        "You are an assistant for question-answering tasks. Your job is to recommend and summarize papers from the retrieved context."
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Do not make up sources or use sources that are not in the retrieved context."
        "\n\n"
        f"{docs_content}"
    )

    prompt = [SystemMessage(system_message_content)] + [
        message for message in state["messages"]
        if message.type in ("human", "system") or (message.type == "ai" and not message.tool_calls)
    ]   
    response = await model.bind_tools(
        [PaperSummaryTool],
        tool_choice="PaperSummaryTool"
    ).ainvoke(
        prompt,
        config)
    response = response.tool_calls[0]["args"]
    return {"answer": response, "paper_metadata": response["metadata"]}

def compile_graph():
    graph_builder = StateGraph(ResearchState)
    graph_builder.add_node(query_or_respond)
    graph_builder.add_node(tools)
    graph_builder.add_node(generate_summary_node)
    graph_builder.set_entry_point("query_or_respond")
    graph_builder.add_conditional_edges(
        "query_or_respond",
        tools_condition,
        {END: END, "tools": "tools"},
    )
    graph_builder.add_edge("tools", "generate_summary_node")
    graph_builder.add_edge("generate_summary_node", END)
    checkpointer = MemorySaver()
    graph = graph_builder.compile(checkpointer=checkpointer)
    return graph

RAG = compile_graph()
