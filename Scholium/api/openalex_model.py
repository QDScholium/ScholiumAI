import os
import logging

from api.preprocessing import search_parameters_to_search as search_open_alex
from api.openalex import IDHandler, WorksHandler

from langchain_core.tools import tool
from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableConfig

from langgraph.graph import END
from langgraph.prebuilt import ToolNode
from langgraph.graph import MessagesState, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI

from openai import OpenAI
from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from copilotkit.langgraph import copilotkit_customize_config

load_dotenv()

logger = logging.getLogger('uvicorn.error')

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
pinecone_api_key = os.environ.get("PINECONE_API_KEY")
model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=1,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

client = OpenAI(api_key=OPENAI_API_KEY)
idhandler = IDHandler("sunny@scholium.ai")
workshandler = WorksHandler("sunny@scholium.ai")

class ResearchState(MessagesState):
    """
    This is the state of the agent.
    It is a subclass of the MessagesState class from langgraph.
    """
    answer: Optional[str]
    citations: Optional[list[str]]

@tool
def retrieve(query: str):
    """Retrieve information related to a query."""
    retrieved_docs = search_open_alex(query=query, client=client, idhandler=idhandler, workshandler=workshandler)
    logger.debug(query)
    return retrieved_docs

system_prompt = """
Decide explicitly if the user's query is one of academic nature. 

- If yes, respond strictly in this format: TOOL_CALL: <query> 
- If no, respond conversationally.
"""

async def query_or_respond(state: dict) -> dict:
    prompt_messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = await model.ainvoke(prompt_messages)
    return {"messages": state["messages"] + [response]}

tools = ToolNode([retrieve])

def tools_condition_fn(state):
    # Check if the latest message is triggering a tool call
    last_msg = state["messages"][-1].content
    if "TOOL_CALL:" in last_msg:
        return ["tools"]
    return END

class Result(BaseModel):
    """A result from the academic paper search, containing the paper's title, abstract summary, and identifier.
    
    This model represents a structured output for academic paper search results,
    providing essential information about the paper including its title, a
    concise summary of its abstract content, and its OpenAlex ID for proper citation
    and reference tracking. The structured format ensures consistent presentation
    of research findings across the application."""
    title: str = Field(description="The title of the academic paper strictly in this format: <Title>")
    summary: str = Field(description="A concise summary of the paper's abstract highlighting key findings and methodology, formatted in markdown with appropriate styling")
    id: str = Field(description="The OpenAlex ID of the paper for citation and reference purposes")

class SummaryInput(BaseModel):
    """Input for the summarize tool"""
    results: list[Result] = Field(description="A list of academic paper results to be summarized")

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
    query = state["messages"][-1].content[len("TOOL_CALL:"):]

    results = search_open_alex(query, client=client, idhandler=idhandler, workshandler= workshandler)

    docs_content = ""
    paper_metadata = {}

    if not results:
        return {"answer": "NO PAPERS FOUND", "paper_metadata": {}}
    
    for paper in results:
        title = paper.get('title', 'No title available')
        abstract = paper.get('abstract', 'No abstract available')
        
        # Format the paper information
        open_alex_id = paper.get('open_alex_id', 'No ID available')
        docs_content += f"Title: {title}\nAbstract: {abstract}\nOpenAlex ID: {open_alex_id}\n\n"
        
        # Extract metadata for citation purposes
        metadata = paper.get('metadata', {})
        metadata["title"] = title  # Add title to the metadata dictionary
        paper_metadata[open_alex_id] = metadata
    # metadata_str = "".join(str(meta) for meta in paper_metadata)
    system_message_content = (
        f"Your job is to  summarize each paper relavent to the query: {query} from the retrieved context."
        "Use every following piece of retrieved context to answer"
        "the question. Write about a paragraph for each." 
        "\n\n"
        f"{docs_content}"
        # f"The metadata: {metadata_str}"
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


    [result.update({"metadata": paper_metadata[result["id"]]}) for result in response["results"]]
        
    return {"answer": response}

def compile_graph():
    graph_builder = StateGraph(ResearchState)
    graph_builder.add_node(query_or_respond)
    graph_builder.add_node(tools)
    graph_builder.add_node(generate_summary_node)
    graph_builder.set_entry_point("query_or_respond")
    graph_builder.add_conditional_edges(
        "query_or_respond",
        tools_condition_fn,
        {END: END, "tools": "tools"},
    )
    graph_builder.add_edge("tools", "generate_summary_node")
    graph_builder.add_edge("generate_summary_node", END)
    checkpointer = MemorySaver()
    graph = graph_builder.compile(checkpointer=checkpointer)
    # graph = graph_builder.compile()
    return graph

# Create the RAG graph with default checkpoint configuration
RAG = compile_graph()

if __name__ == '__main__':
    import asyncio
    query = "Find 2 papers about transformer models by Vaswani and Hinton in English from U of T"
    # query = "Hello!"
    result = asyncio.run(RAG.ainvoke({"messages": [{"role": "user", "content":query}]}))
    print(result)