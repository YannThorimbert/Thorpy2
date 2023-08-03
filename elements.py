"""
***summary***
Most elements have 4 possible states : 'normal', 'pressed', 'hover' and 'locked'.
Each state is linked to a behaviour and a style (see the examples).
The style options are not indicated in the documentation of the elements, as they are extensively
covered in the examples.<br><br>

Getters and setters functions of all the elements are not covered when they are obvious
(e.g) get_value for TextInput returns a string containing the inserted input.<br><br>

Styling of the elements is extensively covered in the examples, as well as in the docs for themes.<br><br>

See the most useful methods of any elements (e.g. set_size, move, etc) in the docs for common elements methods.<br><br>
"""
import os, sys, inspect
import pygame
from . import styles, loops
from . import parameters as p
from .graphics import darken, enlighten
from . import graphics
from .canonical import Element
from . import sorting
import pygame.gfxdraw as gfx
from .styles import get_text_height, get_text_size
from .shadows import auto_set_fast

sys.path.insert(0, "./")

cursor_ibeam = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_IBEAM)
cursor_arrow = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW)
cursor_resize = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_SIZENWSE)
cursor_resize_x = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_SIZEWE)
cursor_resize_y = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_SIZENS)
cursor_hand = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)

cursors_resize = {(True,True):cursor_resize, (True,False):cursor_resize_x, (False,True):cursor_resize_y}

# def set_cursor(what):
#     cursor = eval("cursor_"+what)
#     pygame.mouse.set_cursor(cursor)
#     p.cursor = cursor

def set_cursor_resize(x,y):
    cursor = cursors_resize.get((x,y))
    pygame.mouse.set_cursor(cursor)
    p.cursor = cursor

def set_cursor_arrow():
    pygame.mouse.set_cursor(cursor_arrow)
    p.cursor = cursor_arrow




def choice(alert, element, value=None, ddl=False):
    if value:
        alert.choice = value
    else:
        alert.choice = element.get_value()
    alert.choice_element = element
    if ddl and alert.launcher.show_value:
        alert.launcher.set_text(alert.choice)
    if alert.loop_give_back:
        loop, e, click_outside_cancel = alert.loop_give_back
        loop.to_update.remove(e)
        loop.element = e
        loop.click_outside_cancel = click_outside_cancel
    else:
        loops.quit_current_loop()


