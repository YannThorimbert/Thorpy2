"""We show here how to utilise color gradient graphics from Thorpy.
"""
#tags: color, color gradient, fx, color transition, color_rect, gradient

import math
import pygame
import thorpy as tp

pygame.init()

FPS = 60
W, H = 800, 600
screen = pygame.display.set_mode((W,H))
tp.init(screen, tp.theme_round)

button = tp.Text("Color-gradient demonstration")
button.center_on(screen)

iteration = 0
def blit_before_gui(): #add here the things to do each frame before blitting gui elements
    global iteration
    screen.fill((255,255,255))
    blue = 127 + math.sin(iteration*math.pi*2./FPS) * 127
    gradient = tp.graphics.color_rect(((blue,blue,255), (255,255,255), "v"), (W,H))
    screen.blit(gradient, (0,0))
    iteration += 1
tp.call_before_gui(blit_before_gui)

button.get_updater(fps=FPS).launch(blit_before_gui)

pygame.quit()

