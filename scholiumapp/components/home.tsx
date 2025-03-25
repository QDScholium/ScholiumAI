"use client";

import { useEffect, useState } from "react";
import { Textarea } from "./ui/textarea";
import { cn } from "../lib/utils";
import { motion } from "framer-motion";
import { useCoAgent } from "@copilotkit/react-core";
import { TextMessage, MessageRole } from "@copilotkit/runtime-client-gql";
import type { ResearchState } from "../lib/agent-state";
import { useChatContext } from "../lib/chat-context";


const MAX_INPUT_LENGTH = 250;

export function HomeView() {
  const {setResearchQuery, textInput, setTextInput} = useChatContext();

   const {run: runAgent} = useCoAgent<ResearchState>({ 
    name: "research_agent"
  });

  const handleRequest = (query: string) => {
    setResearchQuery(query);//Updates the context in the DOM 
    runAgent(() => {
      return new TextMessage({role: MessageRole.User, content: query});
    });
  };

  const [isInputFocused, setIsInputFocused] = useState(false);
  const suggestions = [
    { label: "Four Papers on BERT"},
    { label: "5 papers on Roman History" },
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: -50 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.4 }}
      className="h-screen w-full flex flex-col gap-y-2 justify-center items-center p-4 lg:p-0"
    >
      {/* Name Plate */}
      <div className="flex items-center gap-x-3 mb-4 -mt-32">
        <h1 className="text-6xl font-extralight">
          Scholium
        </h1>
        <p className="text-lg text-gray-600 font-light">
          Your personal research assistant
        </p>
      </div>

      {/* Suggestions */}
      <div className="grid grid-cols-2 w-[500px] gap-2 text-sm">
        {suggestions.map((suggestion) => (
          <div
            key={suggestion.label}
            onClick={() => handleRequest(suggestion.label)} 
            className="p-1.5 bg-slate-50/50 rounded border cursor-pointer hover:bg-slate-100"
          >
            {suggestion.label}
          </div>
        ))}
      </div>

      {/* Text Box */}
      <div
        className={cn(
          "w-[500px] h-[150px] bg-slate-100/50 border shadow-sm rounded-md transition-all",
          {
            "ring-1 ring-slate-300": isInputFocused,
          }
        )}
      >
      <Textarea
        placeholder="Ask anything..."
        className="bg-transparent p-4 resize-none focus-visible:ring-0 focus-visible:ring-offset-0 border-0 "
        maxLength={MAX_INPUT_LENGTH}
        value={textInput}
        onChange={(e) => setTextInput(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleRequest(textInput);
          }
        }}
      />

    </div>
    </motion.div>
  );
}