def launch_blocking_choice(title, choices, mode="h", pos=None, children=None, func_before=None):
    """_obsolete."""
    a = AlertWithChoices(title, choices, choice_mode=mode, children=children)
    if pos is None:
        pos = pygame.mouse.get_pos()
        a.set_bottomright(*pos)
    elif pos == "center":
        a.set_center(W//2, H//2)
    else:
        raise Exception("Invalid pos argument for launch choice")
    a.clamp(a.surface.get_rect())
    a.draggable_x = True
    a.draggable_y = True
    a.generate_shadow()
    a.launch_alone(func_before=func_before, extract_helpers=True)
    return a

def assign_styles():
    """_Ensure there is a default style (i.e. not None) for each element class.
    Attention: this ensure each element class corresponds to a style class, not a class instance !
    """
    clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    for name, cls in clsmembers:
        if name == "Element" or name == "SliderWithText":
            continue
        if not cls.style_normal:
            # warnings.warn("Fallback style for " + str(cls))
            cls.style_normal = styles.SimpleStyle
        for style_name in ["style_hover", "style_pressed", "style_locked"]:
            if not getattr(cls, style_name):
                setattr(cls, style_name, cls.style_normal)


class Button(Element):
    """Standard button that can be clicked by the user to execute an action.
    ***Mandatory arguments***
    <text> : text of the button shown to the user.
    ***Optional arguments***
    <generate_surfaces> can be set to False if you plan to change the style of the button before displaying it.
    <children> elements can be given to the button.
    <all_styles_as_normal> forces all styles to be the same as style_normal.
    You can specify the style of the button with the styles arguments, though carefully
    setting the theme of your menu is probably a better solution.
    """
    hand_cursor = True

    def __init__(self, text, style_normal=None, style_hover=None,
                    style_pressed=None, generate_surfaces=True, children=None,
                    style_locked=None, all_styles_as_normal=False):
        Element.__init__(self, children)
        self.state = "normal"
        if not style_normal: style_normal = self.__class__.style_normal.copy()
        if all_styles_as_normal:
            style_hover = style_normal.copy()
            style_pressed = style_normal.copy()
            style_locked = style_normal.copy()
        else:
            if not style_hover: style_hover = self.__class__.style_hover.copy()
            if not style_pressed: style_pressed = self.__class__.style_pressed.copy()
            if not style_locked: style_locked = self.__class__.style_locked.copy()
        self.styles = {"normal":style_normal, "hover":style_hover,
                        "pressed":style_pressed, "locked":style_locked}
        self.text = text
        if generate_surfaces:
            self.generate_surfaces()

    def set_text(self, text, adapt_parent=True, only_if_different=True, max_width=None):
        """Regenerate element's surfaces with new text content.
        ***Mandatory arguments***
        <text> : the new text.
        ***Optional arguments***
        <adapt_parent> : if True, then parent's size is adapted according to its last imposed
        margins.
        <only_if_different> : set to True if you want the element's surfaces to be regenerated only when the
        new text is different than the current element's text.
        <max_width> : set to True to automatically insert line breaks. This width is then the
        whole element's width, including its margin.
        """
        if text == self.text and only_if_different:
            return
        self.text = text
        if max_width:
            self.set_max_text_width(max_width, refresh=False)
        else:
            self.set_max_text_width(0, refresh=False)
        self.refresh_surfaces()
        self.rect = self.get_rect() #rect is inherited from Element
        if adapt_parent and self.parent:
            self.parent.resort()

    def add_text(self, new_text, adapt_parent=True):
        self.set_text(self.text+new_text, adapt_parent)

    def adapt_to_text(self, adapt_parent=True):
        for key, style in self.styles.items():
            if style.size != "auto":
                s = style.copy()
                s.size = "auto"
                self.styles[key] = s
        self.set_text(self.text, adapt_parent)

class Group(Element):
    """Invisible element containing some children elements.
    ***Mandatory arguments***
    <elements> : children of the group.
    ***Optional arguments***
    <mode> : "v", "h", "grid" or None. Specify None if you do not want to sort elements.
    <margins> : 2-tuple of integers for x- and y-margins (in pixels)
    <gap> : integer value for the spacing between elements (in pixels)
    <nx> : number of columns if grid mode is used, or 'auto'
    <ny> : number of lines if grid mode is used, or 'auto'
    <align> : alignement of the choices in the list. Either 'center' (for both vertical and horizontal mode) or 'left', 'right' (for horizontal mode) or 'top', 'bottom' (for vertical mode)
    """
    def __init__(self, elements, mode="v", margins=(5,0), gap=5, nx="auto", ny="auto", align="center"):
        super().__init__(elements)
        if mode is not None:
            self.sort_children(mode,margins=margins,gap=gap,nx=nx,ny=ny,align=align)
            self.center_on(p.screen)
        self.copy_normal_state(True)

    def stick_to(self, other, self_side, other_side, delta=(0,0), move_x=True, move_y=True):
        """Sticks the element to another.
        ***Mandatory arguments***
        <other> : another element or pygame surface.
        <self_side> : side of the element beeing sticked. Can be 'left', 'right', 'top' or 'bottom'.
        <other_side> : side of the other element. Can be 'left', 'right', 'top' or 'bottom'.
        ***Optional arguments***
        <delta> : 2-tuple delta (pixels) to apply after the element has been moved.
        <move_x> : (bool) set to False if x-axis movement should be ignored.
        <move_y> : (bool) set to False if y-axis movement should be ignored.
        """
        if isinstance(other, str):
            other = p.screen
        if not isinstance(other, pygame.Rect):
            other = other.get_rect()
        x0,y0 = sorting.get_side_center(self.get_children_rect(), self_side)
        x1,y1 = sorting.get_side_center(other, other_side)
        self.move((x1-x0+delta[0])*move_x, (y1-y0+delta[1])*move_y)

class Text(Button):
    """Text that can be used as a GUI element taking all standard element states
    (normal, hover, pressed, locked) and actions.
    ***Mandatory arguments***
    <text> : the text content. Can include line breaks.
    ***Optional arguments***
    <font_size> : size of the font (integer).
    <font_color> : color of the font in (R,G,B) format.
    <max_width> : maximum widht of the text element. To cope with tate, line breaks will be
    automatically inserted if needed.
    """
    hand_cursor = False

    def __init__(self, text, font_size=None, font_color=None, style_normal=None,
                 generate_surfaces=True, only_normal=True, max_width=None):
        Element.__init__(self, None)
        self.state = "normal"
        if not style_normal:
            style_normal = self.__class__.style_normal.copy()
        self.styles = {"normal":style_normal,
                       "hover":self.__class__.style_hover.copy(),
                        "pressed":self.__class__.style_pressed.copy(),
                        "locked":self.__class__.style_locked.copy()}
        self.text = text
        self.copy_normal_state(only_normal)
        if max_width:
            self.set_max_text_width(max_width, refresh=False)
        if font_size:
            self.set_font_size(font_size, refresh=False)
        if font_color:
            self.set_font_color(font_color, refresh=False)
        if generate_surfaces:
            self.generate_surfaces()

class Box(Element):
    """Graphical box that contains children elements.
    ***Mandatory arguments***
    <children> : children elements of the box.
    ***Optional arguments***
    <sort_immediately> : set to False if you do not want to sort the elements.
    May be useful if you plan to sort them later and performance is critical.
    <scrollbar_if_needed> : set to True if you want a scrollbar to automatically pop when content exceeds a given size. Otherwise, the size of the box adapts.
    <size_limit> : 2-tuple of integers representing the size limit. Any of these integers can be replaced by 'auto' to let Thorpy decide.
    """

    def __init__(self, children, sort_immediately=True,
                    style_normal=None, generate_surfaces=True, copy_normal_state=True,
                    scrollbar_if_needed=False, size_limit="auto"):
        if not isinstance(children, list):
            children = list(children)
        Element.__init__(self, children)
        # !!! call yourbox.copy_normal_state(False) before generating surfaces if you want to apply other styles than normal for your box.
        self.copy_normal_state(copy_normal_state)
        self.state = "normal"
        self.stop_resize_if_too_small = True
        self.add_scrollbar_if_needed = scrollbar_if_needed #experimental
        self.scrollbar_x = None
        self.scrollbar_y = None
        self.scrollbar_y_factor = 1.
        self.scrollbar_x_factor = 1.
        self.resizer = None
        self.resize_margin = (-10,-10)
        if size_limit == "auto":
            size_limit = ("auto",)*2
        self.size_limit = list(size_limit)
        for i in range(2):
            if size_limit[i] == "auto":
                self.size_limit[i] = p.screen.get_size()[i]
        # self.keep_first_children_inside_when_resize = True
        if not style_normal:
            style_normal = self.__class__.style_normal.copy()
        self.styles = {"normal":style_normal,
                       "hover":self.__class__.style_hover.copy(),
                        "pressed":self.__class__.style_pressed.copy(),
                        "locked":self.__class__.style_locked.copy()}
        if generate_surfaces:
            self.generate_surfaces()
        if sort_immediately:
            self.sort_children()
            # self.center_on(p.screen)

    def set_resizable(self, x, y, clip_children=True):
        """Set the box resizable by the user by dragging the corner and/or the borders.
        ***Mandatory arguments***
        <x> : (bool) set resizable along x-axis.
        <y> : (bool) set resizable along y-axis.
        ***Optional arguments***
        <clip_children> : (bool) clip children elements inside the box."""
        if clip_children:
            self.clip_children()
        else:
            self.unclip_children()
        if x or y:
            self.resizer = Button("")
            self.resizer.copy_normal_state(True)
            self.resizer.at_drag = self.at_resize
            self.resizer.set_draggable(x, y)
            self.resizer.ignore_for_sorting = True
            self.add_child(self.resizer)
            self.resizer.draw = self.resizer.do_nothing
            # self.resizer.set_bck_color((127,)*4)
            self.resizer.at_hover = set_cursor_resize
            self.resizer.at_hover_params = {"x":x, "y":y}
            self.resizer.at_unhover = set_cursor_arrow
            self.refresh_resizer_size()
        else:
            if self.resizer:
                self.remove_child(self.resizer)
                self.resizer = None

    def refresh_resizer_size(self):
        x,y = self.resizer.draggable_x, self.resizer.draggable_y
        if x and y:
            self.resizer.set_size((20,20),False)
            self.resizer.set_center(*self.rect.bottomright)
        elif x:
            self.resizer.set_size((20,self.rect.h),False)
            self.resizer.stick_to(self, "right", "right", (self.resizer.rect.w//2,0))
        elif y:
            self.resizer.set_size((self.rect.w,20),False)
            self.resizer.stick_to(self, "bottom", "bottom", (0,self.resizer.rect.h//2))

    def is_resizable(self):
        """Returns True if the box is resizable on any axis."""
        return self.resizer and (self.resizer.draggable_x or self.resizer.draggable_y)

    def clip_children(self):
        for c in self.children:
            if not c.ignore_for_sorting:
                c.cannot_draw_outside = True

    def unclip_children(self):
        for c in self.children:
            if not c.ignore_for_sorting:
                c.cannot_draw_outside = False

    def set_size(self, size, adapt_parent=True):
        is_reducing = size[0]<self.rect.w or size[1]<self.rect.h
        if self.stop_resize_if_too_small and is_reducing:
            r = self.rect.inflate(*self.resize_margin)
            if not r.contains(self.get_children_rect(margins=(0,0))):
                set_cursor_arrow()
                if self.resizer:
                    self.refresh_resizer_size()
                return
        Element.set_size(self, size, adapt_parent)
        if self.resizer:
            self.refresh_resizer_size()
#         if self.keep_first_children_inside_when_resize:
#             if not self.rect.contains(self.children[0].rect):
#                 if self.last_sorted:
#                     mx,my = self.last_sorted[3]
# ##                    dx = self.children[0].rect.x - self.rect.x + mx
#                 else:
#                     my, mx = 5, 5
#                 x = min([c.rect.x for c in self.children if not c.ignore_for_sorting])
#                 dx = x - self.rect.x + mx
#                 dy = self.children[0].rect.y - self.rect.y + my
#                 for c in self.children:
#                     if not c.ignore_for_sorting:
#                         c.move(-dx,-dy)
        if self.add_scrollbar_if_needed:
            rects = [e.rect for e in self.children if not e.ignore_for_sorting]
            #x scrollbar######################################
            m = min([rect.left for rect in rects])
            M = max([rect.right for rect in rects])
            children_dx = M-m
            should_have_scrollbar = self.rect.w < children_dx
            if not(self.scrollbar_x) and should_have_scrollbar:
                self.add_scrollbar("h", children_dx)
            elif self.scrollbar_x and not(should_have_scrollbar):
                self.remove_child(self.scrollbar_x.parent)
                self.scrollbar_x = None
            #y scrollbar######################################
            m = min([rect.top for rect in rects])
            M = max([rect.bottom for rect in rects])
            children_dy = M - m
            should_have_scrollbar = self.rect.h < children_dy
            if not(self.scrollbar_y) and should_have_scrollbar:
                self.add_scrollbar("v", children_dy)
            elif self.scrollbar_y and not(should_have_scrollbar):
                self.remove_child(self.scrollbar_y.parent)
                self.scrollbar_y = None


    def add_scrollbar(self, mode, delta, thickness=None, button_size=None ):
        sw,sh = p.screen.get_size()
        if mode == "h":
            length = min(sw,self.rect.w*0.6)
        else:
            length = min(sh,self.rect.h*0.6)
        if button_size is None:
            button_size = (int(self.styles["normal"].font.get_height() * 0.8),) * 2
        button_text = {"h":("left","right"), "v":("up","down")}
        deltas = {"h":(-1,0), "v":(0,-1)}
        # b1 = ArrowButton(button_text[mode][0],button_size)
        # b2 = ArrowButton(button_text[mode][1],button_size)
        # if thickness is None:
        #     thickness = max(b1.rect.size) + 5
        if thickness is None:
            thickness = 10
        s = Slider(mode, length, thickness, dragger_length=length//4, dragger_thick_factor=0.9)
        # b1._at_click = self.at_scroll
        # b1._at_click_params = {"dx": deltas[mode][0], "dy": deltas[mode][1], "dragger": s.dragger,
        #                         "force":True}
        # b2._at_click = self.at_scroll
        # b2._at_click_params = {"dx": -deltas[mode][0], "dy": -deltas[mode][1], "dragger": s.dragger,
        #                        "force":True}
        #slider
        s.set_relative_value(0.5)
        s.rect = s.get_rect()
        s.ignore_for_sorting = False
        s.dragger.at_drag = self.at_scroll
        # s.add_child(b1)
        # s.add_child(b2)
        # if mode == "h":
        #     b1.set_center(s.rect.left - b1.rect.w / 2, s.rect.centery)
        #     b2.set_center(s.rect.right + b1.rect.w / 2, s.rect.centery)
        # else:
        #     b1.set_center(s.rect.centerx, s.rect.top-b1.rect.h/2)
        #     b2.set_center(s.rect.centerx, s.rect.bottom+b1.rect.h/2)
        s.set_relative_value(0.05)
        max_to_move = delta - length
        sbox_margins = (4,4)
        if mode == "h":
            self.scrollbar_x = s
            s.set_topleft(self.rect.x + s.dragger.rect.w + sbox_margins[0],
                            self.rect.bottom - s.rect.h - sbox_margins[1])
            space_allowed = s.rect.w
            self.scrollbar_x_factor = int(max_to_move / space_allowed) + 1
        else:
            self.scrollbar_y = s
            s.set_topleft(self.rect.right-s.rect.w-sbox_margins[0],
                            self.rect.top+s.dragger.rect.h + sbox_margins[1])
            space_allowed = s.rect.h
            self.scrollbar_y_factor = int(max_to_move / space_allowed) + 1
        sbox = Box([s],sort_immediately=False)
        sbox.add_scrollbar_if_needed = False
##        sbox.englobe_children(margins=(3,3), adapt_parent=False)
        sbox.rect.center = s.rect.center
        # rect = s.rect.unionall([b1,b2])
        rect = s.rect
        sbox.set_size(rect.inflate(*sbox_margins).size, adapt_parent=False)
        sbox.ignore_for_sorting = True
        self.add_child(sbox)
        if mode == "h":
            sbox.stick_to(self, "top", "bottom")
        elif mode == "v":
            # sbox.stick_to(self, "left", "right")
            sbox.set_topright(*self.rect.topright)

    def react_button(self, button):
        Element.react_button(self, button)
        if self.state == "hover":
            selected = self.scrollbar_y
            dx,dy = 0, 1
            if self.scrollbar_x and self.scrollbar_y:
                if self.scrollbar_x.bar.state == "hover":
                    selected = self.scrollbar_x
                    dx,dy = 1,0
            elif self.scrollbar_x:
                selected = self.scrollbar_x
                dx,dy = 1,0
            if selected:
                if button == 4: #wheel mouse
                    self.at_scroll(-dx,-dy,selected.dragger)
                elif button == 5: #wheel mouse
                    self.at_scroll(dx,dy,selected.dragger)

    def correct_draggers_pos(self):
        if self.scrollbar_x:
            d = self.scrollbar_x.dragger
            delta_d = self.scrollbar_x.bar.rect.x - d.rect.x
            if delta_d > 0:
                d.move(delta_d,0)
            else:
                delta_d = self.scrollbar_x.bar.rect.right - d.rect.right
                if delta_d < 0:
                    d.move(delta_d,0)
        if self.scrollbar_y:
            d = self.scrollbar_y.dragger
            delta_d = self.scrollbar_y.bar.rect.y - d.rect.y
            if delta_d > 0:
                d.move(0,delta_d)
            else:
                delta_d = self.scrollbar_y.bar.rect.bottom - d.rect.bottom
                if delta_d < 0:
                    d.move(0,delta_d)

    def at_scroll(self, dx, dy, dragger=False, force=False):
        if self.scrollbar_x:
            vx = self.scrollbar_x.get_relative_value()
            if not force and ((vx <= 0 and dx < 0) or (vx >= 1 and dx > 0)):
                dx = 0
            value = vx
        if self.scrollbar_y:
            vy = self.scrollbar_y.get_relative_value()
            if not force and ((vy <= 0 and dy < 0) or (vy >= 1 and dy > 0)):
                dy = 0
            value = vy
        self.correct_draggers_pos()
        # !!!! works only for scrollbar y now !!
        margins = self.get_margins((5,5))
        if not self.children_rect:
            self.children_rect = self.get_children_rect(margins)
        top = self.rect.y - value * self.children_rect.h + margins[1]
        current_y = top
        for e in self.children:
            if not e.ignore_for_sorting:
                e.set_topleft(e.rect.x, current_y)
                current_y += e.rect.h
                current_y += margins[1]
                # e.move(-dx*self.scrollbar_x_factor,-dy*self.scrollbar_y_factor)
        if dragger:
            dragger.move(dx,dy)


    def at_resize(self, dx, dy):
        size = self.rect.size
        w = max(0,size[0] + 2*dx)
        h = max(0,size[1] + 2*dy)
        new_size = (w,h)
        self.set_size(new_size)
        # self.resizer.set_bottomright(*self.rect.bottomright)


    def get_margins(self, margins):
        if self.styles["normal"].__class__.__name__.startswith("TitleBox"):
            if not margins:
                try:
                    h = max(30,self.get_current_style().rtext.h*1.5)
                    margins = (15,h)
                except:
                    r_text, lines = self.get_current_style().get_text_rect_and_lines(self.text)
                    margins = (15, r_text.h*1.5)
        if margins is None:
            margins = (5,5)
        return margins

    def sort_children(self, mode="v", align="center", gap=5,
                        margins=None, offset=0, nx="auto", ny="auto", grid_gaps=(5,5),
                        horizontal_first=False, englobe_children=True):
        margins = self.get_margins(margins)
        Element.sort_children(self, mode, align, gap, margins, offset, nx, ny,
                              grid_gaps, horizontal_first, englobe_children,
                              self.size_limit)
        self.children_rect = self.get_children_rect(margins)

##    def add_vertical_scrollbar(self):
##        up =

class TitleBox(Box):
    """Graphical box that contains children elements and displays a title.
    ***Mandatory arguments***
    <text> : title of the box.
    <children> : children elements of the box.
    ***Optional arguments***
    <sort_immediately> : set to False if you do not want to sort the elements.
    May be useful if you plan to sort them later and performance is critical.
    <scrollbar_if_needed> : set to True if you want a scrollbar to automatically pop when content exceeds a given size. Otherwise, the size of the box adapts.
    <size_limit> : 2-tuple of integers representing the size limit. Any of these integers can be replaced by 'auto' to let Thorpy decide.
    """
    

    def __init__(self, text, children, sort_immediately=True,
                    style_normal=None, generate_surfaces=True, copy_normal_state=True,
                    scrollbar_if_needed=False, size_limit="auto"):
        Box.__init__(self, children, generate_surfaces=False, sort_immediately=False,
                     copy_normal_state=copy_normal_state, scrollbar_if_needed=scrollbar_if_needed,
                     size_limit=size_limit)
        self.resize_margin = (-30,-50)
        self.text = text
        self.state = "normal"
        if not style_normal:
            style_normal = self.__class__.style_normal.copy()
        self.styles = {"normal":style_normal,
                       "hover":self.__class__.style_hover.copy(),
                        "pressed":self.__class__.style_pressed.copy(),
                        "locked":self.__class__.style_locked.copy()}
        if sort_immediately and not generate_surfaces:
            raise Exception("Contradictory arguments. Cannot sort without generating surfaces.")
        if sort_immediately:
            self.rect = pygame.Rect(0,0,1,1)
            self.sort_children()
        elif generate_surfaces and not self.has_surfaces_generated:
            self.generate_surfaces()
        # if generate_surfaces:
        #     self.generate_surfaces()
        # if sort_immediately:
        #     self.sort_children()


class AlertWithChoices(TitleBox):

    def __init__(self, title, choices, text=None, children=None, choice_mode="h", bck_func=None,
                    overwrite_choices=True):
        """Alert popping to the screen and allowing the user to choose among choices. 
        ***Mandatory arguments***
        <title> : string displayed as the title of the alert.
        <choices> : a sequence containing strings or elements (like in a DropDownListButton).
        ***Optional arguments***
        <text> : supplementary text displayed above the choices.
        <choice_mode> : either 'h' or 'v'.
        <children> : either None or a list of elements or a string.
        <bck_func> : either None or a function.
        <overwrite_choices> : if True, then if buttons are passed as choices, their at_unclick and at_unclick_params are overwritten.
        """
        self.choice = None
        self.choice_element = None
        if children is None:
            children = []
        if text:
            children = [Text(text)]+children
        if choices:
            buttons = []
            for e in choices:
                if isinstance(e, str):
                    b = Button(e)
                    b.at_unclick = choice
                    b.at_unclick_params = {"alert":self, "element":b}
                    buttons.append(b)
                else:
                    buttons.append(e)
                    if overwrite_choices:
                        e.at_unclick = choice
                        e.at_unclick_params = {"alert":self, "element":e}
        group_buttons = Group(buttons, choice_mode)
        children += [group_buttons]
        TitleBox.__init__(self, title, children)
        self.center_on(self.surface)
        self.choice_buttons = group_buttons
        self.bck_func = bck_func
##        self.box = Box(children, title)
##        self.box.set_center(400,300)
##        self.choice_buttons = group_buttons
##        self.bck_func = bck_func

    def get_button(self, choice_str_or_index):
        """Return the choice button corresponding to the passed arg.
        ***Mandatory arguments***
        <choice_str_or_number> : either a string corresponding to the content of the button we want to get,
        or an integer representing the index of the choice."""
        n = choice_str_or_index
        if isinstance(choice_str_or_index, str):
            for i,e in enumerate(self.choice_buttons.children):
                if e.text == choice_str_or_index:
                    n = i
                    break
        if isinstance(n, str):
            raise Exception("No choice with text", choice_str_or_index)
        return self.choice_buttons.children[n]

    def set_choice_func(self, choice_str_or_index, func, params=None):
        """Redefine the function to be called when clicking on a given choice.
        ***Mandatory arguments***
        <choice_str_or_number> : either a string corresponding to the content of the button we want to get,
        or an integer representing the index of the choice.
        <func> : the function to be called.
        ***Optional arguments***
        <params> : (dict) arguments passed to the function."""
        button = self.get_button(choice_str_or_index)
        button.at_unclick = func
        if params is None:
            params = {}
        button.at_unclick_params = params

    def get_value(self):
        """Return the choice made by the user, after the alert with choices has been launched !
        The value is None if user has not chosen yet or if the alert has been cancelled by the user."""
        return self.choice



class Alert(AlertWithChoices):
    """Alert popped to the screen and displaying a message.
    ***Mandatory arguments***
    <title> : string displayed as the title of the alert.
    <text> : supplementary text displayed above the choices.
    ***Optional arguments***
    <ok_text> : text of the 'okay' button to remove the alert.
    <bck_func> : either None or a function.
    <children> : either None or a list of elements or a string.
    """

    def __init__(self, title, text, ok_text="Ok", bck_func=None, children=None):
        choices = (ok_text,)
        AlertWithChoices.__init__(self, title, choices, text, children, "h", bck_func)



class TextInput(Button):
    """Alert popping to the screen and displaying a message. Most of the customization parameters are
    meant to be set after initialization. Have a look at the example of TextInput !
    ***Mandatory arguments***
    <text> : string displayed on the left of the input.
    ***Optional arguments***
    <placeholder> : text of the placeholder (empty by default).
    """
    def __init__(self, text, placeholder="", style_normal=None, style_hover=None,
                    style_pressed=None, generate_surfaces=True, placeholder_color=None):
        self.focused = False
        self.value = text
        self.initial_value = self.value
        self.placeholder = placeholder
        self.placeholder_color = placeholder_color
        self.stop_if_too_large = False
        self.max_length = 32
        self.adapt_size_force = False
        self.adapt_size_if_too_large = True
        self.max_size_if_too_large = 2000
        self.adapt_parent_if_too_large = True
        self.input_margin_x = 4
        self.last_keydown = -1000
        self.keys_validate = [pygame.K_RETURN]
        self.keys_cancel = [pygame.K_ESCAPE]
        self.cursor_img = None
        self.cursor_width = 2
        self.cursor_blinking_mod = 30
        self.cursor_pos = len(self.value)
        self.showing_cursor = False
        self.only_numbers = False
        self.only_integers = False
        self.only_alpha = False
        Button.__init__(self, "", style_normal, style_hover, style_pressed, generate_surfaces)
        self.update_max_size(self.get_value())
        self.action = self.default_at_click

    def update_max_size(self, txt):
        width = self.styles["normal"].get_line_size(txt)[0] + self.input_margin_x
        self.set_size((width,None))

    def refresh_surfaces_build(self):
        Button.refresh_surfaces_build(self)
        h = self.get_current_style().font.get_height()
        self.cursor_img = pygame.Surface((self.cursor_width, h))
        self.cursor_img.fill(self.get_current_style().font_color)

    def refresh_surfaces_copy(self):
        Button.refresh_surfaces_copy(self)
        h = self.get_current_style().font.get_height()
        self.cursor_img = pygame.Surface((self.cursor_width, h))
        self.cursor_img.fill(self.get_current_style().font_color)

    def get_frame(self, state, it):
        text, need_resize = self.can_add()
        if need_resize:
            w = text.get_width() + self.input_margin_x + self.cursor_width + 1
            h = self.surfaces[self.state][0].get_height()
            center = self.rect.center
            for style in self.styles.values():
                if style:
                    style.size = (w,h)
            Button.refresh_surfaces_build(self) #slow
            self.rect = self.get_rect()
            self.rect.center = center
            if self.adapt_parent_if_too_large and self.parent:
                self.parent.resort()
        #
        surface = Button.get_frame(self, state, it).copy()
        text_rect = text.get_rect()
##        text_rect.center = surface.get_rect().center
        surface_rect = surface.get_rect()
        text_rect.centery = surface_rect.centery
        text_rect.x = surface_rect.x + self.input_margin_x
        surface.blit(text, text_rect.topleft)
        if self.showing_cursor and self.focused:
            style = self.get_current_style()
            x = text_rect.x + style.font.size(self.value[0:self.cursor_pos])[0]
            y = text_rect.y
            surface.blit(self.cursor_img, (x,y))
        return surface

    def update(self, mouse_delta):
        if self.cursor_pos > len(self.value):
            self.cursor_pos = len(self.value)
        dragged = Button.update(self, mouse_delta)
        if self.it % self.cursor_blinking_mod == 0:
            self.showing_cursor = not(self.showing_cursor)
        return dragged

    def can_add(self): #TODO: use size !
        style = self.get_current_style()
        if self.placeholder and not(self.value):
            if self.placeholder_color is None:
                self.placeholder_color = TextInput.style_locked.font_color
            text = style.font.render(self.placeholder, True, self.placeholder_color)
        else:
            text = style.font.render(self.value, True, style.font_color)
        current_width = self.surfaces[self.state][0].get_width()
        if text.get_width() >= current_width - self.input_margin_x - self.cursor_width:
            if self.focused and self.stop_if_too_large:
                self.value = self.value[0:-1]
                return self.can_add()
            else:
                can_grow1 = self.adapt_size_force and not(self.focused)
                can_grow2 = self.adapt_size_if_too_large
                if can_grow1 or can_grow2:
                    return text, True
        return text, False

    def on_validation(self):
        """Function to be called when user validates a text. Redefine it as you like."""
        pass

    def get_value(self):
        return self.value

    def reaction_keyboard(self, e):
        if e.type == pygame.KEYDOWN:
            self.last_keydown = self.it
            if e.key in self.keys_validate: #Validation
                loops.quit_current_loop()
                self.on_validation()
            elif e.key in self.keys_cancel: #Cancellation
                self.value = self.initial_value
                if e.key != pygame.K_ESCAPE: #K_ESC is already captured by the loop
                    loops.quit_current_loop()
            elif e.key == pygame.K_BACKSPACE: #Erase
                self.value = self.value[0:self.cursor_pos-1] + self.value[self.cursor_pos:]
                self.cursor_pos -= 1
            elif e.key == pygame.K_LEFT:
                self.cursor_pos -= 1
                if self.cursor_pos < 0:
                    self.cursor_pos = 0
            elif e.key == pygame.K_RIGHT:
                self.cursor_pos += 1
                if self.cursor_pos > len(self.value):
                    self.cursor_pos = len(self.value)
            else: #Add new char
                if len(self.value) < self.max_length:
                    if e.unicode and ord(e.unicode)>31:
                        if not self.accept_char(e.unicode):
                            return
                        self.value = self.value[0:self.cursor_pos] + e.unicode + self.value[self.cursor_pos:]
##                        self.value += e.unicode
                        self.cursor_pos += 1

    def accept_char(self, char):
        if self.only_numbers:
            not_decimal = not char.isdecimal()
            if not_decimal and not(char == "."):
                return False
            elif self.only_integers and not_decimal:
                return False
        elif self.only_alpha:
            if not char.isalpha():
                return False
        return True

    def set_only_numbers(self):
        """Set the text input to accept only numbers (float)."""
        self.only_numbers = True
        self.only_integers = False
        self.only_alpha = False

    def set_only_integers(self):
        """Set the text input to accept only integers."""
        self.only_numbers = True
        self.only_integers = True
        self.only_alpha = False

    def set_only_alpha(self):
        """Set the text input to accept only alphabetical chars."""
        self.only_numbers = False
        self.only_integers = False
        self.only_alpha = True

    def set_accept_all(self):
        """Set the text input to accept any type of string."""
        self.only_numbers = False
        self.only_integers = False
        self.only_alpha = False

    def default_at_click(self):
        Button.default_at_click(self)
        self.focus()

    def unfocus(self):
        if self.focused:
            loops.quit_current_loop()

    def focus(self):
        if self.focused: #then set the cursor to the mouse pos
            pos = pygame.mouse.get_pos()
            r = self.get_rect()
            dx = pos[0] - (r.x + self.input_margin_x)
            style = self.get_current_style()
            scores = []
            for i in range(len(self.value)+1):
                w = style.font.size(self.value[0:i])[0]
                scores.append((abs(w-dx),i))
            score, i = min(scores)
            self.cursor_pos = i
        else: #then enter loop for text input
            self.initial_value = self.value
            self.focused = True
            root = self.root() #oldest ancester
            self.launch_and_lock_others(root, click_outside_cancel=True, reaction=self.reaction_keyboard)
            self.focused = False

    def default_at_hover(self):
        Button.default_at_hover(self)
        pygame.mouse.set_cursor(cursor_ibeam)

    def default_at_unhover(self):
        Button.default_at_hover(self)
        pygame.mouse.set_cursor(cursor_arrow)


class DropDownListButton(Button):
    """When this button is clicked, a list of choices is displayed to the user, who can choose one of them (or none) to close the list.
    ***Mandatory arguments***
    <choices> : sequence of strings or elements.
    ***Optional arguments***
    <title> : text to display on the button to launche the list of choices.
    <show_value> : (bool) display the last chosen value as the title of the button.
    <choice_mode> : either 'v' or 'h' (vertical or horizontal).
    <align> : alignement of the choices in the list. Either 'center' (for both vertical and horizontal mode) or 'left', 'right' (for horizontal mode) or 'top', 'bottom' (for vertical mode)
    <gap> : (int) space between two choice in the list (in pixels).
    <all_same_width> : (bool) forces each choice button to be the same width as the others.
    <bck_func> : function to be called each frame when menu is launched in blocking mode. If None, Thorpy
    will call the global call_before_gui function that has been set.
    <click_outside_cancel> (bool) : set to False if at least one element of the list must be chosen.
    <launch_nonblocking> (bool) : set to True if you want to launch the list in non-blocking mode.
    <overwrite_choices> : (bool) if True, the behaviour of the potential elements passed in choices is shadowed.
    <size_limit> : 2-tuple of integers to define the maximum size of the box in which choices are displayed.
    <generate_shadow> : 2-tuple whose first value is a boolean stating whether a shadow should be generated for the list,
    and whose second value is either 'auto' or a boolean stating whether the shadow generation should be done in fast mode.
    """

    def __init__(self, choices, title=None, style_normal=None, generate_surfaces=True,
                    choice_mode="v", bck_func=None, overwrite_choices=True, click_outside_cancel=True,
                    parent_to_lock=None, launch_nonblocking=False, show_value=True,
                    size_limit=("auto","auto"), generate_shadow=(True,"auto"), align=None, gap=5,
                    all_same_width=True):
        if title is None:
            title = choices[0]
        Button.__init__(self, title, style_normal=style_normal, generate_surfaces=generate_surfaces)
        self.show_value = show_value
        self.bck_func = bck_func
        self.click_outside_cancel = click_outside_cancel
        self.parent_to_lock = parent_to_lock
        self.ddl = DropDownList(self, choices, choice_mode, bck_func, overwrite_choices,
                                size_limit, generate_shadow, align, gap, all_same_width)
        self.launch_nonblocking = launch_nonblocking
        self.action = self.default_at_unclick

##        faire txt a cote

    def default_at_unclick(self):
        self.ddl.bck_func = self.bck_func
        if self.parent_to_lock is None:
            self.parent_to_lock = self.root()
        self.ddl.set_topleft(*self.get_rect().bottomleft)
        if self.launch_nonblocking:
            self.ddl.launch_nonblocking(click_outside_cancel=self.click_outside_cancel)
        else:
            self.ddl.launch_and_lock_others(self.parent_to_lock, func_before=self.bck_func,
                                            click_outside_cancel=self.click_outside_cancel)
            if self.at_unclick:
                self.at_unclick()
        

    def get_value(self):
        return self.ddl.choice
    
    def set_value(self, text):
        super().set_value(text)
        self.ddl.choice = text

    def set_reaction(self, func, params=None):
        self.ddl.at_unclick = func
        if params:
            self.ddl.at_unclick_params = params




class SliderWithText(Element):
    """Provides a way for the user to pick a value in a given range like a normal slider,
    plus textual indications.
    ***Mandatory arguments***
    <text> : string displayed on the left side of the slider.
    <min_value> : minimum value of the slider.
    <max_value> : maximum value of the slider.
    <initial_value> : initial value of the slider (must be in the range you chose)
    <length> : length of the slider bar along the axis defined by the mode.
    ***Optional arguments***
    <mode> : either 'h' (horitontal) or 'v' (vertical).
    <show_value_on_right_side> : (bool) dynamically display (or not) the current value on the right side of the slider.
    <round_decimal> : (bool) used to round the result (e.g. round_decimals=2 will give results with 2 decimals). By default it is set to -1 ; in this case the result is an integer.
    <show_value_on_cursor> : (bool) used to display the value on the slider's dragger. This is experimental for now and
        may cause issues, especially regarding the initial value of the slider.
    <thickness> : thickness of the slider bar.
    <set_when_click> : (bool) set the value when user click the slider's bar (instead of the cursor)
    <dragger_height> : (int or 'auto') length of the dragger in pixels.
    <dragger_length> : (int or 'auto') height of the dragger in pixels.
    <edit> : (bool) set to False if you want to forbid that user insert text to edit the value.
    """

    

    def __init__(self, text, min_value, max_value, initial_value, length, mode="h",  edit=True, thickness=5,
                    show_value_on_right_side=True, round_decimals=-1, show_value_on_cursor=False,
                    dragger_size=None, set_when_click=True):
        self.min_value = min_value
        self.max_value = max_value
        if isinstance(min_value, float) or isinstance(max_value, float) or isinstance(initial_value, float):
            if round_decimals == -1:
                round_decimals = 2
        self.round_decimals = round_decimals
        self.mode = mode
        self.slider = Slider(mode, length, thickness, set_when_click=set_when_click)
        self.edit = edit
        if self.edit:
            self.text = _LabelButton(text)
        else:
            self.text = Text(text)
        children = [self.text, self.slider]
        if edit and not show_value_on_right_side:
            raise Exception("Slider's show_value_on_right_side must be true to activate edit attribute.")
        if show_value_on_right_side:
            str_value = str(max(abs(max_value), abs(min_value)))
            if self.round_decimals > 0:
                str_value += "." + "0"*self.round_decimals
            if edit:
                self.value_text = TextInput(str_value)
                                            # input_margin=50)
                self.value_text.on_validation = self.validate_value_text
                self.value_text.adapt_size_if_too_large = False
                self.value_text.adapt_size_force = True
                self.value_text.stop_if_too_large = True
                if self.round_decimals == -1:
                    self.value_text.set_only_integers()
                else:
                    self.value_text.set_only_numbers()
                self.text.default_at_unclick = self.value_text.action
            else:
                self.value_text = Text(str_value)
            children.append(self.value_text)
        else:
            self.value_text = None
        self.show_value_on_cursor = show_value_on_cursor
        if self.show_value_on_cursor:
            self.slider.dragger.set_style_attr("margins", (1,5), refresh=False)
            #
            self.slider.dragger.set_text(str(self.max_value))
            self.slider.dragger.adapt_to_text() #need this if size != "auto"
            #
            self.slider.dragger.set_text(text)
        elif dragger_size:
            if dragger_size[1] == "auto":
                dragger_size = (dragger_size[0], get_text_height())
            self.slider.dragger.set_size(dragger_size)
        Element.__init__(self, children)
        self.sort_children(mode, gap=10)
        # self.englobe_children()
        self.set_value(initial_value)

    def update_input_size(self, txt=None):
        if txt is None:
            a,b = str(self.max_value), str(self.min_value)
            if len(a) > len(b):
                txt = a
            else:
                txt = b
        self.value_text.update_max_size(txt)


    def set_font_size(self, size, states="all", copy_style=True, refresh=True,
                      apply_to_children=False, update_input_size=True):
        super().set_font_size(size, states, copy_style, refresh, apply_to_children)
        if update_input_size:
            self.font_size.update_input_size()

    def get_delta(self):
        return self.max_value - self.min_value

    def validate_value_text(self):
        n = self.value_text.get_value()
        if n == "":
            return
        if self.round_decimals == -1:
            n = int(n)
        else:
            n = float(n)
        if n < self.min_value:
            n = self.min_value
        elif n > self.max_value:
            n = self.max_value
        self.set_value(n)
        self.on_text_validation()

    def on_text_validation(self):
        """Redefine this method to launch a function at text validation."""
        pass

    def set_value(self, value):
        rel_val = (value - self.min_value) / self.get_delta()
        self.slider.set_relative_value(rel_val)
        #we need the piece of code below because pixel-bound slider can result in rounding errors
        if self.round_decimals == -1:
            #initial set is half a pixel
            delta_rel = 0.5 / (self.slider.bar.rect.w - self.slider.dragger.rect.w)
            for i in range(6): #arbitrary iteration limit
                actual_value = self.get_value()
                if actual_value == value:
                    break
                elif actual_value < value:
                    rel_val += delta_rel
                    self.slider.set_relative_value(rel_val)
                else:
                    rel_val -= delta_rel
                    self.slider.set_relative_value(rel_val)
                delta_rel *= 0.8

    def get_value(self):
        rel_val = self.slider.get_relative_value()
        value = self.min_value + rel_val * self.get_delta()
        if self.round_decimals == -1:
            return int(value)
        else:
            return round(value, self.round_decimals)

    def update(self, mouse_delta):
        dragged = Element.update(self, mouse_delta)
        if not self.value_text and not self.show_value_on_cursor:
            return dragged
        text = str(self.get_value())
        if self.show_value_on_cursor:
            if self.slider.dragger.text != text:
                self.slider.dragger.set_text(text)
                # self.slider.dragger.adapt_to_text() #need this if size != "auto"
        if self.value_text:
            if self.edit:
                if text != self.value_text.get_value():
                    self.value_text.value = text
                    # self.sort_children(self.mode, gap=10)
            else:
                if text != self.value_text.text:
                    self.value_text.set_text(text)
                    # self.sort_children(self.mode, gap=10)
        return dragged
    

class Helper(Element):
    """Text that pops when user is hovering another element. Typically used to display hints to the user.
    ***Mandatory arguments***
    <text> argument is the text shown to the user.
    <parent> element that triggers the helper when hovered for a given amount of time.
    ***Optional arguments***
    <countdown> : time in frames before the helper pops when user is hovering the linked element (i.e. self.parent)
    <generate_shadow> : 2-tuple whose first value is a boolean stating whether a shadow should be generated for the list,
    and whose second value is either 'auto' or a boolean stating whether the shadow generation should be done in fast mode.
    <offset> : offset of the helper from the mouse position (in pixels)
    <max_width> : maximum width of the helper before line breaks are automatically inserted. Can be None for infinite.
    <follow_mouse> : (bool) set to True if you want the help to follow the mouse when hovering the parent.
    """

    def __init__(self, text, parent, countdown=30, generate_shadow=(True,"auto"), offset=(0,-20),
                    style_normal=None, generate_surfaces=True, children=None, max_width=None,
                    follow_mouse=False):
        Element.__init__(self, children)
        self.state = "normal"
        self.ignore_for_sorting = True
        if not style_normal: style_normal = self.__class__.style_normal.copy()
        self.styles = {"normal":style_normal,"hover":style_normal,
                        "pressed":style_normal, "locked":style_normal}
        self.copy_normal_state(True)
        self.text = text
        if max_width:
            self.set_max_text_width(max_width, refresh=False)
        if generate_surfaces:
            self.generate_surfaces()
        self.event_parent = parent #can be different than blit-update parent
        parent.add_child(self)
        parent.helper = self
        self.countdown = countdown
        self.time_before_launch = self.countdown
        self.last_parent_state_was_hover = False
        if generate_shadow[0]:
            shadow_fast = auto_set_fast(self, generate_shadow[1])
            self.generate_shadow(shadow_fast)
        self.clamp_rect = p.screen.get_rect()
        self.offset = offset
        self.follow_mouse = follow_mouse
        self.anchor = None

    def must_draw(self):
        return self.time_before_launch <= 0

    def update(self,  mouse_delta):
        dragged = Element.update(self,  mouse_delta)
        if self.event_parent.state == "hover":
            self.time_before_launch -= 1
            self.last_parent_state_was_hover = True
        elif self.last_parent_state_was_hover:
            self.time_before_launch = self.countdown
            self.anchor = None
        #

        if self.time_before_launch <= 0:
            if not self.anchor or self.follow_mouse:
                self.anchor = pygame.mouse.get_pos()
            self.set_center(*self.anchor)
            self.move(*self.offset)
        return dragged

class ColorPicker(Element):
    """Allows the user to pick a color in a pseudo continuum of colors.
    ***Optional arguments***
    <mode> : either 'google', 'red', 'green' or 'blue'.
    <initial_value> : initial color of the color picker. Experimental : may not be very accurate in some cases.
    <slider_align> : either 'h' or 'v' for horizontal or vertical slider bar.
    <length> : length of the color frame in which user can click.
    <height> : height of the color frame in which user can click.
    <thickness> : thickness of the colorbar (slider bar).
    <show_rgb_code> : (bool) display the RGB code of the selected color on the thumbnail.
    <colorframe_size> : 2-tuple indicating the size of the colorframe in pixels.
    <colorbar_length> : length of the colorbar (slider) in pixels.
    """

    def __init__(self, mode="google", initial_value=(255,0,0), slider_align="h",
                    length=None, height=None, thickness=None, show_rgb_code=True,
                    colorframe_size=None, colorbar_length=None):
        self.slider_align = slider_align
        if length is None:
            if slider_align == "h":
                length = p.screen.get_width()//4
            if slider_align == "v":
                length = p.screen.get_height()//4
        if height is None:
            height = 2 * length // 3
        if colorframe_size is None:
            colorframe_size = (height,)*2
        if thickness is None:
            thickness = get_text_height()//2
        mode = mode.lower()
        self.mode = mode
        self.show_rgb_code = show_rgb_code
        inverse_align = "h" if slider_align == "v" else "v"
        if mode == "google":
            col_frame = ((255,255,255), initial_value, (0,0,0), (0,0,0), "q")
        elif mode == "blue":
            col_frame = ((255,0,0), (0,0,0), (0,255,0), (0,0,0), "q")
        elif mode == "green":
            col_frame = ((255,0,0), (0,0,0), (0,0,255), (0,0,0), "q")
        elif mode == "red":
            col_frame = ((0,0,255), (0,0,0), (0,255,0), (0,0,0), "q")

        # self.colorframe = Button("",generate_surfaces=False)
        self.colorframe = _ColorFrameForColorPicker("",generate_surfaces=False)
        self.colorframe.copy_normal_state(True)
        self.colorframe.set_style_attr("radius", 1, refresh=False)
        self.colorframe.set_bck_color(col_frame, refresh=False)
        self.colorframe.set_size((length,height))
        self.colorframe._at_click = self.click_frame

        # self.colorelement = Button("", generate_surfaces=False)
        self.colorelement = _ColorFrameForColorPicker("", generate_surfaces=False)
        self.colorelement.copy_normal_state(True)
        self.colorelement.set_style_attr("radius", 3, refresh=False)
        self.colorelement.set_size(colorframe_size)

        self.visor = _ColorFrameForColorPicker("", generate_surfaces=False)
        self.visor.copy_normal_state(True)
        self.visor.set_bck_color((255,255,255,127),refresh=False)
        self.visor.set_size((10,10))
        self.visor.draggable_x = True
        self.visor.draggable_y = True
        self.visor.cannot_drag_outside = False
        self.visor.at_drag = self.visor_to_color
        self.colorframe.add_child(self.visor)

        grp = Group([self.colorelement, self.colorframe], "h")
        
        if mode == "google":
            col_bar = ((255,0,0), (255,255,0), (0,255,0), (0,255,255), (0,0,255), (255,0,255), (255,0,0), slider_align)
        elif mode == "blue": 
            col_bar = ((0,0,0), (0,0,255), slider_align)
        elif mode == "green": 
            col_bar = ((0,0,0), (0,255,0), slider_align) 
        elif mode == "red": 
            col_bar = ((0,0,0), (255,0,0), slider_align) 
        
        if colorbar_length is None:
            colorbar_length = grp.rect.w
        self.colorbar = Slider(slider_align, colorbar_length, thickness, dragger_thick_factor="auto")
        self.colorbar.dragger.at_drag = self.update_slider
        self.colorbar.bar.set_bck_color(col_bar)


        self.colorbar.bar.default_at_click = self.click_bar

        self.colors_in_bar = col_bar[0:-1] #without the orientation
        #
        Element.__init__(self, [grp, self.colorbar])
        self.sort_children(inverse_align)
        #
        if mode == "google":
            self.visor.set_center(*self.colorframe.rect.topright)
        # self.visor_to_color()
        # self.update_slider()
        self.set_value(initial_value)

    def click_bar(self):
        if self.colorbar.set_when_click:
            pos = pygame.mouse.get_pos()
            if not self.colorbar.dragger.rect.collidepoint(pos):
                self.colorbar.dragger.set_topleft(*pos)
                self.colorbar.control_dragger_pos()
            self.update_slider()

    def update_slider(self, dx=0, dy=0):
        if self.mode == "google":
            k = self.colorbar.get_relative_value()
            col = graphics.interpolate_ncolors(self.colors_in_bar, k)
            new_color = ((255,255,255), col, (0,0,0), (0,0,0), "q")
        elif self.mode == "blue":
            b = int(self.colorbar.get_value() * 255)
            new_color = ((255,0,b), (0,0,b), (0,255,b), (0,0,b), "q")
        elif self.mode == "green":
            g = int(self.colorbar.get_value() * 255)
            new_color = ((255,g,0), (0,g,0), (0,g,255), (0,g,0), "q")
        elif self.mode == "red":
            r = int(self.colorbar.get_value() * 255)
            new_color = ((r,0,255), (r,0,0), (r,255,0), (r,0,0), "q")
        self.colorframe.set_bck_color(new_color)
        self.visor_to_color()

    def get_value(self):
        vr = self.visor.rect.clamp(self.colorframe.rect)
        x = vr.centerx - self.colorframe.rect.x
        y = vr.centery - self.colorframe.rect.y
        return self.colorframe.get_current_frame().get_at((x,y))[0:3]

    def click_frame(self, xy=None):
        if xy is None:
            xy = pygame.mouse.get_pos()
        rect = self.colorframe.rect.inflate((-2,-2))
        if rect.collidepoint(xy):
            x = xy[0] - self.colorframe.rect.x
            y = xy[1] - self.colorframe.rect.y
            col = self.colorframe.get_current_frame().get_at((x,y))[0:3]
            self.colorelement.set_bck_color(col)
            if self.show_rgb_code:
                self.colorelement.set_font_color(graphics.opposite_color(self.get_value()))
                self.colorelement.set_text(str(self.get_value()))
            self.visor.set_center(*xy)

    def visor_to_color(self, dx=0, dy=0):
        if not self.colorframe.rect.collidepoint(self.visor.rect.center):
            point = pygame.Rect(self.visor.rect.center, (1,1))
            vr = point.clamp(self.colorframe.rect)
            self.visor.set_center(*vr.center)
        self.colorelement.set_bck_color(self.get_value())
        if self.show_rgb_code:
            self.colorelement.set_font_color(graphics.opposite_color(self.get_value()))
            self.colorelement.set_text(str(self.get_value()))

    def set_value(self, col):
        if len(col) > 3:
            col = col[0:3]
        # best = min((graphics.color_distance(col, col2),i,col2) for i,col2 in enumerate(self.colors_in_bar))
        precision = 256
        best = (float("inf"), 0)
        for k in range(precision):
            col2 = graphics.interpolate_ncolors(self.colors_in_bar, k/precision)
            distance = graphics.color_distance(col, col2)
            if distance < best[0]:
                best = (distance, k/precision)
        self.colorbar.set_relative_value(best[1])
        self.update_slider()
        s = self.colorframe.get_current_frame()
        r = s.get_rect()
        best = ((0,0), float("inf"))
        for x in range(r.w):
            for y in range(r.h):
                col2 = s.get_at((x,y))[0:3]
                d = graphics.color_distance(col, col2)
                if d < best[1]:
                    best = ((x,y), d)
                    if d < 1:
                        break
        ox,oy = self.colorframe.rect.topleft
        x,y = best[0]
        self.visor.set_center(ox + x, oy + y)
        self.update_slider()


class ColorPickerRGB(Element):
    """Allows the user to pick a color in a pseudo continuum of colors, by choosing the red, green and blue values independantly.
    ***Optional arguments***
    <initial_value> : initial color of the color picker.
    <slider_align> : either 'h' or 'v' for horizontal or vertical slider bar.
    <length> : length of the slider bars for red, green and blue.
    <thickness> : thickness of the colorbar (slider bar).
    <show_rgb_code> : (bool) display the RGB code of the selected color on the thumbnail.
    <colorframe_size> : 2-tuple indicating the size of the colorframe in pixels.
    """

    def __init__(self, initial_value=(255,0,0), slider_align="h",
                    length=256, thickness=None, show_rgb_code=True,
                    colorframe_size="auto"):
        self.slider_align = slider_align
        if length is None:
            if slider_align == "h":
                length = p.screen.get_width()//2
            if slider_align == "v":
                length = p.screen.get_height()//4
        if thickness is None:
            thickness = get_text_height()//2
        self.show_rgb_code = show_rgb_code
        inverse_align = "h" if slider_align == "v" else "v"


        self.colorelement = Button("", generate_surfaces=False)
        self.colorelement.copy_normal_state(True)
        self.colorelement.hand_cursor = False
        # self.colorelement.set_style_attr("radius", 3, refresh=False)
        if colorframe_size == "auto" or colorframe_size is None:
            w = int(1.2*get_text_size(str((255,255,255)))[0])
            if self.show_rgb_code:
                colorframe_size = (w,2*get_text_height())
            else:
                colorframe_size = (50,50)
        self.colorelement.set_size(colorframe_size)
        
        self.r = SliderWithText("R", 0, 255, initial_value[0], slider_align, length,
                                thickness=thickness, dragger_size=(10,"auto"), edit=True)
        self.g = SliderWithText("G", 0, 255, initial_value[1], slider_align, length,
                                thickness=thickness, dragger_size=(10,"auto"), edit=True)
        self.b = SliderWithText("B", 0, 255, initial_value[2], slider_align, length,
                                thickness=thickness, dragger_size=(10,"auto"), edit=True)
        self.r.slider.bar.set_bck_color(((0,0,0), (255,0,0), slider_align))
        self.g.slider.bar.set_bck_color(((0,0,0), (0,255,0), slider_align))
        self.b.slider.bar.set_bck_color(((0,0,0), (0,0,255), slider_align))
        self.r.slider.bar.default_at_click = self.click_bar_r
        self.g.slider.bar.default_at_click = self.click_bar_g
        self.b.slider.bar.default_at_click = self.click_bar_b
        


        for el in self.r, self.g, self.b:
            el.slider.dragger.at_drag = self.update_slider
            el.on_text_validation = self.update_slider
        grp = Group([self.r, self.g, self.b], inverse_align)
        #
        Element.__init__(self, [self.colorelement, grp])
        self.sort_children(inverse_align)
        self.update_slider()


    def click_bar(self, slider):
        if slider.set_when_click:
            pos = pygame.mouse.get_pos()
            if not slider.dragger.rect.collidepoint(pos):
                slider.dragger.set_topleft(*pos)
                slider.control_dragger_pos()
            self.update_slider()

    def click_bar_r(self):
        self.click_bar(self.r.slider)

    def click_bar_g(self):
        self.click_bar(self.g.slider)

    def click_bar_b(self):
        self.click_bar(self.b.slider)

    def update_slider(self, dx=0, dy=0):
        col = self.get_value()
        self.colorelement.set_bck_color(col)
        if self.show_rgb_code:
            self.colorelement.set_font_color(graphics.opposite_color(col))
            self.colorelement.set_text(str(col))

    def get_value(self):
        return (self.r.get_value(), self.g.get_value(), self.b.get_value())

    def set_value(self, col):
        r,g,b = col
        self.r.set_value(r)
        self.g.set_value(g)
        self.b.set_value(b)
        self.update_slider()



class ColorPickerPredefined(Element):
    """Allows the user to pick a color in a discrete set of colors, potentially predefined by you.
    ***Optional arguments***
    <colors> : a sequence of predefined colors. If set to None (or by default), this sequence
    will automatically be populated by Thorpy.
    <mode> : either 'grid, 'h' or 'v'. This defines the way the colours are sorted and displayed.
    <nx> : number of columns (int) or 'auto'.
    <ny> : number of lines (int) or 'auto'.
    <auto_cols_steps> : if colors sequence is None, then this is the number of steps used to auto populate it.
    <manual_cols_step> : if colors sequence is None and auto_cols_steps is zero, then this is the step used
    to populate the color sequence.
    <col_size> : 2-tuple indicating the size of the choice buttons.
    <init_color_index> : index of the initial color.
    """

    def __init__(self, colors=None, mode="grid", nx="auto", ny="auto",
                    auto_cols_steps=0, manual_cols_step=None, col_size=(30,30),
                    init_color_index=0):
        els = []
        self.colors = []
        if not colors and auto_cols_steps==0 and manual_cols_step is None:
            #then provide default behaviour
            auto_cols_steps=4
        if not(auto_cols_steps is None) and auto_cols_steps > 0:
            step = 255 // auto_cols_steps
        elif manual_cols_step:
            step = manual_cols_step
        self.alert = None
        if auto_cols_steps or manual_cols_step:
            for r in range(0,255,step):
                for g in range(0,255,step):
                    for b in range(0,255,step):
                        color_i = (r,g,b)
                        s = pygame.Surface(col_size)
                        s.fill(color_i)
                        e = ImageButton("", s, no_copy=True)
                        e.at_unclick = self.click_col
                        e.at_unclick_params = {"c":color_i}
                        els.append(e)
                        self.colors.append(color_i)
        else:
            self.colors = colors
            for c in colors:
                s = pygame.Surface(col_size)
                s.fill(c)
                e = ImageButton("", s, no_copy=True)
                e.at_unclick = self.click_col
                e.at_unclick_params = {"c":c}
                els.append(e)
        grp = Group(els, mode, nx=nx, ny=ny)
        Element.__init__(self, [grp])
        self.set_value(self.colors[init_color_index])
        self.sort_children()

    def click_col(self, c):
        self.set_value(c)
        if self.alert:
            choice(self.alert, self, c)

    def get_value(self):
        return self.current_color

    def set_value(self, color):
        if color in self.colors:
            self.current_color = color
            if self.parent and isinstance(self.parent, LabelledColorPicker):
                self.parent.refresh_color_thumbnail()
        else:
            raise Exception(color, "not in ColorPicker predefined colors.")

   



class Labelled(Element):
    """Associate itself another element, on the left side of which a label text is displayed.
    ***Mandatory arguments***
    <label> : a string defining the label of the element.
    <element> : the element to labellize.
    ***Optional arguments***
    <cls_label> : a Thorpy element class to be used as the label.
    """

    def __init__(self, label, element, cls_label=None):
        forbidden = [ColorPickerRGB, ColorPicker, ColorPickerPredefined, SliderWithText]
        if element.__class__ in forbidden:
            raise Exception("The element passed to the Labelled instance cannot be of type",
                            element.__class__, ". Try SliderWithText or LabelledColorPicker instead.")
        if cls_label:
            self.label = cls_label(label)
        else:
            self.label = _LabelButton(label)
        self.element = element
        super().__init__(children=[self.label, self.element])
        self.sort_children("h", margins=(5,0), gap=5, nx="auto", ny="auto", align="center")
        self.copy_normal_state(True)
        def at_unclick():
            if element.action:
                element.action()
        self.label.default_at_unclick = at_unclick
        if hasattr(element, "get_value"):
            self.get_value = element.get_value
        if hasattr(element, "set_value"):
            self.set_value = element.set_value

class LabelledColorPicker(Labelled):
    """Forms a group with a color picker, on the left side of which a label text is displayed.
    ***Mandatory arguments***
    <label> : a string defining the label of the element.
    <element> : the colorpicker to labellize.
    ***Optional arguments***
    <ok> : string of the validation text
    <cancel> : string of the cancellation text
    <color_size> : 2-tuple for the size of the color thumbnail
    <launch_mode> : either 'launch_nonblocking' or 'launch_blocking' or 'launch_alone'
    """

    def __init__(self, label, element, ok="Ok", cancel="Cancel",
                 color_size=(20,20), launch_mode="launch_alone"):
        if isinstance(element, ColorPickerPredefined):
            validation_choices = (cancel,)
        else:
            validation_choices = (ok,cancel)
        alert = AlertWithChoices(label, validation_choices, children=[element])
        alert.center_on("screen")
        img = pygame.Surface(color_size)
        img.fill(element.get_value())
        imgb = ImageButton("",img,no_copy=True)
        button_col = _ButtonColor("")
        button_col.add_child(imgb)
        button_col.englobe_children()
        super().__init__(label, button_col)
        self.element = element
        self.element.parent = self
        element.alert = alert
        def choose_color():
            color_before = element.get_value()
            getattr(alert, launch_mode)()
            if alert.choice != ok and not(isinstance(alert.choice, tuple)):
                element.set_value(color_before)
            imgb.get_current_frame().fill(element.get_value())
            if isinstance(element, ColorPickerPredefined):
                self.refresh_color_thumbnail()
            alert.choice = None
        def refresh_color_thumbail():
            imgb.get_current_frame().fill(element.get_value())
        self.at_unclick = choose_color
        self.children[-1].at_unclick = choose_color
        self.children[0].at_unclick = choose_color
        self.children[0].action = choose_color
        self.get_value = element.get_value
        self.set_value = element.set_value
        self.refresh_color_thumbnail = refresh_color_thumbail
        if len(validation_choices) > 1:
            alert.get_button(ok)._at_click = refresh_color_thumbail



class TogglablesPool(Element):
    """Provides a way for the user to switch between different, predefined values. Only one value at a time can be chosen.
    Each value is represented by a togglable button. When a button is pressed, all the others are unpressed.
    ***Mandatory arguments***
    <label> : string displayed on the left side of the switches.
    <choices> : sequence of strings.
    <initial_value> : text of the initial value chosen.
    <togglable_type> : (str) either 'toggle', 'radio' or 'checkbox'.
    """

    def __init__(self, label, choices, initial_value, togglable_type="toggle"):
        assert initial_value in choices
        self.label = _LabelButton(label)
        e_choices = []
        self.togglable_type = togglable_type
        def update_pool(tog):
            print("update")
            count = 0
            for e in self.togglables:
                if not(e is tog):
                    e.set_value(False)
                count += e.get_value()
            tog.set_value(False)
            if self.at_unclick:
                self.at_unclick()
        for c in choices:
            if togglable_type == "toggle":
                tog = ToggleButton(c)
                tog._at_click = update_pool
                tog._at_click_params = {"tog":tog}
            elif togglable_type == "radio":
                tog = Labelled(c, Radio())
            elif togglable_type == "checkbox":
                tog = Labelled(c, Checkbox())
            else:
                raise ValueError("You should indicate either 'toggle', 'radio' or 'checkbox'.")
            if togglable_type != "toggle":
                tog.element._at_click = update_pool
                tog.label._at_click = update_pool
                tog.element._at_click_params = {"tog":tog}
                tog.label._at_click_params = {"tog":tog}
            e_choices.append(tog)
            if c == initial_value:
                tog.set_value(True)
        self.togglables = e_choices
        if togglable_type == "toggle":
            sort_mode = "h"
        else:
            sort_mode = "v"
            e_choices = [Box(e_choices)]
        super().__init__(children=[self.label] + e_choices)
        self.sort_children(sort_mode, margins=(5,0), gap=5, nx="auto", ny="auto", align="center")
        self.copy_normal_state(True)
    
    def get_value(self):
        """Returns the text of the chosen element."""
        if self.togglable_type == "toggle":
            for e in self.togglables:
                if e.get_value():
                    return e.text
        else:
            for e in self.togglables:
                if e.get_value():
                    return e.label.text
                
    def get_choice_button(self, text):
        """Returns the choice element corresponding to the text given as argument."""
        for e in self.togglables:
            if e.text == text:
                return e
            




class TextAndImageButton(Button):
    """Button formed of both a text and an image as separate elements.
    Useful when user may not know what the items in a list look like, e.g. typically for inventory lists in games.
    ***Mandatory arguments***
    <text> : string to display
    <img> : pygame surface
    ***Optional arguments***
    <mode> : "h", "v" for horizontal or vertical
    <reverse> : (bool) if True, then image comes first and the text is displayed on its right side.
    <cls> : Thorpy element class to make the button. By default cly = thorpy.Button.
    <margins> :  2-tuple of integers for x- and y-margins (in pixels)
    """

    def __init__(self, text, img, mode="h", reverse=False, cls=Button, margins=(5,5)):
        style_normal = styles.TextStyle()
        style_normal.font_color = Button.style_normal.font_color
        style_hover = style_normal.copy()
        style_hover.font_color = Button.style_hover.font_color
        style_pressed = style_hover.copy()
        e1 = Button(text, style_normal=style_normal, style_hover=style_hover, style_pressed=style_pressed)
        #
        e2 = Image(img)
        if reverse:
            children = [e2,e1]
        else:
            children = [e1,e2]
        super().__init__(text="", children=children)
        if mode is not None:
            self.sort_children(mode,margins=margins,gap=5, nx="auto", ny="auto", align="center")
        self.copy_normal_state(True)

class ToggleButton(Button):
    """Button than stays pressed when user click on it and returns to normal state only after it is clicked again.
    This is typically used to model on/off options.
    ***Mandatory arguments***
    <text> : text of the button shown to the user.
    ***Optional arguments***
    <value> : initial value. Set to False for normal state or True for pressed state.
    """
     


    def __init__(self, text, style_normal=None, style_hover=None,
                    style_pressed=None, generate_surfaces=True, children=None,
                    style_locked=None, value=False):
        Button.__init__(self, text, style_normal, style_hover, style_pressed, False, children, style_locked)
        self.value = value
        self.surfaces["nothoverpressed"] = []
        if generate_surfaces:
            self.generate_surfaces()
        self.action = self.default_at_unclick

    def generate_surfaces(self):
        Button.generate_surfaces(self)
        style = self.styles["pressed"].copy()
        style.font_color = self.styles["normal"].font_color
        # style.shadowgen = None
        self.surfaces["nothoverpressed"] = style.generate_images(self.text)
        self.get_frame = self.get_frame_togglable

    def toggle(self):
        """Use this method to toggle the state (normal to pressed or pressed to normal)"""
        self.value = not self.value

    def default_at_unclick(self): #toggle delegated to click if pressed
        self.toggle()

    # def get_current_style(self):
    #     if self.value and self.state != "hover":
    #         return self.styles["pressed"]
    #     return Button.get_current_style(self)

    def get_current_shadow_frame(self):
        if self.value: #not hover and pressed or hover and pressed
            state = "pressed"
        else:
            state = self.state
        return self.shadows.get(state)[self.i_frame]

    def get_frame_togglable(self, state, it):
        if self.value and state == "hover":
            state = "pressed" #with hovered text
        elif self.value and state != "hover":
            state = "nothoverpressed" #without hovered text
        return self.surfaces[state][it]

    def get_value(self):
        return self.value
    
    def set_value(self, value):
        self.value = value
    


class Checkbox(ToggleButton):
    """Checkbox that can be (un)checked by the user to model an on/off interaction.
    ***Optional arguments***
    <value> : initial value. Set to False for unchecked or True for checked.
    <size> : 2-tuple indicating the size of the element in pixels, or 'auto' for auto size.
    """

    def __init__(self, value=False, size="auto", style_normal=None, generate_surfaces=True):
        ToggleButton.__init__(self, "", value=value, generate_surfaces=False)
        if size == "auto":
            size = self.styles["normal"].font.get_height()-4
            if size < 16:
                size = 16
        for s in styles.ALL_STYLES:
            self.styles[s] = self.styles[s].copy()
            self.styles[s].size = (size,size)
        if generate_surfaces:
            self.generate_surfaces()

    def generate_surfaces(self):
        Button.generate_surfaces(self)
        #1. Resize check sign ###############################################
        from thorpy import fn
        self.check_sign = pygame.image.load(fn("data/check.png"))
        r = self.check_sign.get_rect()
        if r.w > 2*self.check_sign.get_width():
            r = r.inflate((-self.rect.w//3, -self.rect.h//3))
            self.check_sign = pygame.transform.scale(self.check_sign, r.size)
##        self.check_sign.set_colorkey((255,)*3)

        #2. Now, blit check sign on pressed state ###########################
        color_check_sign = self.get_style("pressed").font_color
        graphics.change_color_on_img_ip(self.check_sign, (51,)*3, color_check_sign)
        r = self.check_sign.get_rect()
        for s in self.surfaces["pressed"]:
            r.center = self.rect.center
            r.x -= self.rect.x
            r.y -= self.rect.y
            s.blit(self.check_sign, r.topleft)
        #
        style = self.styles["pressed"].copy()
        graphics.change_color_on_img_ip(self.check_sign, color_check_sign, (51,)*3)
        self.surfaces["nothoverpressed"] = style.generate_images(self.text)
        for s in self.surfaces["nothoverpressed"]:
            r.center = self.rect.center
            r.x -= self.rect.x
            r.y -= self.rect.y
            s.blit(self.check_sign, r.topleft)
        self.get_frame = self.get_frame_togglable


class Radio(Checkbox):
    """Radio button that can be (un)checked by the user to model an on/off interaction.
    ***Optional arguments***
    <value> : initial value. Set to False for unchecked or True for checked.
    <size> : 2-tuple indicating the size of the element in pixels, or 'auto' for auto size.
    """

    def __init__(self, value=False, size="auto", style_normal=None, generate_surfaces=True):
        ToggleButton.__init__(self, "", value=value, generate_surfaces=False)
        if size == "auto":
            # size = self.styles["normal"].font.get_height() - 4
            size = int(self.styles["normal"].font.get_height() * 0.75)
        for s in styles.ALL_STYLES:
            self.styles[s] = self.styles[s].copy()
            self.styles[s].size = (size,size)
        if generate_surfaces:
            self.generate_surfaces()

    def generate_surfaces(self):
        Button.generate_surfaces(self)
        r = self.surfaces["pressed"][0].get_rect()
        for s in self.surfaces["pressed"]:
            r.center = self.rect.center
            r.x -= self.rect.x
            r.y -= self.rect.y
            gfx.filled_circle(s, r.centerx, r.centery, r.w//6, (0,0,255))
            gfx.aacircle(s, r.centerx, r.centery, r.w//6, (0,0,255))
        #
        style = self.styles["normal"].copy()
        self.surfaces["nothoverpressed"] = style.generate_images(self.text)
        for s in self.surfaces["nothoverpressed"]:
            r.center = self.rect.center
            r.x -= self.rect.x
            r.y -= self.rect.y
            gfx.filled_circle(s, r.centerx, r.centery, r.w//6, (0,0,0))
            gfx.aacircle(s, r.centerx, r.centery, r.w//6, (0,0,0))
        self.get_frame = self.get_frame_togglable

class SwitchButton(Button):
    """Switch button that can be (un)checked by the user to model an on/off interaction.
    ***Optional arguments***
    <value> : initial value. Set to False for unchecked or True for checked.
    <size> : 2-tuple indicating the size of the outer switch in pixels, or 'auto' for auto size.
    <drag_size> : 2-tuple indicating the size of the inner switch in pixels, or 'auto' for auto size.
    """

    def __init__(self, value=False, size="auto", drag_size="auto", style_normal=None):
        Button.__init__(self, "",style_normal=style_normal, generate_surfaces=False)
        self.value = value
        if not style_normal:
            style_normal = self.__class__.style_normal.copy()
        self.styles = {"normal":style_normal,
                       "hover":self.__class__.style_hover.copy(),
                        "pressed":self.__class__.style_pressed.copy(),
                        "locked":self.__class__.style_locked.copy()}
        if size == "auto":
            size = ("auto",)*2
        if size[0] is None or size[0] == "auto":
            size = (50, size[1])
        if size[1] is None or size[1] == "auto":
            size = (size[0], self.styles["normal"].font.get_height()+self.styles["normal"].margins[1]*2)
        if drag_size[0] is None or drag_size[0] == "auto":
            drag_size = (25, drag_size[1])
        if drag_size[1] is None or drag_size[1] == "auto":
            drag_size = (drag_size[0], size[1]-6)
        self.margin_x = 2
        self.set_style_attr("size", size, refresh=True)
        self.dragger = Button("", generate_surfaces=False)
        self.dragger.copy_normal_state(True)
        color_dragger = darken(self.styles["normal"].bck_color)
        self.dragger.set_style_attr("bck_color", color_dragger, refresh=False)
        self.dragger.set_style_attr("size", drag_size, refresh=False)
        self.dragger.set_style_attr("shadowgen", None, refresh=False)
        self.dragger.set_style_attr("nframes", 1, refresh=True)
        self.add_child(self.dragger)
        self.refresh_dragger_pos()
        self.action = self.default_at_unclick

    def get_value(self):
        return self.value

    def default_at_click(self):
        self.value = not(self.value)
        self.refresh_dragger_pos()

    def refresh_dragger_pos(self):
        if not self.value:
            self.dragger.stick_to(self,"left","left",(self.margin_x,0))
##            self.set_bck_color((255,0,0),"normal")
        else:
            self.dragger.stick_to(self,"right","right",(-self.margin_x,0))
##            self.set_bck_color((0,0,255),"normal")

class SwitchButtonWithText(Element):
    """Switch button that can be (un)checked by the user to model an on/off interaction. The difference with
    the normal SwitchButton is that this one switches between two texts that are displayed next to the widget.
    ***Mandatory arguments***
    <title> : label value on the left side of the element.
    <texts> : 2-tuple containing two strings (one for each state of the switch, e.g ('on','off')).
    ***Optional arguments***
    <value> : initial value. Set to False for unchecked or True for checked.
    <size> : 2-tuple indicating the size of the outer switch in pixels, or 'auto' for auto size.
    <drag_size> : 2-tuple indicating the size of the inner switch in pixels, or 'auto' for auto size.
    """

    def __init__(self, title, texts, value=False, size=(None,None), drag_size=(None,None),
                 style_normal=None):
        self.texts = texts
        self.switch = SwitchButton(value, size, drag_size, style_normal)
        self.right_text = Text(self.get_value())
        self.left_text = _LabelButton(title)
        self.adapt_to_text = True
        Element.__init__(self, [self.left_text, self.switch, self.right_text])
        self.englobe_children()
        self.sort_children("h")
        self.action = self.switch.action
        # self.left_text.default_at_click = self.action
        self.left_text.default_at_unclick = self.switch.default_at_click
        

    def get_value(self):
        return self.texts[self.switch.value]

    def update(self, mouse_delta):
        self.right_text.set_text(self.get_value(), adapt_parent=self.adapt_to_text, only_if_different=True)
        return Element.update(self, mouse_delta)
        

class Image(Element):
    """
    Image surface that can be used as a GUI element taking all standard element states
    (normal, hover, pressed, locked) and actions.
    ***Mandatory arguments***
    <img> : a pygame surface.
    """

    def __init__(self, img, style_normal=None, generate_surfaces=True, children=None):
        Element.__init__(self, children)
        self.copy_normal_state(True)
        self.img = img
        self.state = "normal"
        if not style_normal:
            style = self.__class__.style_normal.copy()
        else:
            style = style_normal
        self.styles = {"normal":style, "hover":style,
                        "pressed":style, "locked":style}
        self.text = ""
        if generate_surfaces:
            self.generate_surfaces()


    def refresh_surfaces_build(self):
        for key, style in self.styles.items():
            if style:
                self.surfaces[key] = style.generate_images(self.img)
        self.has_surfaces_generated = True
        self.refresh_surfaces_shadow()

    def refresh_surfaces_copy(self):
        s = self.styles["normal"].generate_images(self.img)
        for key in self.styles.keys():
            self.surfaces[key] = s
        self.has_surfaces_generated = True
        self.refresh_surfaces_shadow()


class ImageButton(Button):
    """Image that behaves like a button.
    ***Mandatory arguments***
    <text> : string to display on the image (can be empty if needed).
    <img> : a pygame surface.
    ***Optional arguments***
    <no_copy> : set it to True if you want a copy of the image for each state of the button (slower at initialization).
    """

    def __init__(self, text, img, img_hover=None, img_pressed=None, img_locked=None, no_copy=False):
        if img_hover is None:
            if no_copy:
                img_hover = img
            else:
                img_hover = img.copy()
        if img_locked is None:
            if no_copy:
                img_locked = img
            else:
                img_locked = img.copy()
        if img_pressed is None:
            if no_copy:
                img_pressed = img
            else:
                img_pressed = img.copy()
        self.imgs = {"normal":img, "hover":img_hover, "pressed":img_pressed, "locked":img_locked}
        Button.__init__(self, text)


    def refresh_surfaces_build(self):
        for key, style in self.styles.items():
            if style:
                self.surfaces[key] = style.generate_images(self.imgs[key], self.text)
        self.has_surfaces_generated = True
        self.refresh_surfaces_shadow()

    def refresh_surfaces_copy(self):
        s = self.styles["normal"].generate_images(self.imgs["normal"], self.text)
        for key in self.styles.keys():
            self.surfaces[key] = s
        self.has_surfaces_generated = True
        self.refresh_surfaces_shadow()


class AnimatedGif(Image):
    """Animation that can be used as a GUI element taking all standard element states
    (normal, hover, pressed, locked) and actions. 
    ***Mandatory arguments***
    <filename> : filename of a gif file. The frames will automatically be extracted to form pygames surfaces.
    You can also directly provide a sequence of pygame surfaces that are all of the same size.
    ***Optional arguments***
    <frame_mod> : number of logics updates between each frame update. Can be seen as the slowness of the animation. Must be at least 1.
    <size_factor> : 2-tuple of positive real values corresponding to the size multiplicator of the original images to produce the actual images.
    <loops> : number of times the animation must be played. Can be any integer or float('inf').
    <freeze_frame> : number of the frame to display if the animation is not played. Set to None to hide the element when not played.
    """

    def __init__(self, filename, frame_mod=2, size_factor=(1.,1.), loops=float("inf"),
                 freeze_frame=0, generate_surfaces=True):
        style_normal = styles.MultipleImagesStyle()
        if isinstance(filename, str):
            imgs = graphics.extract_frames(filename, size_factor=size_factor)
        else:
            imgs = filename
        super().__init__(imgs, style_normal, generate_surfaces, children=None)
        style_normal.frame_mod = frame_mod
        self.loops = loops
        self.freeze_frame = freeze_frame

    def update_iframe(self):
        style = self.get_current_style()
        if self.loops > 0 and style and style.frame_mod > 0:
            if self.it % style.frame_mod == 0:
                self.i_frame += 1
            if self.i_frame == style.nframes:
                self.i_frame = 0
                self.loops -= 1
        else:
            self.i_frame = 0
        if self.loops <= 0:
            if self.freeze_frame is None:
                self.set_invisible(True)
            self.i_frame = self.freeze_frame

    def update(self, mouse_delta):
        """_Update state of the element. Return True if element was dragged."""
        if self.state == "locked":
            return False
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        dragged = False #self has been dragged ?
##        self.being_dragged = False
        children_dragged = False
        for e in self.children:
            children_dragged += e.update(mouse_delta)
        #Caution : self.state may be changed by children
        really_active = self.state != "unactive" and self.state != "locked"
        if not really_active:
            self.it += 1
        else:
            self.rect = self.get_rect()
            if self.rect.collidepoint(mouse_pos):
                if mouse_pressed[0]: #left click
                    if not self.other_is_dragged():
                        if self.state != "pressed":
                            # self.i_frame = 0
                            self.state = "pressed"
                            if self._at_click:
                                self.draw()
                                pygame.display.update(self.rect)
                                self._at_click(**self._at_click_params)
                            self.default_at_click()
                        if not children_dragged:
                            if self.draggable_x or self.draggable_y:
                                p.element_being_dragged = self
                                self.drag_if_needed(mouse_delta)
                                dragged = True
                                self.being_dragged = True
                else: #mouse not pressed
                    self.being_dragged = False
                    if self.state == "pressed":
                        # self.i_frame = 0
                        self.state = "hover"
                        if self.at_unclick:
                            self.at_unclick(**self.at_unclick_params)
                        self.default_at_unclick()
                    elif self.state != "hover":
                        # self.i_frame = 0
                        self.state = "hover"
                        # if self.hand_cursor:
                        #     pygame.mouse.set_cursor(cursor_hand)
                        if self.at_hover:
                            self.at_hover(**self.at_hover_params)
                        self.default_at_hover()
            else: #mouse do not collide with element
                if self.being_dragged:
                    dragged = False
                    if not mouse_pressed[0]:
                        self.being_dragged = False
                    else:
                        self.drag_if_needed(mouse_delta)
                        if self.rect.collidepoint(mouse_pos):
                            dragged = True
                else:
                    if self.state == "hover":
                        # self.i_frame = 0
                        self.state = "normal"
                        if self.hand_cursor:
                            pygame.mouse.set_cursor(cursor_arrow)
                        if self.at_unhover:
                            self.at_unhover(**self.at_unhover_params)
                        self.default_at_unhover()
                        self.being_dragged = False
                    if self.state != "normal":
                        # self.i_frame = 0
                        self.state = "normal"
            self.it += 1
            self.update_iframe()
        if self.state == "hover" and self.hand_cursor:
            pygame.mouse.set_cursor(cursor_hand)
        return dragged
        



class ArrowButton(Button):
    """Button displaying an arrow (e.g in scrollbars).
    ***Mandatory arguments***
    <orientation> : string in ['up', 'down', 'left', 'right']
    <size> : 2-tuple of ints (pixels) or 'auto'
    """

    def __init__(self, orientation, size):
        self.orientation = orientation
        Button.__init__(self, "", generate_surfaces=False)
        # self.set_bck_color((255,0,0), "pressed")
        self.set_style_attr("size",size)


    def refresh_surfaces_build(self):
        for key, style in self.styles.items():
            if style:
                self.surfaces[key] = style.generate_images(self.text, self.orientation)
        self.has_surfaces_generated = True
        self.refresh_surfaces_shadow()

    def refresh_surfaces_copy(self):
        s = self.styles["normal"].generate_images(self.text, self.orientation)
        for key in self.styles.keys():
            self.surfaces[key] = s
        self.has_surfaces_generated = True
        self.refresh_surfaces_shadow()








class Line(Element):
    """Graphical line separator that is either vertical or horizontal.
    ***Mandatory arguments***
    <mode> : either 'v' or 'h' (vertical or horizontal).
    <length> : length in pixels (integer).
    ***Optional arguments***
    <thickness> : thickness of the line in pixels.
    """

    def __init__(self, mode, length, thickness=3, style_normal=None, generate_surfaces=True,
                 copy_normal_state=True):
        Element.__init__(self)
        self.state = "normal"
        if not style_normal:
            style_normal = self.__class__.style_normal.copy()
        self.styles = {"normal":style_normal,
                       "hover":self.__class__.style_hover.copy(),
                        "pressed":self.__class__.style_pressed.copy(),
                        "locked":self.__class__.style_locked.copy()}
        if copy_normal_state:
            self.copy_normal_state(True)
        if mode == "h":
            self.styles["normal"].size = (length,thickness)
        elif mode == "v":
            self.styles["normal"].size = (thickness,length)
        if generate_surfaces:
            self.generate_surfaces()

class Slider(Element):
    """Provides a way to pick a value in the range [0,1].
    Note that in most cases you probably want to use SliderWithText instead, as this is a slider with nothing else.
    ***Mandatory arguments***
    <mode> : either 'h' (horitontal) or 'v' (vertical).
    <length> : length of the slider bar along the axis defined by the mode.
    ***Optional arguments***
    <thickness> : thickness of the slider bar.
    <set_when_click> : (bool) set the value when user click the slider's bar (instead of the cursor)
    <dragger_height> : (int or 'auto') length of the dragger in pixels.
    <dragget_length> : (int or 'auto') height of the dragger in pixels.
    """

    def __init__(self, mode, length, thickness=5, dragger_length='auto',
                 dragger_thick_factor=-1,
                 set_when_click=True,
                 dragger_height='auto'):
        dragger_length = None if dragger_length == 'auto' else dragger_length
        dragger_height = None if dragger_height == 'auto' else dragger_height
        self.bar = _SliderBar(mode, length, thickness)
        #Note that dragger limit doesnt have to be controlled when dragged, since
        #it is naturally locked to its parent through cannot_drag_outside.
        self.set_when_click = set_when_click
        self.at_modif = None
        self.mode = mode
        if mode == "h":
            styles = []
            for s in ["normal", "hover", "pressed", "locked"]:
                style = getattr(_DraggerButton, "style_"+s).copy()
                if style.size != "auto":
                    size = [style.size[1],style.size[0]]
                    if dragger_length:
                        size[0] = dragger_length
                    if dragger_thick_factor == "auto":
                        size = (size[0], get_text_height())
                    elif dragger_thick_factor > 0:
                        size[1] *= dragger_thick_factor
                    elif dragger_height:
                        size[1] = dragger_height
                    style.size = tuple(size)
                styles.append(style)
            self.dragger = _DraggerButton(" ", styles[0], styles[1], styles[2], style_locked=styles[-1])
            self.dragger.draggable_x = True
        elif mode == "v":
            styles = []
            for s in ["normal", "hover", "pressed", "locked"]:
                style = getattr(self.__class__, "style_"+s).copy()
                size = [style.size[0],style.size[1]]
                if style.size != "auto":
                    if dragger_length:
                        size[1] = dragger_length
                    if dragger_thick_factor == "auto":
                        size = (size[0], get_text_height())
                    elif dragger_thick_factor > 0:
                        size[0] *= dragger_thick_factor
                    style.size = tuple(size)
                styles.append(style)
            self.dragger = _DraggerButton(" ", styles[0], styles[1], styles[2], style_locked=styles[-1])
            self.dragger.draggable_y = True
        else:
            raise Exception("Slider mode must be either 'h' or 'v'.")
        self.dragger.cannot_drag_outside = False
        Element.__init__(self, [self.bar, self.dragger])
        self.englobe_children()
        self.exact_value = 0. #may differ to pixel-bound position of cursor
        self.set_relative_value(self.exact_value)
        self.control_dragger_pos()
        self.bar.default_at_click = self.bar_click
        


    def get_relative_value(self):
        # dx = 0 #dead zone size
        if self.mode == "h":
            delta = self.dragger.rect.left - self.bar.rect.left
            delta_max = self.bar.rect.width - self.dragger.rect.width #amount of pix in which we can move
        else:
            delta = self.dragger.rect.top - self.bar.rect.top
            delta_max = self.bar.rect.height - self.dragger.rect.height
        value = delta / delta_max
        if value < 0:
            value = 0
        elif value > 1:
            value = 1
        return value

    def get_value(self):
        """Returns the value of the slider in the range [0,1], 0 beeing the minimum and 1 the maximum
        value that the slider can take."""
        return self.get_relative_value()

    def set_relative_value(self, value):
        """Set the value of the slider in the range [0,1], 0 beeing the minimum and 1 the maximum
        value that the slider can take."""
        self.exact_value = value
        if self.mode == "h":
            y = self.bar.rect.centery
            x = value * (self.bar.rect.w - self.dragger.rect.w) + self.bar.rect.left
            self.dragger.set_center(x + self.dragger.rect.w//2, y)
        elif self.mode == "v":
            x = self.bar.rect.centerx
            y = value * (self.bar.rect.h - self.dragger.rect.h) + self.bar.rect.top
            self.dragger.set_center(x, y + self.dragger.rect.h//2)
        if self.at_modif:
            self.at_modif(None, None)

    def control_dragger_pos(self):
        """_Ensure that the dragger is in between the min and max."""
        if self.mode == "v":
            dy = self.dragger.rect.top - self.bar.rect.top
            yf = 0
            dx = self.dragger.rect.centerx - self.bar.rect.centerx
            if dy < 0:
                yf = -1
            else:
                dy = self.dragger.rect.bottom - self.bar.rect.bottom
                if dy > 0:
                    yf = -1
            self.dragger.move(-dx,dy*yf)
        else:
            dx = self.dragger.rect.left - self.bar.rect.left
            xf = 0
            if dx < 0:
                xf = -1
            else:
                dx = self.dragger.rect.right - self.bar.rect.right
                if dx > 0:
                    xf = -1
            dy = self.dragger.rect.centery - self.bar.rect.centery
            self.dragger.move(dx*xf,-dy)


    def update(self, mouse_delta):
        dragged = Element.update(self, mouse_delta)
        self.control_dragger_pos()
        return dragged

    def bar_click(self):
        if self.set_when_click:
            pos = pygame.mouse.get_pos()
            if not self.dragger.rect.collidepoint(pos):
                self.dragger.set_topleft(*pos)
                self.control_dragger_pos()
                if self.at_modif:
                    self.at_modif(None, None)
                
    
    def function_to_call(self, func):
        self.at_modif = func
        self.dragger.at_drag = func









class DropDownList(Box):
    """_List of choices (buttons) that is launched by a DropDownListButton instance.
    ***Mandatory arguments***
    <launcher> : launcher element (instance of DropDownListButton).
    <choices> : sequence of strings or elements.
    ***Optional arguments***
    <choice_mode> : either 'v' or 'h' (vertical or horizontal).
    <align> : alignement of the choices in the list. Either 'center' (for both vertical and horizontal mode) or 'left', 'right' (for horizontal mode) or 'top', 'bottom' (for vertical mode)
    <gap> : (int) space between two choice in the list (in pixels).
    <all_same_width> : (bool) forces each choice button to be the same width as the others.
    <bck_func> : function to be called each frame when menu is launched.
    <overwrite_choices> : (bool) if True, the behaviour of the potential elements passed in choices is shadowed.
    <size_limit> : 2-tuple of integers to define the maximum size of the box in which choices are displayed.
    <generate_shadow> : 2-tuple whose first value is a boolean stating whether a shadow should be generated for the list,
    and whose second value is either 'auto' or a boolean stating whether the shadow generation should be done in fast mode.
    """

    def __init__(self, launcher, choices, choice_mode="v", bck_func=None,
                overwrite_choices=True, size_limit="auto", generate_shadow=(True,"auto"),
                align=None, gap=5, all_same_width=True):
        if size_limit == "auto":
            size_limit = ("auto",)*2
        self.choice = None
        self.choice_element = None
        buttons = []
        for e in choices:
            if isinstance(e, str): #then e is the text of the choice
                b = _DropDownButton(e)
                b.at_unclick = choice
                b.at_unclick_params = {"alert":self, "element":b, "ddl":True}
                buttons.append(b)
            else:
                buttons.append(e)
                if overwrite_choices:
                    e.at_unclick = choice
                    e.at_unclick_params = {"alert":self, "element":e, "ddl":True}
        group_buttons = Group(buttons, choice_mode)
        # children = [group_buttons]
        style = DropDownList.style_normal.copy()
        style.radius = 0
        self.launcher = launcher
        #sort elements as grid:
        # Box.__init__(self, buttons, style_normal=style, scrollbar_if_needed=True,
        #              sort_immediately=False)
        # self.sort_children("grid")
        Box.__init__(self, buttons, style_normal=style, scrollbar_if_needed=True,
                     size_limit=size_limit,
                     sort_immediately=False,
                     generate_surfaces=False)
        if align is None:
            if choice_mode == "v":
                align = "left"
            elif choice_mode == "h":
                align = "center"
        if all_same_width:
            max_w = max([e.rect.width for e in buttons])
            for e in buttons:
                e.set_size((max_w, e.rect.h))
        self.sort_children(mode=choice_mode, align=align, gap=gap)
        #placement of the box
        self.clamp(p.screen.get_rect())
        self.children_rect = None
        if self.parent:
            bottom = self.parent.bottom
        else:
            bottom = p.screen.get_size()[1]
        #resizing the box if too tall
        if self.rect.bottom > bottom:
            w,h = self.rect.size
            self.set_size((w,bottom-self.rect.top), adapt_parent=False)
        self.clip_children()
        self.set_topleft(*launcher.get_rect().bottomleft)
        self.choice_buttons = group_buttons
        self.bck_func = bck_func
        if generate_shadow[0]:
            shadow_fast = auto_set_fast(self, generate_shadow[1])
            self.generate_shadow(shadow_fast)
        # self.action = self.launcher.at_unclick

    # def launch_nonblocking(self, loop=None, click_outside_cancel=True):
    #     return super().launch_nonblocking(loop, click_outside_cancel)






class Lifebar(Group):
    """Lifebar or loading bar that displays how much is left of a given quantity between 0% and 100%.
    Hence, the value of a Lifebar is always a float between 0. and 1.
    ***Mandatory arguments***
    <text> : string to display on the bar.
    <length> : length of the bar in pixels.
    ***Optional arguments***
    <bck_color> : background color of the bar. By default, it takes the current theme bck color for Button.
    <height> : height of the bar in pixels.
    <initial_value> : initial value between 0 and 1.
    <font_color> : font_color in RGB format.
    <auto_adapt_length> : (bool) if True and the specified length is too short for the text,
    then the length is adjusted to fit the text.
    <auto_show_percentage> : (bool) if True, then the text is replaced by a text
    indicating the current percentage of the bar.
    """

    def __init__(self, text, length, bck_color=None, height=None, initial_value=1., font_color=None,
                 auto_adapt_length=True, auto_show_percentage=None):
        from .themes import get_theme_main_bck_color
        if bck_color is None:
            bck_color = get_theme_main_bck_color()
        self.auto_show_percentage = auto_show_percentage
        if self.auto_show_percentage:
            text = str(int(initial_value * 100)) + "%"
        self.life_text = Text(text, font_color=font_color)
        #
        style_frame = styles.FrameStyle() #TODO write wrappers to customize children
        self.e_frame = DeadButton("", style_frame)
        if auto_adapt_length and self.life_text.rect.w > length - 5:
            length = self.life_text.rect.w + 5
        self.e_frame.set_size((length, height))
        #
        style_rect = styles.SimpleStyle()
        style_rect.bck_color = bck_color
        style_rect.size = self.e_frame.rect.inflate((-style_frame.border_thickness,)*2).size
        self.e_rect = DeadButton("",style_rect)
        #
        self.life_text.center_on(self.e_rect)
        self.e_frame.center_on(self.e_rect)
        #
        self.max_length = length
        super().__init__([self.e_frame, self.e_rect, self.life_text, ], None)
        self.englobe_children()
        self.value = initial_value
        if initial_value != 1.:
            self.set_value(initial_value)

    def auto_text_refresh(self):
        text = self.get_str_value_times() + "%"
        self.life_text.set_text(text, adapt_parent=False)
        self.life_text.center_on(self.e_frame)

    def set_value(self, value):
        """The value of a lifebar must be greater than zero. It will automatically be set to zero if you put greater value."""
        value = 0 if value < 0 else value
        self.value = value
        x = self.e_rect.rect.x
        size = value*self.max_length
        self.e_rect.set_size((size, None), False, False)
        self.e_rect.set_topleft(x, self.e_rect.rect.y)
        if self.auto_show_percentage:
            self.auto_text_refresh()

    def get_value(self):
        return self.value
        # return self.e_rect.get_current_width() / self.max_length
    
    def get_str_value_times(self, factor=100, rounding=-1):
        """Return the value of the bar times a given factor. By default, the factor is 100 so that
        the value can be interpreted as a percentage.
        ***Optional arguments***
        <factor> : the factor that multiplies the value.
        <rounding> : negative value means round as integer. Other values use Python built-in round function with
        *rounding* decimals.
        """
        val = self.get_value()*factor
        if rounding < 0:
            return str(int(val))
        return str(round(val, rounding))
    
    def set_size(self, size, adapt_parent=True, adapt_text=False):
        # self.generate_frame(length=size[0], height=size[1])
        super().set_size(size, adapt_parent, adapt_text)
    
    # def generate_frame(self, rect_color=(255,)*3, frame_color=(0,0,0), frame_thickness=1,
    #                    length=None, height=None):
    #     style_frame = styles.FrameStyle()
    #     style_frame.border_color = frame_color
    #     style_frame.border_thickness = frame_thickness
    #     self.e_frame.refresh_surfaces()
    #     #
    #     style_rect = styles.SimpleStyle()
    #     style_rect.bck_color = rect_color
    #     style_rect.size = self.e_frame.rect.inflate((-style_frame.border_thickness,)*2).size
    #     self.e_rect.refresh_surfaces()
    #     #
    #     self.life_text.center_on(self.e_rect)


    
class WaitingBar(Lifebar):
    """Auto-animated element indicating to the user he has to wait
    (typically used during loading sequences). Note that a global waiting_bar can be defined with
    thorpy.set_waiting_bar function.
    Then, it can be refreshed from any place of the code with thorpy.refresh_waiting_bar().
    ***Mandatory arguments***
    <text> : the text to be displayed on the bar (can be empty).
    ***Optional arguments***
    <length> : the length in pixels of the bar.
    <rect_color> : the color of the moving rect of the animation.
    <speed> : the speed of the moving rect of the animation.
    <rel_width> : the length of the moving rect, relatively to the length of the bar.
    <height> : the height of the bar (thickness).
    <font_color> : 3-tuple (RGB) indicating the color of the text to show, if any. If None,
    the default font_color will be used.
    <auto_adapt_length> : (bool) if True and the specified length is too short for the text,
    then the length is adjusted to fit the text.
    """

    def __init__(self, text, length=200, rect_color=None, speed=1., rel_width=0.2,
                 height=None, font_color=None, auto_adapt_length=True):
        self.speed = speed
        if rect_color is None:
            rect_color = graphics.get_main_color(Button.style_normal.bck_color)
        super().__init__(text, length, rect_color, height, rel_width, font_color, auto_adapt_length)
        self.remove_child(self.e_rect)
        self.e_frame.add_child(self.e_rect)
        self.e_rect.cannot_draw_outside = True
        self.center_on(p.screen)
        

    def update(self, mouse_delta):
        if self.e_rect.rect.left >= self.e_frame.rect.right:
            self.e_rect.set_topright(self.e_frame.rect.left, None)
        else:
            self.e_rect.move(self.speed, 0)
        return super().update(mouse_delta)
    
    def refresh(self):
        """Function to call each time you want the waiting bar to be updated and drawn on screen."""
        self.update((0,0))
        self.draw()
        pygame.display.flip()

class DeadButton(Text):
    """Element that looks like a button but do not react when pressed or hovered.
    ***Mandatory arguments***
    <text> : string to display on the button.
    ***Optional arguments***
    <max_width> : set to True to automatically insert line breaks when size exceeds the max width.
    <font_color> : font_color in RGB format.
    <font_size> : (integer) font_size.
    """

    def __init__(self, text, style_normal=None, generate_surfaces=True,
                 only_normal=True, max_width=None, font_color=None, font_size=None):
        super().__init__(text, font_size, font_color, style_normal,
                        generate_surfaces, only_normal, max_width)


class ShowFPS(Text):
    """Text displaying the current FPS of the app.
    ***Mandatory arguments***
    <clock> : pygame.Clock instance that is used to controle the framerate of your app.
    ***Optional arguments***
    <pre> : string displayed on the left of the FPS.
    <post> : string displayed on the right of the FPS.
    <font_color> : font_color in RGB format.
    <font_size> : (integer) font_size.
    """

    def __init__(self, clock, pre="", post="", font_size=None, font_color=None,
                 style_normal=None, generate_surfaces=True, only_normal=True):
        self.pre = pre
        self.post = post
        self.clock = clock
        text = self.pre + str(60) + self.post
        super().__init__(text, font_size, font_color, style_normal, generate_surfaces, only_normal, None)
        self.adapt_parent = False

    def update(self, mouse_delta):
        text = self.pre + str(round(self.clock.get_fps())) + self.post
        self.set_text(text, adapt_parent=self.adapt_parent)
        return super().update(mouse_delta)

class TkDialog(Labelled):
    """Uses Tkinter to browse files on the user's machine.
    ***Mandatory arguments***
    <label> : a string defining the label of the element.
    <tk_dialog> : the tkinter dialog launch, e.g. askfolder, askfiles, etc.
    Can also be a string in 'filename', 'filenames', 'folder', 'save'. 
    ***Optional arguments***
    <initial_value> : (str) the initial value of the element.
    <basename> : (bool) keep only the basename of the path.
    <extension> : (bool) keep the extension of the file.
    <filetypes> : sequence like [("Excel files", ".xlsx .xls"), ...]
    <initial_dire> : initial location.
    <cls_label> : a Thorpy element class to be used as the label (default is Text).
    <cls_text> : a Thorpy element class to be used as the element displaying
    the value from the tkinter dialog (default is Text).
    """

    def __init__(self, label, tk_dialog, initial_value="...",
                 basename=True, extension=True,
                 filetypes=None, initial_dir="./",
                 cls_label=None, cls_text=None):
        from tkinter import filedialog as fd
        tk_dialog = tk_dialog.lower()
        if tk_dialog == "folder" or tk_dialog == "directory":
            self.tk_dialog = fd.askdirectory
        elif tk_dialog == "filename":
            self.tk_dialog = fd.askopenfilename
        elif tk_dialog == "filenames":
            self.tk_dialog = fd.askopenfilenames
        elif tk_dialog == "save":
            self.tk_dialog = fd.asksaveasfilename
        if cls_text is None:
            cls_text = Text
        self.initial_value = initial_value
        self.tk_dialog_value = cls_text(initial_value)
        self.tk_dialog_value.hand_cursor = True
        self.basename = basename
        self.extension = extension
        self.filetypes = filetypes
        self.initial_dir = initial_dir
        super().__init__(label, self.tk_dialog_value, cls_label)
        self.tk_dialog_value.default_at_unclick = self.default_at_unclick
        self.label.default_at_unclick = self.default_at_unclick
        self.action = self.default_at_unclick

    def clean_value(self, value):
        if self.basename:
            value = os.path.basename(value)
        if not self.extension:
            e = value.split(".")[-1]
            value = value.replace("."+e,"")
        return value

    def default_at_unclick(self):
        if self.filetypes:
            value = self.tk_dialog(initialdir=self.initial_dir, filetypes=self.filetypes)
        else:
            value = self.tk_dialog(initialdir=self.initial_dir)
        if not(isinstance(value,str)):
            value = [self.clean_value(v) for v in value]
            value = "\n".join(value)
        else:
            value = self.clean_value(value)
        self.tk_dialog_value.set_text(value)
    
    def get_value(self):
        return self.tk_dialog_value.get_value()


class HeterogeneousTexts(Group):
    """Group of text elements with different styles.
    ***Mandatory arguments***
    <texts> : a sequence on the form [(text, properties), ...], where the properties are
    given as a dictionnary, e.g. {"size":12, "name":"arial", "color":(255,0,0)}.
    ***Optional arguments***
    <mode> : "v", "h", "grid" or None. Specify None if you do not want to sort elements.
    <margins> : 2-tuple of integers for x- and y-margins (in pixels)
    <gap> : integer value for the spacing between elements (in pixels)
    <nx> : number of columns if grid mode is used, or 'auto'
    <ny> : number of lines if grid mode is used, or 'auto'
    <align> : alignement of the choices in the list. Either 'center' (for both vertical and horizontal mode) or 'left', 'right' (for horizontal mode) or 'top', 'bottom' (for vertical mode)
    """

    def __init__(self, texts, mode="h", margins=(5, 0), gap=0, nx="auto", ny="auto", align="auto"):
        elements = []
        if align == "auto":
            if mode == "h":
                align = "bottom"
            elif mode == "v":
                align = "left"
            else:
                align = "center"
        for text, properties in texts:
            e = Text(text, generate_surfaces=False)
            e.set_style_attr("margins", (0,0), refresh=False)
            for property_name, value in properties.items():
                e.set_style_attr("font_"+property_name, value, refresh=False)
            e.generate_surfaces()
            elements.append(e)
        super().__init__(elements, mode, margins, gap, nx, ny, align)





#Elements classes starting with underscore are not meant to be used by end-user code. They are wrappers for style behaviour.
class _DropDownButton(Button):
    ...

class _LabelButton(Button):
    ...

class _DraggerButton(Button):
    ...

class _SliderBar(Line):
    ...

class _ColorFrameForColorPicker(DeadButton):
    ...

class _ButtonColor(Button):
    ...