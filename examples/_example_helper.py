"""We show here how to set up a helper (or hint) that is displayed to the user when an element is hovered
for a given amount of time"""
#tags: help, hint, events handling, display help, display hint, trigger help, launch help, helper

import pygame, thorpy as tp

pygame.init()

screen = pygame.display.set_mode((1200, 700))
tp.init(screen, tp.theme_human) #bind screen to gui elements and set theme

my_button = tp.Button("Hello, world.")
my_button.center_on(screen)

#simple helper
my_helper = tp.Helper("Hint : click on the button to make it pressed. Yep.", my_button)
#customized helper
# my_helper = tp.Helper("Hint : click on the button to make it pressed. Yep.", #content of the helper
#                       my_button, #parent that triggers the help
#                       countdown=10, #number of frames before popping help when parent hovered
#                       generate_shadow=(True, "auto"), #[0] : does generate shadow ? [1] : fast method or accurate method ? you can set [1] = "auto"
#                       offset=(0,0), #offset of the helper compared to mouse_pos
#                       max_width=150) #maximum width of the helper (helper is always clamped to screen)

def before_gui(): #add here the things to do each frame before blitting gui elements
    screen.fill((250,)*3)
tp.call_before_gui(before_gui) #tells thorpy to call before_gui() before drawing gui.

#For the sake of brevity, the main loop is replaced here by a shorter but blackbox-like method
player = my_button.get_updater().launch()
pygame.quit()
