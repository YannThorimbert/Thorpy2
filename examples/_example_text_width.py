"""We show here several methods to impose a maximum text width to an element."""
#tags: text width, text, max text width, font_auto_multilines_width, set_max_text_width, set_size

import pygame
import thorpy as tp

pygame.init()

W, H = 1200, 700
screen = pygame.display.set_mode((W,H))
bck = pygame.image.load(tp.fn("data/bck.jpg"))
bck = pygame.transform.smoothscale(bck, (W,H)) #load some background pic
def before_gui(): #add here the things to do before blitting gui elements
    screen.blit(bck, (0,0)) #blit background pic

tp.set_screen(screen) #bind screen to gui elements
tp.themes.theme_classic() #specify style theme for gui elements

some_long_text = "Hello, world. This is a long text that I wrote for the demo. "*8


#let's replace the \n inserted in the str above. Note that you can manually place line breaks, but
#   we do remove them here as we want to illustrate auto line break only.
some_long_text = some_long_text.replace("\n", " ")

#Method 1 : set the max width for all the elements sharing the same style.
#   Choose this method if you want this behaviour to be also applied to other objects
##for style in tp.Button.iter_styles():
##    style.font_auto_multilines_width = 200
##my_button = tp.Button(some_long_text)

#Method 2: refresh the element's surfaces with new max width
#   Choose this method if you think performance is not an issue (most probable)
##my_button = tp.Button(some_long_text)
##my_button.set_max_text_width(200)

#Method 3: set the max width before generating element's surfaces
#   Choose this method if you think performance is critical when generating the element.
my_button = tp.Button(some_long_text, generate_surfaces=False)
my_button.set_max_text_width(150)

#Method 4: externally handle the text before feeding the element's constructor
#   Choose this method if you think performance is critical when generating the element.
#   Note that in this case, you have to manually take element's inside margin into account.
##text = tp.Button.style_normal.insert_auto_breakline(some_long_text, 200)
##my_button = tp.Button(text)

##my_button.set_size((150,300))

##my_button.set_text("This is short again", max_width=None) #erase max_width constraint

my_button.center_on(screen)

t = tp.Text("See how the text can adapt to the width constraint.")
t.stick_to(my_button, "bottom", "top")
my_button.add_child(t)

m = tp.Loop(element=my_button)
clock = pygame.time.Clock()
while m.playing:
    clock.tick(m.fps)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            m.playing = False
    m.update(before_gui)
    my_button.set_size((min(W-20,my_button.rect.w+1),my_button.get_text_size()[1]), adapt_text=True)
    pygame.display.flip()

pygame.quit()

