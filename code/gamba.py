import random
from pico2d import *
import game_world
import game_framework
from mario import *

class Gamba:

    def __init__(self):
        self.image = load_image('gamba.png')
        self.x, self.y = random.randint(0, 1600-1), 60
        self.frame = 0

    def get_bb(self):
        return self.x - 16, self.y - 15, self.x + 15, self.y + 15

    def draw(self):
        self.image.clip_draw(int(self.frame) * 32, 0, 31, 32, self.x, self.y)

        #self.image.draw(self.x, self.y)
        # fill here for draw
        draw_rectangle(*self.get_bb())

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        self.x += 20 * game_framework.frame_time

    #fill here for def stop


# fill here
# class BigBall