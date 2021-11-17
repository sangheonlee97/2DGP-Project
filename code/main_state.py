import random
import json
import os

from pico2d import *
import game_framework
import game_world

from boy import Boy
from grass import Grass
from ball import Ball
from gamba import Gamba
from turtle import Turtle

name = "MainState"

boy = None
grass = None
balls = []
big_balls = []
gambas = []
turtles = []


def collide(a, b):
    # fill here
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

def collide_mob(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    if left_a < right_b: print('1')
    if right_a > left_b: print('12')
    if top_a > bottom_b: print('13')
    if bottom_a < top_b: print('14')

    return True


def enter():
    global boy
    boy = Boy()
    game_world.add_object(boy, 1)

    global grass
    grass = Grass()
    game_world.add_object(grass, 0)

    # fill here for balls
    global balls
    balls = [Ball() for i in range(10)]
    game_world.add_objects(balls, 1)

    global gambas
    gambas = [Gamba() for i in range(10)]
    game_world.add_objects(gambas, 1)

    global turtles
    turtles = [Turtle() for i in range(10)]

    game_world.add_objects(turtles, 1)


def exit():
    game_world.clear()

def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        else:
            boy.handle_event(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()
    if boy.y >= 90:
        boy.fall = True
    else:
        boy.fall = False
    # if collide(boy, grass):
    #     boy.fall = False
    # else:
    #     boy.fall = True
    for ball in balls:
        if collide(boy, ball):

            balls.remove(ball)
            game_world.remove_object(ball)
    for gamba in gambas:
        #if collide(boy, gamba):
        if collide_mob(boy, gamba):
            boy.y += 100
            boy.temp += 1
            gambas.remove(gamba)
            game_world.remove_object(gamba)

    for turtle in turtles:
        #if collide(boy, gamba):
        if collide_mob(boy, turtle):
            if turtle.life == 1:
                boy.y += 100
                boy.temp += 1

            turtle.life = 0




def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()






