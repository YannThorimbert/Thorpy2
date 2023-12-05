"""
Module regrouping some functions for image processing.
Some of the functions make use of Python Imaging Library and NumPy.
"""
from typing import Union, Sequence, cast, Any, Dict
import math
import numpy as np
from PIL import Image, ImageFilter
PILimage = Image.Image

from .thorpytypehints import *

import pygame
import pygame.surfarray as surfarray
from pygame.image import tostring, fromstring
from pygame import Surface, SRCALPHA
import pygame.gfxdraw as gfx

from functools import cache

MAX_NORM = 3*(255**2)


def darken_or_enlighten(color:RGB_OR_RGBA, factor:float=0.8, also_alpha:bool=False, min_value=20)->RGB_OR_RGBA:
    """Returns either a darkened or enlightened version of the color.
    Refer to darken( ) and enlighten( ) functions for the explanation of the parameters."""
    if factor < 1:
        return darken(color, factor, also_alpha)
    return enlighten(color, factor, min_value, also_alpha)

def darken(color:RGB_OR_RGBA, factor:float=0.8, also_alpha:bool=False)->RGB_OR_RGBA:
    """Returns a darkened version of the color.
    ***Mandatory arguments***
    <color> : 3-tuple or 4-tuple color.
    ***Optional arguments***
    <factor> : (float) how much of the color we want to keep. E.g. 0.8 means we want
    to keep only 80% of the original color.
    also_alpha : (bool) specify whether you also want alpha to be affected."""
    color = get_main_color(color)
    assert factor <= 1
    if len(color) > 3:
        color = cast(RGBA, color)  # Explicitly tell mypy that color is RGBA in this block
        if also_alpha:
            return (int(color[0]*factor), int(color[1]*factor), int(color[2]*factor), int(color[3]*factor))
        else:
            return (int(color[0]*factor), int(color[1]*factor), int(color[2]*factor), color[3])
    else:
        return int(color[0]*factor), int(color[1]*factor), int(color[2]*factor)

def enlighten(color:RGB_OR_RGBA, factor=1.2, min_value=20, also_alpha=False)->RGB_OR_RGBA:
    """Returns a enlightened version of the color.
    ***Mandatory arguments***
    <color> : 3-tuple or 4-tuple color.
    ***Optional arguments***
    <factor> : (float) how much of the color we want to increase. E.g. 1.2 means we want
    to get 120% of the original color.
    <min_value> : minimum value of color components in 255 bytes format.
    also_alpha : (bool) specify whether you also want alpha to be affected."""
    color = get_main_color(color)
    assert factor >= 1
    def mc(value):
        return min(int(value*factor + min_value),255)
    if len(color) > 3:
        color = cast(RGBA, color)  # Explicitly tell mypy that color is RGBA in this block
        if also_alpha:
            return mc(color[0]), mc(color[1]), mc(color[2]), mc(color[3])
        else:
            return mc(color[0]), mc(color[1]), mc(color[2]), color[3]
    else:
        return mc(color[0]), mc(color[1]), mc(color[2])

def change_alpha(color:RGB_OR_RGBA, alpha:int)->RGBA:
    """_Always returns RGBA color"""
    return (color[0], color[1], color[2], alpha)


def process_gradient_color(gradient_color:GradientColor)->ProcessedGradient:
    """_Return color and orientation.
    We absolutely don't care that this seems slow.
    In comparison with the time that graphical computations take,
    this is nothing."""
    is_gradient = is_color_gradient(gradient_color)
    if is_gradient:
        return gradient_color[0:-1], gradient_color[-1] # type: ignore
    else:
        gradient_color = cast(RGBA, gradient_color)
        return gradient_color, None # type: ignore
    


def get_main_color(gradient_color:GradientColor)->RGB_OR_RGBA:
    all_colors, orientation = process_gradient_color(gradient_color)
    if orientation:
        return all_colors[0] # type: ignore
    return all_colors # type: ignore

def interpolate_2colors(c1:RGB_OR_RGBA, c2:RGB_OR_RGBA, k:float)->RGB_OR_RGBA:
    """Returns a color that is in between c1 and c2, with a factor k.
    For instance, if k = 0.75, then the color will be made of 75% of c1 and 25% of c2.
    Note that c1 and c2 must be of the same length in RGB or RGBA format.
    <c1> : first color (3-tuple) or (4-tuple).
    <c2> : second color (3-tuple) or (4-tuple).
    <k> : a float between 0. and 1.
    """
    assert len(c1) == len(c2)
    one_minus_k = 1. - k
    return tuple(k*c1[i]+one_minus_k*c2[i] for i in range(len(c1))) # type: ignore

#used for things like colorbars in google mode
def interpolate_ncolors(colors:ColorPair, k:float)->RGB_OR_RGBA: 
    """Returns a color that is in between two colors among the colors passed, with a factor k.
    For instance, if k = 0.75, then the color will be an interpolation of the two surrounding colors
    (see interpolate_colors) at 75% of the list of colors.
    <colors> : a list of RGB colors (3-tuple) or (4-tuple), but same length for each.
    <k> : a float between 0. and 1.
    """
    if k <= 0:
        return colors[0]
    elif k >= 1.:
        return colors[-1]
    N = len(colors) - 1
    i1 = int(k*N)
    i2 = i1 + 1 #index color 2
    k1 = i1/N
    k2 = i2/N
    new_k = (k-k1)/(k2-k1)
    return interpolate_2colors(colors[i2], colors[i1], new_k)

def color_distance(c1:RGB_OR_RGBA, c2:RGB_OR_RGBA)->float:
    """Euclidian distance between two colors, ignoring alpha value."""
    return square_color_norm((c2[0]-c1[0],c2[1]-c1[1],c2[2]-c1[2]))

