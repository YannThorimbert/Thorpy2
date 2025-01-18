"""We show here how to draw a dashed line. You can choose the dash length and the anti-aliasing, as well as the thickness of the line."""
#tags: dashed, line, thickness, anti-aliasing
import pygame, thorpy as tp

pygame.init()
W, H = 1200, 700
screen = pygame.display.set_mode((W,H))
tp.init(screen, tp.theme_human) #here we start from 'human' theme as starting point


text = tp.Text("Dashed line example")
text.center_on(screen)

def at_refresh(): #add here the things to do each frame before blitting gui elements
    screen.fill((255,255,255))
    # tp.graphics.draw_dashed_line(screen, (0,0), (W,H), (0,0,0), 5, 5)
    tp.graphics.draw_dashed_line(screen, color=(255,0,0),
                                 start=text.rect.center,
                                 end=pygame.mouse.get_pos(),
                                 dash_length=20,
                                 aa=True, #anti-aliasing
                                 thickness=1) #if greater than 1, the anti-aliasing is disabled

#For the sake of brevity, the main loop is replaced here by a shorter but blackbox-like method
player = text.get_updater().launch(at_refresh)
pygame.quit()
