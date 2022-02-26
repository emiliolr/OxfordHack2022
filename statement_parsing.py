import spacy

# Input text, to be collected by speech to text
IDEAL_TEXT = 'Let\'s put a red box in the top right corner, a blue circle in the bottom left, and a grey square anywhere.'
TEST_TEXT = 'A small blue circle, a large red square.'

# Keywords to use and translate to a location map for all desired objects
KEYWORDS = ['box', 'circle', 'line', 'triangle']
LOCATION_MAP = {'top' : None, 'bottom' : None, 'left' : None, 'right' : None}

# spaCy for extracting dependencies from input text
nlp = spacy.load('en_core_web_sm')
doc = nlp(TEST_TEXT)

for token in doc:
    print(token.text, token.dep_, token.head.text, token.head.pos_,
          [child for child in token.children])
