import math

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900
ARENA_CENTER_X = 450
ARENA_CENTER_Y = 450
ARENA_WIDTH = 700
ARENA_HEIGHT = 700
FONT_SIZE = 16
PLAYER_SIZE = 0.1

# arena coordinates go from -1 to +1 in each dimension.
# 0 is the center of both coordinate systems
def coordsToPix(coords):
    return Vector(coords.x * ARENA_WIDTH/2 + ARENA_CENTER_X,
        coords.y * ARENA_HEIGHT/2 + ARENA_CENTER_Y)

def rotateVector(vec, angle):
    a = math.radians(angle)
    return Vector(vec.x*math.cos(a)-vec.y*math.sin(a), vec.x*math.sin(a)+vec.y*math.cos(a))

def sizeToPix(size):
    return size * ARENA_WIDTH/2

class Vector:
    def __init__(self, x, y=None):
        if isinstance(x, list) or isinstance(x, tuple):
            assert(len(x) == 2)
            self.vals = list(x)
        elif isinstance(x, Vector):
            self.vals = [x.x, x.y]
        else:
            assert(y is not None)
            self.vals = [x, y]

    @property
    def x(self):
        return self.vals[0]
    @x.setter
    def x(self, val):
        self.vals[0] = val
    @property
    def y(self):
        return self.vals[1]
    @y.setter
    def y(self, val):
        self.vals[1] = val

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __str__(self):
        return f'({self.x:.2f}, {self.y:.2f})'

    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self, length=1.0):
        if self.x==0 and self.y==0:
            return (0, 0)
        vecLen = self.length()
        return Vector(self.x/vecLen*length, self.y/vecLen*length)
