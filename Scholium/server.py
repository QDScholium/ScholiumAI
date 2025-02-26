"""
This is for the copilotkit remote endpoint
"""
import os
from dotenv import load_dotenv 
load_dotenv()
from fastapi import FastAPI
from copilotkit.integrations.fastapi import add_fastapi_endpoint
from copilotkit import CopilotKitRemoteEndpoint, Action as CopilotAction
from copilotkit import CopilotKitRemoteEndpoint, LangGraphAgent
from api.model import RAG
import uvicorn
app = FastAPI()

sdk = CopilotKitRemoteEndpoint(
    agents=[
        LangGraphAgent(
            name="research_agent",
            description="Research agent.",
            graph=RAG,
        ),
    ],
)
 
add_fastapi_endpoint(app, sdk, "/copilotkit")

def main():
    """Run the uvicorn server."""
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(
        "server:app",
        host="localhost",
        port=port,
        reload=True,
    )

if __name__ == '__main__':
    main()