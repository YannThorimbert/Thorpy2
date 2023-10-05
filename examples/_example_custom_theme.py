"""In this example we show how to customize GUI style from a default theme."""
#tags: style, styling, advanced styling, default, default style, set default style, mystyle, assign style, theme, customize theme, set_style_attr, set_default_font
import pygame
import thorpy as tp

pygame.init()

W, H = 1200, 700
screen = pygame.display.set_mode((W,H))

tp.set_default_font(["PressStart2P-Regular.ttf", "arial"], 20) #must come before init
tp.init(screen, tp.theme_human) #here we start from 'human' theme as starting point

#set elements radius to 40% of their own height, except for boxes
tp.set_style_attr("radius", 0.4, exceptions_cls=[tp.Box])

#set elements background as a color gradient
new_color = ((100,100,255), (220,220,220), "h") #(from, to, 'h' 'v', 'r'(radial) or 'q'(square))
tp.set_style_attr("bck_color", new_color, exceptions_cls=[tp.Box, tp.Text])
new_color_pressed = ((220,220,220), (100,100,255) , "h")
tp.set_style_attr("bck_color", new_color_pressed, "pressed", exceptions_cls=[tp.Box, tp.Text])

#customize TitleBox properties
# tp.Box.style_normal.bck_color = (255,255,255)
tp.TitleBox.style_normal.bck_color = (100,100,255,127) # type: ignore
tp.TitleBox.style_normal.radius = 10 # type: ignore
tp.TitleBox.style_normal.bottom_line = False # type: ignore
tp.TitleBox.style_normal.left_line = False # type: ignore
tp.TitleBox.style_normal.right_line = False # type: ignore


elements = [tp.Text("Hello, world.\nHere is some text."),
            tp.Button("Test"),
            tp.Box([tp.Button("Button"+str(i)) for i in range(5)]),
            tp.Box([tp.SliderWithText("Choose value", 20, 120, 50, length=120, dragger_size=(20,20))])]


grp = tp.TitleBox("Hello, world", children=elements)
grp.center_on(screen)

bck = pygame.image.load(tp.fn("data/bck.jpg")) #load some background pic for testing
bck = pygame.transform.smoothscale(bck, (W,H))
def before_gui(): #add here the things to do each frame before blitting gui elements
    screen.blit(bck, (0,0)) #blit background pic
tp.call_before_gui(before_gui) #tells thorpy to call before_gui() before drawing gui.

#For the sake of brevity, the main loop is replaced here by a shorter but blackbox-like method
player = grp.get_updater().launch()
pygame.quit()

