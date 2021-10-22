from pico2d import *

keydown = False
pre = 4

class Mario():
    def __init__(self):
        self.x, self.y = 90, 90
        self.frame = 0
        self.gasok = 0
        self.speed = 0
        self.right = True
        self.onblock = True
        self.dash = False
        self.yy = 0
        self.f = 0
        self.image = load_image('animation_sheet.png')

    def update(self):
        if self.speed < 0:
            self.right = False
        elif self.speed > 0:
            self.right = True




        t = 0.5
        self.x = (1-t) * self.x + t * (self.x + self.speed)
        self.y = (1 - t) * self.y + t * (self.y + self.yy)
        if self.y == 90:        #나중에 맵구현후에 발판 밟는 상황으로 변경
            self.onblock = True
        elif self.y > 90:       #마찬가지
            self.onblock = False
        if self.y > 90:
            self.yy -= 30
        elif self.onblock:
            self.yy = 0


    def speed_update(self):
        self.frame = (self.frame + 1) % 8

        if self.gasok != 0:
            if self.gasok > 10:
                self.gasok = 10
            elif self.gasok < -10:
                self.gasok = -10
            self.speed += self.gasok
            if mario.dash:
                if self.speed > 60:
                    self.speed = 60
                elif self.speed < -60:
                    self.speed = -60
            else:
                if self.speed > 40:
                    self.speed = 40
                elif self.speed < -40:
                    self.speed = -40
        else:
            if self.speed > 0:
                self.speed -= 5
            elif self.speed < 0:
                self.speed += 5
        print('spdup : speed = ')
        print(self.speed)
        print(self.gasok)
    def forward(self):
        self.gasok += 5
    def backward(self):
        self.gasok -= 5

    def jump(self):
        self.yy = 120


    def draw(self):
        if self.speed == 0:
            if self.right:
                self.image.clip_draw(self.frame * 100, 100 * 3, 100, 100, self.x, self.y)
            else:
                self.image.clip_draw(self.frame * 100, 100 * 2, 100, 100, self.x, self.y)
        else:
            if self.right:
                self.image.clip_draw(self.frame * 100, 100 * 1, 100, 100, self.x, self.y)
            else:
                self.image.clip_draw(self.frame * 100, 100 * 0, 100, 100, self.x, self.y)

class Grass():
    def __init__(self):
        self.image = load_image('grass.png')
    def draw(self):
        self.image.draw(400, 30)

def handle_events():
    global running
    global mario
    global keydown
    global pre
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_a:
            mario.backward()
            keydown = True
            pre = 0
        elif event.type == SDL_KEYDOWN and event.key == SDLK_d:
            mario.forward()
            keydown = True
            pre = 1
        elif event.key == SDLK_j:
            if mario.onblock:
                mario.jump()
            keydown = True
        elif event.key == SDLK_k:
            if mario.dash:
                mario.dash = False
            else:
                mario.dash = True

        elif event.type == SDL_KEYUP:
            keydown = False

        elif event.key:
            if mario.gasok > 0:
                mario.gasok -= 5
            elif mario.gasok < 0:
                mario.gasok += 5


open_canvas(1280, 800)
mario = Mario()
grass = Grass()
running = True


while running:
    handle_events()
    mario.speed_update()
    mario.update()
    if keydown:
        if pre == 0:
            mario.backward()
        elif pre == 1:
            mario.forward()
        pass
    else:
        if mario.gasok > 0:
            mario.gasok -= 5
        elif mario.gasok < 0:
            mario.gasok += 5

    clear_canvas()
    mario.draw()
    grass.draw()
    update_canvas()
    mario.f = False
    mario.b = False
    delay(0.05)

close_canvas()