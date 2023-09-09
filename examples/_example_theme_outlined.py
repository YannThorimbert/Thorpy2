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

tp.set_default_font("arial", 40)
tp.init(screen, tp.theme_text_outlined)

group = tp.Group([tp.Button("Button "+str(i)) for i in range(1,8)])
group.center_on(screen)

#For the sake of brevity, the main loop is replaced here by a shorter but blackbox-like method
tp.call_before_gui(before_gui) #tells thorpy to call before_gui() before drawing gui.
player = group.get_updater()
player.launch()
pygame.quit()