"""We show here 3 methods to let the user select a RGB color.
See example colorpicker fine tuning for fine tuning options."""
#tags: colorpicker, color, picker, RGB, ColorPickerRGB, ColorPickerPredefined, LabelledColorPicker, Group

import pygame, thorpy as tp

pygame.init()

screen = pygame.display.set_mode((1200, 700))
tp.init(screen, tp.theme_simple) #bind screen to gui elements and set theme

#TODO invalid for game1
e1 = tp.LabelledColorPicker("Google-like", tp.ColorPicker())
e2 = tp.LabelledColorPicker("RGB style", tp.ColorPickerRGB())
e3 = tp.LabelledColorPicker("Discrete set", tp.ColorPickerPredefined(auto_cols_steps=4))
my_colors = [(255,0,0), (255,100,100), (255,200,200), (0,0,255), (0,255,0)]
e4 = tp.LabelledColorPicker("Predefined", tp.ColorPickerPredefined(my_colors, mode="h")) 


group = tp.Group([e1,e2,e3,e4])

def before_gui(): #add here the things to do each frame before blitting gui elements
    screen.fill((200,)*3)
tp.call_before_gui(before_gui) #tells thorpy to call before_gui() before drawing gui.
#For the sake of brevity, the main loop is replaced here by a shorter but blackbox-like method
player = group.get_updater().launch()
pygame.quit()

