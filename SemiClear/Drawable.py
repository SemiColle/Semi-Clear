import arcade
from .helper import coordsToPix, Vector


class Drawable:
    def __init__(self):
        self.active = True

    def update(self, dt):
        pass

    def draw(self):
        pass


class Circle(Drawable):
    def __init__(self, center, radius, color):
        super().__init__()
        self.center = Vector(center)
        self.radius = radius
        self.color = color

    def draw(self):
        pixPos = coordsToPix(self.center)
        arcade.draw_circle_filled(pixPos.x, pixPos.y, self.radius, self.color)


class CastBar(Drawable):
    def __init__(self, duration, text='', center=(1.3, 0.5), width=150):
        super().__init__()
        self.center = Vector(center)
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
                arcade.color.WHITE, 16, align='center', font_name='calibri', anchor_x='center')
