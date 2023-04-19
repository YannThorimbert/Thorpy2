"""We show here how to use a bar whose level indicates the amount of something."""
#tags: Lifebar, loading bar, load bar, level bar, progress bar, progredd, loading, life


import pygame, thorpy as tp

pygame.init()

screen = pygame.display.set_mode((1200, 700))
tp.init(screen, tp.theme_human) #bind screen to gui elements and set theme

my_color = ((255,100,100), (150,30,30), "v") #light gray to dark gray vertical gradient
fuel = tp.Lifebar("Fuel (click to refuel)", 400, my_color, font_color=(200,)*3)
fuel.center_on(screen)

#we define below a way to refuel the bar
def refuel():
    fuel.set_value(1.)
fuel.children[-1].at_unclick = refuel
fuel.children[-1].hand_cursor = True

def before_gui(): #add here the things to do each frame before blitting gui elements
    screen.fill((200,)*3)
    current = fuel.get_value()
    new_val = max(0., current-0.001)
    fuel.set_value(new_val)
tp.call_before_gui(before_gui) #tells thorpy to call before_gui() before drawing gui.

#For the sake of brevity, the main loop is replaced here by a shorter but blackbox-like method
player = fuel.get_updater().launch()
pygame.quit()

