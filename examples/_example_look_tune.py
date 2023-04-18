

"""
In this example, we let the user choose a font amongst the available system fonts.
"""

import pygame
import thorpy

pygame.init()
screen = pygame.display.set_mode((1200, 700))
thorpy.init(screen, thorpy.theme_human) #bind screen to gui elements and set theme

button = thorpy.Button("Sample button")
button.set_font_color((0,255,0), states="all")
button.set_font_color((255,0,0), states="hover")
button.set_font_size(30)
button.set_style_attr("radius", button.rect.h//2)
button.set_style_attr("margins", (10,10))
#other parameters : border_color, border_thickness, + some others dependint on the style used


button2 = thorpy.Button("B") #for all the commands below, use refresh=False if performance is critical
button2.set_font_size(30)
button2.set_size((100,100))
button2.set_style_attr("radius",50)
button2.set_font_color((255,255,255), ["hover", "pressed"])
button2.set_bck_color(((255,100,100), (155,0,0), "v"), "hover")
button2.set_bck_color(((155,0,0), (255,100,100), "v"), "pressed")
button2.set_style_attr("offset", (3,3), "pressed")


group = thorpy.Group([button, button2])

def at_refresh():
    screen.fill((255,)*3)

group.get_updater().launch(at_refresh)
pygame.quit()