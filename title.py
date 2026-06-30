import curses
from pygamii.objects import Object
from pygamii.scene import BaseScene
from pygamii.action import BaseKeyboard
from highscore import load_highscore

class titledrop(Object):
    def __init__(self):
        super().__init__()
        self.width = 84
        self.height = 13
        self.x = 8
        self.y = 6
        self.color = 'green'
    def __str__(self):
        return r"""                                                                                    
                                                                                    
  ,----..                 ___                ,---,                                  
 /   /   \              ,--.'|_            .'  .' `\                     ,-.----.   
|   :     :             |  | :,'         ,---.'     \   __  ,-.   ,---.  \    /  \  
.   |  ;. /             :  : ' :         |   |  .`\  |,' ,'/ /|  '   ,'\ |   :    | 
.   ; /--`   ,--.--.  .;__,'  /          :   : |  '  |'  | |' | /   /   ||   | .\ : 
;   | ;     /       \ |  |   |           |   ' '  ;  :|  |   ,'.   ; ,. :.   : |: | 
|   : |    .--.  .-. |:__,'| :           '   | ;  .  |'  :  /  '   | |: :|   |  \ : 
.   | '___  \__\/: . .  '  : |__         |   | :  |  '|  | '   '   | .; :|   : .  | 
'   ; : .'| ," .--.; |  |  | '.'|        '   : | /  ; ;  : |   |   :    |:     |`-' 
'   | '/  :/  /  ,.  |  ;  :    ;        |   | '` ,/  |  , ;    \   \  / :   : :    
|   :    /;  :   .'   \ |  ,   /         ;   :  .'     ---'      `----'  |   | :    
 \   \ .' |  ,     .-./  ---`-'          |   ,.'                         `---'.|    
  `---`    `--`---'                      '---'                             `---`    
                                                                                    """
    
class introtext(Object):
    def __init__(self):
        super().__init__()
        self.width = 29
        self.height = 1
        self.x = 38
        self.y = 25
        self.color = 'green'
        self.score = load_highscore()
    def __str__(self):
        return f"High Score: {self.score}\nPress the spacebar to START..."

class starter(BaseKeyboard):
    def handler(self, key):
        if key == 32:
            self.scene.stop()

class menu(BaseScene):
    def __init__(self, *args, **kwargs):
        super(menu, self).__init__(*args, **kwargs)
        self.cols = 100
        self.rows = 35

        self.title = titledrop()
        self.add_object(self.title)

        self.intro = introtext()
        self.add_object(self.intro)

        self.starter = starter()
        self.add_action(self.starter)


