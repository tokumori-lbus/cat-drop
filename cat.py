import curses
from pygamii.action import BaseKeyboard
from pygamii.objects import Object

class Car(Object):
    def __init__(self,score):
        super().__init__()
        self.width = 7
        self.height = 4
        self.x = 1
        self.y = 31
        self.color = 'yellow'
        self.rightus = r"""\    /\
 )  ( ')
(  /  )
 \(__)|"""
        self.leftus = r""" /\    /      
(' )  (       
 (  \  )      
 |(__)/"""
        self.status = self.rightus
        self.lives = 3
        self.score = score
        self.speed = (self.score.points//50) + 1
    def __str__(self, *args, **kwargs):
        return self.status
    def left(self):
        self.status = self.leftus
        self.x -= self.speed
        if self.collision(self.scene.wall_A):
            self.x += self.speed
    def right(self):
        self.status = self.rightus
        self.x += self.speed
        if self.collision(self.scene.wall_B):
            self.x -= self.speed


class Keyboard(BaseKeyboard):
    def handler(self, key):
        if key == curses.KEY_LEFT:
            self.scene.car.left()
            return True
        elif key == curses.KEY_RIGHT:
            self.scene.car.right()
            return True
        elif key == 'q' or key == ord('q'):
            self.scene.stop()