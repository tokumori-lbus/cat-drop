from pygamii.objects import Object

class Wall(Object):
    def __init__(self, position):
        super().__init__()
        self.x = position
        self.y = 0
        self.width = 1
        self.height = 35
        self.color = 'blue'
        self.char = '~'