"""Here is shown fine tuning of ColorPicker's appearance and behaviour"""

import pygame, thorpy as tp

pygame.init()

screen = pygame.display.set_mode((1200, 700))
tp.init(screen, tp.theme_human) #bind screen to gui elements and set theme

picker = tp.ColorPicker(mode="google", #google, red, green, blue
                            initial_value=(50,127,255), #approx initial color
                            slider_align="v", #h or v
                            show_rgb_code=False,
                            length=300, height=200,
                            colorbar_length=200,
                            colorframe_size=(90,90),
                            thickness=None) #thickness of the colorbar
picker.visor.set_size((20,20), adapt_parent=False)

# picker = tp.ColorPickerRGB(initial_value=(50,127,255),
#                                 slider_align="h", #h or v
#                                 show_rgb_code=False,
#                                 length=256, #length of RGB sliders
#                                 colorframe_size = (100,100))

# picker = tp.ColorPickerPredefined(colors=None, #here you can give a list of colors (3-tuples)
#                                       mode="grid", #grid, h or v
#                                       nx="auto", ny="auto", #number of cols and lines, if mode is grid
#                                       col_size=(30,30), #size of each color button
#                                       init_color_index=-1, #initial default value
#                                       #The two options below generates a discrete set of colors.
#                                       #if you use one of them, then use None for the other one
#                                       auto_cols_steps=None, #number of steps for each prime color
#                                       manual_cols_step=63) #tones step size for each prime color



picker.center_on(screen)
def before_gui(): #add here the things to do each frame before blitting gui elements
    screen.fill((155,155,155))
tp.call_before_gui(before_gui) #tells thorpy to call before_gui() before drawing gui.
#For the sake of brevity, user loop is replaced here by a shorter but blackbox-like method
player = picker.get_updater().launch()
pygame.quit()

