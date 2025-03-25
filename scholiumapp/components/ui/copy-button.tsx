"use-client";

import React, { useState } from 'react';
import { useCoAgent } from "@copilotkit/react-core";
import { ResearchState } from '../../lib/agent-state';
import { processAndGenerateCitations } from '../../lib/metadata-citations';
import { useStyleContext } from '../../lib/citation-context';
import { Button } from "@radix-ui/themes";

const CopyToClipboard: React.FC = () => {
  const { state: agentState } = useCoAgent<ResearchState>({
    name: "research_agent"
  });
  const { style} = useStyleContext();
  const [copied, setCopied] = useState(false);
  const citations = processAndGenerateCitations(agentState?.answer?.paper_metadata, style).join('\n')
  
  const textToCopy = citations;
  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(textToCopy);
      setCopied(true);

      // Reset the copied status after 2 seconds
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      console.error("Failed to copy text:", error);
    }
  };

  return (
    <div className="p-4 max-w-md mx-auto">
      <Button
        onClick={handleCopy}
      >
        Copy Citations
      </Button>
    </div>
  );
};

export default CopyToClipboard;