"""We show here how to build elements that are made of both an image and a text."""
#tags: image, text, image with text, text with image, TextAndImageButton, image button


import pygame
import thorpy as tp

pygame.init()

W, H = 1200, 700
screen = pygame.display.set_mode((W,H))
tp.init(screen)

my_img = pygame.image.load(tp.fn("data/my_img.png"))
my_img.set_colorkey(my_img.get_at((0,0)))
e = tp.TextAndImageButton("My button", my_img,
                              reverse=False) #reverse=True switches img and txt (left<-->right)
e.center_on(screen)

def refresh_screen():
    screen.fill((255,)*3)

e.get_updater().launch(refresh_screen)
pygame.quit()

