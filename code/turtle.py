import random
from pico2d import *
import game_world
import game_framework
from boy import *

class Turtle:

    def __init__(self):
        self.image = load_image('turtle.png')
        self.x, self.y = random.randint(0, 1600-1), 60
        self.frame = 0
        self.life = 1

    def get_bb(self):
        if self.life == 1:
            return self.x - 16, self.y - 15, self.x + 15, self.y + 35
        else:
            return self.x - 16, self.y - 15, self.x + 15, self.y + 17



    def draw(self):
        if self.life == 1:
            self.image.clip_draw(int(self.frame) * 32, 0, 32, 50, self.x, self.y + 10)
        else:
            self.image.clip_draw(int(self.frame + 2) * 32, 0, 32, 50, self.x, self.y + 10)

        #self.image.draw(self.x, self.y)
        # fill here for draw
        draw_rectangle(*self.get_bb())

    def update(self):
        if self.life == 1:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        else:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        self.x += 20 * game_framework.frame_time
