import drawSvg as draw
import random
import math


def create_hex_grid(img_bounds, hex_size):
    """returns an array of hexagon positions denoted by the bottom corner that fill an area of img_bounds
    which should be given as a tuple of four floats indicating bottom left and top right
    hex_size indicates the radius of hexagon to fill the area with
    """
    grid = []
    center = ((img_bounds[0] + img_bounds[2])/2, (img_bounds[1] + img_bounds[3])/2)
    size = (img_bounds[2] - img_bounds[0], img_bounds[3] - img_bounds[1])
    rows = 2 * math.ceil((size[1] / hex_size + 2) / 3) - 1
    columns = 2 * math.ceil((size[1] / hex_size) / math.sqrt(3)) + 1
    first_row = center[1] - hex_size - (rows // 2) * 1.5 * hex_size
    first_col = center[0] - (columns // 2) * hex_size * math.sqrt(3)
    for row in range(rows):
        grid.append([])
        y_coord = row * 1.5 * hex_size + first_row
        for col in range(columns):
            x_coord = col * hex_size * math.sqrt(3) + first_col
            if row % 2 != (rows // 2) % 2:
                x_coord += hex_size * math.sqrt(3) / 2
            grid[-1].append((x_coord, y_coord))
    return grid


def flat_points(coord, hex_size, closed=False):
    points = (coord[0], coord[1],
              coord[0] - math.sqrt(3) * hex_size / 2, coord[1] + 0.5 * hex_size,
              coord[0] - math.sqrt(3) * hex_size / 2, coord[1] + 1.5 * hex_size,
              coord[0], coord[1] + 2 * hex_size,
              coord[0] + math.sqrt(3) * hex_size / 2, coord[1] + 1.5 * hex_size,
              coord[0] + math.sqrt(3) * hex_size / 2, coord[1] + 0.5 * hex_size)
    if closed:
        points += (coord[0], coord[1])
    return points


def to_hex(red, green, blue):
    red = int(min(max(red, 0), 255))
    green = int(min(max(green, 0), 255))
    blue = int(min(max(blue, 0), 255))
    return '#{0:02X}{1:02X}{2:02X}'.format(red, green, blue)


def random_color():
    return to_hex(random.randrange(256), random.randrange(256), random.randrange(256))


if __name__ == "__main__":
    width = 1600
    height = 900
    pic = draw.Drawing(width, height, origin='center', displayInline=False)
    tile_size = 80
    hex_grid = create_hex_grid((-width/2, -height/2, width/2, height/2), tile_size)

    # draw background
    grad = draw.LinearGradient(-width / 2, -height / 2, width / 2, height / 2)
    grad.addStop(0, to_hex(153, 217, 234))
    grad.addStop(1, to_hex(230, 230, 10))
    pic.append(draw.Rectangle(-width / 2, -height / 2, width, height, fill=grad))

    grad = draw.LinearGradient(-width / 2, -height / 2, width / 2, height / 2)
    grad.addStop(0, to_hex(128, 0, 192))
    grad.addStop(0.5, to_hex(0, 0, 200))
    grad.addStop(1, to_hex(0, 220, 220))

    # draw a bunch of hexagons
    c1 = random_color()
    c2 = random_color()
    c3 = random_color()
    for f in hex_grid:
        for g in f:
            num = random.randrange(6)
            if num == 0:
                grad = draw.LinearGradient(g[0] - math.sqrt(3) * tile_size / 2, g[1] + 0.5 * tile_size,
                                           g[0] + math.sqrt(3) * tile_size / 2, g[1] + 1.5 * tile_size)
            elif num == 1:
                grad = draw.LinearGradient(g[0] - math.sqrt(3) * tile_size / 2, g[1] + 1.5 * tile_size,
                                           g[0] + math.sqrt(3) * tile_size / 2, g[1] + 0.5 * tile_size)
            elif num == 2:
                grad = draw.LinearGradient(g[0], g[1], g[0], g[1] + 2 * tile_size)
            elif num == 3:
                grad = draw.LinearGradient(g[0] + math.sqrt(3) * tile_size / 2, g[1] + 1.5 * tile_size,
                                           g[0] - math.sqrt(3) * tile_size / 2, g[1] + 0.5 * tile_size)
            elif num == 4:
                grad = draw.LinearGradient(g[0] + math.sqrt(3) * tile_size / 2, g[1] + 0.5 * tile_size,
                                           g[0] - math.sqrt(3) * tile_size / 2, g[1] + 1.5 * tile_size)
            else:
                grad = draw.LinearGradient(g[0], g[1] + 2 * tile_size, g[0], g[1])
            img_grad = (1 * g[0] + g[1]) / 20
            grad.addStop(1-math.sqrt(3)/2, c1)
            grad.addStop(0.5, c2)
            grad.addStop(math.sqrt(3)/2, c3)
            pic.append(draw.Lines(*flat_points((g[0], g[1]), tile_size), close=True, fill=grad))

    pic.setPixelScale(1)  # Set number of pixels per geometry unit
    pic.saveSvg('images\\example.svg')
