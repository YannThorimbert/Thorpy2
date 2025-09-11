
"""We show here how to set up a group of sliders such that the sum of their values is constant.
Using this example, you can easily adapt it to any type of constraint on the sliders."""
#tags: slider, constraint, sum
import pygame, thorpy as tp

pygame.init()
W, H = 1200, 700
screen = pygame.display.set_mode((W,H))
tp.init(screen, tp.theme_human) #here we start from 'human' theme as starting point

tp.Alert("Not implemented", "This feature is in development. Please wait for the next version.").launch_alone()
exit()

class SelectionRectSurface(tp.DeadButton):
    def __init__(self, size="auto", color=(0,0,0,0)):
        if size == "auto":
            size = screen.get_size()
        style = tp.styles.SimpleStyle()
        style.bck_color = color
        style.size = size
        tp.DeadButton.__init__(self, "", style)
        self.last_click = None
        self.selection_rect = pygame.Rect(0,0,0,0)

    def default_at_click(self, ):
        self.last_click = pygame.mouse.get_pos()

    def default_at_unclick(self):
        return super().default_at_unclick()

s = SelectionRectSurface(size=screen.get_size(), color=(0,0,0,0))

group = tp.Group([s])

def at_refresh(): #add here the things to do each frame before blitting gui elements
    screen.fill((255,255,255))

#For the sake of brevity, the main loop is replaced here by a shorter but blackbox-like method
player = group.get_updater().launch(at_refresh)
pygame.quit()
