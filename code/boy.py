import game_framework
from pico2d import *
from ball import Ball

import game_world

# Boy Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8



# Boy Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SLEEP_TIMER, DASH_DOWN, DASH_UP, JUMP = range(8)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_a): DASH_DOWN,
    (SDL_KEYUP, SDLK_a): DASH_UP,
    (SDL_KEYDOWN, SDLK_s): JUMP
}


# Boy States

class IdleState:

    def enter(boy, event):

        if event == DASH_DOWN:
            boy.dash = 2
        elif event == DASH_UP:
            boy.dash = 1
        if event == RIGHT_DOWN:
            boy.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            boy.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            boy.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            boy.velocity += RUN_SPEED_PPS
        boy.timer = 1000

    def exit(boy, event):
        if event == JUMP and boy.fall == False:
            boy.temp = 7

    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        boy.timer -= 1
        if boy.timer == 0:
            boy.add_event(SLEEP_TIMER)
        if boy.temp > 0:
            boy.y += 30 + (boy.velocity * game_framework.frame_time)
            boy.temp -= 1
        if boy.fall == True and boy.temp == 0:
            boy.y -= 12

    def draw(boy):
        if boy.dir == 1:
            boy.image.clip_draw(int(boy.frame) * 100, 300, 100, 100, boy.x, boy.y)
        else:
            boy.image.clip_draw(int(boy.frame) * 100, 200, 100, 100, boy.x, boy.y)


class RunState:

    def enter(boy, event):
        if event == DASH_DOWN:
            boy.dash = 2
        elif event == DASH_UP:
            boy.dash = 1
        if event == RIGHT_DOWN:
            boy.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            boy.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            boy.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            boy.velocity += RUN_SPEED_PPS

        boy.dir = clamp(-1, boy.velocity, 1)

    def exit(boy, event):
        if event == JUMP and boy.fall == False:
            boy.temp = 7


    def do(boy):
        #boy.frame = (boy.frame + 1) % 8
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        boy.x += boy.velocity * game_framework.frame_time * boy.dash
        boy.x = clamp(25, boy.x, 1600 - 25)
        if boy.temp > 0:
            if boy.velocity > 0:
                boy.y += 30 + (boy.velocity * game_framework.frame_time * boy.dash)
            else:
                boy.y += 30 + (-boy.velocity * game_framework.frame_time * boy.dash)
            boy.temp -= 1
        if boy.fall == True and boy.temp == 0:
            boy.y -= 12

    def draw(boy):
        if boy.dir == 1:
            boy.image.clip_draw(int(boy.frame) * 100, 100, 100, 100, boy.x, boy.y)
        else:
            boy.image.clip_draw(int(boy.frame) * 100, 0, 100, 100, boy.x, boy.y)

class SleepState:

    def enter(boy, event):
        boy.frame = 0

    def exit(boy, event):
        pass

    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

    def draw(boy):
        if boy.dir == 1:
            boy.image.clip_composite_draw(int(boy.frame) * 100, 300, 100, 100, 3.141592 / 2, '', boy.x - 25, boy.y - 25, 100, 100)
        else:
            boy.image.clip_composite_draw(int(boy.frame) * 100, 200, 100, 100, -3.141592 / 2, '', boy.x + 25, boy.y - 25, 100, 100)






next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState, SLEEP_TIMER: SleepState, DASH_DOWN: IdleState, DASH_UP: IdleState, JUMP: IdleState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState, DASH_DOWN: RunState, DASH_UP: RunState, JUMP: RunState},
    SleepState: {LEFT_DOWN: RunState, RIGHT_DOWN: RunState, LEFT_UP: RunState, RIGHT_UP: RunState, JUMP: IdleState, DASH_DOWN: IdleState, DASH_UP: IdleState}
}

class Boy:

    def __init__(self):
        self.x, self.y = 1600 // 2, 90
        self.image = load_image('animation_sheet.png')
        self.font = load_font('ENCR10B.TTF', 16)
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        self.temp = 0
        self.fall = False
        self.dash = 1

    def get_bb(self):
        # fill here
        return self.x - 20, self.y - 35, self.x + 20, self.y + 40


    def fire_ball(self):
        ball = Ball(self.x, self.y, self.dir * RUN_SPEED_PPS * 10)
        game_world.add_object(ball, 1)


    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)
        self.font.draw(1400, 550, '(Time: %3.2f)' % get_time(), (1, 1, 1))
        draw_rectangle(*self.get_bb())


    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

