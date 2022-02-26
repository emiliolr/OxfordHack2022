from PIL import Image, ImageDraw

def draw_shape(draw, size, color, location_params, screen_height, screen_width, shape):
    div = 3 if size == 'large' else 7
    side = max(int(screen_height / div), int(screen_width / div)) # side of bbox for shape

    height_map = {
        'top' : 0 + 10,
        'middle' : int(screen_height / 2),
        'bottom' : int(screen_height) - side - 10
    }
    width_map = {
        'left' : 0 + 10,
        'right' : int(screen_width) - side - 10
    }

    for h in height_map.keys():
        for w in width_map.keys():
            if h in location_params and w in location_params:
                location = [(width_map[w], height_map[h]), (width_map[w] + side, height_map[h] + side)]
                if shape == 'square':
                    draw.rectangle(location, fill = color)
                elif shape == 'circle':
                    draw.ellipse(location, fill = color)

    # TODO: figure out how to deal w/more ambiguous inputs (i.e., just saying "middle")
    if len(location_params) == 1:
        pass

# Test layout to hold test input
TEST_LAYOUT = {
    'circle' : {'desc': {'size' : 'large',
                         'color' : '#0000ff'},
               'loc' : ['left', 'top']},
    'square' : {'desc' : {'size' : 'small',
                          'color' : '#008000'},
                'loc' : ['bottom', 'right']}
}

# Layout space parameters
HEIGHT = 1000
WIDTH = 600

# PIL canvas for visualization before integrating w/Flutter
im = Image.new('RGB', (WIDTH, HEIGHT), (255, 255, 255))
draw = ImageDraw.Draw(im)

# TODO: add extra functionality to ensure that shapes don't overlap...
#  - maybe an array of shape screen that has 1 if pixel is occupied, 0 otherwise

for shape in TEST_LAYOUT.keys():
    size = TEST_LAYOUT[shape]['desc']['size']
    loc = TEST_LAYOUT[shape]['loc']
    color = TEST_LAYOUT[shape]['desc']['color']

    print(size)
    draw_shape(draw, size, color, loc, HEIGHT, WIDTH, shape)

im.save('layouts/PIL_draw_test.png', quality = 150)
