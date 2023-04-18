"""***summary***


<b>By 'element' we mean any UI element, widget or component</b> of any type
(e.g. buttons, text input, sliders, etc).<br><br>

<b>You can read-access an element's rect with : <code>my_element.rect</code>.</b>
Regarding modifications, there are methods for manipulating position an size of the elements (see below),
it is your responsibility not to modify the rect directly.<br><br>

<b>All the methods presented below can be called on any Thorpy element.</b> They are primarily defined
in the file canonical.py for the Element class, and maybe redefined for the specialized class
of your element in elements.py. <br><br>

"""
import pygame
from . import sorting
from . import shadows
from . import parameters as p
from . import loops
import warnings

arrow_cursor = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW)
hand_cursor = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)


def get_blit_rects(parent_rect, rect):
        if not parent_rect:
            return rect, None
        pr = parent_rect.inflate((-3,-3))
        sr = rect
        if pr.contains(sr):
            return rect, None
        clip = sr.clip(pr)
        area = pygame.Rect(0,0,clip.width,clip.height)
        if sr.y < pr.y:
            area.y = sr.height - clip.height
        if sr.x < pr.x:
            area.x = sr.width - clip.width
        return clip, area

class Element:
    current_id = 0
    style_normal = None
    style_hover = None
    style_pressed = None
    style_locked = None
    hand_cursor = None
    multi_shadows = False

    @classmethod
    def iter_styles(cls):
        yield cls.style_normal
        yield cls.style_hover
        yield cls.style_pressed
        yield cls.style_locked

    #classmethod
    def get_class_style(cls, state):
        if state == "normal": return cls.style_normal
        elif state == "hover": return cls.style_normal
        elif state == "pressed": return cls.style_normal
        elif state == "locked": return cls.style_normal

    def __init__(self, children=None):
        """_Abstract element used as the basis for all graphical elements."""
        self.parent = None
        self.surface = p.screen
        self.children = children
        self.helper = None
        if children is None:
            self.children = []
        else:
            for c in self.children:
                c.parent = self
        self.rect = pygame.Rect(0,0,0,0)
        self.last_sorted = None
        self.text = ""
        self.styles = {"normal":None, "hover":None, "pressed":None, "locked":None}
        self.surfaces = {"normal":[], "hover":[], "pressed":[], "locked":[]}
        self.shadows = {"normal":[], "hover":[], "pressed":[], "locked":[]}
        self.multi_shadows = self.__class__.multi_shadows
        self.state = "unactive"
        self.refresh_surfaces = self.refresh_surfaces_build
        self.get_current_frame = self.get_current_frame_normal
        self.it = 0
        self.i_frame = 0
        self.special_frames = None
        self.draggable_x = False
        self.draggable_y = False
        self.being_dragged = False
        self.cannot_drag_outside = True
        self.cannot_draw_outside = False
        self._at_click = None
        self._at_click_params = {}
        self.at_unclick = None
        self.at_unclick_params = {}
        self.at_hover = None
        self.at_hover_params = {}
        self.at_unhover = None
        self.at_unhover_params = {}
        self.at_drag = None
        self.at_drag_params = {}
        self.at_cancel = None
        self.action = self.default_at_unclick
        self.hand_cursor = self.__class__.hand_cursor
