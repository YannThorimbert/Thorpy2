"""Inspired by FluffyPotatoe's example on youtube, but improved blurry lights"""
#tags: light, light emitter, light emission, lighting, emit light, particle, particles, oscillating light, oscillating, generate_oscillating_lights, image


import pygame, sys, random
from thorpy.graphics import generate_oscillating_lights as gen_lights

pygame.init()
W, H = 800,600
screen = pygame.display.set_mode((W, H))

#load some background pic for testing
bck = pygame.image.load(tp.fn("bck.jpg")) 
bck = pygame.transform.smoothscale(bck, (W,H))

#particles parameters
MAX_RADIUS = 10
RADIUS_FACTOR = 2
RADIUS_DECAY = MAX_RADIUS / 200
LIGHT_COLOR = (20, 20, 60)
N = RADIUS_FACTOR*MAX_RADIUS


def circle_transp_bck(radius, color):
    surf = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((0, 0, 0))
    return surf

def draw_light_particle(particle):
    pygame.draw.circle(screen,
                        (255, 255, 255),
                        [int(particle[0][0]), int(particle[0][1])],
                        int(particle[2]))
    radius = particle[2] * RADIUS_FACTOR
    
    c = circle_transp_bck(radius, LIGHT_COLOR)
    r = c.get_rect()
    r.center = particle[0]
    #Fluffy Potatoe version: ############################################
    # screen.blit(c, r.topleft, special_flags=pygame.BLEND_RGB_ADD)
    #Thorpy version: ####################################################
    light = surfaces_light[int(radius)]
    rlight = light.get_rect()
    rlight.center = r.center
    screen.blit(light, rlight.topleft)

def generate_and_update_particles():
    #generate new particles
    particles.append([list(pygame.mouse.get_pos()), #pos
                      [1.3*(random.random()*2 - 1), -4], #vel
                      random.randint(MAX_RADIUS//2, MAX_RADIUS)]) #radius
    #update particles
    for particle in particles:
        particle[0][0] += particle[1][0] #update x
        particle[0][1] += particle[1][1] #update y
        particle[2] -= RADIUS_DECAY #reduce radius as time goes by
        particle[1][1] += 0.1 #gravity (update vy)
        draw_light_particle(particle)
        if particle[2] <= 0: #remove particle with negative or zero size
            particles.remove(particle)

#put lights in cache (can take some time)
surfaces_light = []
for i in range(N+1):
    img = circle_transp_bck(i, LIGHT_COLOR)
    img_light = gen_lights(img,
                           n=1, #number of frames
                           inflation=0,
                           radius_amplitude=3,
                           alpha_factor_base=0.9*i/N + 0.1,
                           alpha_factor_amplitude=0.,
                           color=(255,255,255)
                           )[0]
    surfaces_light.append(img_light)


particles = []
clock = pygame.time.Clock()
playing = True
while playing:
    screen.blit(bck, (0,0))
    generate_and_update_particles()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
    ... #your stuff goes here
    pygame.display.flip()
    clock.tick(60)

pygame.quit()