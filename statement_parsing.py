import spacy
import matplotlib.colors as colors

# Input text, to be collected by speech to text
TEST_TEXT = 'A small blue circle in the top left, a large green square in the middle left, and a small red triangle anywhere.'

# Keywords to use and translate to a location map for all desired objects
KEYWORDS = {
    'OBJECTS' : ['square', 'circle', 'triangle'],
    'LOCATIONS' : ['top', 'bottom', 'left', 'right', 'middle', 'any'],
    'SIZE' : ['small', 'large'],
    'COLOR' : list(colors.get_named_colors_mapping().keys())
}

# spaCy language model for extracting dependencies from input text
nlp = spacy.load('en_core_web_sm')
doc = nlp(TEST_TEXT)

# TODO:
#  - figure out some structured way to extract RELATIVE location
#  - make more robust to more natural sentence structures
#  - allow compound stuff (i.e., dark blue)

found_objects = {}  # to hold onto keywords and descriptions/locations

for token in doc: # main loop to collect keyword objects
    if token.dep_ in ['ROOT', 'appos', 'conj'] and token.text in KEYWORDS['OBJECTS']:
        found_objects[token.text] = {'desc' : {'size' : None, 'color' : None}, 'loc' : []}
        for child in token.children: # second loop to collect descriptions/locations
            if child.dep_ == 'amod' and child.text in KEYWORDS['SIZE']:  # size
                found_objects[token.text]['desc']['size'] = child.text
            elif child.dep_ == 'amod' and child.text in KEYWORDS['COLOR']:  # color
                found_objects[token.text]['desc']['color'] = colors.to_hex(child.text)
            if child.dep_ == 'prep':  # location
                for subchild in child.children:
                    if subchild.dep_ == 'pobj' and subchild.text in KEYWORDS['LOCATIONS']:  # found absolute location
                        found_objects[token.text]['loc'].append(subchild.text)
                        for subsubchild in subchild.children:  # find any modifiers to base location
                            if subsubchild.dep_ == 'amod' and subsubchild.text in KEYWORDS['LOCATIONS']:
                                found_objects[token.text]['loc'].append(subsubchild.text)

    # print(token.text, token.dep_, token.head.text, token.head.pos_, [child for child in token.children])

print(found_objects)
