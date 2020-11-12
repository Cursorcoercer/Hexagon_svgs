import drawSvg as draw
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


if __name__ == "__main__":
    width = 1600
    height = 900
    pic = draw.Drawing(width, height, origin='center', displayInline=False)
    tile_size = 91
    hex_grid = create_hex_grid((-width/2, -height/2, width/2, height/2), tile_size)

    # draw background
    grad = draw.LinearGradient(- width / 2, -height / 2, width / 2, height / 2)
    grad.addStop(0, to_hex(254, 174, 60))
    grad.addStop(1, to_hex(254, 246, 203))
    pic.append(draw.Rectangle(- width / 2, -height / 2, width, height, fill=grad))

    # draw a bunch of hexagons
    for f in hex_grid:
        for g in f:
            grad = draw.LinearGradient(g[0] - math.sqrt(3) * tile_size / 2, g[1] + 0.5 * tile_size,
                                       g[0] + math.sqrt(3) * tile_size / 2, g[1] + 1.5 * tile_size)
            img_grad = (1 * g[0] + g[1]) / 20
            grad.addStop(0, to_hex(255, 180 + img_grad, 0))
            grad.addStop(0.55, to_hex(255, 121 + 1.4 * img_grad + 20, 30))
            grad.addStop(1, to_hex(200 + img_grad, 80 + img_grad, 0))
            pic.append(draw.Lines(*flat_points((g[0], g[1]+10), tile_size-10), close=True, fill=grad,
                                  stroke=to_hex(128 + 1.6*img_grad, 53 + img_grad/2, 0), stroke_width=6.25))
    pic.setPixelScale(1)  # Set number of pixels per geometry unit
    pic.saveSvg('images\\hex grad grad.svg')
