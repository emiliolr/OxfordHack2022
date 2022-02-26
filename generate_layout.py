from PIL import Image, ImageDraw

def draw_square(draw, size, color, location_params, screen_height, screen_width):
    div = 5 if size == 'big' else 10
    height = screen_height / div

    height_map = {
        'top' : 0 + 10,
        'middle' : int(screen_height / 2),
        'bottom' : int(screen_height) - height - 10
    }
    width_map = {
        'left' : 0 + 10,
        'right' : int(screen_width) - height - 10
    }

    for h in height_map.keys():
        for w in width_map.keys():
            if h in location_params and w in location_params:
                draw.rectangle([(width_map[w], height_map[h]),
                                (width_map[w] + height, height_map[h] + height)],
                               fill = color)

    # TODO: figure out how to deal w/more ambiguous inputs (i.e., just saying "middle")
    if len(location_params) == 1:
        pass

def draw_circle():
    pass

# Test layout to hold test input
TEST_LAYOUT = {
    'circle' : {'desc': {'size' : 'small',
                         'color' : '#0000ff'},
               'loc' : ['left', 'top']},
    'square' : {'desc' : {'size' : 'large',
                          'color' : '#008000'},
                'loc' : ['middle', 'right']}
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

for shape in TEST_LAYOUT.keys():
    size = TEST_LAYOUT[shape]['desc']['size']
    loc = TEST_LAYOUT[shape]['loc']
    color = TEST_LAYOUT[shape]['desc']['color']

    if shape == 'square':
        draw_square(draw, size, color, loc, HEIGHT, WIDTH)
    elif shape == 'circle':
        pass

im.save('layouts/PIL_draw_test.png', quality = 95)
