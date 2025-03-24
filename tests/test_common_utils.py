import json
from api.common_utils import parse_authors, inverted_index_to_string

json_data = '''
            {
            "authorships": [
                {
                "author_position": "first",
                "author": {
                    "id": "https://openalex.org/A5031152245",
                    "display_name": "Alex Krizhevsky",
                    "orcid": null
                },
                "institutions": [
                    {
                    "id": "https://openalex.org/I185261750",
                    "display_name": "University of Toronto",
                    "ror": "https://ror.org/03dbr7087",
                    "country_code": "CA",
                    "type": "funder",
                    "lineage": [
                        "https://openalex.org/I185261750"
                    ]
                    }
                ],
                "countries": [
                    "CA"
                ],
                "is_corresponding": false,
                "raw_author_name": "Alex Krizhevsky",
                "raw_affiliation_strings": [
                    "University of Toronto"
                ],
                "affiliations": [
                    {
                    "raw_affiliation_string": "University of Toronto",
                    "institution_ids": [
                        "https://openalex.org/I185261750"
                    ]
                    }
                ]
                },
                {
                "author_position": "middle",
                "author": {
                    "id": "https://openalex.org/A5006446297",
                    "display_name": "Ilya Sutskever",
                    "orcid": null
                },
                "institutions": [
                    {
                    "id": "https://openalex.org/I185261750",
                    "display_name": "University of Toronto",
                    "ror": "https://ror.org/03dbr7087",
                    "country_code": "CA",
                    "type": "funder",
                    "lineage": [
                        "https://openalex.org/I185261750"
                    ]
                    }
                ],
                "countries": [
                    "CA"
                ],
                "is_corresponding": false,
                "raw_author_name": "Ilya Sutskever",
                "raw_affiliation_strings": [
                    "University of Toronto"
                ],
                "affiliations": [
                    {
                    "raw_affiliation_string": "University of Toronto",
                    "institution_ids": [
                        "https://openalex.org/I185261750"
                    ]
                    }
                ]
                },
                {
                "author_position": "last",
                "author": {
                    "id": "https://openalex.org/A5108093963",
                    "display_name": "Geoffrey E. Hinton",
                    "orcid": null
                },
                "institutions": [
                    {
                    "id": "https://openalex.org/I185261750",
                    "display_name": "University of Toronto",
                    "ror": "https://ror.org/03dbr7087",
                    "country_code": "CA",
                    "type": "funder",
                    "lineage": [
                        "https://openalex.org/I185261750"
                    ]
                    }
                ],
                "countries": [
                    "CA"
                ],
                "is_corresponding": false,
                "raw_author_name": "Geoffrey E. Hinton",
                "raw_affiliation_strings": [
                    "University of Toronto"
                ],
                "affiliations": [
                    {
                    "raw_affiliation_string": "University of Toronto",
                    "institution_ids": [
                        "https://openalex.org/I185261750"
                    ]
                    }
                ]
                }
            ]
            }
            '''
data = json.loads(json_data)
authorships = data["authorships"]
print(parse_authors(authorships))



inverted_index = {
    "We": [0, 120],
    "trained": [1],
    "a": [2, 77, 90, 108, 123, 134],
    "large,": [3],
    "deep": [4],
    "convolutional": [5, 62],
    "neural": [6, 49],
    "network": [7],
    "to": [8, 116, 143],
    "classify": [9],
    "the": [10, 16, 21, 26, 45, 96, 103, 129, 147],
    "1.2": [11],
    "million": [12, 54],
    "high-resolution": [13],
    "images": [14],
    "in": [15, 102, 128],
    "ImageNet": [17],
    "LSVRC-2010": [18],
    "contest": [19],
    "into": [20],
    "1000": [22],
    "different": [23],
    "classes.": [24],
    "On": [25],
    "test": [27, 137],
    "data,": [28],
    "we": [29, 85, 106],
    "achieved": [30, 133, 145],
    "top-1": [31],
    "and": [32, 38, 56, 72, 89, 132],
    "top-5": [33, 136],
    "error": [34, 138],
    "rates": [35],
    "of": [36, 60, 65, 95, 125, 140],
    "37.5%": [37],
    "17.0%": [39],
    "which": [40, 51, 66],
    "is": [41],
    "considerably": [42],
    "better": [43],
    "than": [44],
    "previous": [46],
    "state-of-the-art.": [47],
    "The": [48],
    "network,": [50],
    "has": [52],
    "60": [53],
    "parameters": [55],
    "650,000": [57],
    "neurons,": [58],
    "consists": [59],
    "five": [61],
    "layers,": [63, 71],
    "some": [64],
    "are": [67],
    "followed": [68],
    "by": [69, 146],
    "max-pooling": [70],
    "three": [73],
    "fully-connected": [74, 104],
    "layers": [75, 105],
    "with": [76],
    "final": [78],
    "1000-way": [79],
    "softmax.": [80],
    "To": [81, 99],
    "make": [82],
    "training": [83],
    "faster,": [84],
    "used": [86],
    "non-saturating": [87],
    "neurons": [88],
    "very": [91, 118],
    "efficient": [92],
    "GPU": [93],
    "implementation": [94],
    "convolution": [97],
    "operation.": [98],
    "reduce": [100],
    "overriding": [101],
    "employed": [107],
    "recently-developed": [109],
    "regularization": [110],
    "method": [111],
    "called": [112],
    "dropout": [113],
    "that": [114],
    "proved": [115],
    "be": [117],
    "effective.": [119],
    "also": [121],
    "entered": [122],
    "variant": [124],
    "this": [126],
    "model": [127],
    "ILSVRC-2012": [130],
    "competition": [131],
    "winning": [135],
    "rate": [139],
    "15.3%,": [141],
    "compared": [142],
    "26.2%": [144],
    "second-best": [148],
    "entry.": [149]
}

# Convert the inverted index into a string and print the result
reconstructed_text = inverted_index_to_string(inverted_index)
print(reconstructed_text)