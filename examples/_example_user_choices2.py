"""We show here how to let the user choose among different textual options."""

import pygame, thorpy as tp

pygame.init()

screen = pygame.display.set_mode((800, 400))
tp.init(screen, tp.theme_human) #bind screen to gui elements and set theme

def before_gui(): #add here the things to do each frame before blitting gui elements
    screen.fill((250,)*3)
tp.call_before_gui(before_gui) #tells thorpy to call before_gui() before drawing gui.

def paint_green():
    alert.set_bck_color((0,255,0))
    launcher.set_bck_color((0,255,0))

my_button = tp.Button("Paint things in green")
my_button.at_unclick = paint_green
choices = ("I want A!", "No, I want B.", "Actually, I do not know.", my_button)
more_text = "Okay, tell me what you want."
alert = tp.AlertWithChoices("Some title", choices, more_text, choice_mode="h", overwrite_choices=False)

# laisser la possibilite de boite sans title, ou du moins proposer un style sans les traits à la windows

def my_func():
    alert.launch_alone() #see _example_launch for more options
    print("User has chosen:", alert.choice)

launcher = tp.Button("Click here to make a choice")
launcher.center_on(screen)
launcher.at_unclick = my_func 

#For the sake of brevity, the main loop is replaced here by a shorter but blackbox-like method
player = launcher.get_updater().launch()
pygame.quit()

