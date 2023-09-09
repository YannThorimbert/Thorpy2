"""We show here how to create a discrete 'lifebar'. This is useful for displaying and setting infos
about something such as life hearts, stars, etc."""
#tags: DiscreteLifebar, life, hearts, stars
import pygame, thorpy as tp

pygame.init()

W, H = 1200, 700
screen = pygame.display.set_mode((W,H))
tp.init(screen, tp.theme_human) #here we start from 'human' theme as starting point

img_empty = pygame.image.load(tp.fn("data/star_empty_32.png"))
img_full = pygame.image.load(tp.fn("data/star_full_32.png"))

#Do what you want for hover (by default, it will just inflate the base image).
#e.g here, we set the hover images to have yellow color instead of black color on the outline.
#toggle the comments of the next 4 lines to see the default behaviour
img_empty_hover = tp.graphics.change_color_on_img(img_empty, (0,0,0), (255,255,0), (0,0,0))
# img_empty_hover = None
img_full_hover = tp.graphics.change_color_on_img(img_full, (0,0,0), (255,255,0), (0,0,0))
# img_full_hover = None

bar = tp.DiscreteLifebar(img_empty, img_full,
                        n_slots=7,
                        initial_value=3,
                        clickable=True,
                        img_slot_empty_hover=img_empty_hover,
                        img_slot_full_hover=img_full_hover,
                        auto_inflate=(2,2), #x and y inflation of slots at hover
                        gap=20 #the space between slots
                        )

bck = pygame.image.load(tp.fn("data/bck.jpg"))
bck = pygame.transform.smoothscale(bck, (W,H))

def before_gui(): #add here the things to do each frame before blitting gui elements
    screen.blit(bck, (0,0))

#For the sake of brevity, the main loop is replaced here by a shorter but blackbox-like method
player = bar.get_updater().launch(before_gui)
pygame.quit()
