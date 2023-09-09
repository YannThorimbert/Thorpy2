"""We show here how to create a discrete 'lifebar'. This is useful for displaying and setting infos
about something such as life hearts, stars, etc.
See the fine tuned version of this example for more details."""
#tags: DiscreteLifebar, life, hearts, stars
import pygame, thorpy as tp

pygame.init()
W, H = 1200, 700
screen = pygame.display.set_mode((W,H))
tp.init(screen, tp.theme_human) #here we start from 'human' theme as starting point

#choose your images
img_empty = pygame.image.load(tp.fn("data/heart_empty_32.png"))
img_full = pygame.image.load(tp.fn("data/heart_full_32.png"))
dlb = tp.DiscreteLifebar(img_empty, img_full, n_slots=5, initial_value=3)

def before_gui(): #add here the things to do each frame before blitting gui elements
    screen.fill((255,255,255))

#For the sake of brevity, the main loop is replaced here by a shorter but blackbox-like method
player = dlb.get_updater().launch(before_gui)
pygame.quit()