##        self._at_click_outside = None
##        self._at_click_outside_params = {}
        self.loop_give_back = None
        self.ignore_for_sorting = False
        self.clamp_rect = None
        self.last_player = None
        self.id = Element.current_id
        self.has_surfaces_generated = False
        Element.current_id += 1

    def __repr__(self):
        return str(self.__class__.__name__) + "(id=" + str(self.id) + ")"
    
    # @property
    # def topleft(self):
    #     return self.rect.topleft
    
    # @property
    # def center(self):
    #     return self.rect.center

    

    #--- Styling ---#

    def set_bck_color(self, color, states="all", copy_style=True, refresh=True, apply_to_children=False):
        """Set the background color of the element (depending on how its style handles it).
        ***Mandatory arguments***
        <color> : either a RGB or RGBA color, or an gradient color (see tagged example).
        ***Optional arguments***
        <states> : either 'all' or any state name (e.g. 'hover') or a sequence of state names (excluding 'all').
        <copy_style> : (bool) make a copy of the current style, so that it does not affect element sharing the same style object.
        <refresh> : (bool) refresh element surfaces.
        <apply_to_children> : (bool) apply the same change to children elements.
        """
        self.set_style_attr("bck_color", color, states, copy_style, refresh, apply_to_children)

    def set_font_color(self, color, states="all", copy_style=True, refresh=True, apply_to_children=False):
        """Set the font color of the element (depending on how its style handles it).
        ***Mandatory arguments***
        <color> : a RGB color.
        ***Optional arguments***
        <states> : either 'all' or any state name (e.g. 'hover') or a sequence of state names (excluding 'all').
        <copy_style> : (bool) make a copy of the current style, so that it does not affect element sharing the same style object.
        <refresh> : (bool) refresh element surfaces.
        <apply_to_children> : (bool) apply the same change to children elements.
        """
        self.set_style_attr("font_color", color, states, copy_style, refresh, apply_to_children)

    def set_font_size(self, size, states="all", copy_style=True, refresh=True, apply_to_children=False):
        """Set the font size of the element (depending on how its style handles it).
        ***Mandatory arguments***
        <size> : (integer) new font size.
        ***Optional arguments***
        <states> : either 'all' or any state name (e.g. 'hover') or a sequence of state names (excluding 'all').
        <copy_style> : (bool) make a copy of the current style, so that it does not affect element sharing the same style object.
        <refresh> : (bool) refresh element surfaces.
        <apply_to_children> : (bool) apply the same change to children elements.
        """
        self.set_style_attr("font_size", size, states, copy_style, refresh, apply_to_children)

    def set_font_name(self, name, states="all", copy_style=True, refresh=True, apply_to_children=False):
        """Set the font family of the element (depending on how its style handles it).
        ***Mandatory arguments***
        <name> : (string) new font name.
        ***Optional arguments***
        <states> : either 'all' or any state name (e.g. 'hover') or a sequence of state names (excluding 'all').
        <copy_style> : (bool) make a copy of the current style, so that it does not affect element sharing the same style object.
        <refresh> : (bool) refresh element surfaces.
        <apply_to_children> : (bool) apply the same change to children elements.
        """
        self.set_style_attr("font_name", name, states, copy_style, refresh, apply_to_children)

    def set_font_auto_multilines_width(self, width, states="all", copy_style=True, refresh=True, apply_to_children=False):
        self.set_style_attr("font_auto_multilines_width", width, states, copy_style, refresh, apply_to_children)

    def set_max_text_width(self, width, states="all", copy_style=True, refresh=True, apply_to_children=False):
        """Set the maximum text width of the element before line breaks are automatically inserted.
        ***Mandatory arguments***
        <width> : (float or integer) the new max width. If a value smaller than 1 is given, then text is not automatically processed as a multiline text. Otherwise,
        line breaks are automatically inserted to fit the maximum width specified.
        ***Optional arguments***
        <states> : either 'all' or any state name (e.g. 'hover') or a sequence of state names (excluding 'all').
        <copy_style> : (bool) make a copy of the current style, so that it does not affect element sharing the same style object.
        <refresh> : (bool) refresh element surfaces.
        <apply_to_children> : (bool) apply the same change to children elements.
        """
        self.set_font_auto_multilines_width(width, states="all", copy_style=True, refresh=True, apply_to_children=False)

    def set_font_rich_text_tag(self, tag, states="all", copy_style=True, refresh=True, apply_to_children=False):
        """Set the tag for creating rich text. See the tagged examples for rich text usage.
        ***Mandatory arguments***
        <tag> : (string) the new tag for rich texts.
        ***Optional arguments***
        <states> : either 'all' or any state name (e.g. 'hover') or a sequence of state names (excluding 'all').
        <copy_style> : (bool) make a copy of the current style, so that it does not affect element sharing the same style object.
        <refresh> : (bool) refresh element surfaces.
        <apply_to_children> : (bool) apply the same change to children elements.
        """
        self.set_style_attr("font_rich_text_tag", tag, states, copy_style, refresh, apply_to_children)

    def set_style(self,  style, states, refresh=True, copy=False):
        states = self.get_states_names(states)
        for s in states:
            self.styles[s] = style
        if refresh:
            self.generate_surfaces()
        # if resort_and_englobe:
        #     self.sort_children()
        #     self.englobe_children()

    def set_style_attr(self, attr, value, states="all", copy_style=True,
                       refresh=True, apply_to_children=False):
        """Set any style attribute of the element.
        ***Mandatory arguments***
        <attr> : (str) the name of the style attribute.
        <value> : the value of the style attribute.
        ***Optional arguments***
        <states> : either 'all' or any state name (e.g. 'hover') or a sequence of state names (excluding 'all').
        <copy_style> : (bool) make a copy of the current style, so that it does not affect element sharing the same style object.
        <refresh> : (bool) refresh element surfaces.
        <apply_to_children> : (bool) apply the same change to children elements.
        """
        # if self.refresh_surfaces == self.refresh_surfaces_copy: #do not use "is" !
        #     states = ["normal"]
        # else:
        states = self.get_states_names(states)
        for state in states:
            style = self.styles[state]
            if style:
                if copy_style:
                    style = style.copy()
                if attr.startswith("font_"): #then call function
                    getattr(style,"set_"+attr)(value)
                else:
                    if not hasattr(style, attr):
                        warnings.warn("No attribute " + attr + " for style " + str(style.__class__))
                    setattr(style, attr, value)
                self.styles[state] = style
        if refresh:
