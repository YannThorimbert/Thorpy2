"""
In this example, I've built a mini game (Flappy-Bird-like) and its menu.
The purpose of this example is to show how easy it is to couple the menu with a game.
"""
#tags: game, real situation, updater, get_updater, flappy

import pygame, math
import thorpy

from _example_standard_game_utils import play_game #game logics (nothing to do with menus) is here

pygame.init()
screen = pygame.display.set_mode((1200, 700))
thorpy.set_default_font("PressStart2P-Regular.ttf", 20)
thorpy.init(screen, thorpy.theme_text) #bind screen to gui elements and set theme


start = thorpy.Button("Start new game") 
howto = thorpy.Button("How to play")
options = thorpy.Button("Options")
bye = thorpy.Button("Quit")

group = thorpy.Group([start, howto, options, bye])

title = thorpy.Text("My Demo Game", font_color=(255,255,255))
title.set_font_size(50)
title.stick_to(screen, "top", "top", (0,10))
gradient = thorpy.graphics.color_gradient(((50,50,255), (255,255,255)), screen.get_size(), "v")
def refresh_frame():
    screen.blit(gradient, (0,0))
    title.draw()
    yellow = round(220+30*math.sin(gui_loop.iteration*math.pi*1./gui_loop.fps))
    title.set_font_color((yellow,yellow,0))

FPS = 60
clock = pygame.time.Clock()
gui_loop = group.get_updater(fps=FPS)
playing = True
def main_menu():
    while playing:
        clock.tick(60)
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                quit_game()
        gui_loop.update(refresh_frame, events=events)
        pygame.display.flip()

def quit_game():
    global playing
    playing = False

hero_color = thorpy.LabelledColorPicker("Hero color", thorpy.ColorPicker(initial_value=(255,0,0)))
difficulty = thorpy.TogglablesPool("Difficulty", ("Beginner", "Intermediate", "Pro"), "Beginner")
def launch_options():
    menu = thorpy.Alert("Options", "", children=[hero_color, difficulty])
    menu.launch_nonblocking()

def launch_play_game():
    play_game(screen, difficulty.get_value(), hero_color.get_value())

def launch_help():
    help_txt = "#RGB(255,0,0)Goal#\n"+\
    "This is a Flappy-Bird-like game written for demonstration purpose."+\
    "The velocity of the 'bird' (well...) increases with time."+\
    "The goal is to survive for the given duration."+\
    "The duration depends on the difficulty level.\n\n"+\
    "#RGB(255,0,0)Commands#\n"+\
    "#RGB(0,255,0)<space>#: jump\n\n"+\
    "#RGB(255,0,0)Credits#\n"+\
    "Yann Thorimbert"
    help_element = thorpy.Text(help_txt)
    help_element.set_font_rich_text_tag("#")
    help_element.set_max_text_width(3*screen.get_width()//4)
    alert = thorpy.Alert("Help", text="", children=[help_element])
    alert.launch_nonblocking()

bye.at_unclick = quit_game
start.at_unclick = launch_play_game
options.at_unclick = launch_options
howto.at_unclick = launch_help

main_menu()  
pygame.quit()