def opposite_color(c:RGB_OR_RGBA)->RGB_OR_RGBA:
    """Return the conjugate of a color. For instance, if (255,0,127) is passed, then
    (0,255,127) is returned."""
    return tuple(255-v for v in c) # type: ignore

def square_color_norm(c:RGB_OR_RGBA)->float:
    """Magnitude of a color, ignoring alpha value."""
    return c[0]**2 + c[1]**2 + c[2]**2

# def is_color_gradient(color:GradientColor)->bool:
#     return isinstance(color, Gradient)
#     # if isinstance(color[0],int) or isinstance(color[0],float):
#     #     return False
#     # return True

def is_color_gradient(color:GradientColor)->bool:
    if isinstance(color[0],int) or isinstance(color[0],float):
        return False
    return True

def get_alpha(color:RGB_OR_RGBA)->float:
    color = get_main_color(color)
    if len(color) < 4:
        return 255
    color = cast(RGBA, color)
    return color[3]

def color_rect(gradient_color:GradientColor, size:Size)->pygame.Surface:
    """Return a colored rect.
    <gradient_color> : a gradient color (see below).
    <size> : 2-tuple beeing the size of the rect.<br>
    ---<br>
    gradient color can be:<br>
    *3-tuple or 4-tuple specifying the RGB or RGBA value of the color (in this case, this is a simple color);<br>
    *Tuple or list of 3-tuples or 4-tuples, plus an optional string at the end
        indicating the orientation of the gradient : either 'h', 'v', 'r'(radial) or 'q'(square).
        In this case, a gradient of colors is defined. Alpha component is ignored for gradients.<br>
        When the orientation is 'q' (square), colors are on the form (topleft, topright, bottomleft, bottomright).<br>
    All examples below are valid:<br>
        (255,0,0) #red with alpha = 255<br>
        (255,0,0,90) #red with alpha = 90<br>
        ( (255,0,0), (0,255,0) ) # gradient from red to green, with default orientation (vertical)<br>
        ( (255,0,0), (0,0,255), (0,255,0), "h" ) #horizontal gradient from red to blue to green<br>
        ( (255,0,0), (0,0,255), "h" ) #red to blue, horizontal<br>
        ( (0,0,0), (0,255,0), "r") #black to green, radial
    """
    if is_color_gradient(gradient_color):
        last_val = gradient_color[-1]
        if isinstance(last_val, str):
            orientation = last_val
        else:
            orientation = "v" #default orientation
        colors = gradient_color[0:-1]
        colors = cast(Sequence[RGB_OR_RGBA],colors)
        if len(colors[0]) == 4:
            alpha = colors[0][-1]
        else:
            alpha = 255
        s = color_gradient(colors, size, orientation)
        s.set_alpha(alpha) #type:ignore #pygame handles the cast to integer
        return s
    else:
        L = len(gradient_color)
        if L == 4:
            s = pygame.Surface(size).convert_alpha()
        elif L == 3:
            s = pygame.Surface(size).convert()
        else:
            raise ValueError("Invalid color argument : " + str(gradient_color))
        gradient_color = cast(RGB_OR_RGBA, gradient_color)
        s.fill(gradient_color) #type:ignore #pygame handles the cast to integers
        return s

def color_gradient(colors:RGB_OR_RGBA_SEQ, size:Size, orientation:str)->pygame.Surface:
    "_Horizontal or vertical gradient between ordered colors, ignoring alpha."
    L = len(colors)
    if orientation == "h":
        r = pygame.Surface((L,1))
        for i,c in enumerate(colors):
            gfx.pixel(r,i,0,c) #type:ignore #pygame handles the cast to integer
    elif orientation == "v":
        r = pygame.Surface((1,L))
        for i,c in enumerate(colors):
            gfx.pixel(r,0,i,c) #type:ignore #pygame handles the cast to integer
    elif orientation == "r":
        return color_gradient_radial(colors, size)
    elif orientation == "q":
        r = pygame.Surface((2,2))
        colors = cast(RGBA, colors)
        gfx.pixel(r,0,0,colors[0]) #type:ignore #pygame handles the cast to integer
        gfx.pixel(r,1,0,colors[1]) #type:ignore #pygame handles the cast to integer
        gfx.pixel(r,0,1,colors[2]) #type:ignore #pygame handles the cast to integer
        gfx.pixel(r,1,1,colors[3]) #type:ignore #pygame handles the cast to integer
    else:
        raise Exception("Orientation must be either 'h', 'v', 'r' or 'q'.")
    s = pygame.transform.smoothscale( r, size )
    return s

def color_gradient_radial(colors:RGB_OR_RGBA_SEQ, size:Size)->pygame.Surface:
    "_Radial gradient with color c1 in center and c2 in borders, ignoring alpha."
    n = len(colors)*2
    r = pygame.Surface((n,n))
    rect = r.get_rect()
    for c in colors:
        pygame.draw.rect(r,c,rect,1) #type:ignore #pygame handles the cast to integer
        rect.inflate_ip((-2,-2))
##        gfx.pixel(r,1,1,c1)
    s = pygame.transform.smoothscale( r, size )
    return s

def pygame_surf_to_pil_img(surf:pygame.Surface, color_format:PygCol="RGBA")->PILimage:
    size = surf.get_size()
    pil_string_image = tostring(surf, color_format, False)
    return Image.frombytes(color_format, size, pil_string_image) 

def pil_img_to_pygame_surf(img:Any, color_format:PygCol2="RGBA")->pygame.Surface: 
    size = img.size
    data = img.convert(color_format).tobytes("raw", color_format)
    return fromstring(data, size, color_format)

def get_black_white_pil(surf:pygame.Surface, black:int=128,
                        color_format:PygCol="RGBA", convert:bool=True)->PILimage:
    img = pygame_surf_to_pil_img(surf)
    gray = img.convert('L')
    bw = gray.point(lambda x: 0 if x<black else 255, '1')
    if convert:
        bw = bw.convert(color_format)
    return bw

