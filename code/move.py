from pico2d import *

keydown = False
pre = 4

class Boy():
    global keydown
    def __init__(self):
        self.x, self.y = 90, 90
        self.frame = 0
        self.xx, self.yy = 90, 90
        self.image = load_image('run_animation.png')

    def update_r(self):
        self.frame = (self.frame + 1) % 8
        self.xx += 20
    def update_l(self):
        self.frame = (self.frame + 1) % 8
        self.xx -= 20
    def update_u(self):
        self.frame = (self.frame + 1) % 8
        self.yy += 20
    def update_d(self):
        self.frame = (self.frame + 1) % 8
        self.yy -= 20
    def update(self):
        for i in range(0, 200, 20):
            t = i / 100
            tx, ty = self.x, self.y
            self.x = (1-t) * tx + t * self.xx
            self.y = (1-t) * ty + t * self.yy
            self.draw()
            update_canvas()

    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)


class Grass():
    def __init__(self):
        self.image = load_image('grass.png')
    def draw(self):
        self.image.draw(400, 30)

def handle_events():
    global running
    global boy
    global keydown
    global pre
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_w:
            boy.update_u()
            keydown = True
            pre = 0
        elif event.type == SDL_KEYDOWN and event.key == SDLK_s:
            boy.update_d()
            keydown = True
            pre = 2
        elif event.type == SDL_KEYDOWN and event.key == SDLK_a:
            boy.update_l()
            keydown = True
            pre = 1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_d:
            boy.update_r()
            keydown = True
            pre = 3
        elif event.type == SDL_KEYUP:
            keydown = False


open_canvas()

boy = Boy()
grass = Grass()

running = True


while running:
    handle_events()

    boy.update()
    if keydown:
        if pre == 0:
            boy.update_u()
            boy.update()
        elif pre == 1:
            boy.update_l()
            boy.update()
        elif pre == 2:
            boy.update_d()
            boy.update()
        elif pre == 3:
            boy.update_r()
            boy.update()

    clear_canvas()
    grass.draw()

    delay(0.05)

close_canvas()