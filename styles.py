import sys, inspect, math, random
import warnings

import pygame.gfxdraw as gfx
import pygame
from typing import Optional

from . import parameters as p
from .graphics import darken, enlighten
from . import graphics
from .shadows import Shadow



ALL_STYLES = ("normal", "pressed", "hover", "locked")
COLOR_TAG = "RGB"

def get_trigon(rtrig, arrow):
    if arrow == "up":
        x1,y1 = rtrig.bottomleft
        x2,y2 = rtrig.bottomright
        x3,y3 = rtrig.centerx, 0
    elif arrow == "down":
        x1,y1 = rtrig.topleft
        x2,y2 = rtrig.topright
        x3,y3 = rtrig.centerx, rtrig.bottom
    elif arrow == "right":
        x1,y1 = rtrig.right, rtrig.centery
        x2,y2 = rtrig.bottomleft
        x3,y3 = rtrig.topleft
    else:
        x1,y1 = rtrig.x, rtrig.centery
        x2,y2 = rtrig.bottomright
        x3,y3 = rtrig.topright
    return (x1,y1),(x2,y2),(x3,y3)
    # return x1,y1,x2,y2,x3,y3


def get_font(obj):
    if not obj.__class__.font:
        return pygame.font.SysFont(p.fallback_font_name, p.fallback_font_size)
    else:
        return obj.__class__.font

def set_default_font(font_name, font_size):
    """Set the default font for all thorpy elements.
    This function must be called before thorpy.init()
    <font_name> : a string with the name or path of the font, or a list of font names.
    In the latter case, the first existing font in the user system will be chosen.
    <font_size : integer font size."""
    clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    if not isinstance(font_name, str):
        font_name = get_first_existing_font(font_name)
    font = generate_font(font_name, font_size)
    for name, cls in clsmembers:
        cls.font_name = font_name
        cls.font_size = font_size
        cls.font = font

def get_first_existing_font(fontnames):
    all_fonts = pygame.font.get_fonts()
    for fontname in fontnames:
        if fontname in all_fonts:
            return fontname

def generate_font(font_name, font_size, bold=False, italic=False):
    try:
        try:
            font = pygame.font.Font(font_name, font_size)
        except:
            font = pygame.font.SysFont(font_name, font_size)
    except:
        warnings.warn("Couldn't generate font:" + str(font_name) + str(font_size))
        font = pygame.font.SysFont(p.fallback_font_name, font_size, bold, italic)
    return font

def get_default_font(style=None):
    """Get the font used by default if an element is created now.
    <style> : reference style. thorpy.TextStyle by default."""
    if style is None:
        style = TextStyle
    if not style.font_name:
        return p.fallback_font_name
    return style.font_name

def get_text_height(cls=None):
    """Returns the height in pixels of the current default style for texts. This is a different value
    than the height of an element including the text, since elements typically include margins.
    <cls> : class of the element used as reference. thorpy.Text by default."""
    from .elements import Text
    if cls is None:
        cls = Text
    return cls.style_normal.get_font_height()

def get_text_size(text, cls=None):
    """Returns the size in pixels of the current default style. This is a different value
    than the size of an element including the text, since elements typically include margins.
    <text> : the text for which you want to know the size.
    <cls> : class of the element used as reference. thorpy.Text by default."""
    from .elements import Text
    if cls is None:
        cls = Text
    return cls.style_normal.font.size(text)

