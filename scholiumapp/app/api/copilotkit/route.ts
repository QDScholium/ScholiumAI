import {
    CopilotRuntime,
    OpenAIAdapter,
    copilotRuntimeNextJSAppRouterEndpoint,
    langGraphPlatformEndpoint,
    copilotKitEndpoint,
  } from '@copilotkit/runtime';
  import { NextRequest } from 'next/server';
  import OpenAI from "openai";

  require('dotenv').config();
  const langsmithApiKey = process.env.LANGSMITH_API_KEY as string 
  const openai = new OpenAI({ apiKey: process.env.NEXT_PUBLIC_OPENAI_API_KEY });
  const serviceAdapter = new OpenAIAdapter({ openai } as any);
  export const maxDuration = 300;
 
  export const POST = async (req: NextRequest) => {

    const searchParams = req.nextUrl.searchParams
    const deploymentUrl = searchParams.get('lgcDeploymentUrl') || process.env.LGC_DEPLOYMENT_URL;
    console.log("Deployment URL:", deploymentUrl);
    const remoteEndpoint = deploymentUrl ? langGraphPlatformEndpoint({
      deploymentUrl,
      langsmithApiKey,
      agents: [
        {
          name: "research_agent",
          description: "Research agent",
        },
      ],
    }) : copilotKitEndpoint({
      url: process.env.REMOTE_ACTION_URL || "http://localhost:8000/copilotkit",// http://localhost:8000/copilotkit for local devlopment https://scholium-api.vercel.app//copilotkit
    })
    
    const runtime = new CopilotRuntime({
      remoteEndpoints: [remoteEndpoint],
    });
    
    const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
      runtime,
      serviceAdapter,
      endpoint: '/api/copilotkit',
    });
   
    return handleRequest(req);
  };