##            self.refresh_surfaces()
            self.generate_surfaces() #same as refresh_surfaces with rect update
        if apply_to_children:
            for c in self.children:
                c.set_style_attr(attr, value, states, copy_style, refresh, apply_to_children)

    

    def get_current_style(self):
        """Returns the current style object of the element, using its current state."""
        return self.styles.get(self.state)

    def get_style(self, state):
        """Returns the style object of the element corresponding to a given state.
        <state> : name of the state ("normal", "pressed", "hover" or "locked")."""
        return self.styles[state]

    

    

    "#--- Size and position ---#"

    def move(self, dx, dy):
        """Moves the element (update from the current position).
        ***Mandatory arguments***
        <dx> : the number of pixels along x axis.
        <dy> : the number of pixels along y axis.
        """
        self.rect.x += dx
        self.rect.y += dy
        for e in self.children:
            e.move(dx,dy)

    def clamp(self, rect):
        """Moves self inside rect argument, using Pygame's clamp function.
        <rect> : the pygame Rect object in which the element should be clamped."""
        r = self.rect.clamp(rect)
        self.move(r.x - self.rect.x, r.y - self.rect.y)

    def set_topleft(self, x, y):
        """Set the absolute topleft position of the element.
        ***Mandatory arguments***
        <x> : x-coordinate (in pixels) of the topleft corner of the element.
        None can be passed to leave this coordinate unchanged.
        <y> : y-coordinate (in pixels) of the topleft corner of the element.
        None can be passed to leave this coordinate unchanged.
        """
        dx = 0 if x is None else x - self.rect.x
        dy = 0 if y is None else y - self.rect.y
        self.move(dx,dy)

    def set_bottomright(self, x, y):
        """Set the absolute bottomright position of the element.
        ***Mandatory arguments***
        <x> : x-coordinate (in pixels) of the bottomright corner of the element.
        None can be passed to leave this coordinate unchanged.
        <y> : y-coordinate (in pixels) of the bottomright corner of the element.
        None can be passed to leave this coordinate unchanged.
        """
        dx = 0 if x is None else x - self.rect.right
        dy = 0 if y is None else y - self.rect.bottom
        self.move(dx, dy)

    def set_bottomleft(self, x, y):
        """Set the absolute bottomleft position of the element.
        ***Mandatory arguments***
        <x> : x-coordinate (in pixels) of the bottomleft corner of the element.
        None can be passed to leave this coordinate unchanged.
        <y> : y-coordinate (in pixels) of the bottomleft corner of the element.
        None can be passed to leave this coordinate unchanged.
        """
        dx = 0 if x is None else x - self.rect.left
        dy = 0 if y is None else y - self.rect.bottom
        self.move(dx, dy)

    def set_topright(self, x, y):
        """Set the absolute topright position of the element.
        ***Mandatory arguments***
        <x> : x-coordinate (in pixels) of the topright corner of the element.
        None can be passed to leave this coordinate unchanged.
        <y> : y-coordinate (in pixels) of the topright corner of the element.
        None can be passed to leave this coordinate unchanged.
        """
        dx = 0 if x is None else x - self.rect.right
        dy = 0 if y is None else y - self.rect.y
        self.move(dx,dy)

    def set_center(self, x, y):
        """Set the absolute position of the element's center.
        ***Mandatory arguments***
        <x> : x-coordinate (in pixels) of the center of the element.
        None can be passed to leave this coordinate unchanged.
        <y> : y-coordinate (in pixels) of the center of the element.
        None can be passed to leave this coordinate unchanged.
        """
        dx = 0 if x is None else x-self.rect.centerx
        dy = 0 if y is None else y-self.rect.centery
        self.move(dx, dy)

    def center_on(self, what):
        """Centers the element on another, or on a pygame Surface or Rect.
        <what> : either a pygame Rect, a pygame Surface or a thorpy element.
        It is also possible to specify what = 'screen' as a shortcut for screen's rect.
        """
        if isinstance(what, str):
            rect = p.screen.get_rect()
        elif not isinstance(what, pygame.Rect): #works both for surfaces and elements.
            rect = what.get_rect()
        self.set_center(*rect.center)

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
        x0,y0 = sorting.get_side_center(self.rect, self_side)
        x1,y1 = sorting.get_side_center(other, other_side)
        self.move((x1-x0+delta[0])*move_x, (y1-y0+delta[1])*move_y)

    def englobe_children(self, margins=(5,5), adapt_parent=True, size_limit=(float("inf"), float("inf"))):
        """Resizes the element so that its size englobes that of its children.
        ***Optional arguments***
        <margins> : space between self's border and its children.
        <adapt_parent> : (bool) if False, parent of self won't be adapted accordingly.
        <size_limit> : (2-tuple) specifying the maximum width and height of the new size.
        """
        if self.children: #self's may be a ghost (unactive)
            self.rect = self.get_children_rect(margins)
            self.rect.w = min(size_limit[0], self.rect.w)
            self.rect.h = min(size_limit[1], self.rect.h)
            self.set_size(self.rect.size, adapt_parent) #generate surfaces if needed

    def set_size(self, size, adapt_parent=True, adapt_text=False):
        """Rebuild element's surfaces with imposed size.
        ***Mandatory arguments***
        <size> : 2-tuple on the form (w, h), where w and/or h can be None (in this case, it remains unchanged).
        <adapt_parent> : (bool) if True, then parent's size is adapted to fit the new self's size.
        <adapt_text> : (bool) if True, then self's text is automatically cut in several lines if needed, for
        instance if the new size if smaller than the old one and the textual content is now overflowing.
        """
        w,h = size
        if self.has_surfaces_generated:
            if w is None:
                w = self.get_current_width()
            if h is None:
                h = self.get_current_height()
            center = self.get_rect().center
        else:
            if w is None:
                w = self.rect.w
            if h is None:
                h = self.rect.h
            center = self.rect.center
        for key,value in self.styles.items():
            if value:
                self.styles[key] = value.copy()
                self.styles[key].size = (w,h)
                if adapt_text:
                    self.styles[key].font_auto_multilines_width = w
        if self.state != "unactive": #self.styles[self.state]: #e.g. ghost has no style
            self.generate_surfaces()
        self.rect.center = center
        if adapt_parent and self.parent:
            self.parent.resort()

    def rotate(self, angle, states="all"):
        """Rotate the images of the element.
        ***Mandatory arguments***
        <angle> : the angle of rotation in degrees.
        <states> : the states affected (either a list of strings or a specific state name or 'all')"""
        states = self.get_states_names(states)
        for state in states:
            for i in range(len(self.surfaces[state])):
                surface = self.surfaces[state][i]
                new_surface = pygame.transform.rotate(surface, angle)
                self.surfaces[state][i] = new_surface
                print("rotating", state, new_surface.get_rect())
        self.rect = self.get_rect()

    def get_current_width(self):
        """Returns the width of the element using its current state."""
        return self.get_current_frame().get_width()

    def get_current_height(self):
        """Returns the height of the element using its current state."""
        return self.get_current_frame().get_height()

    def get_text_size(self, state=None):
        """Return the size of the text within the element.
        ***Optional arguments***
        <state> : specify which state has to be taken into account (if None, then current state is used).
        """
        if self.text:
            if not state:
                state = self.state
            style = self.styles.get(state)
            return style.get_text_rect_and_lines(self.text)[0].size