class BaseStyle:
    font = None
    font_antialias = True
    font_name = None
    font_size = p.fallback_font_size
    font_color = (20,)*3
    font_leading = 0
    font_align = "l" #can be either "l", "c" or "r"
    font_auto_multilines_width = 0
    font_rich_text_tag = None
    size = "auto"
    margins = (6,6)
    bck_color = (220,)*3
    shadowgen:Optional[Shadow] = None
    offset = (0,0)
    radius = 0
    # draw_in_2_times = False

    def __init__(self): #en chantier, a tester sur example thorpy
        self.font_antialias = self.__class__.font_antialias
        self.font_name = self.__class__.font_name
        self.font_size = self.__class__.font_size
        self.bck_color = self.__class__.bck_color
        self.font_color = self.__class__.font_color
        self.font = get_font(self)
        self.margins = self.__class__.margins
        self.size = self.__class__.size
        self.has_second_draw = False
        self.frame_mod = 0 #TODO: why not class attribute like others ?
        self.nframes = 1
        #not copied
        self.r_text = None
        self.text_lines = None

    def generate_images(self, img, arrow=False):
        raise Exception("BaseStyle cannot be used as a Style (it is abstract).")

    def autoset_has_second_draw(self):
        color = graphics.get_main_color(self.bck_color)
        print("autoset", color)
        if len(color) == 4 and color[-1] < 255:
            self.has_second_draw = True
        else:
            self.has_second_draw = False
        

    def set_font_antialias(self, value):
        self.font_antialias = value
        self.refresh_font()

    def set_font_name(self, value):
        self.font_name = value
        self.refresh_font()

    def set_font_size(self, value):
        self.font_size = value
        self.refresh_font()

    def set_font_color(self, value):
        self.font_color = value

    def set_font_leading(self, value):
        self.font_leading = value

    def set_font_align(self, value):
        assert value in ("l", "c", "r")
        self.font_align = value

    def set_font_auto_multilines_width(self, w):
        self.font_auto_multilines_width = w

    def set_font_rich_text_tag(self, tag):
        self.font_rich_text_tag = tag

    def get_line_size(self, text):
        if self.font_rich_text_tag:
            w,h = 0, 0
            for part, color in text:
                size = self.font.size(part)
                w += size[0]
                h = size[1]
            return (w,h)
        return self.font.size(text)
    
    def get_font_height(self):
        return self.font.get_height()

    def process_rich_text(self, text):
        L = len(COLOR_TAG)
        s = text.split(self.font_rich_text_tag)
        new_parts = []
        for part in s:
            color = self.font_color
            if part.startswith(COLOR_TAG):
                i_start = L + 1
                i_end = part.index(")")
                if i_end > i_start:
                    color_str = part[i_start:i_end]
                    color = tuple(map(int, color_str.split(',')))
                new_parts.append((part[i_end+1:], color))
            else:
                new_parts.append((part, color))
        return new_parts

    def process_rich_lines(self, lines):
        new_lines = []
        L = len(COLOR_TAG)
        for line in lines:
            s = line.split(self.font_rich_text_tag)
            new_parts = []
            for part in s:
                color = self.font_color
                if part.startswith(COLOR_TAG):
                    i_start = L + 1
                    i_end = part.index(")")
                    if i_end > i_start:
                        color_str = part[i_start:i_end]
                        color = tuple(map(int, color_str.split(',')))
                    new_parts.append((part[i_end+1:], color))
                else:
                    new_parts.append((part, color))
            new_lines.append(new_parts)
        return new_lines

    def extract_lines_from_text(self, text):
        if self.font_rich_text_tag:
            rich_text = self.process_rich_text(text)
            if self.font_auto_multilines_width > 0:
                lines = self.autocut_rich_text(rich_text, self.font_auto_multilines_width - 2*self.margins[0])
            else:
                lines = self.split_linebreak_rich_text(rich_text)
        else:
            if self.font_auto_multilines_width > 0:
                lines = self.autocut_text(text, self.font_auto_multilines_width - 2*self.margins[0])
            else:
                lines = text.split("\n")
        return lines

    def autocut_text(self, text, max_w, sep=" ", newline_symbol="\n"):
        """_Return a list of strings with one line per element in order to make line length
        not exceed <max_w>."""
        lines = []
        current_line = ""
        current_line_w = 0
        for words in text.split(sep):
            break_split = words.split(newline_symbol)
            for i,word in enumerate(break_split):
                if word:
                    new_line_value = current_line + word + sep
                else:
                    new_line_value = current_line
                current_line_w = self.get_line_size(new_line_value)[0]
                if i>0 or current_line_w > max_w:
                    lines.append(current_line)
                    if word:
                        current_line = word + sep #next one will start with word
                    else:
                        current_line = ""
                    current_line_w = 0
                else:
                    current_line = new_line_value
        lines.append(current_line)
        return lines

    def autocut_rich_text(self, rich_text, max_w, sep=" ", newline_symbol="\n"):
        """_Return rich lines with line breaks inserted in order to make line length
        not exceed <max_w>."""
        lines = []  #[  [(txt, color), (txt,color), ...],  [(txt, color), (txt,color), ...]]
        current_line = []
        current_line_txt = ""
        current_line_w = 0
        for k,data in enumerate(rich_text):
            words, color = data
            current_line.append(["",color]) #laisse des dechets innoffenssifs normalement
            break_split = words.split(newline_symbol)
            for i,part in enumerate(break_split):
                if i>0 or current_line_w > max_w:
                    lines.append(current_line)
                    current_line = [["", color]]
                    current_line_w = 0
                    current_line_txt = ""
                for j,word in enumerate(part.split(sep)):
                    if j > 0:
                        added = sep + word
                        current_line_w = self.font.size(current_line_txt + added)[0]
                    else:
                        current_line_w = self.font.size(word)[0]
                        added = word
                    if current_line_w > max_w and j > 0:
                        lines.append(current_line)
                        current_line = [[word, color]]
                        current_line_w = 0
                        current_line_txt = word
                    else:
                        current_line[-1][0] += added
                        current_line_txt += added
        lines.append(current_line)
        return lines

    def split_linebreak_rich_text(self, rich_text):
        lines = [] #[  [(txt, color), (txt,color), ...],  [(txt, color), (txt,color), ...]]
        current_line = [] #[(txt, color), (txt,color), ...]
        for text, color in rich_text:
            text_broken = text.split("\n")
            for i,line in enumerate(text_broken):
                if i > 0:
                    lines.append(current_line)
                    current_line = []
                current_line.append((line, color))
        if current_line:
            lines.append(current_line)
        return lines

    def insert_auto_breakline(self, text, max_w, sep=" ", newline_symbol="\n"):
        lines = self.autocut_text(text, max_w, sep=" ", newline_symbol="\n")
        return newline_symbol.join(lines)


    def get_text_rect_and_lines(self, text):
        max_w, tot_h = 0, 0
        lines = self.extract_lines_from_text(text)
        n = len(lines)
        self.text_lines = tuple(lines)
        if n == 1:
            self.r_text = pygame.Rect((0,0), self.get_line_size(lines[0]))
        else:
            sizes = [self.get_line_size(line) for line in lines]
            max_w = max(sizes)[0]
            h = sizes[0][1]
            tot_h = n * h + (n-1) * self.font_leading
            self.r_text = pygame.Rect((0,0), (max_w, tot_h))
        return self.r_text, self.text_lines
    
    def font_render(self, text, color):
        return self.font.render(text, self.font_antialias, color)

    def get_rendered_text(self, lines):
        if self.font_rich_text_tag:
            renderings = []
