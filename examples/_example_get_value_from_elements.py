"""Elements like sliders, text input, colorpicker and so on store values.
We show here how to interact with element's value."""
#tags: interact, interaction, get_value, set_value

import pygame
import thorpy as tp

pygame.init()
screen = pygame.display.set_mode((1200, 700))
tp.set_default_font(("arialrounded", "arial", "calibri", "century"), font_size=20) 
tp.init(screen, tp.theme_human) #bind screen to gui elements and set theme

#Declare some elements to tune the look of the screen
check = tp.Labelled("Black screen:",tp.Checkbox(False))
title_color = tp.LabelledColorPicker("Title font color:", tp.ColorPicker())
title = tp.Text("Initial title")
title.set_font_size(40)
title.stick_to(screen, "top", "top")
text_input = tp.Labelled("Screen's title:",tp.TextInput("", title.get_value()))
slider = tp.SliderWithText("Title offset:", -100, 100, 0, "h", 200, edit=True) #slider is labelled by default

def refresh():#some function that you call once per frame
    if check.get_value(): #user wants black background
        screen.fill((0,0,0))
    else: #user wants white background
        screen.fill((255,)*3)
    title.set_font_color(title_color.get_value())
    if text_input.get_value(): #change title text if there is one
        title.set_text(text_input.get_value())
    offset = slider.get_value()
    title.stick_to(screen, "top", "top", delta=(offset, 0))
tp.call_before_gui(refresh) #tells thorpy to call before_gui() before drawing gui.

box = tp.Box([check,title_color,text_input,slider])
box.center_on(screen)

group = tp.Group([box, title], mode=None) #mode=None because we dont want to sort elements
m = group.get_updater(fps=40)

while m.playing:
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            m.playing = False
        else:
            ... #do your stuff
    m.update(func_before=refresh, events=events)
    pygame.display.flip()
pygame.quit()

