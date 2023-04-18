"""Minimalistic example : we declare a button and put in the center of the screen."""
#tags: button, hello world, helloworld, center, centering, click, simple

import pygame
import thorpy as tp

pygame.init()

screen = pygame.display.set_mode((1200, 700))
tp.init(screen) #bind screen to gui elements and set theme

my_button = tp.Button("Hello, world.\nThis button uses the default theme.")
my_button.center_on(screen)

def before_gui(): #add here the things to do each frame before blitting gui elements
    screen.fill((250,)*3)
tp.call_before_gui(before_gui) #tells thorpy to call before_gui() before drawing gui.

#For the sake of brevity, the main loop is replaced here by a shorter but blackbox-like method
player = my_button.get_updater().launch()
pygame.quit()
