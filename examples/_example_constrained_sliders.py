"""We show here how to set up a group of sliders such that the sum of their values is constant.
Using this example, you can easily adapt it to any type of constraint on the sliders."""
#tags: slider, constraint, sum
import pygame, thorpy as tp

pygame.init()
W, H = 1200, 700
screen = pygame.display.set_mode((W,H))
tp.init(screen, tp.theme_human) #here we start from 'human' theme as starting point


text = tp.Text("In this example, the sum of the sliders must be 100.")


n = 5 #number of sliders
sliders = [tp.SliderWithText(f"Slider {i}",
                             min_value=1,
                             max_value=100-n+1,
                             initial_value=100/n,
                             length=400) for i in range(n)]

def last_drag():
    for s in sliders:
        if s.get_dragger().being_dragged:
            return s

group = tp.Group([text]+sliders)

def at_refresh(): #add here the things to do each frame before blitting gui elements
    screen.fill((255,255,255))
    last_dragged = last_drag()
    if last_dragged:
        sum_sliders = sum([s.get_value() for s in sliders])
        v = last_dragged.get_value()
        sum_others = sum_sliders - v
        # k * sum_others + v = 100 <==> k = (100-v)/sum_others
        k = (100-v)/sum_others
        for s in sliders:
            if s is not last_dragged:
                s.set_value(round(k*s.get_value()))



#For the sake of brevity, the main loop is replaced here by a shorter but blackbox-like method
player = group.get_updater().launch(at_refresh)
pygame.quit()
