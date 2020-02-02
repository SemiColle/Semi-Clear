from operator import attrgetter


class Event:
    def __init__(self, gameWindow, time):
        self.gameWindow = gameWindow
        self.time = time

    def trigger(self):
        pass


class MessageEvent(Event):
    def __init__(self, gameWindow, time, message):
        super().__init__(gameWindow, time)
        self.message = message

    def trigger(self):
        print(self.message)


class RemoveDrawableEvent(Event):
    def __init__(self, gameWindow, time, drawable):
        super().__init__(gameWindow, time)
        self.drawable = drawable

    def trigger(self):
        self.drawable.active = False


class DrawableEvent(Event):
    def __init__(self, gameWindow, time, drawable):
        super().__init__(gameWindow, time)
        self.drawable = drawable

    def trigger(self):
        self.gameWindow.sprites.append(self.drawable)


class CallbackEvent(Event):
    def __init__(self, gameWindow, time, callback):
        super().__init__(gameWindow, time)
        self.callback = callback

    def trigger(self):
        self.callback()


class GotoEvent(Event):
    def __init__(self, gameWindow, time, who, targetPos, targetAngle, scatter, speed):
        super().__init__(gameWindow, time)
        self.who = who
        self.targetPos = targetPos
        self.targetAngle = targetAngle
        self.scatter = scatter
        self.speed = speed

    def trigger(self):
        self.who.goto(self.targetPos, self.targetAngle, self.scatter, self.speed)


class KnockbackEvent(Event):
    def __init__(self, gameWindow, time, angle, distance):
        super().__init__(gameWindow, time)
        self.angle = angle
        self.distance = distance

    def trigger(self):
        self.gameWindow.party.knockback(self.angle, self.distance)


class EventQueue:
    def __init__(self):
        self.queue = []
        self.time = 0

    def update(self, dt):
        self.time += dt
        while len(self.queue) > 0 and self.time >= self.queue[0].time:
            self.queue.pop(0).trigger()

    def addDrawableEvent(self, gameWindow, time, drawable, duration, relative=True):
        draw = DrawableEvent(gameWindow, time, drawable)
        self.addEvent(draw, relative)
        remove = RemoveDrawableEvent(gameWindow, time+duration, drawable)
        self.addEvent(remove, relative)

    def addEvent(self, event, relative=True):
        if relative:
            assert(event.time >= 0)
            event.time += self.time
        elif len(self.queue) > 0:
            # if absolute, make sure queue stays sorted
            assert(event.time >= self.queue[-1].time)
        self.queue.append(event)
        if relative:
            self.sortEvents()

    def sortEvents(self):
        self.queue.sort(key=attrgetter('time'))