def get_black_white(surf:pygame.Surface, black:int=128,
                    color_format:PygCol2="RGBA", convert:bool=True)->pygame.Surface:
    """Returns a monochrome version of the image, using PIL.
    ***Mandatory arguments***
    <surf> : the image you want to blur (pygame.Surface).
    ***Optional arguments***
    <black> : the gray level that is considered as black.
    <color_format> : an accepted color format by PIL."""
    img = pygame_surf_to_pil_img(surf)
    gray = img.convert('L')
    bw = gray.point(lambda x: 0 if x<black else 255, '1')
    if convert:
        bw = bw.convert(color_format)
    return pil_img_to_pygame_surf(bw, color_format)

def get_blurred(surf:pygame.Surface, radius:int=2,
                color_format:PygCol2="RGBA")->pygame.Surface:
    """Returns a blurred version of the image, using PIL.
    ***Mandatory arguments***
    <surf> : the image you want to blur (pygame.Surface).
    ***Optional arguments***
    <radius> : radius of the blurry zone.
    <color_format> : an accepted color format by PIL."""
    img = pygame_surf_to_pil_img(surf, color_format)
    img = img.filter(ImageFilter.GaussianBlur(radius))
    surface = pil_img_to_pygame_surf(img, color_format)
    return surface

def get_shadow(surf:pygame.Surface, radius:int=2, black:int=255,
               color_format:PygCol2="RGBA", alpha_factor:int=255,
               decay_mode:str="exponential", color:RGB_OR_RGBA=(0,0,0))->pygame.Surface:
    """_prefer the Shadow class if possible
    <black> : gray value below which the pixel is considered as opaque."""
    img = get_black_white_pil(surf, black, color_format)
    img = img.filter(ImageFilter.GaussianBlur(radius))
    surface = pil_img_to_pygame_surf(img, color_format)
    surface = set_alpha_from_intensity(surface, alpha_factor, decay_mode, color)
    return surface

def set_alpha_from_intensity(surface:pygame.Surface, alpha_factor:float,
                             decay_mode:str, color:RGB_OR_RGBA)->pygame.Surface:
    rect = surface.get_rect()
    newsurf = Surface(rect.size, SRCALPHA, depth=surface.get_bitsize())
    newsurf = newsurf.convert_alpha()
    newsurf.blit(surface, (0, 0))
    arrayrgb = surfarray.pixels3d(newsurf)
    arraya = surfarray.pixels_alpha(newsurf)
    bulk_color = tuple(color)
    tuning_factor = 1.03
    is_linear = decay_mode == "linear"
    for x in range(rect.left, rect.right):
        for y in range(rect.top, rect.bottom):
            color = tuple(arrayrgb[x][y]) #type:ignore
            light = square_color_norm(color)
            alpha = float(light)/MAX_NORM * 255
            arrayrgb[x][y][0] = bulk_color[0]
            arrayrgb[x][y][1] = bulk_color[1]
            arrayrgb[x][y][2] = bulk_color[2]
            if is_linear:
                actual_alpha = int(255 - alpha)
            else:
                actual_alpha = int(255*tuning_factor**-alpha)
##            elif decay_mode == "quadratic":
##                pass
##            else:
##                raise Exception("decay_mode not recognized: " + decay_mode)
            # actual_alpha *= alpha_factor
            actual_alpha = int(alpha_factor * actual_alpha)
            arraya[x][y] = actual_alpha
    return newsurf


def detect_frame(surf:pygame.Surface, vacuum:RGB_OR_RGBA=(255, 255, 255))->pygame.Rect:
    """_Returns a Rect of the minimum size to contain all that is not vacuum."""
    vacuum = np.array(vacuum) #type:ignore
    array = pygame.surfarray.array3d(surf)
    x_found = False
    last_x = 0
    miny = float("inf") #previously : 1000000000
    maxy = 0
    len_x = len(array)
    len_y = len(array[0])
    for x in range(len_x):
        if x % 100 == 0:
            print("scanning pixel line " + str(x))
        for y in range(len_y):
            if (array[x][y] != vacuum).any():
                if not x_found:
                    x_found = True
                    first_x = x
                last_x = x
                if y < miny:
                    miny = y
                if y > maxy:
                    maxy = y
    return pygame.Rect(first_x, miny, last_x - first_x, maxy - miny)


def capture_screen(surface:pygame.Surface, rect:Union[pygame.Rect,None]=None)->pygame.Surface:
    """_Returns a copy of the surface <surface>, with restriction <rect>
    (None means the whole surface)"""
    if not rect:
        rect = surface.get_rect()
    return surface.copy().subsurface(rect).convert()


def draw_gradient_along_path(surface:pygame.Surface, path:Sequence[Coord],
                             gradient:GradientColor)->None:
    """Draw a 1 D color gradient along a path.
    ***Mandatory arguments***
    <surface> : pygame Surface on which to draw.
    <path> : sequence of (x,y) coordinates.
    <gradient> : Thorpy gradient_color value."""
    import math
    #we do not want radial gradients !
    # assert gradient[-1] == "h" or gradient[-1] =="v" or not(isinstance(gradient[-1], str))
    all_colors, orientation = process_gradient_color(gradient)
    if is_color_gradient(gradient):
        all_colors = [tuple(int(c) for c in col) for col in all_colors] #type:ignore #(pygame auto casts)
    else:
        pygame.draw.aalines(surface, all_colors, True, path) #type:ignore #(pygame auto casts)
        return
    i = 1
    tot_length = 0.
    for x,y in path[1:]:
        prevx, prevy = path[i-1]
        tot_length += math.hypot(x-prevx, y-prevy)
        i += 1
    print("Total length", tot_length)
    i = 1
    colors = [all_colors[0]]
    d = 0.
    for x,y in path[1:]:
        prevx, prevy = path[i-1]
        d += math.hypot(x-prevx, y-prevy)
        fractional_d = d / tot_length
        print("INTERTP", all_colors, fractional_d)
        end_color = interpolate_ncolors(all_colors, fractional_d)
        # pygame.draw.aalines(surface, (255,)*3, True, path)
        draw_gradient_line(surface, colors[-1], end_color, (prevx,prevx), (x,y))
        colors.append(end_color)
        i += 1
    draw_gradient_line(surface, colors[-1], colors[0], path[-1], path[0])
    