##            return style.get_rendered_text(self.text).get_rect().size
        return (0,0)
    
    def sort_children(self, mode="v", align="center", gap=5,
                        margins=(5,5), offset=0, nx="auto", ny="auto", grid_gaps=(5,5),
                        horizontal_first=False, englobe_children=True,
                        limit_size_if_englobe=(float("inf"),float("inf"))):
        """Sort/organize children elements. See the tagged examples as they illustrate a lot of common situations.
        ***Optional arguments***
        <mode> : either 'v' (vertical), 'h' (horizontal) or 'grid'.
        <gap> : (integer) space between elements.
        <margins> : 2-tuple of integers specifying the margins.
        <offset> : (integer) offset of the whole rearrangment.
        <nx> : number of columns (in grid mode).
        <ny> : number of lines (in grid mode).
        <grid_gaps> : gap to use if grid mode used.
        <horizontal_first> : (bool) whether columns are filled first in grid mode (otherwise, lines are filled first).
        <englobe_children> : update self's size after sorting so that it englobes its children.
        <limit_size_if_englobe> : (2-tuple) specifying the maximum width and height of the new size, if englobe_children is True.
        """
        children = [e for e in self.children if not e.ignore_for_sorting]
        self.last_sorted = (mode, align, gap, margins, offset, nx, ny, grid_gaps, horizontal_first, englobe_children)
        sts = self.get_text_size() #Self Text Size = (0,0) if no text
        rects_w = [e.rect.width for e in children]+[sts[0]]
        rects_h = [e.rect.height for e in children]+[sts[1]]
        if mode == "v":
            w = max(rects_w) + 2*margins[0]
            h = sum(rects_h) + (len(children)-1)*gap + 2*margins[1]
