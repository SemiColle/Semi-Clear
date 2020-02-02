import arcade, math
from .helper import coordsToPix, Vector, sizeToPix
from . import helper


class Drawable:
    # layers: 0:arena, 1:floor, 2:players, 3:boss, 4:coverall
    def __init__(self, layer=4, center=Vector(0, 0), color=None, snapshot=False):
        self.active = True
        self.layer = layer
        self.center, self.centerTarget = self.copyOrReference(center)
        self.color = color
        self.snapshot = snapshot

    def copyOrReference(self, center):
        # if it's a static position like (0.1, 1), make a copy
        if isinstance(center, tuple) or isinstance(center, list) or isinstance(center, Vector):
            return Vector(center), None
        elif isinstance(center, Drawable): # if it's a drawable, make a copy, but keep the reference
            return Vector(center.center), center
        else:
            assert(False, 'Drawable center should be tuple, list, Vector or Drawable')

    def update(self, dt):
        if self.centerTarget is not None:
            self.center = Vector(self.centerTarget.center)
        if self.snapshot:
            self.centerTarget = None

    def draw(self):
        pass


class Circle(Drawable):
    def __init__(self, center, radius, color, layer=1, snapshot=False):
        super().__init__(layer, center, color, snapshot)
        self.radius = radius

    def draw(self):
        pixPos = coordsToPix(self.center)
        pixRad = sizeToPix(self.radius)
        arcade.draw_circle_filled(pixPos.x, pixPos.y, pixRad, self.color)


class Donut(Drawable):
    def __init__(self, center, innerRad, outerRad, color, layer=1, snapshot=False):
        super().__init__(layer, center, color, snapshot)
        self.radius = (outerRad + innerRad) / 2
        self.thickness = outerRad - innerRad

    def draw(self):
        pixPos = coordsToPix(self.center)
        pixRad = sizeToPix(self.radius)
        pixThick = sizeToPix(self.thickness)
        arcade.draw_circle_outline(pixPos.x, pixPos.y, pixRad, self.color, pixThick)


class TargetedDrawable(Drawable):
    def __init__(self, layer=4, center=Vector(0, 0), end=Vector(0, 0), color=None, snapshot=False):
        super().__init__(layer, center, color, snapshot)
        self.end, self.endTarget = self.copyOrReference(end)

    def update(self, dt):
        super().update(dt)
        if self.endTarget is not None:
            self.end = Vector(self.endTarget.center)
        if self.snapshot:
            self.endTarget = None


class ThickLine(TargetedDrawable):
    def __init__(self, center, end, thickness, color, length=None, layer=1, snapshot=False):
        super().__init__(layer, center, end, color, snapshot)
        self.thickness = thickness
        self.length = length

    def update(self, dt):
        super().update(dt)

    def draw(self):
        startPos = coordsToPix(self.center)
        if self.length is None:
            endPos = coordsToPix(self.end)
        else:
            direction = (self.end-self.center).normalize(self.length)
            endPos = coordsToPix(self.center + direction)
        pixThick = sizeToPix(self.thickness)
        if startPos.x == endPos.x and startPos.x == endPos.y:
            startPos.y += 1
        arcade.draw_line(startPos.x, startPos.y, endPos.x, endPos.y, self.color, pixThick)


class AngledLine(ThickLine):
    def __init__(self, center, angle, length, thickness, color, layer=1, snapshot=False):
        direction = helper.rotateVector(Vector(0, length), angle)
        end = direction + Vector(center)
        super().__init__(center, end, thickness, color, layer, snapshot)


class Cone(TargetedDrawable):
    def __init__(self, center, end, angleWidth, color, length=None, layer=1, snapshot=False):
        super().__init__(layer, center, end, color, snapshot)
        self.angleWidth = angleWidth
        self.length = length

    def update(self, dt):
        super().update(dt)

        direction = helper.rotateVector(self.end-self.center, -self.angleWidth/2)
        if self.length is not None:
            direction = direction.normalize(self.length)
        pointCoord = [self.center, self.center+direction]
        steps = int(self.angleWidth / 10) + 1
        angleStep = self.angleWidth / steps
        for _ in range(steps):
            direction = helper.rotateVector(direction, angleStep)
            pointCoord.append(self.center+direction)
        self.points = []
        for p in pointCoord:
            pix = coordsToPix(p)
            self.points.append(pix.vals)

    def draw(self):
        arcade.draw_polygon_filled(self.points, self.color)


class CastBar(Drawable):
    def __init__(self, duration, text='', center=(1.3, 0.5), width=0.3, layer=4):
        super().__init__(layer, center)
        self.width = width
        self.duration = duration
        self.filled = 0
        self.text = text

    def update(self, dt):
        super().update(dt)
        self.filled += dt/self.duration
        if self.filled > 1:
            self.filled = 1

    def draw(self):
        height = 10
        pixPos = coordsToPix(self.center)
        pixWidth = sizeToPix(self.width)
        arcade.draw_rectangle_filled(pixPos.x, pixPos.y,
            pixWidth, height, arcade.color.BISTRE)
        arcade.draw_xywh_rectangle_filled(pixPos.x-pixWidth/2, pixPos.y-height/2,
            pixWidth*self.filled, height, arcade.color.WHITE)
        arcade.draw_rectangle_outline(pixPos.x, pixPos.y,
            pixWidth, height, arcade.color.AMBER, 2)
        if len(self.text) > 0:
            arcade.draw_text(self.text, pixPos.x, pixPos.y-30,
                arcade.color.WHITE, helper.FONT_SIZE, align='center', font_name='calibri', anchor_x='center')


class SpriteDrawable(Drawable):
    def __init__(self, icon, center, layer, width, height, offset=Vector(0, 0)):
        super().__init__(layer, center)
        self.sprite = arcade.Sprite(icon)
        self.sprite.width, self.sprite.height = sizeToPix(width), sizeToPix(height)
        self.offset = offset

    def draw(self):
        pixPos = coordsToPix(self.center + self.offset)
        self.sprite.center_x = pixPos.x
        self.sprite.center_y = pixPos.y
        self.sprite.draw()


class TextDrawable(Drawable):
    def __init__(self, text, center, color, size, layer):
        super().__init__(layer, center, color)
        self.text = text
        self.size = size

    def draw(self):
        pixPos = coordsToPix(self.center)
        arcade.draw_text(self.text, pixPos.x, pixPos.y,
            self.color, self.size, align='center', font_name='calibri', anchor_x='center')
