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
tp.init(screen, tp.theme_simple) #bind screen to gui elements and set theme

# my_pool = tp.TogglablesPool("Difficulty",
#                                ("Beginner", "Intermediate", "Pro"), #possibilities
#                                "Beginner") #initial value
my_pool = tp.ListView("", #title - let empty for no title
                        ["Entry "+str(i) for i in range(1,11)], #possibilities
                        initial_value=4, #initial value (you can aldo pass its str content, e.g. 'Entry5')
                        togglable_type="toggle") #either 'toggle', 'radio' or 'checkbox'


box = tp.TitleBox("List View Example", [my_pool])
box.center_on(screen)

def refresh():#some function that you call once per frame
    screen.fill((255,255,255))
        
#For the sake of brevity, the main loop is replaced here by a shorter but blackbox-like method
player = box.get_updater().launch(refresh)
pygame.quit()

