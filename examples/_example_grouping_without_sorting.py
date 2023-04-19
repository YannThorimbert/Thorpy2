"""
We show here how to group elements inside a common parent without
changing the way the elements are arranged.
"""
#tags: group, sorting, store elements, parent, children, invisible, order, order elements, Box, stick_to


import pygame, random
import thorpy

pygame.init()

W, H = 1200, 700
screen = pygame.display.set_mode((W,H))
thorpy.init(screen, thorpy.theme_classic) #bind screen to gui elements and set theme

children = [thorpy.Button("Button "+str(i)) for i in range(6)] #create the elements
#Let's make some random placements
children[1].stick_to(children[0], "top", "bottom")
children[2].stick_to(children[0], "bottom", "top")
children[3].stick_to(children[0], "right", "left")
children[4].stick_to(children[0], "left", "right")

group = thorpy.Group(children, None)
group.center_on(screen) #now the group can be treated as a whole

def refresh():
    screen.fill((200,200,200))
#For the sake of brevity, the main loop is replaced here by a shorter but blackbox-like method
player = group.get_updater()
player.launch(refresh)
pygame.quit()

