"""
We show here how to set up a pool of Togglables (on/off) elements, in such a way that
only once at a time is in the state 'on'. This can be seen as a system of tabs.
"""
#tags: TogglablesPool, grouping & positioning, events handling, ToggleButton, Togglable, radio, checkbox

import pygame
import thorpy as tp

pygame.init()
W,H = 1200, 700
screen = pygame.display.set_mode((W, H))
tp.init(screen, tp.theme_human) #bind screen to gui elements and set theme

# my_pool = tp.TogglablesPool("Difficulty",
#                                ("Beginner", "Intermediate", "Pro"), #possibilities
#                                "Beginner") #initial value
my_pool = tp.TogglablesPool("Difficulty",
                               ("Beginner", "Intermediate", "Pro"), #possibilities
                               "Beginner", #initial value
                               togglable_type="toggle") #either 'toggle', 'radio' or 'checkbox'
choice = tp.Text("Your choice: " + my_pool.get_value())
box = tp.TitleBox("Togglables Pool Example", [my_pool, choice])
box.center_on(screen)

def refresh():#some function that you call once per frame
    screen.fill((255,255,255))
    if my_pool.get_value():
        choice.set_text("Your choice: " + my_pool.get_value())
        print(box.rect, box.get_children_rect())
        
#For the sake of brevity, the main loop is replaced here by a shorter but blackbox-like method
player = box.get_updater().launch(refresh)
pygame.quit()

