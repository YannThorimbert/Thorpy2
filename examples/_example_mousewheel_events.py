"""We show here how to react to mouse wheel events. The button changes its color each time the mouse wheel is used."""
#tags: mousebuttondown, wheel, events, custom events, reactions

import pygame
import thorpy as tp

pygame.init()

screen = pygame.display.set_mode((1200, 700))
tp.init(screen, tp.theme_human) #bind screen to gui elements and set theme

my_button = tp.Button("Active mouse wheel while hovering me")
my_button.center_on(screen)

button_color = (200,200,200)
my_button.set_bck_color(button_color)

def my_react(mousebuttondown_button): #reaction to the button click
    global button_color
    print("Mouse wheel event")
    if mousebuttondown_button == 4:
        intensity = max(button_color[0]-10, 0)
    else:
        intensity = min(button_color[0]+10, 255)
    button_color = (intensity,)*3
    my_button.set_bck_color(button_color)
    my_button.set_text("Color: " + str(button_color))
my_button.react_buttondown = my_react

def before_gui(): #add here the things to do each frame before blitting gui elements
    screen.fill((250,)*3)
tp.call_before_gui(before_gui) #tells thorpy to call before_gui() before drawing gui.

#For the sake of brevity, the main loop is replaced here by a shorter but blackbox-like method
player = my_button.get_updater().launch()
pygame.quit()
