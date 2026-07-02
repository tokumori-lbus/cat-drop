import random
import logging
from pygamii.objects import Object
from pygamii.action import Action


class Fih(Object):
    def __init__(self):
        super().__init__()
        self.width = 7
        self.height = 4
        self.x = 0
        self.y = 1
        self.color = 'green'
    def __str__(self):
        return r"""   _\_   
\\/  o\ 
//\___=
   ''"""
    def down(self):
        self.y += 1
   
         

class jellyFih(Object):
    def __init__(self):
        super().__init__()
        self.width = 13
        self.height = 11
        self.x = 30
        self.y = 1
        self.color = 'magenta'
    def __str__(self):
        return r"""     _____
   /^ Oo ^\
  /^^  oO^^\
 {-_-__--_-_}
  /|||  \ ||
  /{{|  } |\
 {}/|   \ /}
 /{{{   \ |{
{/ \}   } \ \
 } |{   { } /
 { |    /}
 \ /    ` {
   {     }"""
    def left(self):
        self.x -= 3
        if self.collision(self.scene.wall_A):
            self.x += 3
    def right(self):
        self.x += 3
        if self.collision(self.scene.wall_B):
            self.x -= 3
    def down(self):
        self.y += 1
    
        if not hasattr(self, 'scene') or self.scene is None:
            return
        
        if self.collision(self.scene.car):
            self.scene.remove_object(self)
        elif self.y > 43:
            self.scene.remove_object(self)

class goldFih(Object):
    def __init__(self):
        super().__init__()
        self.width = 7
        self.height = 4
        self.x = 0
        self.y = 1
        self.color = 'yellow'
    def __str__(self):
        return r"""   _\_   
\\/  o\ 
//\___=
   ''"""
    def down(self):
        self.y += 2
    def left(self):
        self.x -= 5
        if self.collision(self.scene.wall_A):
            self.x += 5
    def right(self):
        self.x += 5    
        if self.collision(self.scene.wall_B):
            self.x -= 5

class FishSpawner(Action):
    def __init__(self, scene, spawn_every=15):
        super().__init__()
        self.interval = 0.1
        self.scene = scene
        self.spawn_every = spawn_every
        self.timer = 0

    def do(self):
        logging.debug("spawner do() called, timer={}".format(self.timer))
        if not hasattr(self.scene, 'score'):
            logging.debug("no score yet")
            return
        
        self.timer += 1
        if self.timer >= self.spawn_every:
            self.timer = 0
            try:
                fish = Fih()
                fish.x = random.randint(2, 92)
                fish.y = 0
                self.scene.add_object(fish)
                self.scene.add_action(FishFallAction(fish, self.scene.car, self.scene.score))
                logging.debug("fish spawned at x={}".format(fish.x))
            except Exception as e:
                logging.exception("crash in FishSpawner.update")
                raise