def draw_gradient_line(surface:pygame.Surface, col1:RGB_OR_RGBA, col2:RGB_OR_RGBA,
                       p1:Coord, p2:Coord)->None:
    """Draw a line between two points using a color gradient.
    CAUTION ! This is a very slow function to use only in initialization phases.
    ***Mandatory arguments***
    <surface> : pygame Surface on which to draw.
    <col1> : from RGB color tuple.
    <col2> : to RGB color tuple.
    <p1> : from coordinate tuple.
    <p2> : to coordinate tuple."""
    x1,y1 = p1
    x2,y2 = p2
    n = int(max(abs(x2-x1),abs(y2-y1)))
    dpix_x = (x2-x1)/n
    dpix_y = (y2-y1)/n
    print("***", p1, p2, n, dpix_x, dpix_y)
    x,y = x1, y1
    for i in range(n):
        color = (0,0,255)
        gfx.pixel(surface, round(x), round(y), color)
        x += dpix_x
        y += dpix_y


def change_color_on_img(img:pygame.Surface,
                        color_source:PygameAcceptedColor,
                        color_target:PygameAcceptedColor,
                        colorkey:RGB_OR_RGBA_OR_NONE=None)->pygame.Surface:
    """Return a copy of the image where all color_source pixels have been converted
    to color_target pixels.
    ***Mandatory arguments***
    <img> : the image you want to blur (pygame.Surface).
    <color_source> : a color accepted by pygame.
    <color_target> : a color accepted by pygame.
    ***Optional arguments***
    <colorkey> : pixels color that must be transparent (can be None)"""
    px = pygame.PixelArray(img.copy())
    px.replace(color_source, color_target) #type:ignore #(pygame does the cast)
    img2 = px.make_surface()
    if colorkey is not None:
        img2.set_colorkey(colorkey, pygame.RLEACCEL) #type:ignore #(pygame does the cast)
    return img2.convert()

def change_color_on_img_ip(img:pygame.Surface,
                           color_source:PygameAcceptedColor,
                           color_target:PygameAcceptedColor,
                           colorkey:RGB_OR_RGBA_OR_NONE=None)->pygame.Surface:
    """Modify the image in place so that all color_source pixels have been converted
    to color_target pixels.
    ***Mandatory arguments***
    <img> : the image you want to blur (pygame.Surface).
    <color_source> : a color accepted by pygame.
    <color_target> : a color accepted by pygame.
    ***Optional arguments***
    <colorkey> : pixels color that must be transparent (can be None)"""
    px = pygame.PixelArray(img)
    px.replace(color_source, color_target) #type:ignore #(pygame does the cast)
    img2 = px.make_surface()
    if colorkey is not None:
        img2.set_colorkey(colorkey, pygame.RLEACCEL) #type:ignore #(pygame does the cast)
    return img2.convert()


@cache
def helper_smoothed_polygon(size:Size, points:Sequence[Coord])->pygame.Surface:
    surface = pygame.Surface(size, pygame.SRCALPHA)
    pygame.draw.polygon(surface, (0,0,0), points)
    return surface

@cache
def smoothed_polygon(n_smooth:int, color:PygameAcceptedColor,
                     size:Size, points:Sequence[Coord])->pygame.Surface:
    orig_size = size
    big = (size[0]*n_smooth, size[1]*n_smooth)
    points = tuple((x*n_smooth, y*n_smooth) for x,y in points)
    s = Surface(big, pygame.SRCALPHA)
    polygon = helper_smoothed_polygon(big, points)
    s.blit(polygon, (0,0))
    color = pygame.Color(*color)
    alpha = color.a
    color.a = 0
    s.fill(color, special_flags=pygame.BLEND_RGBA_MAX)
    #fill with alpha white using blend_rgba_min in order to make transparent
    s.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MIN)
    return pygame.transform.smoothscale(s, orig_size)

def polygon_aa(color:RGB_OR_RGBA, size:Size, points:Sequence[int], n_smooth:int=1)->pygame.Surface:
    all_colors, orientation = process_gradient_color(color)
    if orientation: #then color is a gradient
        if len(all_colors[0]) == 4: #type:ignore
            color = (255,255,255,all_colors[0][-1]) #type:ignore
        else:
            color = (255,255,255)
    s = smoothed_polygon(n_smooth, color, size, points)
    surface = pygame.Surface(size, flags=pygame.SRCALPHA).convert_alpha()
    surface.blit(s, (0,0))
    if orientation:
        scolor = color_gradient(all_colors, s.get_size(), orientation)
        surface.blit(scolor, (0,0), special_flags=pygame.BLEND_RGBA_MIN)
    return surface