##            self.rect.width = w
##            self.rect.height = h
            if align == "center":
                x = self.rect.centerx
            elif align == "left":
                x = self.rect.x
            elif align == "right":
                x = self.rect.right
            x += offset
            y = self.rect.y + margins[1]
            sorting.sort_children(children, (x,y), mode, align, gap)
        elif mode == "h":
            w = sum(rects_w) + 2*margins[0] + (len(children)-1)*gap
            h = max(rects_h)  + 2*margins[1]
            if align == "center":
               y = self.rect.centery
            elif align == "top":
               y = self.rect.y
            elif align == "bottom":
               y = self.rect.bottom
            y += offset
            x = self.rect.x + margins[0]
            sorting.sort_children(children, (x,y), mode, align, gap)
        elif mode == "grid":
            max_w = max(rects_w)
            max_h = max(rects_h)
            x = self.rect.x + margins[0]
            y = self.rect.y + margins[1]
            sorting.sort_children_grid(children, (x,y), nx, ny, (max_w,max_h), horizontal_first, grid_gaps[0], grid_gaps[1])
        else:
            raise ValueError("<mode> must be either 'h', 'v' or 'grid'.")
        if englobe_children:
            self.englobe_children(margins, size_limit=limit_size_if_englobe)

    def resort(self):
        """Try to sort using the last parameters as for last call to sort."""
        if self.last_sorted:
            self.sort_children(*self.last_sorted)
            self.set_center(*self.rect.center)

    "#--- Behaviour ---#"

    #convenience function for users
    def get_current_state(self):
        """Return the current state (string) of the element."""
        return self.state
    
    def set_invisible(self, value):
        """Set the element as invisible.
        <value> : if False, the element is visible, otherwise it is invisible."""
        if not value:
            self.state = "normal"
        else:
            self.state = "unactive"

    def set_locked(self, value):
        """Set the current state from 'locked' to 'normal' or from 'normal' to 'locked'.
        <value> : (bool) if True, the new state will be 'locked', wheras if False, the new state
        will be 'normal'. Also adapt the children states.
        """
        if value:
            self.state = "locked"
        else:
            self.state = "normal"
        for c in self.get_all_descendants():
            c.state = self.state

    def set_draggable(self, x_axis=True, y_axis=True, cannot_drag_outside=True, cannot_draw_outside=True,
                        adapt_cursor_style=True):
        """Set whether the element can be dragged by the user. If you set your element as draggable,
            keep in mind that whenever you change the size of the parent element it resets the original position
            of the draggable element. If you want to always keep the position of the element, make sure you set to
            False the adapt_parent argument of methods that modify the appearance of the parent and any of its children,
            e.g : some_sister_element.set_text("This is a new text", adapt_parent=False).
        ***Optional arguments***
        <x_axis> : (bool) determines whether the element can be dragger on x-axis.
        <y_axis> : (bool) determines whether the element can be dragger on y-axis.
        <cannot_drag_outside> : (bool) if True, the element cannot be dragged outside of its parent.
        <cannot_draw_outside> : (bool) if True, the element cannot be drawn outside of its parent.
        <adapt_cursor_style> : (bool) if True, mouse cursor will appear as a hand when hovering the element.
        """
        self.draggable_x = x_axis
        self.draggable_y = y_axis
        self.cannot_drag_outside = cannot_drag_outside
        self.cannot_draw_outside = cannot_draw_outside
        if adapt_cursor_style and (self.draggable_x or self.draggable_y):
            self.hand_cursor = True

    def drag_if_needed(self, mouse_delta):
        # mp = pygame.mouse.get_pos()
        # if not self.rect.collidepoint(mp):
        #     print(self.id, self.text)
        #     if self.parent:
        #         if self.parent.rect.collidepoint(mp):
        #             return
        dx, dy = 0, 0
        if self.draggable_x:
            dx = mouse_delta[0]
        if self.draggable_y:
            dy = mouse_delta[1]
        if dx != 0 or dy != 0:
            if self.at_drag:
                self.at_drag(dx, dy, **self.at_drag_params)
            #do not directly move the elements, as there may be a clamp correction, and we
            #do not want to apply the correction recursively to children
            rect = self.rect.move(dx,dy)
            if self.cannot_drag_outside and self.parent:
                if not (self.parent.__class__ is Element):
                    rect.clamp_ip(self.parent.rect)
            dx = rect.x - self.rect.x
            dy = rect.y - self.rect.y
            self.move(dx,dy)

    def react_button(self, button):
        for e in self.children:
            e.react_button(button)

    def default_at_unclick(self):
        pass

    def default_at_click(self):
        pass

    def default_at_hover(self):
        pass

    def default_at_unhover(self):
        pass

    def other_is_dragged(self):
        """Returns True if another element is beeing dragged by the user."""
        if p.element_being_dragged:
            return not (p.element_being_dragged is self)
        return False

    def get_value(self):
        """Returns the value stored in the element. For non-specialized elements, simply returns their text content."""
        return self.text
    
    def set_value(self, text):
        """Set the value stored in the element. For non-specialized elements, simply change their text content."""
        self.set_text(text)


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
                            self.i_frame = 0
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
                        self.i_frame = 0
                        self.state = "hover"
                        if self.at_unclick:
                            self.at_unclick(**self.at_unclick_params)
                        self.default_at_unclick()
                    elif self.state != "hover":
                        self.i_frame = 0
                        self.state = "hover"
                        # if self.hand_cursor:
                        #     pygame.mouse.set_cursor(hand_cursor)
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
                        self.i_frame = 0
                        self.state = "normal"
                        if self.hand_cursor:
                            pygame.mouse.set_cursor(arrow_cursor)
                        if self.at_unhover:
                            self.at_unhover(**self.at_unhover_params)
                        self.default_at_unhover()
                        self.being_dragged = False
                    if self.state != "normal":
                        self.i_frame = 0
                        self.state = "normal"
            self.it += 1
            self.update_iframe()
        if self.state == "hover" and self.hand_cursor:
            pygame.mouse.set_cursor(hand_cursor)
        return dragged
    
    def update_iframe(self):
        style = self.get_current_style()
        if style and style.frame_mod > 0:
            if self.it % style.frame_mod == 0:
                self.i_frame += 1
            self.i_frame %= style.nframes
        else:
            self.i_frame = 0


    def update_no_state_change(self, mouse_delta):
        """_Visual update only. Call the next frame in the animation."""
        if self.state == "locked":
            return False
        for e in self.children:
            e.update_no_state_change(mouse_delta)
        #self.state may be changed by children
        if self.state != "unactive" and self.state != "locked":
            self.it += 1
            self.update_iframe()

    def lock_all_and_get_states(self):
        self.i_frame = 0
        states = []
        for c in self.children:
            states += c.lock_all_and_get_states()
        states += [(self, self.state)]
        self.state = "locked"
        return states
    
    def get_children_rect(self, margins):
        r = self.children[0].rect.unionall([e.rect for e in self.children if not e.ignore_for_sorting])
        r.inflate_ip((margins[0]*2, margins[1]*2))
        return r

    def get_rect_with_children(self):
        if self.children:
            return self.rect.unionall([e.rect for e in self.children if not e.ignore_for_sorting])
        else:
            return self.rect

    
    def fill_surfaces_for_debug(self, color=(0,0,0)):
        for key, style in self.styles.items():
            if style:
                for s in self.surfaces[key]:
                    s.fill(color)
                    s.set_alpha(255)

    def refresh_surfaces_shadow(self):
        if self.multi_shadows:
            for style_name, style in self.styles.items():
                if style.shadowgen:
                    # print("generating shadow for state", style_name, "el:", self, "--> size=", self.rect.size)
                    s = style.shadowgen.generate_image(self.get_frame(style_name, 0))
                    self.shadows[style_name] = [s for surf in self.surfaces[style_name]]
                else:
                    self.shadows[style_name] = [None for surf in self.surfaces[style_name]]
        else:
            shadowgen_used = None
            style_to_copy = None
            for style_name, style in self.styles.items():
                if not style:
                    continue
                if style.shadowgen:
                    if shadowgen_used:
                        s = self.shadows[style_to_copy][0]
                        self.shadows[style_name] = [s for surf in self.surfaces[style_name]]
                    else:
                        # print("generating shadow2 for state", style_name, "el:", self, "--> size=", self.rect.size)
                        # if self.id == 179:assert False
                        s = style.shadowgen.generate_image(self.get_frame(style_name, 0))
                        self.shadows[style_name] = [s for surf in self.surfaces[style_name]]
                        shadowgen_used = style.shadowgen
                        style_to_copy = style_name
                else: #no shadowgen at all means no shadow
                    self.shadows[style_name] = [None for surf in self.surfaces[style_name]]

    def refresh_surfaces_build(self):
        """_Refresh surfaces using the current style object"""
        for key, style in self.styles.items():
            if style:
                self.surfaces[key] = style.generate_images(self.text)
        self.has_surfaces_generated = True
        self.refresh_surfaces_shadow()

    def refresh_surfaces_copy(self):
        """_Refresh surfaces using a new style object"""
        if not self.styles["normal"]:
            return
        s = self.styles["normal"].generate_images(self.text)
        for key in self.styles.keys():
            self.surfaces[key] = s
        self.has_surfaces_generated = True
        self.refresh_surfaces_shadow()

    def get_current_frame_normal(self):
        return self.get_frame(self.state, self.i_frame)
    
    def get_frame(self, state, it):
        return self.surfaces[state][it]
    
    def autoset_nframes(self):
         for key, value in self.styles.items():
            if value:
                self.styles[key].nframes = len(self.surfaces[key])
    
    def pump_special_frame(self):
        if self.special_frames:
            return self.special_frames.pop()
        else:
            self.stop_special_frames()
            return self.get_current_frame()
        
    def get_current_shadow_frame(self):
        return self.shadows.get(self.state)[self.i_frame]
    
    

    def get_rect(self):
        """_Returns the current rect of the element, using its current state."""
        if self.get_current_style():
            current_center = self.rect.center
            r = self.get_current_frame().get_rect()
            r.center = current_center
            return r
        else:
            return self.rect

    def extract_all_helpers(self):
        """_Get a list of all the descendants helpers."""
        helpers = [e.helper for e in self.get_all_descendants() if e.helper]
        return helpers

    def get_blit_rects(self):
        if self.parent:
            pr = self.parent.rect
        else:
            pr = None
        return get_blit_rects(pr,self.rect)