class FishFallAction(Action):
    def __init__(self, fih, car, score):
        super().__init__()
        self.fih = fih
        self.car = car
        self.score = score
        self.speed = 3
        self.interval = 0.5*(1/(self.score.points//10 + 1))  # frames between each drop, lower = faster

    def do(self):
        if not hasattr(self.fih, 'scene') or self.fih.scene is None:
            return
        try:
            self.fih.down()
            if self.fih.y > self.fih.scene.rows:
                if self.score.points > 0:
                    self.score.points -= 1
                    if self.score.points == 0:
                        self.car.lives -= 1
                elif self.score.points == 0:
                    self.car.lives -= 1
                self._remove()
                return
            if self.fih.collision(self.car):
                self.score.points += 1
                self._remove()
        except Exception as e:
            logging.exception("crash in FishFallAction.update")
            raise

    def _remove(self):
        try:
            if self.fih in self.fih.scene.objects:
                self.fih.scene.remove_object(self.fih)
        except Exception as e:
            logging.exception("crash in _remove")
        self.stop()  # ← instead of self.active = False

class JellyFishSpawner(Action):
    def __init__(self, scene, spawn_every=15):
        super().__init__()
        self.scene = scene
        self.interval = 2/((self.scene.score.points//20) + 1)  # frames between each drop, lower = faster
        self.spawn_every = spawn_every
        self.timer = 0

    def do(self):
        logging.debug("spawner do() called, timer={}".format(self.timer))
        if not hasattr(self.scene, 'score'):
            logging.debug("no score yet")
            return
        
        self.timer += 1
        if self.timer >= self.spawn_every:
            self.timer = 0
            try:
                fish = jellyFih()
                fish.x = random.randint(2, 85)
                fish.y = 0
                self.scene.add_object(fish)
                self.scene.add_action(JellyFishAction(fish, self.scene.car, self.scene.score))
                logging.debug("jellyfish spawned at x={}".format(fish.x))
            except Exception as e:
                logging.exception("crash in JellyFishSpawner.update")
                raise

class JellyFishAction(Action):
    def __init__(self, jellyFih, car, score):
        super().__init__()
        self.jellyFih = jellyFih
        self.car = car
        self.score = score
        self.speed = 67
        self.interval = 0.5*(1/(self.score.points//10 + 1))  # frames between each drop, lower = faster

    def do(self):
        if not hasattr(self.jellyFih, 'scene') or self.jellyFih.scene is None:
            return
        try:
            self.jellyFih.down()

            decide = random.randint(0, 3)
            if decide == 1:
                self.jellyFih.left()
            elif decide == 2:
                self.jellyFih.right()


            if self.jellyFih.y > self.jellyFih.scene.rows:
                self._remove()
                return
            if self.jellyFih.collision(self.car):
                self.car.lives -= 1
                self._remove()
        except Exception as e:
            logging.exception("crash in JellyfishAction.update")
            raise

    def _remove(self):
        try:
            if self.jellyFih in self.jellyFih.scene.objects:
                self.jellyFih.scene.remove_object(self.jellyFih)
        except Exception as e:
            logging.exception("crash in _remove")
        self.stop()  # ← instead of self.active = False

class goldFishSpawner(Action):
    def __init__(self, scene, spawn_every=67):
        super().__init__()
        self.interval = 0.1
        self.scene = scene
        self.spawn_every = spawn_every
        self.timer = 0

    def do(self):
        logging.debug("spawner do() called, timer={}".format(self.timer))
        if not hasattr(self.scene, 'score'):
            logging.debug("no score yet")
            return
        
        self.timer += 1
        if self.timer >= self.spawn_every:
            self.timer = 0
            try:
                goldfish = goldFih()
                goldfish.x = random.randint(2, 92)
                goldfish.y = 0
                self.scene.add_object(goldfish)
                self.scene.add_action(goldFishFallAction(goldfish, self.scene.car, self.scene.score))
                logging.debug("goldfish spawned at x={}".format(goldfish.x))
            except Exception as e:
                logging.exception("crash in goldFishSpawner.update")
                raise

class goldFishFallAction(Action):
    def __init__(self, goldfih, car, score):
        super().__init__()
        self.goldfih = goldfih
        self.car = car
        self.score = score
        self.speed = 3
        self.interval = 0.5*(1/(self.score.points//10 + 1))  # frames between each drop, lower = faster

    def do(self):
        if not hasattr(self.goldfih, 'scene') or self.goldfih.scene is None:
            return
        try:
            self.goldfih.down()

            decide = random.randint(0, 3)
            if decide == 1:
                self.goldfih.left()
            elif decide == 2:
                self.goldfih.right()
            
            if self.goldfih.y > self.goldfih.scene.rows:
                self._remove()
                return
            if self.goldfih.collision(self.car):
                self.score.points += 5
                self._remove()
        except Exception as e:
            logging.exception("crash in FishFallAction.update")
            raise
    def _remove(self):
        try:
            if self.goldfih in self.goldfih.scene.objects:
                self.goldfih.scene.remove_object(self.goldfih)
        except Exception as e:
            logging.exception("crash in _remove")
        self.stop()  # ← instead of self.active = False