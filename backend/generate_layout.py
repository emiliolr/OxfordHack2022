from PIL import Image, ImageDraw
from random import randint

# TODO:
#  - figure out how to deal w/more ambiguous inputs (i.e., just saying "middle")
#  - add extra functionality to ensure that shapes don't overlap...
#    - maybe an array of shape screen that has 1 if pixel is occupied, 0 otherwise

# Get coordinates, width, height for a shape
def get_shape_params(size, location_params, screen_height, screen_width, shape):
    div = 3 if size in ['large', 'big'] else 7
    side = max(int(screen_height / div), int(screen_width / div))

    height_map = {
        'top' : 0 + 10,
        'middle' : int(screen_height / 2) - int(side / 2),
        'bottom' : int(screen_height) - side - 10
    }
    width_map = {
        'left' : 0 + 10,
        'right' : int(screen_width) - side - 10
    }

    # TODO: will need to tweak here based on what is needed in Flutter!
    if len(location_params) == 0:
        first_coord = (randint(width_map['left'], width_map['right']),
                       randint(height_map['top'], height_map['bottom']))
        second_coord = (first_coord[0] + side, first_coord[1] + side)

        return first_coord, second_coord

    for h in height_map.keys():
        for w in width_map.keys():
            if h in location_params and w in location_params:
                return (width_map[w], height_map[h]), (width_map[w] + side, height_map[h] + side)

# ACTUAL CODE: generate the layout from parsed text and return as a dictionary
def generate_layout(layout_dict, screen_height, screen_width):
    layout = {}

    for shape in layout_dict.keys():
        if shape in ['circle', 'square']:
            size = layout_dict[shape]['desc']['size']
            loc = layout_dict[shape]['loc']
            color = layout_dict[shape]['desc']['color']

            top_left, bottom_right = get_shape_params(size, loc, screen_height, screen_width, shape)

            layout[shape] = {'top_left' : top_left, 'bottom_right' : bottom_right, 'color' : color}

    return layout

# Draw the shape on a PIL canvas - for debugging purposes!
def draw_shape(draw, size, color, location_params, screen_height, screen_width, shape):
    div = 3 if size == 'large' else 7
    side = max(int(screen_height / div), int(screen_width / div))  # side of bbox for shape

    height_map = {
        'top' : 0 + 10,
        'middle' : int(screen_height / 2) - int(side / 2),
        'bottom' : int(screen_height) - side - 10
    }
    width_map = {
        'left' : 0 + 10,
        'right' : int(screen_width) - side - 10
    }

    if len(location_params) == 0:
        first_coord = (randint(width_map['left'], width_map['right']),
                       randint(height_map['top'], height_map['bottom']))
        second_coord = (first_coord[0] + side, first_coord[1] + side)
        location = (first_coord, second_coord)

        if shape == 'square':
            draw.rectangle(location, fill = color)
        elif shape == 'circle':
            draw.ellipse(location, fill = color)

    for h in height_map.keys():
        for w in width_map.keys():
            if h in location_params and w in location_params:
                location = [(width_map[w], height_map[h]), (width_map[w] + side, height_map[h] + side)]
                if shape == 'square':
                    draw.rectangle(location, fill = color)
                elif shape == 'circle':
                    draw.ellipse(location, fill = color)

# Generate a save layout as image using a PIL canvas
def generate_layout_PIL(layout_dict, screen_height, screen_width):
    im = Image.new('RGB', (screen_width, screen_height), (255, 255, 255))  # PIL canvas
    draw = ImageDraw.Draw(im)

    for shape in layout_dict.keys():
        size = layout_dict[shape]['desc']['size']
        loc = layout_dict[shape]['loc']
        color = layout_dict[shape]['desc']['color']

        draw_shape(draw, size, color, loc, screen_height, screen_width, shape)

    im.save('layouts/PIL_draw_test.png', quality = 150)

if __name__ == '__main__':
    from statement_parsing import parse_text

    # TEST_TEXT = 'Let\'s do a small blue circle in the top left, a large green square in the middle left, and a small red triangle anywhere.'
    TEST_TEXT = 'A big green square.'
    TEST_TEXT = TEST_TEXT.replace(' ', '%')
    TEST_LAYOUT = parse_text(TEST_TEXT)

    # Layout space parameters
    HEIGHT = 1000
    WIDTH = 600

    # Generate and save layout with PIL
    print(generate_layout(TEST_LAYOUT, HEIGHT, WIDTH))
    generate_layout_PIL(TEST_LAYOUT, HEIGHT, WIDTH)
