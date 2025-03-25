import { generateAPACitation, generateMLACitation, generateChicagoCitation, generateHarvardCitation, generateVancouverCitation, CitationData, Author } from "./citation-styles";


/**
 * Formats raw metadata into the CitationData format required for citation generation
 * @param rawMetadata Array of raw metadata objects from the API
 * @returns Array of formatted CitationData objects
 */
export function formatMetadata(rawMetadata: any[]): CitationData[] {
  return (rawMetadata).map(item => {
    // Extract and format authors
    const authors: Author[] = item.authors?.map((authorArray: string[]) => {
      return {
        firstName: authorArray[0] || "",
        lastName: authorArray[1] || ""
      };
    }) || [];

    // Extract year from publication date
    const year = item.publication_date ? 
      parseInt(item.publication_date.substring(0, 4)) : 
      new Date().getFullYear();

    // Determine publisher (use journal name if available)
    const publisher = item.journal || "";

    return {
      authors,
      title: item.title || "",
      publisher,
      year
    };
  });
}



/**
 * Generates citations from metadata based on the specified citation style
 * @param metadata Array of citation metadata
 * @param style Citation style (APA, MLA, Chicago, Harvard, or Vancouver)
 * @returns Array of formatted citations
 */
function generateCitations(metadata: CitationData[], style: string): string[] {
  return metadata.map(data => {
    switch(style.toUpperCase()) {
      case "APA":
        return generateAPACitation(data);
      case "MLA": 
        return generateMLACitation(data);
      case "CHICAGO":
        return generateChicagoCitation(data);
      case "HARVARD":
        return generateHarvardCitation(data);
      case "VANCOUVER":
        return generateVancouverCitation(data);
      default:
        return generateAPACitation(data); // Default to APA if style not recognized
    }
  });
}

/**
 * Combines metadata extraction and citation generation into a single function
 * @param rawMetadata Array of raw metadata objects
 * @param style Citation style (APA, MLA, Chicago, Harvard, or Vancouver)
 * @returns Array of formatted citations
 */
export function processAndGenerateCitations(rawMetadata: any[], style: string): string[] {
  const citationData = formatMetadata(rawMetadata);
  // Then generate citations in requested style
  return generateCitations(citationData, style);
}