def extract_frames(src:str, out_folder:Union[str,None]=None,
                   size_factor:Size=(1., 1.))->Sequence[pygame.Surface]:
    """Extract the frames of a GIF animation. Needs PIL.
    ***Mandatory arguments***
    <src> : filename of the gif.
    ***Optional arguments***
    <out_folder> : location where the frames are written to the disk.
    If None, frames are only kept in memory.
    <size_factor> : (2-tuple of floats) relative size increase of each frame compared to the original."""
    from PIL import Image
    frame = Image.open(src)
    nframes = 0
    imgs = []
    while frame:
        snframe = str(nframes).zfill(3)
        surface = pil_img_to_pygame_surf(frame)
        if size_factor != (1., 1.):
            w,h = surface.get_size()
            w = int(w*size_factor[0])
            h = int(h*size_factor[1])
            surface = pygame.transform.scale(surface, (w,h) )
        imgs.append(surface)
        if out_folder:
            frame.save(out_folder + snframe+".gif", 'GIF')
        nframes += 1
        try:
            frame.seek( nframes )
        except EOFError:
            break
    return imgs

def spritesheet_frames(src:str, nx:int, ny:int, line_number:int,
                       colorkey:RGB_OR_RGBA_OR_NONE=None)->Sequence[pygame.Surface]:
    """Return a list of pygame surfaces corresponding to a given line of the spritesheet.
    ***Mandatory arguments***
    <src> : filename of the spritesheet.
    <nx> : number of sprites along x-axis.
    <ny> : number of sprites along y-axis.
    <line_number> : line at which the frames are picked."""
    sheet = pygame.image.load(src)
    w,h = sheet.get_size()
    assert w%nx == 0 and h%ny == 0
    frame_w = w // nx
    frame_h = h // ny
    frame_size = (frame_w, frame_h)
    frames = []
    current_rect = pygame.Rect((0,0), frame_size)
    y = line_number * frame_h
    x = 0
    for i in range(nx):
        current_rect.topleft = x,y
        s = pygame.Surface(current_rect.size)
        s.blit(sheet, (0,0), current_rect)
        if colorkey:
            s.set_colorkey(colorkey) #type:ignore #Pygame does the cast
        frames.append(s)
        x += frame_w
    return frames

def draw_arrow(screen:pygame.Surface, start_coord:Coord, end_coord:Coord, arrow_color:RGB_OR_RGBA,
               arrowhead_length:int=13,
               arrowhead_angle:float=math.pi/6)->None:
    """Draws an arrow on the screen from start_coord to end_coord, pointing towards end_coord."""
    angle = math.atan2(end_coord[1] - start_coord[1], end_coord[0] - start_coord[0])
    # Draw the arrow line
    pygame.draw.aaline(screen, arrow_color, start_coord, end_coord) #type:ignore #pygame does the cast
    # Draw the arrowhead
    # arrowhead_length = 13
    # arrowhead_angle = math.pi / 6  # 30 degrees in radians
    arrowhead_points = [
        (
            end_coord[0] - arrowhead_length * math.cos(angle + arrowhead_angle),
            end_coord[1] - arrowhead_length * math.sin(angle + arrowhead_angle)
        ),
        end_coord,
        (
            end_coord[0] - arrowhead_length * math.cos(angle - arrowhead_angle),
            end_coord[1] - arrowhead_length * math.sin(angle - arrowhead_angle)
        )
    ]
    trigon = [(int(v[0]), int(v[1])) for v in arrowhead_points]
    a,b,c = trigon
    gfx.filled_trigon(screen, a[0],a[1], b[0],b[1], c[0],c[1],  arrow_color) #type:ignore #pygame does the cast
    gfx.aatrigon(screen, a[0],a[1], b[0],b[1], c[0],c[1],  arrow_color) #type:ignore #pygame does the cast

@cache
def generate_non_uniform_rect_shadow(size:Size, color:RGB_OR_RGBA,
                                     alpha_factor:float, shadow_radius:int)->pygame.Surface:
    shadow = Surface(size).convert_alpha()
    if len(color) == 3:
        color = change_alpha(color, int(alpha_factor * 255))
    shadow.fill(color) #type:ignore #pygame does the cast
    for i in range(shadow_radius//2):
        alpha = int(alpha_factor * 255 * i / shadow_radius)
        pygame.draw.rect(shadow, (0,0,0,alpha), shadow.get_rect().inflate((-i,-i)), 1)
##        shadow.set_alpha(self.alpha_factor*255)
    return shadow


def generate_oscillating_lights(surface:pygame.Surface, n:int, inflation:int=8, radius_amplitude:int=3,
                    alpha_factor_base:float=0.1, alpha_factor_amplitude:float=0.3,
                    color:RGB_OR_RGBA=(255,255,255),
                    base_radius:int=1)->List[pygame.Surface]:
    """Prepares the frames of lights animation. This is a complex function that should be used as described in
    the tagged examples."""
    from .shadows import Shadow
    n //= 2
    if n < 1:
        n = 1
    s  = Shadow()
    s.offset = (0,0)
    s.sun_angle = 45
    s.vertical = False
    surfaces = []
    for i in range(1,n+1):
        size = surface.get_rect().inflate((inflation*i, inflation*i)).size
        inflated = pygame.transform.scale(surface, size)
        s.shadow_radius = base_radius + radius_amplitude*i
        s.color = color
        s.alpha_factor = min(0.99, alpha_factor_base + i/n * alpha_factor_amplitude)
        surfaces.append(s.generate_image(inflated))
    surfaces += surfaces[::-1][1:-1]
    return surfaces

def generate_static_light(surface:pygame.Surface, inflation:int=8,alpha:float=0.1,
                          color:RGB_OR_RGBA=(255,255,255),radius:int=1)->pygame.Surface:
    """Return an image that can be used as the light halo around an object.
    See the tagged examples for detailed use."""
    return generate_oscillating_lights(surface, 2, inflation, 0, alpha, 0, color, radius)[0]

# @cache
def smoothed_circle(radius:int)->pygame.Surface:
    diameter = 2*radius
    circle = pygame.Surface((diameter,diameter), pygame.SRCALPHA)
    # pygame.draw.ellipse(circle, (0, 0, 0), circle.get_rect())
    pygame.draw.circle(circle, (0,0,0), (radius,radius), radius)
    return circle

@cache
def smoothed_round_rect(n_smooth:int, color:RGB_OR_RGBA,
                        size:Size, radius:FloatOrInt, force_radius:bool)->pygame.Surface:
    orig_size = size
    size = (size[0]*n_smooth, size[1]*n_smooth)
    if radius == 0:
        return color_rect(color, size)
    rect = pygame.Rect((0, 0), size)
    s = Surface(rect.size, pygame.SRCALPHA)
    square_side = min(rect.size)
    if radius < 1:
        radius = int(radius * square_side)
        if radius > square_side // 2 - 2:
            radius = square_side // 2 - 2
    else:
        radius *= n_smooth
    if not(force_radius) and radius > square_side // 2 - 2:
        radius = square_side//2 - 2
    #
    if radius < 0:
        radius = 0
    diameter = 2*radius
    #a circle is drawn on each corner of the rect
    circle = smoothed_circle(radius) #type:ignore #we are sure here that radius is an int
    r = pygame.Rect(0,0,diameter,diameter)
    r.topleft = rect.topleft
    s.blit(circle, r)
    r.bottomright = rect.bottomright
    s.blit(circle, r)
    r.topright = rect.topright
    s.blit(circle, r)
    r.bottomleft = rect.bottomleft
    s.blit(circle, r)
    #black-fill of the internal rect except the circle quarters, that have been done (actually, these are full circles).
    s.fill((0, 0, 0), rect.inflate(-r.w, 0))
    s.fill((0, 0, 0), rect.inflate(0, -r.h))
    color = pygame.Color(*color) #type:ignore #pygame does the cast
    alpha = color.a #type:ignore #pygame does the cast
    color.a = 0 #type:ignore #pygame does the cast
    #Now, if color is not a gradient, it is unchanged from the arg passed by the user.
    #fill with color using blend_rgba_max
    s.fill(color, special_flags=pygame.BLEND_RGBA_MAX) #type:ignore #pygame does the cast
    #fill with alpha white using blend_rgba_min in order to make transparent
    s.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MIN)
    if n_smooth == 1:
        return s
    return pygame.transform.smoothscale(s, orig_size)


