import Markdown from "react-markdown";
import { Card, Checkbox} from "@radix-ui/themes";
import { useStyleContext } from '../lib/citation-context';
import { useState } from "react";




export function DisplayMarkdown({ title, contents, idx, results }: { title: string; contents: string; idx: number; results: any[] }) {
  const {papers, setPapers} = useStyleContext();
  const [ticked, setTicked] = useState(false);
  function handleClick(idx){
    console.log(results)
    console.log(idx)
    if(!ticked){
      const metadata = results[idx].metadata;
      setPapers([...papers, { metadata }]);
    } else {
      const metadata = results[idx].metadata;
      setPapers(papers.filter(paper => paper.metadata !== metadata));
    }
    setTicked(!ticked);
    console.log("Papers collection updated:", papers);
  }

  return (
    <>
      <div className="mt-4">
        <br className="my-2" />
      </div>
      <Card>
      <div className="flex justify-end">
        <Checkbox 
          checked={ticked}
          onClick={() => {
            handleClick(idx);
          }} 
        />
      </div>
        <div className="markdown-wrapper list-decimal space-y-8 [&>p]:mb-8">
            <h1 className="text-2xl mb-4 flex items-center gap-1">{title}</h1>

            <hr className="my-4" />
            
            <Markdown>
            {contents}
            </Markdown>

            

        </div>
      </Card>
    </>
  );
}