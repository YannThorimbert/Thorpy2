"""In this example are shown 3 possibilities of launching new elements in an app
that already contains other, previously defined elements. This typically covers
the case when an alert pops, asking the user to choose between different options.

Here are the 3 ways such a new element can be integrated :
    1) alone (i.e. the other elements are frozen and aren't shown, until the new element is closed)
    2) blocking (i.e. the others elements are frozen but are shown, until the new element is closed)
    3) non-blocking (i.e. the new element is integrated to the current menu and will be removed when closed)
"""
#tags: pop, events handling, alert, set_draggable, pop alert, launch, launch menu, launch alert, pop up, pop-up, launch_nonblocking, launch_alone, launch_and_lock_others

import math
import pygame
import thorpy as tp

pygame.init()

W, H = 1200, 700
screen = pygame.display.set_mode((W,H))
tp.init(screen, tp.theme_round)

my_button = tp.Button("Click me to pop an alert")
my_button.center_on(screen)

my_box = tp.Alert("Some random menu", "Some random text.\nYep...")
my_box.set_topleft(50,50) #choose some absolute location
#customize a bit my_box, so that the gui refresh involves some job in background
my_box.set_draggable()
my_box.generate_shadow(fast=False)

def blit_before_gui(): #add here the things to do each frame before blitting gui elements
    blue = 127 + math.sin(iteration*math.pi*0.5/loop.fps) * 127
    gradient = tp.graphics.color_gradient(((0,0,blue), (255,255,255)), (W,H), "v")
    screen.blit(gradient, (0,0))

#1) first way to achieve alert popping
def launch_some_menu_alone(): #pop the element alone (hide the others)
    my_box.launch_alone(func_before=blit_before_gui)

#2) second way to achieve alert popping
def launch_some_menu_blocking(): #launch blocking but showing the others as locked
    my_box.launch_and_lock_others(my_button, func_before=blit_before_gui)

#3) third way to achieve alert popping
def launch_some_menu_nonblocking(): #integrate the element to existing ones
    my_box.launch_nonblocking()

# my_button.at_unclick = launch_some_menu_alone
# my_button.at_unclick = launch_some_menu_blocking
my_button.at_unclick = launch_some_menu_nonblocking

#The following structure wraps many non-interesting stuff for you.
loop = my_button.get_updater(fps=60)

#write your own loop, do what you want, just update the loop to refresh gui.
clock = pygame.time.Clock()
iteration = 0
while loop.playing:
    clock.tick(loop.fps)
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            loop.playing = False
        else:
            ... #do what you want, it's your code
    ... #do what you want, it's your code
    loop.update(blit_before_gui, events=events) #refresh gui
    pygame.display.flip()
    #if you increment iteration inside blit_before_gui,
    # then screen color will update even inside blocking calls.
    iteration += 1 

pygame.quit()