# @cache
def round_rect_aa(color:RGB_OR_RGBA, size:Size, radius:FloatOrInt,
                  force_radius:bool=False, n_smooth:float=1.5)->pygame.Surface:
    """Returns a round rectangle.
    ***Mandatory arguments***
    <color> : an gradient color (see below).
    <size> : (2-tuple) size of the rect.
    <radius> : radius of the rounded corners in pixels. If the radius is in ]0;1[, then it is interpreted as
    the relative size of the radius as compared to the smallest side of the rect.
    ***Optional arguments***
    <force_radius> : forces the radius value even if it is not compatible with the size of the rect.
    <n_smooth> : number of times the frame is smoothed. Has an impact on performances.<br>
    ---<br>
    gradient color can be:<br>
    *3-tuple or 4-tuple specifying the RGB or RGBA value of the color (in this case, this is a simple color);<br>
    *Tuple or list of 3-tuples or 4-tuples, plus an optional string at the end
        indicating the orientation of the gradient : either 'h', 'v' 'h' 'v', 'r'(radial) or 'q'(square).
        In this case, a gradient of colors is defined. Alpha component is ignored for gradients.<br>

    All examples below are valid:<br>
        (255,0,0) #red with alpha = 255<br>
        (255,0,0,90) #red with alpha = 90<br>
        ( (255,0,0), (0,255,0) ) # gradient from red to green, with default orientation (vertical)<br>
        ( (255,0,0), (0,0,255), (0,255,0), "h" ) #horizontal gradient from red to blue to green<br>
        ( (255,0,0), (0,0,255), "h" ) #red to blue, horizontal<br>
        ( (0,0,0), (0,255,0), "r") #black to green, radial"""
    if radius == 0:
        return color_rect(color, size)
    all_colors, orientation = process_gradient_color(color)
    if orientation: #then color is a gradient
        if len(all_colors[0]) == 4: #type:ignore #pygame does the cast
            color = (255,255,255,all_colors[0][-1])  #type:ignore #pygame does the cast
        else:
            color = (255,255,255)
    s = smoothed_round_rect(n_smooth, color, size, radius, force_radius)
    surface = pygame.Surface(size, flags=pygame.SRCALPHA).convert_alpha()
    surface.blit(s, (0,0))
    if orientation:
        scolor = color_gradient(all_colors, s.get_size(), orientation)
        surface.blit(scolor, (0,0), special_flags=pygame.BLEND_RGBA_MIN)
    return surface


def draw_pixel_border_ip(surface:pygame.Surface,
                         border_color:RGB_OR_RGBA,
                         color_empty:RGB_OR_RGBA_OR_NONE=None)->None:
    """Draw a color outline around the external (non-transparent) shape of a surface.
    This function is very slow and intended to be used once and for all before any loop,
    most suitably on small sprites. The function uses the defined colorkey as <color_empty> by default."""
    if not color_empty:
        color_empty = surface.get_colorkey()
    if not color_empty:
        raise Exception("You must provide <color_empty> or a surface with non-None colorkey")
    w,h = surface.get_size()
    def draw_pix_if_needed(x,y):
        color = surface.get_at((x,y))
        if color != color_empty:
            gfx.pixel(surface, x, y, border_color) #this or surface.set_at() ?
            return True
    for x in range(w): #columns from top to bottom
        for y in range(h):
            if draw_pix_if_needed(x,y):
                break
    for y in range(h): #lines 
        for x in range(w): #from left to right
            if draw_pix_if_needed(x,y):
                break
        for x in range(w-1, -1, -1): #from right to left
            if draw_pix_if_needed(x,y):
                break


