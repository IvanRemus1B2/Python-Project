from pygame import Surface


class MySurface(Surface):
    def __init__(self, width, height):
        super(MySurface, self).__init__((width, height))
