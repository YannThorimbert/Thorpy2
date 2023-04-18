"""
We show here how to interact with element's value
"""

import pygame
import thorpy as tp

pygame.init()
W,H = 1200, 700
screen = pygame.display.set_mode((W, H))
tp.init(screen, tp.theme_human) #bind screen to gui elements and set theme

my_pool = tp.TogglablesPool("Difficulty",
                               ("Beginner", "Intermediate", "Pro"), #possibilities
                               "Beginner") #initial value
choice = tp.Text(my_pool.get_value())
box = tp.TitleBox("Togglables pool example", [my_pool, choice])
box.center_on(screen)

def refresh():#some function that you call once per frame
    screen.fill((255,255,255))
    if my_pool.get_value():
        choice.set_text("Your choice: " + my_pool.get_value())
        
#For the sake of brevity, the main loop is replaced here by a shorter but blackbox-like method
player = box.get_updater().launch(refresh)
pygame.quit()

