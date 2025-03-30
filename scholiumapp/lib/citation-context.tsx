"use client";

import React from "react";
import { createContext, useContext, useState, ReactNode } from "react";

type StyleContextType = {
    style: string;
    setStyle: (style: string) => void;
    papers: Array<any>;
    setPapers: (papers: Array<any>) => void;
  };

const StyleContext = createContext<StyleContextType | undefined>(undefined);

export const StyleContextProvider = ({ children }: { children: ReactNode }) => {
    const [style, setStyle] = useState<string>("APA");
    const [papers, setPapers] = useState<Array<any>>([]);

      return (
        <StyleContext.Provider
          value={{
            style,
            setStyle,
            papers,
            setPapers
          }}
        >
          {children}
        </StyleContext.Provider>
      );
}

export const useStyleContext = () => {
    const context = useContext(StyleContext);
    if (context === undefined) {
      throw new Error("Provider error. Context Needed.");
    }
    return context;
  };
