from PIL import Image, ImageDraw

# Test layout to hold test input
TEST_LAYOUT = {
    'circle': {'desc': ['small', 'blue'],
               'loc': ['left', 'top']},
    'square': {'desc': ['large', 'green'],
               'loc': ['middle']},
    'triangle': {'desc': ['small', 'red'],
                 'loc': []}
 }

# Layout space parameters
HEIGHT = 1000
WIDTH = 500

# TODO: generate a valid layout (dictionary) using the given layout extracted from text input
#  - we don't want objects to overlap
#  - we don't want to exceed to the size of the screen
#  - we can parameterize the location of different shapes by height, width, radius, etc.

# PIL canvas for visualization before integrating w/Flutter
im = Image.new('RGB', (WIDTH, HEIGHT), (255, 255, 255))
draw = ImageDraw.Draw(im)

im.save('layouts/PIL_draw_test.png', quality = 95)
