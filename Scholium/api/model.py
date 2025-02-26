import os

from langchain_core.tools import tool
from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableConfig
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore

from langgraph.graph import END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import MessagesState, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI,OpenAIEmbeddings

from dotenv import load_dotenv

from typing import Optional
from pydantic import BaseModel, Field

from api.model_utils import get_paper_metadata, extract_paper_titles

from copilotkit.langgraph import copilotkit_customize_config



load_dotenv()

LANGSMITH_API_KEY = os.environ.get("LANGSMITH_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
DB_URI = os.environ.get("DB_URI")
pinecone_api_key = os.environ.get("PINECONE_API_KEY")
model = ChatOpenAI(
    model="gpt-4o",
    temperature=1,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

pc = Pinecone(api_key= pinecone_api_key)
index = pc.Index("scholium-index")
vector_store = PineconeVectorStore(embedding=embeddings, index=index)

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
    retrieved_docs = vector_store.similarity_search(query, k=5)
    serialized_docs = []
    retrieved_metadata = {}
    for doc in retrieved_docs:
        formatted_doc = f"Source: {doc.metadata}\nContent: {doc.page_content}"
        serialized_docs.append(formatted_doc)
        retrieved_metadata[doc.metadata['Title']] = doc.metadata
    serialized = "\n\n".join(serialized_docs)
    return serialized, retrieved_metadata

def query_or_respond(state: MessagesState):
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
def PaperSummaryTool(summary: str): # pylint: disable=invalid-name,unused-argument
    """
    Summarize the contents of each paper excerpt from the retrieved context. Make sure that each summary is one paragraph long and 
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

    system_message_content = (
        "You are an assistant for question-answering tasks. Your job is to recommend and summarize papers from the retrieved context."
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Do not make up sources or use sources that are not in the retrieved context."
        "\n\n"
        f"{docs_content}"
    )

    prompt = [SystemMessage(system_message_content)]

    # Double texting
    for message in state["messages"]:
        if message.type in ("human", "system") or (message.type == "ai" and not message.tool_calls):
            prompt.append(message)
    response = await model.bind_tools(
        [PaperSummaryTool],
        tool_choice="PaperSummaryTool"
    ).ainvoke(
        prompt,
        config)
    response = response.tool_calls[0]["args"]
    return {"answer": response, "paper_metadata": response["metadata"]}



def generate(state: MessagesState, config):
    '''
    Generates the desired answer to the user's question
    '''
    recent_tool_messages = []
    for message in reversed(state["messages"]):
        if message.type == "tool":
            recent_tool_messages.append(message)
        else:
            break
    tool_messages = recent_tool_messages[::-1]

    docs_content = "\n\n".join(doc.content for doc in tool_messages)

    system_message_content = (
        "You are an assistant for question-answering tasks. Your job is to recommend papers from the retrieved context."
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Do not make up sources or use sources that are not in the retrieved context."
        "Surround the titles of the papers with quotation marks."
        "\n\n"
        f"{docs_content}"
    )

    prompt = [SystemMessage(system_message_content)]
    for message in state["messages"]:
        if message.type in ("human", "system") or (message.type == "ai" and not message.tool_calls):
            prompt.append(message)
    response = model.invoke(prompt)
    used_papers = extract_paper_titles(response.content)
    metadata = get_paper_metadata(used_papers, tool_messages[0].artifact)
    print(response)
    return {"messages": [response], "answer": response.content, "paper_metadata": metadata}


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
