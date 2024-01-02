"""We show here how to use sine wave distortion effect on images."""
#tags: fx, image, distortion, sine, wave, deformation, get_sine_wave_images


import pygame
import thorpy as tp

pygame.init()
W, H = 800,600
screen = pygame.display.set_mode((W, H))
tp.init(screen)

#We load an image and scale it for the demo
my_image = pygame.image.load(tp.fn("data/star_full_32.png"))
my_image = pygame.transform.scale(my_image, (100,100))

#We build a list of images that will be used to animate the deformation
imgs = tp.graphics.get_sine_wave_images(my_image,
                                        amplitude=10, #amplitude of the deformation
                                        step=2) #small step means fine grained deformation

#Now we build an animated image from the list of images
e_img = tp.AnimatedGif(imgs)
e_img.center_on(screen)

def before_gui(): #add here the things to do each frame before blitting gui elements
    screen.fill((0,0,0))
tp.call_before_gui(before_gui) #tells thorpy to call before_gui() before drawing gui.
#For the sake of brevity, the main loop is replaced here by a shorter but blackbox-like method
player = e_img.get_updater().launch()
pygame.quit()