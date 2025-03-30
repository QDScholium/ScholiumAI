import { list } from "postcss";

export type ResearchState = {
    //   answer: string;
    //   metadata: string;
    answer: {
        results: Array<{
          title: string;
          summary: string;
          id: string;
          metadata: Array<{
            title: string;
            authors: Array<{
                      first_name: string;
                      last_name: string;
                    }>;
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
        }>;
      };
  }