"use client";

import { createContext, useContext, useState, ReactNode, useEffect } from "react";

type ChatResult = {
    answer: string;
    sources: string[];
  }

type ChatContextType = {
    researchQuery: string;
    setResearchQuery: (query: string) => void;
    textInput: string;
    setTextInput:(input: string) => void;
    researchResult: ChatResult | null;
    setChatResult: (result: ChatResult) => void;
    isLoading: boolean;
    setLoading: (loading: boolean) => void;
  };

const ChatContext = createContext<ChatContextType | undefined>(undefined);

export const ChatContextProvider = ({ children }: { children: ReactNode }) => {
    const [researchQuery, setResearchQuery] = useState<string>("");
    // Need have an intermediate state between query and input so the site doesnt update on every key stroke
    const [textInput, setTextInput] = useState<string>(""); 
    const [researchResult, setChatResult] = useState<ChatResult | null>(null);
    const [isLoading, setLoading] = useState<boolean>(true);
  

  useEffect(() => {
    if (!researchQuery) {
      setChatResult(null);
    }
  }, [researchQuery, researchResult]);

  return (
    <ChatContext.Provider
      value={{
        researchQuery,
        setResearchQuery,
        textInput,
        setTextInput,
        researchResult,
        setChatResult,
        isLoading,
        setLoading
      }}
    >
      {children}
    </ChatContext.Provider>
  );
};

export const useChatContext = () => {
    const context = useContext(ChatContext);
    if (context === undefined) {
      throw new Error("Provider error. Context Needed.");
    }
    return context;
  };