from math import tan, pi
from pygame import Surface
from pygame.transform import rotate, flip, scale

from . import graphics
from . import parameters as p



SUN_ANGLE = 45.
SHADOW_RADIUS = 2
SHADOW_COLOR = (0, 0, 0)
BLACK = 255
ALPHA_FACTOR = 0.55
DECAY_MODE = "exponential"
ANGLE_MODE = "flip" #flip or rotate
MODE_VALUE = (False, False)
##ANGLE_MODE = "rotate"
##MODE_VALUE = 90.
TARGET_ALTITUDE = 0.
OFFSET = (9,9)
VERTICAL = True


class Shadow:

    def __init__(self):
        self.sun_angle = SUN_ANGLE
        self.shadow_radius = SHADOW_RADIUS
        self.black = BLACK
        self.alpha_factor = ALPHA_FACTOR
        self.decay_mode = DECAY_MODE
        self.angle_mode = ANGLE_MODE
        self.mode_value = MODE_VALUE
        self.target_altitude = TARGET_ALTITUDE
        self.offset = OFFSET
        self.vertical = VERTICAL #rpg style : vertical=True
        self.color = SHADOW_COLOR


    def generate_image(self, target_img):
        r = target_img.get_rect()
        #the shadow will be larger in order to make free space for fadeout.
        r.inflate_ip(2*self.shadow_radius, 2*self.shadow_radius)
        img = Surface(r.size)
        img.fill((255, 255, 255, 255))
##        img.fill((0, 0, 0, 0))
        img.blit(target_img, (self.shadow_radius, self.shadow_radius))
        if self.sun_angle <= 0.:
            raise Exception("Sun angle must be greater than zero.")
        elif self.sun_angle != 45. and self.vertical:
            w, h = img.get_size()
            new_h = h / tan(self.sun_angle * pi / 180.)
##            screen_size = functions.get_screen().get_size()
##            new_h = abs(int(min(new_h, max(screen_size))))
            img = scale(img, (w, new_h))
        if self.angle_mode == "flip":
            img = flip(img, self.mode_value[0], self.mode_value[1])
        elif self.angle_mode == "rotate":
            img = rotate(img, self.mode_value)
        else:
            raise Exception("angle_mode not available: " + str(self.angle_mode))
        shadow = graphics.get_shadow(img,
                                        radius=self.shadow_radius,
                                        black=self.black,
                                        alpha_factor=self.alpha_factor,
                                        decay_mode=self.decay_mode,
                                        color=self.color)
        return shadow


class UniformRectShadow(Shadow):

    def generate_image(self, target_img):
        shadow = Surface(target_img.get_size())
        if self.color != (0,0,0):
            shadow.fill(self.color)
        shadow.set_alpha(self.alpha_factor*255)
        return shadow


class NonUniformRectShadow(Shadow):

    def __init__(self):
        Shadow.__init__(self)
        self.shadow_radius = 8
        self.color = (0,0,0,ALPHA_FACTOR*255)

    
    def generate_image(self, target_img):
        return graphics.generate_non_uniform_rect_shadow(target_img.get_size(),
                                                         self.color,
                                                         self.alpha_factor,
                                                         self.shadow_radius)


def propose_shadowgen(style, fast, uniform=False):
    # if fast or (hasattr(style, "radius") and style.radius == 0):
    if fast:
        if uniform:
            return UniformRectShadow()
        else:
            return NonUniformRectShadow()
    else:
        return Shadow()
    

def auto_set_fast(element, fast):
    if fast == "auto":
        return element.rect.w * element.rect.h > p.auto_shadow_threshold
    return fast
    