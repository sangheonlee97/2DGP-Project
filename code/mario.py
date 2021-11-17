import game_framework
from pico2d import *
from ball import Ball

import game_world

# Mario Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Mario Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8



# Mario Event
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


# Mario States

class IdleState:

    def enter(mario, event):

        if event == DASH_DOWN:
            mario.dash = 2
        elif event == DASH_UP:
            mario.dash = 1
        if event == RIGHT_DOWN:
            mario.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            mario.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            mario.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            mario.velocity += RUN_SPEED_PPS
        mario.timer = 1000

    def exit(mario, event):
        if event == JUMP and mario.fall == False:
            mario.jump = 13

    def do(mario):
        mario.frame = 0
        mario.timer -= 1
        if mario.timer == 0:
            mario.add_event(SLEEP_TIMER)
        if mario.jump > 0:
            mario.y += 15 + (mario.velocity * game_framework.frame_time)
            mario.jump -= 1
        if mario.fall == True and mario.jump == 0:
            mario.y -= 7

    def draw(mario):
        if mario.jump > 0:
            if mario.dir == 1:
                mario.image.clip_composite_draw(2 * 27, mario.life * 52, 27, 52 - 14 * mario.life, 0,
                                                'h', mario.x, mario.y - 8 - 7 * mario.life, 27, 52 - 14 * mario.life)  # 작을때 키 38, 클때 52

            else:
                mario.image.clip_draw(2 * 27, mario.life * 52, 27, 52 - 14 * mario.life, mario.x,
                                      mario.y - 8 - 7 * mario.life)  # 작을때 키 38, 클때 52
        else:
            if mario.dir == 1:
                mario.image.clip_composite_draw(int(mario.frame) * 27, mario.life * 52, 27, 52 - 14 * mario.life, 0,
                                                'h', mario.x, mario.y - 8 - 7 * mario.life, 27, 52 - 14 * mario.life)  # 작을때 키 38, 클때 52 8

            else:
                mario.image.clip_draw(int(mario.frame) * 27, mario.life * 52, 27, 52 - 14 * mario.life, mario.x,
                                      mario.y - 8 - 7 * mario.life)  # 작을때 키 38, 클때 52 8


class RunState:

    def enter(mario, event):
        if event == DASH_DOWN:
            mario.dash = 2
        elif event == DASH_UP:
            mario.dash = 1
        if event == RIGHT_DOWN:
            mario.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            mario.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            mario.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            mario.velocity += RUN_SPEED_PPS

        mario.dir = clamp(-1, mario.velocity, 1)

    def exit(mario, event):
        if event == JUMP and mario.fall == False:
            mario.jump = 13


    def do(mario):
        #mario.frame = (mario.frame + 1) % 8
        mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        mario.x += mario.velocity * game_framework.frame_time * mario.dash * 1.5
        mario.x = clamp(25, mario.x, 1600 - 25)
        if mario.jump > 0:
            if mario.velocity > 0:
                mario.y += 15 + (mario.velocity * game_framework.frame_time * mario.dash)
            else:
                mario.y += 15 + (-mario.velocity * game_framework.frame_time * mario.dash)
            mario.jump -= 1
        if mario.fall == True and mario.jump == 0:
            mario.y -= 7

    def draw(mario):
        if mario.jump > 0:
            if mario.dir == 1:
                mario.image.clip_composite_draw(2 * 27, mario.life * 52, 27, 52 - 14 * mario.life, 0,
                                                'h', mario.x, mario.y - 8 - 7 * mario.life, 27,
                                                52 - 14 * mario.life)  # 작을때 키 38, 클때 52
            else:
                mario.image.clip_draw(2 * 27, mario.life * 52, 27, 52 - 14 * mario.life, mario.x,
                                      mario.y - 8 - 7 * mario.life)  # 작을때 키 38, 클때 52
        else:
            if mario.dash == 1:
                if mario.dir == 1:
                    mario.image.clip_composite_draw(int(mario.frame) * 27, mario.life * 52, 27, 52 - 14 * mario.life, 0,
                                                    'h', mario.x, mario.y - 8 - 7 * mario.life, 27,
                                                    52 - 14 * mario.life)  # 작을때 키 38, 클때 52
                else:
                    mario.image.clip_draw(int(mario.frame) * 27, mario.life * 52, 27, 52 - 14 * mario.life, mario.x,
                                          mario.y - 8 - 7 * mario.life)  # 작을때 키 38, 클때 52
            else:
                if mario.dir == 1:
                    mario.image.clip_composite_draw((int(mario.frame) * 2 + 1) * 27, mario.life * 52, 27,
                                                    52 - 14 * mario.life, 0, 'h', mario.x, mario.y - 8 - 7 * mario.life, 27,
                                                    52 - 14 * mario.life)  # 작을때 키 38, 클때 52

                else:
                    mario.image.clip_draw((int(mario.frame) * 2 + 1) * 27, mario.life * 52, 27, 52 - 14 * mario.life,
                                          mario.x, mario.y - 8 - 7 * mario.life)  # 작을때 키 38, 클때 52


class SleepState:

    def enter(mario, event):
        mario.frame = 0

    def exit(mario, event):
        pass

    def do(mario):
        mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

    def draw(mario):
        if mario.dir == 1:
            mario.image.clip_composite_draw(int(mario.frame) * 100, 300, 100, 100, 3.141592 / 2, '', mario.x - 25, mario.y - 25, 100, 100)
        else:
            mario.image.clip_composite_draw(int(mario.frame) * 100, 200, 100, 100, -3.141592 / 2, '', mario.x + 25, mario.y - 25, 100, 100)






next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState, SLEEP_TIMER: SleepState, DASH_DOWN: IdleState, DASH_UP: IdleState, JUMP: IdleState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState, DASH_DOWN: RunState, DASH_UP: RunState, JUMP: RunState},
    SleepState: {LEFT_DOWN: RunState, RIGHT_DOWN: RunState, LEFT_UP: RunState, RIGHT_UP: RunState, JUMP: IdleState, DASH_DOWN: IdleState, DASH_UP: IdleState}
}

class Mario:

    def __init__(self):
        self.x, self.y = 1600 // 2, 90
        self.image = load_image('mario2.png')
        self.font = load_font('ENCR10B.TTF', 16)
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        self.jump = 0
        self.fall = False
        self.dash = 1
        self.life = 0

    def get_bb(self):
        if self.life == 1:
            return self.x - 15, self.y - 35, self.x + 13, self.y + 4
        else:
            return self.x - 15, self.y - 35, self.x + 13, self.y + 18


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

