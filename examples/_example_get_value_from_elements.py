"""Elements like sliders, text input, colorpicker and so on store values.
We show here how to interact with element's value."""
#tags: interact, interaction


import pygame, random
import thorpy

pygame.init()
screen = pygame.display.set_mode((1200, 700))
thorpy.init(screen, thorpy.theme_human) #bind screen to gui elements and set theme

#Declare some elements to tune the look of the screen
check = thorpy.Labelled("Black screen:",thorpy.Checkbox(False))
title_color = thorpy.LabelledColorPicker("Title font color:",thorpy.ColorPicker())
title = thorpy.Text("Initial title")
title.set_font_size(40)
title.stick_to(screen, "top", "top")
text_input = thorpy.Labelled("Screen's title:",thorpy.TextInput("", title.get_value()))
slider = thorpy.SliderWithText("Title offset:", -100, 100, 0, "h", 200, edit=True) #slider is labelled by default

def refresh():#some function that you call once per frame
    if check.get_value():
        screen.fill((0,0,0))
    else:
        screen.fill((255,)*3)
    title.set_font_color(title_color.get_value())
    if text_input.get_value(): #change title text if there is one
        title.set_text(text_input.get_value())
    offset = slider.get_value()
    title.stick_to(screen, "top", "top", delta=(offset, 0))

box = thorpy.Box([check,title_color,text_input,slider])
box.center_on(screen)

group = thorpy.Group([box, title], mode=None) #mode=None because we dont want to sort elements
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

