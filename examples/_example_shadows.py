"""We show here how to generate and binds a shadow to an element."""
#tags: shadow, shadows, shadowgen, shadow generator, generate_shadow, generate shadow, set_draggable

import sys, pygame, thorpy as tp

pygame.init()

screen = pygame.display.set_mode((1200, 700))
tp.init(screen, tp.theme_classic) #bind screen to gui elements and set theme

text = tp.Text("Here we use a dummy, Paint-generated\nimage for demonstration. "+\
                   "Try to move the elements below.")
text.set_max_text_width(400)

#Pure image element(no text)
my_img = pygame.image.load(tp.fn("data/my_img.png"))
my_img.set_colorkey(my_img.get_at((0,0)))

cloud1 = tp.Image(my_img)
cloud1.set_draggable(True, True)
cloud1.generate_shadow(fast=False) #automatic shadow generated from the exact shape of the content


s = tp.shadows.Shadow()
s.sun_angle = 30
s.shadow_radius = 10
s.alpha_factor = 0.8
s.decay_mode = "exponential" #or quadratic
s.angle_mode = "flip"
s.mode_value = (False, True) #y-flip only
# s.angle_mode = "rotate"
# s.mode_value = 30
s.offset = (10,10) #offset from the children
s.vertical = True
cloud2 = tp.Image(my_img)
cloud2.set_draggable(True, True)
cloud2.generate_shadow(shadowgen=s)

s.shadow_radius = 2
s.mode_value = (False, False)
some_text = tp.Text("Hello, world")
some_text.generate_shadow(shadowgen=s)
some_text.set_draggable(True, True)


box = tp.TitleBox("Some demo box", [tp.Text("In this case, fast=True\nmay be well suited.")])
box.set_draggable(True, True)
box.generate_shadow(fast=True)


def before_gui(): #add here the things to do each frame before blitting gui elements
    screen.fill((150,150,150))
tp.call_before_gui(before_gui) #tells thorpy to call before_gui() before drawing gui.

group = tp.TitleBox("Example of automatic shadow generation", [text, box, cloud1, cloud2, some_text])
# group.set_size((500,500))
group.sort_children(gap=50)
group.center_on(screen)
#For the sake of brevity, the main loop is replaced here by a shorter but blackbox-like method
player = group.get_updater().launch()
pygame.quit()

