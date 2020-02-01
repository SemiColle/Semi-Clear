import arcade, math
from .helper import coordsToPix, Vector
from . import helper


class Drawable:
    # layers: 0:arena, 1:floor, 2:players, 3:boss, 4:coverall
    def __init__(self, layer=4, center=Vector(0, 0), color=None):
        self.active = True
        self.layer = layer
        # if it's a static position like (0.1, 1), make a copy
        self.center = Vector(center)
        # if isinstance(center, tuple) or isinstance(center, list):
        #     self.center = Vector(center)
        # elif isinstance(center, Vector): # if it's a vector, keep a reference
        #     self.center = center
        # elif isinstance(center, Drawable): # same for drawable (just for convenience)
        #     self.center = center.center
        # else:
        #     assert(False, 'Drawable center should be tuple, list, Vector or Drawable')
        self.color = color

    def update(self, dt):
        pass

    def draw(self):
        pass


class FollowingDrawable(Drawable):
    def __init__(self, layer, target, color=None):
        # if target is drawable, follow
        if hasattr(target, 'center'):
            super().__init__(layer, target.center, color)
            self.target = target
        else: # otherwise it's just a vector
            super().__init__(layer, target, color)
            self.target = Vector(target)

    def update(self, dt):
        # if not hasattr(self, 'drawn'):
        #     print('drawable drawn')
        #     self.drawn = True
        if hasattr(self.target, 'center'):
            self.center = self.target.center
        else:
            self.center = self.target


class Circle(FollowingDrawable):
    def __init__(self, target, radius, color, layer=1):
        super().__init__(layer, target, color)
        self.radius = radius

    def draw(self):
        pixPos = coordsToPix(self.center)
        arcade.draw_circle_filled(pixPos.x, pixPos.y, self.radius, self.color)


class Donut(FollowingDrawable):
    def __init__(self, target, innerRad, outerRad, color, layer=1):
        super().__init__(layer, target, color)
        self.radius = (outerRad + innerRad) / 2
        self.thickness = outerRad - innerRad

    def draw(self):
        pixPos = coordsToPix(self.center)
        arcade.draw_circle_outline(pixPos.x, pixPos.y, self.radius, self.color, self.thickness)


class ThickLine(FollowingDrawable):
    def __init__(self, target, startPoint, thickness, color, layer=1):
        super().__init__(layer, target, color)
        if hasattr(startPoint, 'center'):
            self.startPoint = startPoint
        else:
            self.startPoint = Vector(startPoint)
        self.start = Vector(0, 0)
        self.thickness = thickness

    def update(self, dt):
        super().update(dt)
        if hasattr(self.startPoint, 'center'):
            self.start = self.startPoint.center
        else:
            self.start = self.startPoint

    def draw(self):
        startPos = coordsToPix(self.start)
        endPos = coordsToPix(self.center)
        arcade.draw_line(startPos.x, startPos.y, endPos.x, endPos.y, self.color, self.thickness)


class AngledLine(ThickLine):
    def __init__(self, center, angle, length, thickness, color, layer=1):
        direction = helper.rotateVector(Vector(0, length), angle)
        end = direction + Vector(center)
        super().__init__(center, end, thickness, color, layer)


class Cone(Drawable):
    def __init__(self, center, target, angleWidth, color, length=None, layer=1):
        super().__init__(layer, center, color)
        target = Vector(target)
        direction = helper.rotateVector(target-self.center, -angleWidth/2)
        if length is not None:
            direction = direction.normalize(length)
        pointCoord = [self.center, self.center+direction]
        steps = int(angleWidth / 10) + 1
        angleStep = angleWidth / steps
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
    def __init__(self, duration, text='', center=(1.3, 0.5), width=150, layer=4):
        super().__init__(layer, center)
        self.width = width
        self.duration = duration
        self.filled = 0
        self.text = text

    def update(self, dt):
        self.filled += dt/self.duration
        if self.filled > 1:
            self.filled = 1

    def draw(self):
        height = 10
        pixPos = coordsToPix(self.center)
        arcade.draw_rectangle_filled(pixPos.x, pixPos.y,
            self.width, height, arcade.color.BISTRE)
        arcade.draw_xywh_rectangle_filled(pixPos.x-self.width/2, pixPos.y-height/2,
            self.width*self.filled, height, arcade.color.WHITE)
        arcade.draw_rectangle_outline(pixPos.x, pixPos.y,
            self.width, height, arcade.color.AMBER, 2)
        if len(self.text) > 0:
            arcade.draw_text(self.text, pixPos.x, pixPos.y-30,
                arcade.color.WHITE, helper.FONT_SIZE, align='center', font_name='calibri', anchor_x='center')


class Debuff(FollowingDrawable):
    def __init__(self, icon, target, relPos=Vector(-0.04, 0.04), layer=2.1):
        super().__init__(layer, target)
        self.sprite = arcade.Sprite(icon, scale=0.8)
        self.relPos = relPos

    def update(self, dt):
        super().update(dt)
        self.center = self.center + self.relPos
        pixPos = coordsToPix(self.center)
        self.sprite.center_x = pixPos.x
        self.sprite.center_y = pixPos.y

    def draw(self):
        self.sprite.draw()
