"""
Text outliner is useful for drawing texts on top of changing background colors.
Any method appliable to stantard Text objects is also appliable to Outlined texts.
Just check Text examples for more.
The graphical text outlining method found here is borrowed from pgzero library.
"""
#tags: outline, outlined, OutlinedText, set_font_rich_text_tag, advanced styling, rich text, rich, text, color text, color, text style, text styling, align, set_font_auto_multilines_width, set_style_attr

import pygame
import thorpy as tp

pygame.init()

W, H = 1200, 700
screen = pygame.display.set_mode((W,H))
bck = pygame.image.load(tp.fn("data/bck.jpg"))
bck = pygame.transform.smoothscale(bck, (W,H)) #load some background pic
def before_gui(): #add here the things to do before blitting gui elements
    screen.blit(bck, (0,0)) #blit background pic

tp.init(screen, tp.theme_classic)

my_text = tp.OutlinedText("Blah blah\nblah",
                          font_size=50, #defaults to theme's font_size
                          font_color=(250,250,250), #defaults to theme's font_color
                          outline_color=(50,50,50), #defaults to (50,50,50)
                          outline_thickness=2) #defaults to 2
my_text.center_on(screen)

#if you want to change the outline color dynamically:
# my_text.set_style_attr("outline_color", (255,0,0))

#if you want to change the outline thickness dynamically:
# my_text.set_style_attr("outline_thickness", 3)

#For the sake of brevity, the main loop is replaced here by a shorter but blackbox-like method
tp.call_before_gui(before_gui) #tells thorpy to call before_gui() before drawing gui.
player = my_text.get_updater()
player.launch()
pygame.quit()