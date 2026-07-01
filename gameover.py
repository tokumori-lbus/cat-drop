from pygamii.action import Action, BaseKeyboard
from pygamii.objects import Object
from pygamii.scene import BaseScene
from highscore import load_highscore, save_highscore

class GameOverChecker(Action):
    def __init__(self, scene):
        super().__init__()
        self.scene = scene
        self.interval = 0.1

    def do(self):
        if self.scene.car.lives <= 0:
            save_highscore(self.scene.score.points)
            self.scene.stop()


class OverText(Object):
    def __init__(self):
        super().__init__()
        self.width = 62
        self.height = 10
        self.x = 38
        self.y = 6
        self.color = 'green'
    def __str__(self):
        return r"""⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⠀⠀⠀⣶⡆⠀⣰⣿⠇⣾⡿⠛⠉⠁
⠀⣠⣴⠾⠿⠿⠀⢀⣾⣿⣆⣀⣸⣿⣷⣾⣿⡿⢸⣿⠟⢓⠀⠀
⣴⡟⠁⣀⣠⣤⠀⣼⣿⠾⣿⣻⣿⠃⠙⢫⣿⠃⣿⡿⠟⠛⠁⠀
⢿⣝⣻⣿⡿⠋⠾⠟⠁⠀⠹⠟⠛⠀⠀⠈⠉⠀⠉⠀⠀⠀⠀⠀
⠀⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⣀⢀⣠⣤⣴⣤⣄⠀
⠀⠀⠀⠀⣀⣤⣤⢶⣤⠀⠀⢀⣴⢃⣿⠟⠋⢹⣿⣣⣴⡿⠋⠀
⠀⠀⣰⣾⠟⠉⣿⡜⣿⡆⣴⡿⠁⣼⡿⠛⢃⣾⡿⠋⢻⣇⠀⠀
⠀⠐⣿⡁⢀⣠⣿⡇⢹⣿⡿⠁⢠⣿⠷⠟⠻⠟⠀⠀⠈⠛⠀⠀
⠀⠀⠙⠻⠿⠟⠋⠀⠀⠙⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"""
class outrotext(Object):
    def __init__(self):
        super().__init__()
        self.width = 29
        self.height = 1
        self.x = 42
        self.y = 25
        self.color = 'green'
        self.score = load_highscore()
    def __str__(self):
        return f"High Score: {self.score}\nPress q to QUIT \nPress r to RESTART"
    
class GameOverScene(BaseScene):
    def __init__(self, *args, **kwargs):
        super(GameOverScene, self).__init__(*args, **kwargs)
        self.cols = 100
        self.rows = 35

        self.overtext = OverText()
        self.add_object(self.overtext)

        self.outro = outrotext()
        self.add_object(self.outro)

        self.options = GameoverOptions()
        self.add_action(self.options)

    
class GameoverOptions(BaseKeyboard):
    def handler(self, key):
        if key == ord('r') or key == ord('R'):
            self.scene.should_restart = True
            self.scene.stop()
        elif key == ord('q') or key == ord('Q'):
            self.scene.should_restart = False
            self.scene.stop()
