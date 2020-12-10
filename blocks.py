import random


def new_blocks():
    blocks = list(TETROMINOS)
    random.shuffle(blocks)
    return [Tetromino(0, 0, mino) for mino in blocks]


class Shape:
    """
    Use the "super rotation system" to represent the blocks relative to one another, in the order:
    I, O, T, S, Z, J, L
    """
    def __init__(self, ind, relative_string):
        self.ind = ind
        self.rotations = len(relative_string)
        self.relative_string = relative_string
        self.shape_coords = []
        self.width = len(relative_string[0])
        self.height = len(relative_string)
        for rotation in range(self.rotations):
            self.shape_coords.append(list(self.get_relative_coords(rotation)))

    def get_string_rep(self, rotation):
        return self.relative_string[rotation % self.rotations]

    def get_shape_coords(self, rotation):
        return self.shape_coords[rotation % self.rotations]

    def get_relative_coords(self, rotation):
        str = self.get_string_rep(rotation)
        width = len(str[0])
        height = len(str)
        for dy in range(height):
            for dx in range(width):
                if str[dy][dx] != ' ':
                    yield dy, dx


SHAPE_I = Shape(1, [[
    '    ',
    'XXXX',
    '    ',
    '    ',
], [
    '  X ',
    '  X ',
    '  X ',
    '  X ',
]])

SHAPE_O = Shape(2, [[
    'XX',
    'XX',
]])

SHAPE_T = Shape(3, [[
    '   ',
    'XXX',
    ' X ',
], [
    ' X ',
    'XX ',
    ' X ',
], [
    ' X ',
    'XXX',
    '   ',
], [
    ' X ',
    ' XX',
    ' X ',
]])

SHAPE_S = Shape(4, [[
    '   ',
    ' XX',
    'XX ',
], [
    ' X ',
    ' XX',
    '  X',
]])

SHAPE_Z = Shape(5, [[
    '   ',
    'XX ',
    ' XX',
], [
    '  X',
    ' XX',
    ' X ',
]])

SHAPE_J = Shape(6, [[
    '   ',
    'XXX',
    '  X',
], [
    ' X ',
    ' X ',
    'XX ',
], [
    'X  ',
    'XXX',
    '   ',
], [
    ' XX',
    ' X ',
    ' X ',
]])

SHAPE_L = Shape(7, [[
    '   ',
    'XXX',
    'X  ',
], [
    'XX ',
    ' X ',
    ' X ',
], [
    '  X',
    'XXX',
    '   ',
], [
    ' X ',
    ' X ',
    ' XX',
]])

TETROMINOS = [SHAPE_I, SHAPE_O, SHAPE_T, SHAPE_S, SHAPE_Z, SHAPE_J, SHAPE_L]


class Tetromino:
    def __init__(self, x, y, shape: Shape, rotation=0):
        self.x = x
        self.y = y
        self.shape = shape
        self.rotation = rotation
        self.shape_coords = None

    def translate(self, x, y):
        self.x += x
        self.y += y
        self.shape_coords = None

    def rotate(self, dir_rotate):
        self.rotation += dir_rotate
        self.shape_coords = None

    def get_coods(self):
        if self.shape_coords is None:
            begin_x = self.x - round(self.shape.width / 2)
            begin_y = self.y
            shape_coords = self.shape.get_relative_coords(self.rotation)
            self.shape_coords = [(begin_x + dx, begin_y + dy) for dy, dx in shape_coords]
        return self.shape_coords
