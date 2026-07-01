from pygamii.objects import Object

class LiveScore(Object):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        self.height = 1
        self.width = 20

    def __str__(self):
        return 'Lives: ' + '♥ ' * self.scene.car.lives


class Score(Object):
    def __init__(self):
        super().__init__()
        self.x = 84
        self.y = 0
        self.height = 1
        self.width = 15
        self.points = 0

    def __str__(self):
        return 'Points: {}'.format(self.points)