def extract_pixel_border(surface:pygame.Surface, border_color:RGB_OR_RGBA,
                         color_empty:RGB_OR_RGBA_OR_NONE=None,
                         thickness:int=1)->pygame.Surface:
    """Return a surface containing only the outline around the external (non-transparent) shape of a surface.
    This function is very slow and intended to be used once and for all before any loop,
    most suitably on small sprites. The function uses the defined colorkey as <color_empty> by default,
    otherwise it looks at the color on the topleft pixel."""
    if not color_empty:
        color_empty = surface.get_colorkey()
    if not color_empty:
        color_empty = surface.get_at((0,0))
        # raise Exception("You must provide <color_empty> or a surface with non-None colorkey")
    w,h = surface.get_size()
    new_surface = pygame.Surface((w,h))
    new_surface.set_colorkey(color_empty) #type:ignore #pygame does the cast
    new_surface.fill(color_empty) #type:ignore #pygame does the cast
    if thickness != 1:
        def draw_pix_if_needed(x,y):
            color = surface.get_at((x,y))
            if color != color_empty:
                for ix in range(-1,2):
                    for iy in range(-1,2):
                        gfx.pixel(new_surface, x+ix, y+iy, border_color)
                return True
    else:
        def draw_pix_if_needed(x,y):
            color = surface.get_at((x,y))
            if color != color_empty:
                gfx.pixel(new_surface, x, y, border_color) #this or surface.set_at() ?
                return True
    for x in range(w): #columns from top to bottom
        for y in range(h):
            if draw_pix_if_needed(x,y):
                break
    for y in range(h): #lines 
        for x in range(w): #from left to right
            if draw_pix_if_needed(x,y):
                break
        for x in range(w-1, -1, -1): #from right to left
            if draw_pix_if_needed(x,y):
                break
    return new_surface


def illuminate_border_ip(surface:pygame.Surface, light_color:RGB_OR_RGBA, orientation:str,
                         depth:int, intensity:float=0.5, color_empty:RGB_OR_RGBA_OR_NONE=None)->None:
    """This function is very slow and intended to be used once and for all before any loop,
    most suitably on small sprites. The function uses the defined colorkey as <color_empty> by default."""
    if not color_empty:
        color_empty = surface.get_colorkey()
    if not color_empty:
        raise Exception("You must provide <color_empty> or a surface with non-None colorkey")
    intensity = 1. - intensity
    w,h = surface.get_size()
    def draw_pix_if_needed(x,y):
        color = surface.get_at((x,y))
        if color != color_empty:
            border_color = interpolate_2colors(color[0:len(light_color)], light_color, intensity)
            gfx.pixel(surface, x, y, border_color) #this or surface.set_at() ?
            return True
    if "top" in orientation:
        for x in range(w): #columns from top to bottom
            for y in range(h):
                if draw_pix_if_needed(x,y):
                    break
    for y in range(h): #lines 
        if "left" in orientation:
            n = 0
            for x in range(w): #from left to right
                if draw_pix_if_needed(x,y):
                    n += 1
                    if n >= depth:
                        break
        if "right" in orientation:
            n = 0
            for x in range(w-1, -1, -1): #from right to left
                if draw_pix_if_needed(x,y):
                    n += 1
                    if n >= depth:
                        break



def fill_nontransparent(surface:pygame.Surface, color:RGB,
                         color_empty:RGB_OR_RGBA_OR_NONE=None)->pygame.Surface:
    if not color_empty:
        color_empty = surface.get_colorkey()
    if not color_empty:
        color_empty = surface.get_at((0,0))
    #
    colorkey = color_empty[:3]
    surfcopy = surface.copy()
    pixel_array = pygame.surfarray.pixels3d(surfcopy)
    # Find which pixels are not the colorkey (not transparent)
    not_colorkey = np.all(pixel_array != colorkey, axis=-1)
    pixel_array[not_colorkey] = color
    del pixel_array
    return surfcopy
    # w,h = surface.get_size()
    # new_surface = pygame.Surface((w,h))
    # new_surface.set_colorkey(color_empty) #type:ignore #pygame does the cast
    # new_surface.fill(color_empty) #type:ignore #pygame does the cast
    # def draw_pix_if_needed(x,y):
    #     color = surface.get_at((x,y))
    #     if color != color_empty:
    #         gfx.pixel(new_surface, x, y, border_color) #this or surface.set_at() ?
    #         return True
    # for x in range(w): #columns from top to bottom
    #     for y in range(h):
    #         if draw_pix_if_needed(x,y):
    #             break
    # for y in range(h): #lines 
    #     for x in range(w): #from left to right
    #         if draw_pix_if_needed(x,y):
    #             break
    #     for x in range(w-1, -1, -1): #from right to left
    #         if draw_pix_if_needed(x,y):
    #             break
    # return new_surface

def scale_image_with_constraint(img:pygame.Surface, w:int, h:int, mode:str, smooth:bool=True)->pygame.Surface:
    """Return an image that is scaled so that it fits or fill, without deformation nor cropping,
    inside a rect of a given size.
    ***Mandatory arguments***
    <img> : a Pygame Surface
    <w>: final width
    <h>: final height
    ***Optional arguments***
    <mode> : (str) either 'fill' or 'fit'.
    <smooth> : (bool) if True, uses pygame's smoothscale, otherwise uses pygame's scale function."""
    if smooth:
        scale_func = pygame.transform.smoothscale
    else:
        scale_func = pygame.transform.scale
    iw, ih = img.get_size()
    scale_w = w/iw
    scale_h = h/ih
    if mode == "fill":
        if scale_w < scale_h:
            new_size = int(scale_h*iw), h
        else:
            new_size = w, int(scale_w*ih)
    else:
        if scale_w > scale_h:
            new_size = int(scale_h*iw), h
        else:
            new_size = w, int(scale_w*ih)
    return scale_func(img, new_size)