##        if not self.parent:
##            return self.rect, None
##        pr = self.parent.rect.inflate((-3,-3))
##        sr = self.rect
##        if pr.contains(sr):
##            return self.rect, None
##        clip = sr.clip(pr)
##        area = pygame.Rect(0,0,clip.width,clip.height)
##        if sr.y < pr.y:
##            area.y = sr.height - clip.height
##        if sr.x < pr.x:
##            area.x = sr.width - clip.width
##        return clip, area

    def draw_shadow_inside(self):
        pr = None
        if self.parent:
            pr = self.parent.rect
        shadow = self.get_current_shadow_frame()
        if shadow:
            r = shadow.get_rect()
            r.topleft = self.rect.topleft
            r.move_ip(self.get_current_style().shadowgen.offset)
            rect_s, area_s = get_blit_rects(pr, r)
            self.surface.blit(shadow, rect_s, area_s)

    def must_draw(self):
        return self.state != "unactive"

    def second_draw(self, style):
        if style.has_second_draw:
            if not(style.r_text is None):
                style.r_text.center = self.rect.center
                style.blit_text(self.surface, style.text_lines, style.r_text)
                

    #--- Launching (pop on screen) ---#
        
    # def launch_alone(self, func_before=None, click_outside_cancel=True, reaction=None, extract_helpers=True,
    #                     func_after=None):
    def launch_alone(self, func_before=None, click_outside_cancel=True, reaction=None, func_after=None):
        """Creates a time loop to interact with this element alone. The element thus 'pops' to the screen for the user.
        ***Optional arguments***
        <func_before> : either None or a function to call before each update and draw of the element.
        <func_after> : either None or a function to call after each update and draw of the element.
        <click_outside_cancel> : (bool) if True, the user can discard the popped element.
        <reaction> : either None or a function to call each frame and that takes as only argument the pygame event.
        """
        # if extract_helpers:
        helpers = self.extract_all_helpers()
        for h in helpers:
            if not(h.parent is self):
                h.parent.remove_child(h)
                self.add_child(h)
        loops.loop_elements(self, [], func_before, click_outside_cancel, reaction, func_after)