##            rich_lines = self.process_rich_lines(lines)
            for line in lines:
                line_render = []
                for text, color in line:
                    # line_render.append(self.font.render(text, self.font_antialias, color))
                    line_render.append(self.font_render(text, color))
                renderings.append(line_render)
            return renderings
        else:
            return [self.font_render(line, self.font_color) for line in lines]
            # return [self.font.render(line, self.font_antialias, self.font_color) for line in lines]


    def blit_text_rich(self, s, lines, r_text):
        dw = 0
        surfs = self.get_rendered_text(lines) #[(surf1, surf2, ...) for line in lines]
        for surf_list in surfs:
            if self.font_align == "c":
                w = sum([s.get_rect().w for s in surf_list])
                r_text.x -= dw
                dw = (r_text.w - w)//2
                r_text.x += dw
            elif self.font_align == "r":
                w = sum([s.get_rect().w for s in surf_list])
                r_text.x -= dw
                dw = (r_text.w - w)
                r_text.x += dw
            line_width = 0
            for s_text in surf_list:
                s.blit(s_text, (r_text.x+line_width, r_text.y))
                line_width += s_text.get_width()
            if surf_list:
                line_height = s_text.get_height()
            else:
                line_height = 0
            r_text.move_ip((0,self.font_leading+line_height))

    def blit_text(self, s, lines, r_text):
        if self.font_rich_text_tag:
            self.blit_text_rich(s, lines, r_text)
            return
        dw = 0
        for s_text in self.get_rendered_text(lines):
            line_size = s_text.get_size()
            if self.font_align == "c":
                r_text.x -= dw
                dw = (r_text.w - line_size[0])//2
                r_text.x += dw
            elif self.font_align == "r":
                r_text.x -= dw
                dw = (r_text.w - line_size[0])
                r_text.x += dw
            s.blit(s_text, r_text)
            r_text.move_ip((0,self.font_leading+line_size[1]))


    def reblit_text(self, surface, text, arrow=False):
        """_ Blit agin the text on an existing surface.
        This is useful because sometimes we do some graphical stuff
        that depends on the first version of the surface."""
        infl = (self.margins[0]*2, self.margins[1]*2)
        s_text = None
        if arrow:
            s_text, r_text = self.set_arrow(arrow, color=(0,0,0))
            lines = [text]
        else:
            r_text, lines = self.get_text_rect_and_lines(text)
        if self.size == "auto":
            r_button = pygame.Rect(0, 0, r_text.w+infl[0], r_text.h+infl[1])
        else:
            r_button = pygame.Rect((0,0), self.size)
        # s = graphics.color_rect(self.bck_color, r_button.size)
        r_text.center = r_button.center
        if not arrow:
            self.blit_text(surface,lines,r_text)
        else:
            surface.blit(s_text, r_text)
        return [surface]

    def refresh_font(self):
        if self.font_name:
            self.font = generate_font(self.font_name, self.font_size)
        else:
            self.font = generate_font(p.fallback_font_name, self.font_size)

    def set_arrow(self, arrow, color):
        gen = self.__class__()
        gen.size = self.size
        # assert False
        gen.nframes = 1
        gen.bck_color = self.bck_color
        s_text = gen.generate_images(" ")[0]
        r_text = s_text.get_rect()
        w,h = r_text.size

        rect_trigon = pygame.Rect(0,0,2*w//4,2*h//4)
        trigon = get_trigon(rect_trigon, arrow)

        strigon = graphics.polygon_aa(color,rect_trigon.size,trigon,4)
        rect_trigon.center = r_text.center
        s_text.blit(strigon, rect_trigon)

        self.text_lines = " "
        self.r_text = r_text
        return s_text, r_text

    def offset_surface(self, surface) -> pygame.Surface:
        ox,oy = self.offset
        if ox or oy:
            w,h = surface.get_size()
            s = pygame.Surface((w+ox, h+oy)).convert_alpha()
            s.fill((0,0,0,0))
            s.blit(surface, (ox,oy))
            return s
        else:
            return surface


    def copy(self):
        c = self.__class__()
        c.font = self.font
        c.font_name = self.font_name
        c.font_size = self.font_size
        c.bck_color = self.bck_color
        c.font_color = self.font_color
        c.font_leading = self.font_leading
        c.margins = self.margins
        c.size = self.size
        c.font_auto_multilines_width = self.font_auto_multilines_width
        c.font_rich_text_tag = self.font_rich_text_tag
        c.shadowgen = self.shadowgen #copy shadowgen too ?
        c.offset = self.offset
        c.has_second_draw = self.has_second_draw
        c.radius = self.radius
        return c


class ImageStyle(BaseStyle):
    margins = (0,0)

    def generate_images(self, img, arrow=False) -> list[pygame.Surface]:
        self.text_lines = ""
        self.r_text = img.get_rect()
        self.size = self.r_text.size
        img = self.offset_surface(img)
        return [img]

class ImageStyleWithText(BaseStyle):
    font_color = (255,)*3
    bck_color = (0,)*4

    def generate_images(self, img, text, arrow=False):
        infl = (self.margins[0]*2, self.margins[1]*2)
        s_text = None
        if arrow:
            s_text, r_text = self.set_arrow(arrow, color=(0,0,0))
            lines = [text]
        else:
            r_text, lines = self.get_text_rect_and_lines(text)
        if self.size == "auto":
            r_button = pygame.Rect(0, 0, r_text.w+infl[0], r_text.h+infl[1])
        else:
            r_button = pygame.Rect((0,0), self.size)

        # s = graphics.color_rect(self.bck_color, r_button.size)
        r_img = img.get_rect()
        r_button.center = r_img.center
        s = img
        r_text.center = r_button.center
        if not arrow:
            self.blit_text(s,lines,r_text)
        else:
            s.blit(s_text, r_text)
        return [self.offset_surface(s)]

class MultipleImagesStyle(BaseStyle):
    margins = (0,0)

    def generate_images(self, imgs, arrow=False):
        self.text_lines = ""
        self.r_text = imgs[0].get_rect()
        self.size = self.r_text.size
        self.nframes = len(imgs)
        self.frame_mod = 1
        return imgs

class TextStyle(BaseStyle):
    font_color = (255,)*3
    bck_color = (0,)*4

    def generate_images(self, text, arrow=False):
        infl = (self.margins[0]*2, self.margins[1]*2)
        s_text = None
        if arrow:
            s_text, r_text = self.set_arrow(arrow, color=(0,0,0))
            lines = [text]
        else:
            r_text, lines = self.get_text_rect_and_lines(text)
        if self.size == "auto":
            r_button = pygame.Rect(0, 0, r_text.w+infl[0], r_text.h+infl[1])
        else:
            r_button = pygame.Rect((0,0), self.size)
        s = graphics.color_rect(self.bck_color, r_button.size)
        r_text.center = r_button.center
        if not arrow:
            self.blit_text(s,lines,r_text)
        else:
            s.blit(s_text, r_text)
        return [self.offset_surface(s)]
    

class OutlinedTextStyle(TextStyle):
    font_color = (255,)*3
    bck_color = (0,)*4
    outline_color = (50,)*3
    outline_thickness = 2

    def get_line_size(self, text):
        w,h = super().get_line_size(text)
        m = 2 * self.outline_thickness
        return w + m, h + m
    
    def get_font_height(self):
        return super().get_font_height() + 2 * self.outline_thickness
    
    def font_render(self, text, color):
        from .graphics import render_outlined_text
        return render_outlined_text(text, self.font, color,
                                        self.outline_color, self.outline_thickness)
    def copy(self):
        c = TextStyle.copy(self)
        c.outline_color = self.outline_color
        c.outline_thickness = self.outline_thickness
        return c



class RoundStyle(BaseStyle):
    radius = 10 #if radius is less than 1, then its relative to min side
    force_radius = False
    n_smooth = 1.5 #impacts perf !
    border_color = (50,50,50)
    border_thickness = 0


    def generate_images(self, text, arrow=False):
        # self.autoset_has_second_draw()
        infl = (self.margins[0]*2, self.margins[1]*2)
        if arrow:
            s_text, r_text = self.set_arrow(arrow, color=self.font_color)
            lines = [text]
        else:
            r_text, lines = self.get_text_rect_and_lines(text)
        # print("***", self.text_lines, id(self.text_lines))
        if self.size == "auto":
            r_button = pygame.Rect(0, 0, r_text.w+infl[0], r_text.h+infl[1])
        else:
            r_button = pygame.Rect((0,0), self.size)
        #
        thick = self.border_thickness
        if thick > 0 and self.radius > 0:
            border_alpha = graphics.get_alpha(self.border_color)
            bck_alpha = graphics.get_alpha(self.bck_color)
            if border_alpha != bck_alpha:
                warnings.warn("Border alpha and background alpha should be the same for round styles")
            s0 = graphics.round_rect_aa(self.border_color, r_button.size,
                                        self.radius, self.force_radius, self.n_smooth).convert_alpha()
            size_s = [r_button.size[0]-2*thick, r_button.size[1]-2*thick]
            size_s = (max(1,size_s[0]), max(1,size_s[1]))
            if self.radius >= 2:
                inner_radius = self.radius - thick
            else:
                inner_radius = self.radius
            s = graphics.round_rect_aa(self.bck_color, size_s, inner_radius,
                                       self.force_radius, self.n_smooth).convert_alpha() #convert needed ?
            s0.blit(s, (thick,thick))
            if border_alpha != bck_alpha:
                alpha = max(border_alpha, bck_alpha)
            else:
                alpha = border_alpha
            s0.set_alpha(alpha)
        else:
            s0 = graphics.round_rect_aa(self.bck_color, r_button.size, self.radius,
                                        self.force_radius, self.n_smooth)
            if thick: #then radius is necessarily zero
                pygame.draw.rect(s0, self.border_color, s0.get_rect(), thick)
        if not self.has_second_draw:
            r_text.center = r_button.center
            if not arrow:
                self.blit_text(s0, lines, r_text)
            else:
                s0.blit(s_text, r_text)
        # return [s0]
        return [self.offset_surface(s0)]

    def copy(self):
        c = BaseStyle.copy(self)
        c.force_radius = self.force_radius
        c.n_smooth = self.n_smooth
        c.border_color = self.border_color
        c.border_thickness = self.border_thickness
        return c

class SimpleStyle(RoundStyle):
    bck_color = (240,240,240)
    radius = 0
    border_thickness = 0

class FrameStyle(RoundStyle):
    bck_color = (240,240,240)
    border_color = (255,255,255)
    radius = 0
    border_thickness = 2



class DDLEntryStyle(SimpleStyle):
    bck_color = (0,0,0,0)

class HumanStyle(RoundStyle):
    border_color = (100,100,100)
    radius = 0.2
    bck_color = ((220,)*3, (110,)*3, "v")
    border_thickness = 1


class CircleStyle(BaseStyle):
    bck_color = (200,200,200)
    border_color = (50,50,50)
    colorkey = (255,)*3

    def generate_images(self, text, arrow=False):
        if graphics.is_color_gradient(self.bck_color):
            raise ValueError("CircleStyle bck_color cannot be a gradient.")
        infl = (self.margins[0]*2, self.margins[1]*2)
        assert not arrow
        r_text, lines = self.get_text_rect_and_lines(text)
        if self.size == "auto":
            r_button = pygame.Rect(0, 0, r_text.w+infl[0], r_text.h+infl[1])
        else:
            r_button = pygame.Rect((0,0), self.size)
        if len(self.bck_color) > 3:
            s = pygame.Surface(r_button.size).convert_alpha()
        else:
            s = pygame.Surface(r_button.size).convert()
        s.set_colorkey(self.colorkey)
        s.fill(self.colorkey)
        x,y = r_button.w//2, r_button.w//2
        gfx.filled_circle(s, x,y,r_button.w//2-2, self.bck_color)
##        gfx.aacircle(s, x+1,y+1,r_button.w//2-3, self.border_color)
        gfx.aacircle(s, x,y,r_button.w//2-2, self.border_color)
        r_text.center = r_button.center
        self.blit_text(s,lines,r_text)
        return [self.offset_surface(s)]

    def copy(self):
        c = BaseStyle.copy(self)
        c.border_color = self.border_color
        c.colorkey = self.colorkey
        return c



class ClassicStyle(BaseStyle):
    bck_color = (220,)*3
    font_color = (50,)*3
    pressed = False
    border_thickness = 2
    border_color = "auto"
    dark_factor = 0.5
    light_factor = 1.3
    light_offset = 80
    pressed_text_delta = "auto"

    def __init__(self):
        BaseStyle.__init__(self)
        self.pressed = self.__class__.pressed
        self.border_thickness = self.__class__.border_thickness
        self.dark_factor = self.__class__.dark_factor
        self.light_factor = self.__class__.light_factor
        self.light_offset = self.__class__.light_offset

    def generate_images(self, text, arrow=False):
        if self.border_color == "auto":
            self.border_color = self.bck_color
        dark = darken(self.border_color, self.dark_factor)
        light = enlighten(self.border_color, self.light_factor, self.light_offset)
        if not self.pressed:
            dark,light = light, dark
        infl = (self.margins[0]*2, self.margins[1]*2)
        if arrow:
            s_text, r_text = self.set_arrow(arrow, color=self.font_color)
            lines = [text]
        else:
            r_text, lines = self.get_text_rect_and_lines(text)
        if self.size == "auto":
            r_button = pygame.Rect(0, 0, r_text.w+infl[0], r_text.h+infl[1])
        else:
            r_button = pygame.Rect((0,0), self.size)
        s = graphics.color_rect(self.bck_color, r_button.size)
        #draw borders
        for i in range(self.border_thickness):
            r_button.inflate_ip((-1,-1))
            pygame.draw.line(s, dark, r_button.topleft, r_button.bottomleft)
            pygame.draw.line(s, dark, r_button.topleft, r_button.topright)
            pygame.draw.line(s, light, r_button.topright, r_button.bottomright)
            pygame.draw.line(s, light, r_button.bottomleft, r_button.bottomright)
        r_text.center = r_button.center
        if self.pressed:
            if self.pressed_text_delta == "auto":
                self.pressed_text_delta = (self.border_thickness,)*2
            r_text.move_ip(self.pressed_text_delta)
        if not arrow:
            self.blit_text(s,lines,r_text)
        else:
            s.blit(s_text, r_text)
        return [self.offset_surface(s)]

    def copy(self):
        c = BaseStyle.copy(self)
        c.pressed = self.pressed
        c.border_thickness = self.border_thickness
        c.dark_factor = self.dark_factor
        c.light_factor = self.light_factor
        c.light_offset = self.light_offset
        c.border_color = self.border_color
        c.pressed_text_delta = self.pressed_text_delta
        return c




class TitleBoxClassicStyle(ClassicStyle):
    dmx = 10
    line_thickness = 2
    line_color = "dark"
    frame_margin = 4
    parent_style = ClassicStyle
    margins = (20,20)
    top_line = True
    bottom_line = True
    left_line = True
    right_line = True

    def __init__(self):
        ClassicStyle.__init__(self)
        if self.border_color == "auto":
            self.border_color = self.bck_color
        self.rtext = None

    def generate_images(self, text, arrow=False):
        """_<text> is the title of the titlebox"""
        assert not arrow
        r_text, lines = self.get_text_rect_and_lines(text)
        margins = (r_text.h+self.frame_margin,)*2
        if not isinstance(self.size, str):
            min_w = r_text.w + 2*self.dmx + 2*margins[0]
            if self.size[0] <= min_w:
                self.size = (min_w, self.size[1])
        parent_style = self.parent_style()
        parent_style.bck_color = self.bck_color
        parent_style.margins = self.margins
        parent_style.radius = self.radius
        parent_style.size = self.size
        s = parent_style.generate_images("")[0]

        # s = self.parent_style.generate_images(self, "")[0]

        sr = s.get_rect()
        self.size = sr.size
        r_text.centerx = sr.centerx
        r_text.y += self.frame_margin - 2
        self.rtext = r_text
        r = sr.inflate((-margins[0],-margins[1]))
        if self.line_color == "dark":
            color = darken(self.bck_color, self.dark_factor)
        elif self.line_color == "light":
            color = enlighten(self.bck_color, self.light_factor, self.light_offset)
        else:
            color = self.line_color
        if self.left_line:
            pygame.draw.line(s, color, r.topleft, r.bottomleft, self.line_thickness)
        if self.bottom_line:
            pygame.draw.line(s, color, r.bottomleft, r.bottomright, self.line_thickness)
        if self.right_line:
            pygame.draw.line(s, color, r.topright, r.bottomright, self.line_thickness)
        if self.top_line:
            pygame.draw.line(s, color, r.topleft, (r_text.x-self.dmx, r.y), self.line_thickness)
            pygame.draw.line(s, color, (r_text.right+self.dmx, r.y), r.topright, self.line_thickness)
        #
        if text:
            self.blit_text(s,lines,r_text)
        return [self.offset_surface(s)]

    def copy(self):
        c = ClassicStyle.copy(self)
        c.dmx = self.dmx
        c.line_thickness = self.line_thickness
        c.line_color = self.line_color
        c.frame_margin = self.frame_margin
        c.top_line = self.top_line
        c.bottom_line = self.bottom_line
        c.left_line = self.left_line
        c.right_line = self.right_line
        return c



class TitleBoxSimpleStyle(TitleBoxClassicStyle):
    parent_style = SimpleStyle
    radius = 0
    force_radius = False
    n_smooth = 1

    def copy(self):
        c = TitleBoxClassicStyle.copy(self)
        c.force_radius = self.force_radius
        c.n_smooth = self.n_smooth
        return c

class TitleBoxRoundStyle(TitleBoxSimpleStyle):
    parent_style = RoundStyle
    radius = 10
    force_radius = False
    n_smooth = 1.5
    bck_color = (220,)*3




class Style1(BaseStyle):
    bck_color = (100,100,250)

    def generate_images(self, text, arrow=False):
        assert not arrow
        infl = (self.margins[0]*2, self.margins[1]*2)
        r_text, lines = self.get_text_rect_and_lines(text)
        if self.size == "auto":
            r_button = pygame.Rect(0, 0, r_text.w+infl[0], r_text.h+infl[1])
        else:
            r_button = pygame.Rect((0,0), self.size)
        s = graphics.color_rect(self.bck_color, r_button.size)
        pygame.draw.line(s, (0,0,0), r_button.topleft, r_button.bottomleft, 3)
        r_text.center = r_button.center
        self.blit_text(s,lines,r_text)
        return [self.offset_surface(s)]

class OscillatingTextStyle(TextStyle):
    font_color = (200,200,200)
    font_color_amplitude = 0.3
    nframes = 20
    frame_mod = 2

    def __init__(self):
        super().__init__()
        self.nframes = 20
        self.frame_mod = 2

    def generate_images(self, text, arrow=False):
        """_Here, we generate the frames of the bright text.
        We simply generate the images as a 'standard' Text,
        except we slightly adjust the color properties for each frame."""
        surfaces = []
        o_col = self.font_color
        for i in range(self.nframes):
            f = math.sin(2*i*math.pi/self.nframes)
            self.font_color = []
            for value in o_col:
                new_val = value * (1 + self.font_color_amplitude * f)
                if new_val > 255: new_val = 255
                if new_val < 0: new_val = 0
                self.font_color.append(new_val)
            surfaces += TextStyle.generate_images(self, text, arrow)
        return surfaces
    
    def copy(self):
        c = super().copy()
        c.font_color_amplitude = self.font_color_amplitude
        return c

# from pygame.gfxdraw import aapolygon, filled_polygon
class GameStyle1(TextStyle):
    bck_color = (150,150,150)
    font_color = (50,)*3
    margins = (8,4)
    border_color = (50,)*3
    border_color2 = (50,)*3
    font_color2 = (50,)*3
    thickness = 1
    diags = (8,8) #new param
    bck_color2 = (250,250,255)
    # color_variation = 0.2 #new param
    offset = (0,0)
    nframes = 1
    frame_mod = 1
    mod_offset = "random"

    def __init__(self):
        super().__init__()
        # self.nframes = 1
        # self.frame_mod = 1 #mandatory frame_mod > 0 for animations
        
    
    def generate_images(self, text, arrow=False):
        surfaces = []
        if self.mod_offset == "random":
            i_offset = random.randint(0, self.nframes-1)
        for i in range(self.nframes):
            p.refresh_waiting_bar()
            i = (i + i_offset)%self.nframes
            value = math.sin(i*math.pi/self.nframes)
            tmp = self.bck_color
            tmp2 = self.font_color
            self.bck_color = (0,0,0,0)
            if self.nframes > 1:
                self.font_color = graphics.interpolate_2colors(self.font_color, self.font_color2, value)
            surface = TextStyle.generate_images(self, text, arrow)[0]
            self.bck_color = tmp
            if self.nframes > 1:
                bck_color = graphics.interpolate_2colors(self.bck_color, self.bck_color2, value)
                border_color = graphics.interpolate_2colors(self.border_color, self.border_color2, value)
            else:
                bck_color = self.bck_color
                border_color = self.border_color
            w,h = surface.get_size()
            mx, my = self.diags
            t = self.thickness
            points = (0, my), (mx,0), (w-1,0), (w-1,h-my), (w-mx, h-1), (0,h-1)
            pygame.draw.polygon(surface, bck_color[0:3], points)
            if t < 2:
                pygame.draw.aalines(surface, border_color, True, points)
                # graphics.draw_gradient_along_path(surface, points, ((0,0,255), (255,255,0), "h"))
            else:
                pygame.draw.polygon(surface, border_color, points, t)
            # start_pos = (max(0,w-2*mx), h-1)
            # end_pos = (min(2*mx, start_pos[0]),h-1)
            # pygame.draw.aaline(surface, border_color, start_pos, end_pos)
            self.reblit_text(surface, text, arrow)
            self.font_color = tmp2
            s = self.offset_surface(surface)
            surfaces.append(s)
        return surfaces
    
    def copy(self):
        c =  super().copy()
        #the properties that you added should be copied
        c.thickness = self.thickness
        c.border_color = self.border_color
        c.border_color2 = self.border_color2
        c.nframes = self.nframes
        c.frame_mod = self.frame_mod
        c.diags = self.diags
        c.bck_color2 = self.bck_color2
        c.mod_offset = self.mod_offset
        c.font_color2 = self.font_color2
        return c
    
class TitleBoxGameStyle(TitleBoxSimpleStyle):
    parent_style = GameStyle1
