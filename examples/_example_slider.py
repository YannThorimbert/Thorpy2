"""We show here many different ways to customize sliders behaviour."""
#tags: slider, SliderWithText, Group

import pygame, thorpy as tp

pygame.init()

screen = pygame.display.set_mode((1200, 700))
tp.init(screen, tp.theme_human) #bind screen to gui elements and set theme


# Sliders with no text
slider0 = tp.Slider("h", 200) #most simple slider : just indicate mode and length
slider1 = tp.Slider(mode="h", length=200,
                        thickness=16, dragger_length=16, dragger_height=16,
                        set_when_click=True) #whether user can click a point in the slider range

# Sliders with text and more options
slider3 = tp.SliderWithText("How old are you ?", 18, 77, 25, 200)
slider4 = tp.SliderWithText("How many games should we play ?",
                                1, 10, 3, #min, max and initial values
                                50, "h", #length and orientation
                                dragger_size=(10,20),
                                show_value_on_right_side=True,
                                edit=True) #allow to edit value as a text
slider5 = tp.SliderWithText("Fine tune some number\n(from -2 to 2)", -2, 2, 1.5, 200,
                                round_decimals=3) #by default, 2 decimals
                                

group = tp.Group([slider0, slider1, slider3, slider4, slider5])

def before_gui(): #add here the things to do each frame before blitting gui elements
    screen.fill((155,155,155))
#For the sake of brevity, the main loop is replaced here by a shorter but blackbox-like method
player = group.get_updater().launch(before_gui)
pygame.quit()

