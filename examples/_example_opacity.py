"""
We show here how to change the opacity (alpha value) of an element's background. This is specially useful
if you don't like the default alpha value of some themes.
"""
#tags: transparency, opacity, alpha, set_alpha, set_opacity, set_opacity_bck_color, set_transparency, set_style_attr

import pygame
import thorpy as tp

W, H = 1200, 700
pygame.init()
screen = pygame.display.set_mode((W,H))
tp.init(screen, tp.theme_game2)

#first option : change the color for all the needed elements
# tp.set_style_attr("bck_color", (255,255,255), only_to_cls=[tp.Box, tp.TitleBox])

bck = pygame.image.load(tp.fn("data/bck.jpg"))
bck = pygame.transform.smoothscale(bck, (W,H)) #load some background pic
def before_gui(): #add here the things to do before blitting gui elements
    screen.blit(bck, (0,0)) #blit background pic

box = tp.Box([tp.Button("Button"+str(i+1)) for i in range(10)])
box.sort_children("grid", nx=5, ny=2)
box.center_on(screen)

#second option : change the opacity for a single element (without changing its color)
box.set_opacity_bck_color(255)

#Your main loop here #########################
m = tp.Loop(element=box)
clock = pygame.time.Clock()
while m.playing:
    clock.tick(m.fps)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            m.playing = False
    m.update(before_gui) #just add this line to handle thorpy elements - the rest is yours
    pygame.display.flip()

pygame.quit()

