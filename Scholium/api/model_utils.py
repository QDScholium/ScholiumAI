import re
import os
import dotenv
from openai import OpenAI

dotenv.load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def extract_paper_titles(text):
    """
    Finds all substrings in `text` that are enclosed in matching single or double quotes.
    
    Parameters:
        text (str): The input string.
    
    Returns:
        List[str]: A list of quoted substrings, including the surrounding quote characters.
    """
    pattern = r'(["\'])(.*?)\1'
    matches = re.finditer(pattern, text)
    return [match.group(0) for match in matches]


def get_paper_metadata(titles:list[str], metadata):
    metadata_list = []
    for title in titles:
        if title.strip("\"") in metadata:
            metadata_list.append(metadata[title.strip("\"")])
    return metadata_list


def filter_results(response, score_cutoff = 0.8):
    '''
    This exists because, for some stupid reason, pinecone doesn't have a way to cutoff low similarity responses
    '''
    new_response = []
    for i, match in enumerate(response):
        score  = match[1]
        if score >= score_cutoff:
            new_response.append(match[0])
    return new_response
