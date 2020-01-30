import arcade
from .helper import coordsToPix, Vector
from . import helper


class Drawable:
    # layers: 0:arena, 1:floor, 2:players, 3:boss, 4:coverall
    def __init__(self, layer, center=Vector(0, 0)):
        self.active = True
        self.layer = layer
        self.center = Vector(center)

    def update(self, dt):
        pass

    def draw(self):
        pass


class FollowingDrawable(Drawable):
    def __init__(self, layer, target):
        # if target is drawable, follow
        if hasattr(target, 'center'):
            super().__init__(layer, target.center)
            self.target = target
        else: # otherwise it's just a vector
            super().__init__(layer, target)
            self.target = Vector(target)

    def update(self, dt):
        if hasattr(self.target, 'center'):
            self.center = self.target.center
        else:
            self.center = self.target


class Circle(FollowingDrawable):
    def __init__(self, target, radius, color, layer=1):
        super().__init__(layer, target)
        self.radius = radius
        self.color = color

    def draw(self):
        pixPos = coordsToPix(self.center)
        arcade.draw_circle_filled(pixPos.x, pixPos.y, self.radius, self.color)


class Donut(FollowingDrawable):
    def __init__(self, target, innerRad, outerRad, color, layer=1):
        super().__init__(layer, target)
        self.radius = (outerRad + innerRad) / 2
        self.thickness = outerRad - innerRad
        self.color = color

    def draw(self):
        pixPos = coordsToPix(self.center)
        arcade.draw_circle_outline(pixPos.x, pixPos.y, self.radius, self.color, self.thickness)


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
