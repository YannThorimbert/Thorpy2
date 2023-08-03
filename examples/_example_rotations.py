"""
We show here how to rotate elements.
"""

import pygame
import thorpy as tp

pygame.init()

W, H = 1000, 700
screen = pygame.display.set_mode((W,H))
tp.init(screen, tp.theme_round) #bind screen to gui elements and set theme

group1 = tp.Group([tp.Button("GroupOne "+str(i)) for i in range(6)], "grid")

group2 = tp.Box([tp.Button("GroupTwo "+str(i)) for i in range(6)])
group2.sort_children("grid", nx=3, ny=2) #nx and ny are optional

button = tp.Button("Hello")

group1.rotate(90) #rotate whole group
group2.rotate(180) #rotate whole group
button.rotate(270) #rotate a single button

#now we place elements in such a way that they don't screen each other
group1.stick_to("screen", "left", "left")
group2.stick_to("screen", "top", "top")
button.stick_to("screen", "right", "right")

#use None to regroup the elements so that it does not store them (we want to keep their location for demo)
metagroup = tp.Group([group1, group2, button], None)
def before_gui(): #add here the things to do each frame before blitting gui elements
    screen.fill((20,)*3)
tp.call_before_gui(before_gui) #tells thorpy to call before_gui() before drawing gui.
#For the sake of brevity, the main loop is replaced here by a shorter but blackbox-like method
player = metagroup.get_updater()
player.launch()
pygame.quit()

# todo: marche pas avec tous les themes

