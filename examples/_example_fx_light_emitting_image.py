"""We show here how to make an object emit light"""
#tags: light, fx, light emitter, light emission, lighting, emit light, oscillating light, oscillating, generate_oscillating_lights, image
import pygame, thorpy as tp

from thorpy.graphics import generate_oscillating_lights as gen_lights

pygame.init()
W, H = 800,600
screen = pygame.display.set_mode((W, H))

#load some background pic for testing
bck = pygame.image.load(tp.fn("data/bck.jpg")) 
bck = pygame.transform.smoothscale(bck, (W,H))

#load some pic to enlight
my_img = pygame.image.load(tp.fn("data/my_img.png"))
my_img.set_colorkey(my_img.get_at((0,0)))

#cache lights images - this can take some time
my_img_lights = gen_lights(my_img,
                           n=20, #number of frames
                           inflation=8,
                           radius_amplitude=3,
                           alpha_factor_base=0.1,
                           alpha_factor_amplitude=0.3,
                           color=(255,255,255)
                           )


i_light = 0 #frame number of light image to blit
clock = pygame.time.Clock()
iteration = 0
playing = True

tp.init(screen)

#for convenience, we blit a thorpy Image element so we can drag it,
#but you can handle everything as a pygame Surface as well
e = tp.Image(my_img)
e.set_draggable()
e.set_topleft(50,50)

FPS = 60
player = e.get_updater(FPS)

while playing:
    screen.blit(bck, (0,0))
    # screen.blit(my_img, my_img_rect) #blit base image (instead of e.draw if you want)
    e.draw()
    #get and blit the bright image around
    if iteration % 2 == 0: #choose the speed of the animation
        i_light = (i_light+1)%len(my_img_lights)
    r = my_img_lights[i_light].get_rect(center=e.rect.center)
    # r.center = my_img_rect.center #move base image (instead of e if you want)
    screen.blit(my_img_lights[i_light], r.topleft)

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            playing = False
    ... #your stuff goes here
    pygame.display.flip()
    clock.tick(FPS)
    iteration += 1
    player.update(events=events)

pygame.quit()