
"""We show here how to extend a Style class to create a custom one and use it for a given element only."""
#tags: style, styling, default, default style, set default style, mystyle, assign style, set_style_attr

import pygame, math, thorpy as tp

pygame.init()

screen = pygame.display.set_mode((1200, 700))
tp.init(screen, tp.theme_human) #bind screen to gui elements and set theme

#In this style, we will simply make a blinking red background
class MyStyle1(tp.styles.SimpleStyle):

    def __init__(self):
        super().__init__()
        self.nframes = 30
        self.frame_mod = 1

    def generate_images(self, text, arrow=False):
        """Here, we generate the frames of the blinking element.
        We simply generate the images as a 'standard' SimpleFrame,
        except we slightly adjust the color properties for each frame."""
        surfaces = []
        for i in range(self.nframes):
            self.bck_color = (200 + 55 * math.sin(i*math.pi/self.nframes),0,0)
            self.font_color = (255-self.bck_color[0],)*3
            surfaces += tp.styles.SimpleStyle.generate_images(self, text, arrow)
        return surfaces

#here we will go from a lower level to make polygonal frame for buttons
class MyStyle2(tp.styles.TextStyle):
    bck_color = (90,90,150)
    font_color = (0,0,0)
    margins = (16,16)

    def __init__(self):
        super().__init__()
        self.thickness = 1
        self.border_color = (0,0,0)
        
    def generate_images(self, text, arrow=False):
        bck_color = self.bck_color
        self.bck_color = (0,0,0,0)
        surface = tp.styles.TextStyle.generate_images(self, text, arrow)[0]
        self.bck_color = bck_color
        w,h = surface.get_size()
        mx, my = self.margins
        t = self.thickness
        points = (0, my), (mx,0), (w-t,0), (w-t,h-my), (w-mx, h-t), (0,h-t)
        pygame.draw.polygon(surface, self.bck_color[0:3], points)
        pygame.draw.polygon(surface, self.border_color, points, t)
        self.reblit_text(surface, text, arrow)
        return [surface]
    
    def copy(self):
        c =  super().copy()
        c.thickness = self.thickness
        c.border_color = self.border_color
        return c
    


style_normal = MyStyle1()
my_button1 = tp.Button("Hello, world.\nThis is a useless button.",
                          style_normal=style_normal,
                          all_styles_as_normal=True)
my_button1.set_style_attr("font_color", (0,255,0), "hover")
my_button1.set_style_attr("border_color", (0,255,0), "hover")


style_normal = MyStyle2()
my_button2 = tp.Button("Hello, world.\nThis is a useless button.",
                          style_normal=style_normal,
                          all_styles_as_normal=True)
my_button2.set_style_attr("font_color", (0,255,0), "hover")
my_button2.set_style_attr("border_color", (0,255,0), "hover")
my_button2.generate_shadow(fast=False)


def before_gui(): #add here the things to do each frame before blitting gui elements
    screen.fill((250,)*3)
tp.call_before_gui(before_gui) #tells thorpy to call before_gui() before drawing gui.

group = tp.Group([my_button1, my_button2], gap=50)

#For the sake of brevity, the main loop is replaced here by a shorter but blackbox-like method
player = group.get_updater().launch()
pygame.quit()