##        if extract_helpers:
##            for h in helpers:
##                h.event_parent.add_child(h)
##                self.remove_child(h)

    def launch_and_lock_others(self, other, func_before=None, click_outside_cancel=True,
                                reaction=None, func_after=None):
        """Creates a time loop to interact with this element.
        The element thus 'pops' to the screen for the user.
        The other elements enters in lock mode ; they are drawn to the screen, but not updated according to events.
        ***Mandatory arguments***
        <other> : parent element of the other elements to block.
        ***Optional arguments***
        <func_before> : either None or a function to call before each update and draw of the element.
        <func_after> : either None or a function to call after each update and draw of the element.
        <click_outside_cancel> : (bool) if True, the user can discard the popped element.
        <reaction> : either None or a function to call each frame and that takes as only argument the pygame event.
        """
        tmp = self.state
        states = other.lock_all_and_get_states()
        self.state = tmp #if other is an ancestor, make sure it doesnt lock us.
        loops.loop_elements(self, [other], func_before, click_outside_cancel, reaction, func_after)
        for element, state in states:
            element.state = state

    def launch_nonblocking(self, loop=None, click_outside_cancel=True):
        """Inserts the element in the current loop, so that other elements are still reacting.
        Works only when using thorpy.Updater's loop.
        ***Optional arguments***
        <loop> : specify a given loop as reference. If None, then use the current loop.
        <click_outside_cancel> : (bool) if True, the user can discard the popped element.
        """
        if loop is None:
            loop = loops.loops[-1]
        self.loop_give_back = (loop, loop.element, loop.click_outside_cancel)
        loop.to_update.append(loop.element)
        loop.element = self
        loop.click_outside_cancel = click_outside_cancel

    def remove_from_loop(self):
        loop, e, click_outside_cancel = self.loop_give_back
        loop.to_update.remove(e)
        loop.element = e
        loop.click_outside_cancel = click_outside_cancel

    def get_updater(self, fps=-1, esc_quit=False):
        """Returns a thorpy Updater object so that you can use thorpy elements in your own loop
        without thinking about how to update and draw thorpy elements. See the tagged examples for
        standard usage.
        ***Optional arguments***
        <fps> : (float) the framerate of the update.
        If fps is negative (which is the case by default), framerate control is unactivated
        (typically, you want it if your application already limitates FPS).
        <esc_quit> : (bool) set to True if you want that the updater exits when user press escape.
        """
        player = loops.Loop(element=self, fps=fps)
        player.esc_quit = esc_quit
        self.last_player = player
        return player
    
    

    def get_states_names(self, name):
        """_Always return a list of strings"""
        if name == "all":
            states = list(self.styles.keys())
        elif isinstance(name, str):
            states = [name]
        else: #we assume name is a list of string, which is standard
            states = name
        return states

    #--- Surface management ---#

    def draw(self):
        """Draws the element according to its current state. Note that in most cases,
        you won't use this method, as the updater of the element will handle it (see tagged example)."""
        if self.must_draw():
            style = self.get_current_style()
            if style:
                if self.clamp_rect:
                    self.clamp(self.clamp_rect)
                if self.cannot_draw_outside and not(self.parent.__class__ is Element):
                    rect, area = self.get_blit_rects()
                    if self.get_current_shadow_frame():
                        self.draw_shadow_inside()
                    self.surface.blit(self.get_current_frame(), rect, area)
                    self.second_draw(style)
                else:
                    shadow = self.get_current_shadow_frame()
                    if shadow:
                        self.surface.blit(shadow, self.rect.move(style.shadowgen.offset))
                    self.surface.blit(self.get_current_frame(), self.rect)
                    self.second_draw(style)
        for e in self.children:
            e.draw()

    def generate_surfaces(self):
        """Build the element surfaces for each style and refresh the element's rect accordingly."""
        self.refresh_surfaces()
        self.rect = self.get_rect()

    def get_current_frame(self):
        """Returns the image of the element being displayed."""
        pass

    def copy_normal_state(self, only_normal):
        """Avoid building multiple times surfaces that are actually the same.
        ***Mandatory arguments***
        <only_normal> : (bool) if False, surfaces are build for each state separately.
        """
        if only_normal:
            self.refresh_surfaces = self.refresh_surfaces_copy
        else:
            self.refresh_surfaces = self.refresh_surfaces_build


    def generate_shadow(self, fast="auto", shadowgen=None, states="all", uniform=False):
        """Generates a shadow and binds it to the element. This function is not meant to be called within the app loop, but only at initialization.
        ***Optional arguments***
        <fast> : (bool) if True, will generate a rectangular shadow whatever the element's shape is. Otherwise,
        this may be slow. You can also pass 'auto' : in this case, you let Thorpy choose whether the computing time
        is acceptable and automatically set fast to False if needed.
        <shadowgen> : you can indicate a shadow generator (see tagged examples) or None to let Thorpy choose.
        <states> : a string or a sequence of strings indicating for which states the shadow should be generated.
        <uniform> : (bool) if True and fast is also True, then the shadow wont have per-pixel alpha values.
        """
        states = self.get_states_names(states)
        if not shadowgen:
            fast = shadows.auto_set_fast(self, fast)
            shadowgen = shadows.propose_shadowgen(self.get_current_style(), fast, uniform)
        for state in states:
            self.set_style_attr("shadowgen", shadowgen, states=state, refresh=False)
        self.refresh_surfaces_shadow()

    def set_special_frames(self, frames):
        """Bypasses the element's style to display special frames instead, until the animation is finished.
        <frames> : a sequence of pygame surfaces."""
        self.special_frames = frames
        self.get_current_frame = self.pump_special_frame

    def stop_special_frames(self):
        """Stops the special frames display (see set_special_frames)"""
        self.get_current_frame = self.get_current_frame_normal
                
    "#--- Children management ---#"

    def add_child(self, element, i=-1):
        """Add a child to the element.
        ***Mandatory arguments***
        <element> : the children element to add.
        ***Optional arguments***
        <i> : (integer) where in the list of children the new one should be added.
        By default -1 : it goes to the end.
        """
        element.parent = self
        if i < 0:
            self.children.append(element)
        else:
            self.children.insert(i, element)

    def remove_child(self, element):
        """Remove a child to the element.
        <element> : the children element to add.
        """
        element.parent = None
        self.children.remove(element)

    def replace_child(self, old_one, new_one, refresh=True):
        """Replaces a child of the element.
        ***Mandatory arguments***
        <old_one> : the children element to remove.
        <new_one> : the children element to add (new_one replaces old_one).
        ***Optional arguments***
        <refresh> : (bool) if False, self's surface and arrangment won't be refreshed.
        """
        i = self.children.index(old_one)
        old_one.parent = None
        new_one.parent = self
        self.children[i] = new_one
        if refresh:
            self.generate_surfaces()

    def get_children(self):
        """Returns the children of the element, but not the children of the children and so on."""
        return self.children
    
    def root(self):
        """Returns the 'oldest' parent of the element, i.e. the parent of its parent of its parent and so on.
        Returns the element itself if it has no parent."""
        if self.parent:
            return self.parent.root()
        else:
            return self
    
    def get_all_descendants(self):
        """Returns all the descendants of the elements,
        i.e. its children, the children of its children and so on."""
        d = [self]
        for e in self.children:
            d += e.get_all_descendants()
        return d
    
    
        
    def has_descendant_in_state(self, state):
        """Returns True if any of the descendants is in the specified state.
        By 'descendants', we mean either self or self's children, or self's children's children and so on.
        <state> : (string) either 'normal', 'pressed', 'hover' or 'locked'."""
        if self.state == state:
            return True
        for e in self.get_all_descendants():
            if e.state == state:
                return True
        return False

    def do_nothing(self):
        pass

