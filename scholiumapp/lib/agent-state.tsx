import { list } from "postcss";

export type ResearchState = {
    //   answer: string;
    //   metadata: string;
    answer: {
        markdown: string;
        paper_metadata: Array<{
          title: string;
          authors: Array<Array<string>>;
          publication_date: string;
          doi: string;
          journal: string;
          biblio?: {
            volume?: string;
            issue?: string;
            first_page?: string;
            last_page?: string;
          };
          referenced_works?: Array<string>;
          related_works?: Array<string>;
        }>;
      };
  }