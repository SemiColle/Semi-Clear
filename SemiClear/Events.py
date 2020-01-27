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


class DrawableEvent(Event):
    def __init__(self, gameWindow, time, drawable, add=True):
        super().__init__(gameWindow, time)
        self.drawable = drawable
        self.add = add

    def trigger(self):
        if self.add:
            self.gameWindow.sprites.append(self.drawable)
        else:
            self.drawable.active = False


class EventQueue:
    def __init__(self):
        self.queue = []
        self.time = 0
        self.nextEvent = 0

    def update(self, dt):
        self.time += dt
        if self.nextEvent < len(self.queue):
            if self.time >= self.queue[self.nextEvent].time:
                self.queue[self.nextEvent].trigger()
                self.nextEvent += 1

    def addEvent(self, event, relative=False, sortEvents=False):
        if relative:
            event.time += self.time
        if event.time >= self.time: # only add future events
            self.queue.append(event)
        if sortEvents:
            self.sortEvents()

    def sortEvents(self):
        self.queue.sort(key=attrgetter('time'))
