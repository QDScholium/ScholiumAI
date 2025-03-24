'''
Common utils 
'''

def parse_authors(authorships):
    author_tuples = []

    # Process each authorship entry
    for authorship in authorships:
        # Extract the author's display name and split it into parts.
        author_name = authorship["author"]["display_name"]
        name_parts = author_name.split()
        
        # Assume the first word is the first name and the last word is the last name.
        first_name = name_parts[0] if name_parts else ""
        last_name = name_parts[-1] if len(name_parts) > 1 else ""
        
        # Get the institution name from the first institution in the list.
        institution = (authorship["institutions"][0]["display_name"]
                    if authorship["institutions"] else "")
        
        # Append the tuple to our list.
        author_tuples.append((first_name, last_name, institution))

    return author_tuples

def get_referenced_works(referenced_works):
    return [url.split("/")[-1] for url in referenced_works]

def inverted_index_to_string(inverted_index):
    # Determine the maximum index across all word positions
    max_index = 0
    for positions in inverted_index.values():
        if positions:
            max_index = max(max_index, max(positions))
    
    # Create a list of tokens with a size equal to max_index+1
    tokens = [None] * (max_index + 1)
    
    # For each word, insert it at each of its positions in the tokens list
    for word, positions in inverted_index.items():
        for pos in positions:
            tokens[pos] = word
    
    # # Check that every position is filled
    # if any(token is None for token in tokens):
    #     raise ValueError("The inverted index is incomplete; some positions are missing.")
    
    # Join the tokens into a single string with spaces between words
    return " ".join(tokens)

if __name__ == "__main__":
    pass