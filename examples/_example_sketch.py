"""Example of a sketch box that allows to draw on a grid with a color picker."""
#tags: drawing, sketch, colorpicker, grid, bucket

import pygame, thorpy as tp

pygame.init()

screen = pygame.display.set_mode((1200, 700))
tp.init(screen, tp.theme_human) #bind screen to gui elements and set theme

def before_gui(): #add here the things to do each frame before blitting gui elements
    screen.fill((250,)*3)

colorpicker = tp.ColorPickerPredefined(colors=[(255,0,0),(0,255,0),(0,0,255),(50,50,50)], mode="h")
# colorpicker = tp.ColorPicker() #See the examples about colorpicker
# colorpicker = tp.ColorPickerRGB() #See the examples about colorpicker
# colorpicker = (0,0,255) #if you pass a tuple, only this color will be available

sketch = tp.Sketch(size=(300,300), #size of the sketch image
                   cells_size=(20,20), #size of the cells of the grid
                   title="Draw your logo", #title of the sketch Box
                   bck_color=(255,255,255), #background color of the sketch
                   colorpicker=colorpicker, #see above for the different options
                   show_grid_text="Show grid", #set empty string if you want to disable grid option
                   bucket_text="Bucket" #set empty string if you want to disable bucket fill option
                   )
sketch.center_on(screen)
# sketch.set_show_grid(True) #set initial value

player = sketch.get_updater(fps=30)

tp.call_before_gui(before_gui) #tells thorpy to call before_gui() before drawing gui.
#For the sake of brevity, the main loop is replaced here by a shorter but blackbox-like method
player.launch()
pygame.quit()

