import sys
import os

def force_terminal_size(rows=30, cols=100):
    if sys.platform != "win32":
        # Check if we are running in an actual interactive terminal environment
        if sys.stdout.isatty():
            # Standard XTerm window manipulation sequence
            sys.stdout.write(f"\x1b[8;{rows};{cols}t")
            sys.stdout.flush()
    else:
        os.system(f"mode con: cols={cols} lines={rows}")

# Put this at the very top of game.py
force_terminal_size(40, 102)

# Now import pygamii
from pygamii.scene import BaseScene
from wallers import Wall
from fishes import FishSpawner, JellyFishSpawner, goldFishSpawner
from cat import Keyboard, Car
from score import LiveScore, Score
from title import menu
from gameover import GameOverChecker, GameOverScene

import logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG)

class Scene(BaseScene):
    def __init__(self, *args, **kwargs):
        try:
            super(Scene, self).__init__(*args, **kwargs)
            logging.debug("super init done")
            self.cols = 100
            self.rows = 35

            self.universal = 15

            self.wall_A = Wall(position=-1)
            self.add_object(self.wall_A)
            self.wall_B = Wall(position=101)
            self.add_object(self.wall_B)
            logging.debug("walls added")

            self.live_score = LiveScore()
            self.add_object(self.live_score)
            self.score = Score()
            self.add_object(self.score)
            logging.debug("scores added")

            self.car = Car(self.score)
            self.add_object(self.car)
            logging.debug("car added")
            self.add_action(Keyboard())
            logging.debug("keyboard added")

            self.add_action(FishSpawner(self, self.universal))

            logging.debug("spawner added")

            self.add_action(JellyFishSpawner(self, self.universal))
            self.add_action(JellyFishSpawner(self, 30))
            
            logging.debug("jellyfish spawner added")

            self.add_action(goldFishSpawner(self, 100))

            if self.score.points%50 == 0 and self.score.points != 0:
                self.universal = (self.universal)/2.5
                
                logging.debug("jellyfish spawner added at 50 points")

            self.add_action(GameOverChecker(self))


        except Exception as e:
            logging.exception("crash in Scene.__init__")
            raise


        
        
        

if __name__ == '__main__':
    menuscene = menu()
    menuscene.start()
    while True:
       scene = Scene()
       scene.start()

       gameoverer = GameOverScene()
       gameoverer.start()

       if not gameoverer.should_restart:
           break
