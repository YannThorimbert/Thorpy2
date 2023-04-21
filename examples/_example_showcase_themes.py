"""This code instantiates the most common types of elements one needs when building a GUI. It also
allows the user to browse some of the default themes. See the showcase number 2 to check all the default themes."""
#tags: showcase, Button, SliderWithText, Text, Checkbox, Radio, DropDownListButton, Labelled, ToggleButton, SwitchButtonWithText, SwitchButton, TitleBox, Group

import sys; sys.path.insert(0, "./")
import pygame
import thorpy as tp

pygame.init()
pygame.key.set_repeat(300,50)

# W,H = 1366, 768 #HD
W,H = 1920, 780 #Full HD
screen = pygame.display.set_mode((W,H))

tp.set_default_font("arial", 20)
tp.init(screen)

bck = pygame.image.load(tp.fn("data/bck.jpg")) #load some background pic for testing
bck = pygame.transform.smoothscale(bck, (W,H))
def before_gui(): #add here the things to do each frame before blitting gui elements
    screen.blit(bck, (0,0)) #blit background pic
tp.call_before_gui(before_gui) #tells thorpy to call before_gui() before drawing gui.

#Display an alert to the user about screen resolution to use for this showcase
alert = tp.Alert("Information", """This example is designed to be display on (at least) full HD.
Have a look at showcase example 2 if your resolution is lower than that.""")
alert.launch_alone()

tp.set_waiting_bar("Building elements...")
tp.refresh_waiting_bar()

def get_group(group_name, box_cls="box"):

    button = tp.Button("Standard button")

    text2 = tp.Text("This is a long text written to show how auto multilines texts work.")
    text2.set_font_auto_multilines_width(200)

    ddlb = tp.DropDownListButton(("Camel", "Cat", "Dog", "Goat"), bck_func=before_gui)
    dropdownlist = tp.Labelled("Dropdown:", ddlb)

    check = tp.Labelled("Checkbox:",tp.Checkbox(True))
    radio = tp.Labelled("Radio:",tp.Radio(True))
    text_input = tp.Labelled("Text input:",tp.TextInput("", "Type text here"))
    slider = tp.SliderWithText("Value:", 10, 80, 30, "h", 100, edit=True) #slider is labelled by default
    toggle = tp.ToggleButton("Toggle button", value=False)
    switch = tp.SwitchButtonWithText("Switch:", ("Foo","Bar")) #switch is labelled by default
    
    if box_cls=="group":
        title_box = tp.Group([button, text_input, slider, text2, dropdownlist, check, toggle, radio, switch])
    else:
        title_box = tp.TitleBox(group_name,
            [button, text_input, slider, text2, dropdownlist, check, toggle, radio, switch])

    return title_box

tp.theme_round2()
classic = get_group("Round2")

tp.themes.theme_game2()
game = get_group("Game2")

tp.theme_simple()
simple = get_group("Simple")

tp.theme_human()
human = get_group("Human")

tp.theme_text_dark()
text = get_group("Dark text")

tp.theme_game1()
game1 = get_group("Game1")

bigbrother = tp.Group([human, classic, game1, game, text, simple], "h")

#For the sake of brevity, the main loop is replaced here by a shorter but blackbox-like method
loop = bigbrother.get_updater()
loop.launch(before_gui)

pygame.quit()


