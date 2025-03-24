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
# print(reconstructed_text)


inverted_index = {
    'Batch-splitting': [0],
    '(data-parallelism)': [1],
    'is': [2, 198],
    'the': [3, 30, 104, 109, 158, 183, 192],
    'dominant': [4],
    'distributed': [5, 90],
    'Deep': [6],
    'Neural': [7],
    'Network': [8],
    '(DNN)': [9],
    'training': [10],
    'strategy,': [11],
    'due': [12],
    'to': [13, 20, 32, 38, 66, 69, 73, 115, 150, 167, 176],
    'its': [14, 18],
    'universal': [15],
    'applicability': [16],
    'and': [17, 43, 72, 101, 191],
    'amenability': [19],
    'Single-Program-Multiple-Data': [21],
    '(SPMD)': [22],
    'programming.': [23],
    'However,': [24],
    'batch-splitting': [25],
    'suffers': [26],
    'from': [27],
    'problems': [28],
    'including': [29],
    'inability': [31],
    'train': [33, 171],
    'very': [34],
    'large': [35, 77],
    'models': [36, 173],
    '(due': [37],
    'memory': [39],
    'constraints),': [40],
    'high': [41],
    'latency,': [42],
    'inefficiency': [44],
    'at': [45, 200],
    'small': [46],
    'batch': [105],
    'sizes.': [48],
    'All': [49],
    'of': [50, 89, 121, 125, 136, 157, 165, 182],
    'these': [51],
    'can': [52, 95, 111],
    'be': [53, 67, 96, 116],
    'solved': [54],
    'by': [55],
    'more': [56],
    'general': [57, 87],
    'distribution': [58],
    'strategies': [59],
    '(model-parallelism).': [60],
    'Unfortunately,': [61],
    'efficient': [62, 153],
    'model-parallel': [63, 155],
    'algorithms': [64],
    'tend': [65],
    'complicated': [68],
    'discover,': [70],
    'describe,': [71],
    'implement,': [74],
    'particularly': [75],
    'on': [76, 186],
    'clusters.': [78],
    'We': [79, 147],
    'introduce': [80],
    'Mesh-TensorFlow,': [81, 108],
    'a': [82, 86, 122, 132],
    'language': [83, 194],
    'for': [84],
    'specifying': [85],
    'class': [88],
    'tensor': [91],
    'computations.': [92],
    'Where': [93],
    'data-parallelism': [94],
    'viewed': [97],
    'as': [98, 145],
    'splitting': [99],
    'tensors': [100],
    'operations': [102, 138],
    'along': [103],
    'dimension,': [106],
    'in': [107],
    'user': [110],
    'specify': [112],
    'any': [113, 119],
    'tensor-dimensions': [114],
    'split': [117],
    'across': [118],
    'dimensions': [120],
    'multi-dimensional': [123],
    'mesh': [124],
    'processors.': [126],
    'A': [127],
    'Mesh-TensorFlow': [128, 149],
    'graph': [129],
    'compiles': [130],
    'into': [131],
    'SPMD': [133],
    'program': [134],
    'consisting': [135],
    'parallel': [137],
    'coupled': [139],
    'with': [140, 174],
    'collective': [141],
    'communication': [142],
    'primitives': [143],
    'such': [144],
    'Allreduce.': [146],
    'use': [148],
    'implement': [151],
    'an': [152],
    'data-parallel,': [154],
    'version': [156],
    'Transformer': [159, 172],
    'sequence-to-sequence': [160],
    'model.': [161],
    'Using': [162],
    'TPU': [163],
    'meshes': [164],
    'up': [166, 175],
    '512': [168],
    'cores,': [169],
    'we': [170],
    '5': [177],
    'billion': [178],
    'parameters,': [179],
    'surpassing': [180],
    'state': [181],
    'art': [184],
    'results': [185],
    "WMT'14": [187],
    'English-to-French': [188],
    'translation': [189],
    'task': [190],
    'one-billion-word': [193],
    'modeling': [195],
    'benchmark.': [196],
    'Mesh-Tensorflow': [197],
    'available': [199],
    'this': [201],
    'https': [202],
    'URL': [203],
    '.': [204]
}

reconstructed_text = inverted_index_to_string(inverted_index)
print(reconstructed_text)