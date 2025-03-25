"use client";

import { HomeView } from "./home";
import {Results} from "./results";
import { AnimatePresence } from "framer-motion";
import { useChatContext } from "../lib/chat-context";
import HomeButton from "./ui/home_button";

export function HomeResearch() {
  const { researchQuery, setTextInput } = useChatContext();
  return (
    <>
      <div className="flex flex-col items-center justify-center relative z-10 w-4/5 mx-auto">
        <div className="absolute top-0 left-0 p-4">
            <HomeButton/>
        </div>
        <div className="mt-16 flex-1 w-full flex justify-center items-center">
          {researchQuery ? (
            <AnimatePresence
              key="results"
              onExitComplete={() => {
                setTextInput("");
              }}
              mode="wait"
            >
              <Results key="results" />
            </AnimatePresence>
          ) : (
            <AnimatePresence key="home" mode="wait">
              <HomeView key="home" />
            </AnimatePresence>
          )}
        </div>
      </div>
    </>
  ); 
}