# def draw_aa(color, func, rect, params):
#     """_Generic function"""
# ##    size = rect.size
#     s = Surface(rect.size, pygame.SRCALPHA)
#     n = 2
# ##    bigs = pygame.Surface((size[0]*n,size[1]*n), pygame.SRCALPHA)
# ##    big_rect = rect.inflate(size) #double size
# ##    x1,y1,x2,y2,x3,y3 = get_trigon_points(big_rect, "up")

# ##    bigs = pygame.Surface(rect.size, pygame.SRCALPHA)
# ##    x1,y1,x2,y2,x3,y3 = get_trigon_points(rect, orientation)
# ##    gfx.filled_trigon(s, x1, y1, x2, y2, x3, y3, color)

#     params["surface"] = s
#     params["rect"] = rect
#     func(**params)

# ##    trigon = pygame.transform.smoothscale(bigs, size)
# ##    s.blit(trigon, (0, 0)) #r is the rect containing affected pixels
# ##    s.blit(bigs, (0, 0)) #r is the rect containing affected pixels
#     #
#     color = pygame.Color(*color)
#     alpha = color.a
#     color.a = 0
#     #fill with color using blend_rgba_max
#     s.fill(color, special_flags=pygame.BLEND_RGBA_MAX)
#     #fill with alpha white using blend_rgba_min in order to make transparent
#     s.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MIN)
#     surface = pygame.Surface(rect.size, flags=pygame.SRCALPHA).convert_alpha()
#     surface.blit(s, rect.topleft)
#     return surface


# def polygon(color, points):
#     orig_size = size
#     size = (size[0]*n_smooth, size[1]*n_smooth)
#     if radius == 0:
#         return color_rect(color, size)
#     rect = pygame.Rect((0, 0), size)
#     s = Surface(rect.size, pygame.SRCALPHA)
#     square_side = min(rect.size)
#     if radius < 1:
#         radius = int(radius * square_side)
#         if radius > square_side // 2 - 2:
#             radius = square_side // 2 - 2
#     else:
#         radius *= n_smooth
#     if not(force_radius) and radius > square_side // 2 - 2:
#         radius = square_side//2 - 2
#     #
#     if radius < 0:
#         radius = 0
#     diameter = 2*radius
#     #a circle is drawn on each corner of the rect
#     circle = smoothed_circle(radius)
#     r = pygame.Rect(0,0,diameter,diameter)
#     r.topleft = rect.topleft
#     s.blit(circle, r)
#     r.bottomright = rect.bottomright
#     s.blit(circle, r)
#     r.topright = rect.topright
#     s.blit(circle, r)
#     r.bottomleft = rect.bottomleft
#     s.blit(circle, r)
#     #black-fill of the internal rect except the circle quarters, that have been done (actually, these are full circles).
#     s.fill((0, 0, 0), rect.inflate(-r.w, 0))
#     s.fill((0, 0, 0), rect.inflate(0, -r.h))
#     color = pygame.Color(*color)
#     alpha = color.a
#     color.a = 0
#     #Now, if color is not a gradient, it is unchanged from the arg passed by the user.
#     #fill with color using blend_rgba_max
#     s.fill(color, special_flags=pygame.BLEND_RGBA_MAX)
#     #fill with alpha white using blend_rgba_min in order to make transparent
#     s.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MIN)
#     if n_smooth == 1:
#         return s
#     return pygame.transform.smoothscale(s, orig_size)


#Borrowed from pgzero
_circle_cache:Dict[int,Sequence[Coord]] = {}
def _circlepoints(r:float)->Sequence[Coord]:
    r = int(round(r))
    if r in _circle_cache:
        return _circle_cache[r]
    x, y, e = r, 0, 1 - r
    _circle_cache[r] = points = []
    while x >= y:
        points.append((x, y))
        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1
    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]
    points.sort()
    return points

def render_outlined_text(text:str, font:pygame.font.Font,
                         gfcolor:RGB_OR_RGBA, ocolor:RGB_OR_RGBA, opx:int)->pygame.Surface:
    textsurface = font.render(text, True, gfcolor).convert_alpha() #type:ignore #pygame casts it
    w = textsurface.get_width() + 2 * opx
    h = font.get_height()
    osurf = pygame.Surface((w, h + 2 * opx)).convert_alpha()
    osurf.fill((0, 0, 0, 0))
    surf = osurf.copy()
    osurf.blit(font.render(text, True, ocolor).convert_alpha(), (0, 0)) #type:ignore #pygame casts it
    for dx, dy in _circlepoints(opx):
        surf.blit(osurf, (dx + opx, dy + opx))

    surf.blit(textsurface, (opx, opx))
    return surf



def darken_every_color_ip(surface:pygame.Surface,
                          factor:float=0.5,
                          color_empty:RGB_OR_RGBA_OR_NONE=None)->pygame.Surface:
    """This function is very slow and intended to be used once and for all before any loop,
    most suitably on small sprites. If <color_empty> is None, then it detects the default colorkey
    of the surface."""
    if not color_empty:
        color_empty = surface.get_colorkey()
    if not color_empty:
        raise Exception("You must provide <color_empty> or a surface with non-None colorkey")
    w,h = surface.get_size()
    for x in range(w): #columns from top to bottom
        for y in range(h):
            color = surface.get_at((x,y))
            if color != color_empty:
                new_color = darken(color, factor) #type:ignore #pygame casts it
                #maybe surface.set_at(...) is more performant than gfx.pixel
                gfx.pixel(surface, x, y, new_color) #type:ignore #pygame casts it
    return surface


# mypy graphics.py | Select-Object -First 1 
# mypy --explicit-package-bases .\graphics.py | Select-Object -First 1
