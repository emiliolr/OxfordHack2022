import spacy
import matplotlib.colors as colors

# TODO:
#  - figure out some structured way to extract RELATIVE location
#  - make more robust to more natural sentence structures
#  - allow compound stuff (i.e., dark blue)

nlp = spacy.load('en_core_web_sm')

def parse_text(text):
    # Removing '%' and adding back in spaces, if necessary
    if '%' in text:
        text = ' '.join(text.split('%'))

    # Keywords to use and translate to a location map for all desired objects
    KEYWORDS = {
        'OBJECTS' : ['square', 'circle', 'triangle'],
        'LOCATIONS' : ['top', 'bottom', 'left', 'right', 'middle'],
        'SIZE' : ['small', 'large', 'big', 'little'],
        'COLOR' : list(colors.get_named_colors_mapping().keys())
    }

    # spaCy language model for extracting dependencies from input text
    doc = nlp(text)

    found_objects = {}  # to hold onto keywords and descriptions/locations

    for token in doc: # main loop to collect keyword objects
        if (token.dep_ in ['ROOT', 'appos', 'conj'] or token.pos_ == 'NOUN') and token.text in KEYWORDS['OBJECTS']:
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
                            for subsubchild in subchild.children:  # find any additional descriptions of location
                                if subsubchild.dep_ in ['amod', 'compound'] and subsubchild.text in KEYWORDS['LOCATIONS']:
                                    found_objects[token.text]['loc'].append(subsubchild.text)

        # print(token.text, token.dep_, token.pos_, token.head.text, token.head.pos_, [child for child in token.children])

    return found_objects

if __name__ == '__main__':
    # Input text, to be collected by speech to text
    # TEST_TEXT = 'Let\'s do a small blue circle in the top left, a large green square in the middle left, and a small red triangle anywhere.'
    TEST_TEXT = 'I want a red square in the top right.'
    TEST_TEXT = TEST_TEXT.replace(' ', '%')

    print(parse_text(TEST_TEXT))
