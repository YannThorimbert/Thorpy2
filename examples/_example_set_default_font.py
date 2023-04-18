"""We show here how to apply a given font as the default one"""
#tags: set_default_font, font, fontname, fontnames, fonts, list of fonts, default font, set_font_name, set_font_size

import pygame, thorpy as tp

pygame.init()

#You can pass a sequence of desired fonts. The first one matching the avalaible
# fonts for user will be chosen.
tp.set_default_font(("arialrounded", "arial", "calibri", "century"), 
                    font_size=20) 

screen = pygame.display.set_mode((1200, 700))
tp.init(screen, tp.theme_human) #must come after set_default_font

my_button = tp.Button("First button")

my_button2 = tp.Button("Second button with a different font")
my_button2.set_font_name("timesnewroman") #lets suppose we want a different font just for thine one.
my_button2.set_font_size(15)

my_button3 = tp.Button("Third button")

def before_gui(): #add here the things to do each frame before blitting gui elements
    screen.fill((250,)*3)
tp.call_before_gui(before_gui) #tells thorpy to call before_gui() before drawing gui.

my_group = tp.Group([my_button, my_button2, my_button3])

#For the sake of brevity, the main loop is replaced here by a shorter but blackbox-like method
player = my_group.get_updater().launch()
pygame.quit()

