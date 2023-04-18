"""We show here how to build buttons around a loaded image."""
#tags: image, ImageButton, image button


import sys, pygame, thorpy as tp

pygame.init()

screen = pygame.display.set_mode((1200, 700))
tp.init(screen, tp.theme_human) #bind screen to gui elements and set theme

text = tp.Text("Here we use dummy, Paint-generated\nimages for demonstration.")

#Pure image element(no text)
my_img = pygame.image.load(tp.fn("my_img.png"))
my_img.set_colorkey(my_img.get_at((0,0)))
pure_image = tp.Image(my_img)
pure_image.set_size((20,20))

#Image button (here, with a color variant when hovering)
variant = tp.graphics.change_color_on_img(my_img, my_img.get_at((50,25)), (200,200,255))
variant.set_colorkey(variant.get_at((0,0)))
image_button = tp.ImageButton("Press me!", my_img.copy(), img_hover=variant)

def before_gui(): #add here the things to do each frame before blitting gui elements
    screen.fill((150,150,150))
tp.call_before_gui(before_gui) #tells thorpy to call before_gui() before drawing gui.

group = tp.TitleBox("Example of image elements", [text, pure_image, image_button])
group.center_on(screen)
#For the sake of brevity, the main loop is replaced here by a shorter but blackbox-like method
player = group.get_updater().launch()
pygame.quit()

