"""We show here how to declare heterogeneous text, i.e. text with mixed font styles."""
#tags: font, font styles, HeterogeneousTexts, advanced styling,

import pygame
import thorpy as tp

pygame.init()

screen = pygame.display.set_mode((1200, 700))
tp.init(screen, tp.theme_human) #bind screen to gui elements and set theme

texts = [("Hello, world. ", {"name":"arialrounded"}),
         ("How ", {"color":(0,0,255)}),
         ("are ", {}),
         ("you ", {"color":(0,255,0), "size":25, "outlined":True}),
         ("doing?", {"name":"timesnewroman"}),
         ]
text = tp.HeterogeneousTexts(texts)
text.center_on(screen)

def before_gui(): #add here the things to do each frame before blitting gui elements
    screen.fill((255,)*3)
tp.call_before_gui(before_gui) #tells thorpy to call before_gui() before drawing gui.

#For the sake of brevity, the main loop is replaced here by a shorter but blackbox-like method
player = text.get_updater().launch()
pygame.quit()
