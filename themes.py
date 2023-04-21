from email.mime import base
from numpy import isin
import pygame
from pyparsing import col
from . import styles
from .elements import Box, TitleBox, Button, Text, Line, assign_styles, DropDownList, ImageButton
from .elements import TextInput, Slider, Image, Helper, Checkbox, Radio, SwitchButton, ToggleButton
from .elements import DeadButton, _DropDownButton, _LabelButton, _DraggerButton, _SliderBar, _ColorFrameForColorPicker
from .elements import ColorPicker, ColorPickerRGB, SwitchButtonWithText
from .graphics import darken, enlighten, change_alpha
from thorpy import graphics
from .shadows import propose_shadowgen
from . import parameters as p

import thorpy

all_classes = [Box, TitleBox, Button, Text, Line, DropDownList,
                TextInput, Slider, Image, Helper, Checkbox, Radio, SwitchButton, ToggleButton, DeadButton,
                _DraggerButton, _DropDownButton, _LabelButton, _SliderBar]


all_themes = "classic", "round", "human", "simple", "text", "text_dark", "game1", "game2", "round_gradient", "round2"

def apply_default_colorpickers():
    _ColorFrameForColorPicker.style_normal = styles.RoundStyle()
    ColorPicker.style_normal = Button.style_normal.copy()
    ColorPickerRGB.style_normal = Button.style_normal.copy()

def apply_default_image_style():
    Image.style_normal = styles.ImageStyle()
    ImageButton.style_normal = styles.ImageStyleWithText()
    ImageButton.style_hover = styles.ImageStyleWithText()
    ImageButton.style_hover.font_color = Button.style_hover.font_color
    ImageButton.style_pressed = styles.ImageStyleWithText()
    ImageButton.style_pressed.font_color = darken(Button.style_pressed.font_color)
    ImageButton.style_locked = styles.ImageStyleWithText()

def apply_default_locked():
    Button.style_locked = Button.style_normal.copy()
    Button.style_locked.dark_factor = 0.9
    Button.style_locked.light_factor = 1.1
    Button.style_locked.light_offset = 0
    Button.style_locked.bck_color = darken(Button.style_normal.bck_color, 0.8)
    # Button.style_locked.font_color = darken(Button.style_locked.bck_color, 0.8)

def apply_default_helper():
    Helper.style_normal = Button.style_normal.copy()
    # Helper.style_normal.dark_factor = 0.9
    # Helper.style_normal.light_factor = 1.1
    # Helper.style_normal.light_offset = 0
    Helper.style_normal.bck_color = enlighten(Helper.style_normal.bck_color, 1.1)
    # Helper.style_normal.bck_color = change_alpha(Helper.style_normal.bck_color, 100)
    # Helper.style_normal.font_color = enlighten(Helper.style_normal.bck_color, 1.3)

def apply_default_checkbox(basestyle, radius=0, bck=None):
    Checkbox.style_normal = basestyle()
    Checkbox.style_normal.shadowgen = Button.style_normal.shadowgen
    Checkbox.style_normal.radius = radius
    Checkbox.style_normal.pressed = True
    if bck:
        Checkbox.style_normal.bck_color = bck
    Checkbox.style_pressed = Checkbox.style_normal.copy()
    Checkbox.style_locked = Checkbox.style_normal.copy()
    Checkbox.style_hover = Checkbox.style_normal.copy()
    Checkbox.style_hover.bck_color = enlighten(Checkbox.style_normal.bck_color)

def apply_default_radio(basestyle, bck_color=(250,250,250), colorkey=(255,255,255)):
    Radio.style_normal = basestyle()
    Radio.style_normal.bck_color = bck_color
    Radio.style_normal.colorkey = colorkey
    Radio.style_hover = Radio.style_normal.copy()
    Radio.style_hover.border_color = (0,0,255)
    Radio.style_pressed = Radio.style_normal.copy()
    Radio.style_locked = Radio.style_normal.copy()
    Radio.style_locked.bck_color = darken(Radio.style_normal.bck_color, 0.8)

def apply_default_line(basestyle, thickness=1):
    Line.style_normal = basestyle()
    Line.style_normal.pressed = True
    Line.style_normal.border_thickness = thickness

def apply_default_slider(basestyle, basecolor):
    Slider.style_normal = basestyle()
    Slider.style_normal.size = (15,20)
    Slider.style_normal.bck_color = basecolor
    Slider.style_hover = Slider.style_normal.copy()
    Slider.style_hover.bck_color = darken(basecolor)
    Slider.style_pressed = Slider.style_hover.copy()
    Slider.style_locked = Slider.style_normal.copy()
    Slider.style_locked.bck_color = darken(Slider.style_normal.bck_color, 0.8)
    _SliderBar.style_normal = basestyle()
    _SliderBar.style_normal.bck_color = (255,)*3
    _SliderBar.style_normal.pressed = True
    

def apply_default_toggle_button(cls, basecolor=None):
    ToggleButton.style_normal = cls()
    ToggleButton.style_hover = cls()
    ToggleButton.style_pressed = cls()
    ToggleButton.style_pressed.pressed = True
    ToggleButton.style_locked = cls()
    if basecolor is None:
        basecolor = Button.style_hover.bck_color
    for s in ToggleButton.iter_styles():
        s.bck_color = basecolor
        s.border_thickness = 1
        s.pressed_text_delta = (0,0)


def apply_default_box(cls):
    Box.style_normal = cls()
    Box.style_locked = cls()
    Box.style_hover = cls()
    Box.style_pressed = cls()
##    Box.style_locked.bck_color = darken(Box.style_locked.bck_color)
    Box.style_locked.font_color = darken(Box.style_locked.bck_color)
    DeadButton.style_normal = Button.style_normal.copy()

def apply_default_titlebox(cls):
    TitleBox.style_normal = cls()
    TitleBox.style_normal.line_color = darken(TitleBox.style_normal.bck_color, 0.8)
    TitleBox.style_normal.font_color = enlighten(TitleBox.style_normal.font_color)
    TitleBox.style_locked = cls()
    # TitleBox.style_locked.bck_color = darken(TitleBox.style_locked.bck_color)
    TitleBox.style_locked.font_color = darken(TitleBox.style_locked.bck_color)

def apply_default_ddl(cls, func=darken):
    DropDownList.style_normal = cls()
    DropDownList.style_locked = cls()
    DropDownList.style_locked.bck_color = darken(DropDownList.style_locked.bck_color)
    DropDownList.style_locked.font_color = darken(DropDownList.style_locked.bck_color)
    #
    _DropDownButton.style_normal = styles.DDLEntryStyle()
    _DropDownButton.style_hover = _DropDownButton.style_normal.copy()
    _DropDownButton.style_hover.bck_color = (100,100,255)
    _DropDownButton.style_pressed = _DropDownButton.style_normal.copy()
    _DropDownButton.style_locked = _DropDownButton.style_normal.copy()
    _DropDownButton.style_locked.bck_color = darken(_DropDownButton.style_normal.bck_color)
    

def apply_default_input(cls, bck=(255,255,255), fontcolor=(50,)*3):
    TextInput.style_normal = cls()
    TextInput.style_normal.bck_color = bck
    if fontcolor:
        TextInput.style_normal.font_color=fontcolor
    # TextInput.style_normal.bck_color = enlighten(TextInput.style_normal.bck_color, 2.)
    TextInput.style_normal.pressed = True
    TextInput.style_locked = Button.style_locked.copy()
    TextInput.style_locked.pressed = True
    TextInput.style_locked.shadowgen = None
    TextInput.style_hover = TextInput.style_normal.copy()
    TextInput.style_pressed = TextInput.style_normal.copy()
    #set placeholder font color
    TextInput.style_locked.font_color = (150,)*3

def apply_default_switch(bck=None):
    SwitchButton.style_normal = Slider.style_normal.copy()
    SwitchButton.style_normal.pressed = True
    if bck:
        SwitchButton.style_normal.bck_color = bck
    SwitchButton.style_hover = Slider.style_hover.copy()
    SwitchButton.style_hover.bck_color = enlighten(Slider.style_normal.bck_color,2.)
    SwitchButton.style_hover.pressed = True
    SwitchButton.style_pressed = Slider.style_pressed.copy()
    SwitchButton.style_pressed.pressed = True
    SwitchButton.style_locked = Slider.style_locked.copy()
    SwitchButton.style_locked.pressed = True

def apply_default_label():
    _LabelButton.style_normal = Text.style_normal.copy()
    _LabelButton.style_hover = Text.style_normal.copy()
    _LabelButton.style_hover.font_color = Button.style_hover.font_color
    _LabelButton.style_pressed = Text.style_normal.copy()
    _LabelButton.style_pressed.font_color = Button.style_pressed.font_color
    _LabelButton.style_locked = Text.style_normal.copy()

def apply_default_dragger(size=(20,10), bck_color=None):
    _DraggerButton.style_normal = Button.style_normal.copy()
    _DraggerButton.style_normal.size = size
    _DraggerButton.style_hover = Button.style_hover.copy()
    _DraggerButton.style_hover.size = size
    _DraggerButton.style_pressed = Button.style_hover.copy()
    _DraggerButton.style_pressed.size = size
    _DraggerButton.style_locked = Button.style_locked.copy()
    _DraggerButton.style_locked.size = size
    if bck_color:
        _DraggerButton.style_normal.bck_color = bck_color
        _DraggerButton.style_hover.bck_color = bck_color
        _DraggerButton.style_pressed.bck_color = bck_color
        _DraggerButton.style_locked.bck_color = bck_color


def theme_classic():
    p.current_theme = "classic"
    #Button
    Button.style_normal = styles.ClassicStyle()
    Button.style_hover = Button.style_normal.copy()
    Button.style_hover.font_color = (20,20,155)
    Button.style_pressed = Button.style_hover.copy()
    Button.style_pressed.pressed = True
    apply_default_locked()
    apply_default_dragger()
    #Box
    apply_default_box(styles.ClassicStyle)
    apply_default_titlebox(styles.TitleBoxClassicStyle)
    apply_default_ddl(styles.ClassicStyle)
    apply_default_input(styles.ClassicStyle)
    apply_default_toggle_button(styles.ClassicStyle)
    TextInput.style_hover.border_color = (0,0,255)
    #Text
    Text.style_normal = styles.TextStyle()
    Text.style_normal.font_color = (50,)*3
    apply_default_label()
    #Lines
    apply_default_line(styles.ClassicStyle)
    #Sliders
    apply_default_slider(styles.ClassicStyle, Box.style_normal.bck_color)
    #Images
    apply_default_image_style()
    #Helpers
    apply_default_helper()
    #Checkboxes and radios
    apply_default_checkbox(styles.ClassicStyle)
    apply_default_radio(styles.CircleStyle)
    apply_default_switch()
    #end
    assign_styles()

def theme_round(base_style=None, base_color=(240,)*3, assign=True):
    p.current_theme = "round"
    if base_style is None:
        base_style = styles.RoundStyle
    #Button
    Button.style_normal = base_style()
    Button.style_normal.bck_color = base_color
    Button.style_hover = Button.style_normal.copy()
    Button.style_hover.font_color = (0,0,255)
    Button.style_pressed = Button.style_hover.copy()
    Button.style_pressed.font_color = (0,0,255)
    Button.style_pressed.bck_color = darken(Button.style_normal.bck_color)
    apply_default_locked()
    apply_default_dragger()
    apply_default_toggle_button(base_style)
    #Box and boxes-like
    apply_default_box(base_style)
    for s in Box.iter_styles():
        s.radius = 10
    Box.style_normal.bck_color = (220,220,220,255)
    # Box.style_locked.bck_color = darken(Box.style_normal.bck_color)
    Button.style_locked.font_color = darken(Box.style_locked.bck_color)
    apply_default_titlebox(styles.TitleBoxRoundStyle)
    # TitleBox.style_normal.bck_color = Box.style_normal.bck_color
    #DropDownList
    apply_default_ddl(base_style)
    DropDownList.style_normal.bck_color = change_alpha(Box.style_normal.bck_color, 200)
##    DropDownList.style_normal.bck_color = darken(Box.style_normal.bck_color)
    apply_default_input(base_style)
    #Text
    Text.style_normal = styles.TextStyle()
    Text.style_normal.font_color = (50,)*3
    apply_default_label()
    #Lines
    apply_default_line(base_style)
    Line.style_normal.bck_color = Button.style_locked.bck_color
    #Sliders
    apply_default_slider(base_style, (220,)*3)
    #Images
    apply_default_image_style()
    #Helpers
    apply_default_helper()
    #Checkboxes and radios
    # apply_default_toggle_button(styles.RoundStyle, enlighten(graphics.get_main_color(Box.style_normal.bck_color), 1.4))
    # ToggleButton.style_pressed.bck_color = darken(graphics.get_main_color(ToggleButton.style_normal.bck_color),0.6)
    # ToggleButton.style_hover.font_color = (0,0,255)
    apply_default_toggle_button(base_style, ((220,)*3, (150,)*3, "v"))
    ToggleButton.style_pressed.bck_color = ((150,)*3, (220,)*3, "v")
    apply_default_checkbox(base_style, radius=0.25, bck=enlighten(Button.style_normal.bck_color))
    apply_default_radio(styles.CircleStyle)
    apply_default_switch(bck=enlighten(Button.style_normal.bck_color))
    #Colorpickers
    apply_default_colorpickers()
    #
    if assign:
        assign_styles()

def theme_round_gradient(colors=((254,218,117), (250,126,30), (214,41,118), (79,91,213), "q")):
    theme_round2((colors[0],colors[1], "h"))
    p.current_theme = "round_gradient"
    set_style_attr("bck_color", colors, ("normal","hover","locked"), only_to_cls=[Button, ToggleButton, SwitchButton, DropDownList])
    set_style_attr("bck_color", (colors[3], colors[2], colors[1], colors[0], "q"),
                   "pressed", only_to_cls=[Button, ToggleButton, SwitchButton])
    _DropDownButton.style_hover.font_color = graphics.get_main_color(colors)
    _DropDownButton.style_hover.bck_color = (0,)*4

def theme_round2(colors=((209,79,153), (255, 86, 105), "h")):
    theme_round(base_color=colors)
    p.current_theme = "round2"
    set_style_attr("radius", 0.5, "all", only_to_cls=[Button])
    inverted = (colors[1], colors[0], colors[-1])
    set_style_attr("bck_color", inverted, "pressed", only_to_cls=[Button])
    set_style_attr("bck_color", (0,0,0,127), "all", only_to_cls=[Box, TitleBox])
    set_style_attr("font_color", (200,)*3, "all")
    set_style_attr("font_color", enlighten(Button.style_normal.font_color), "hover")
    ToggleButton.style_normal = Button.style_normal.copy()
    ToggleButton.style_pressed = Button.style_pressed.copy()
    ToggleButton.style_pressed.bck_color = graphics.get_main_color(colors)
    ToggleButton.style_locked = Button.style_locked.copy()
    ToggleButton.style_hover = Button.style_hover.copy()
    _DropDownButton.style_normal.font_color = Button.style_normal.font_color
    _DropDownButton.style_hover.font_color = Button.style_hover.font_color
    _DropDownButton.style_hover.bck_color = colors[1]
    SwitchButton.style_normal.bck_color = Button.style_normal.bck_color
    SwitchButton.style_hover.bck_color = Button.style_pressed.bck_color
    set_style_attr("font_color", (50,)*3, ["normal", "hover", "pressed"], only_to_cls=[TextInput])
    Box.style_locked.bck_color = Box.style_normal.bck_color
    apply_default_radio(styles.CircleStyle, bck_color=(200,)*3, colorkey=(0,0,0))
    DropDownList.style_normal.bck_color = Button.style_pressed.bck_color

def theme_human(color=None):
    # Button.style_normal.has_second_draw = False
    theme_round(styles.HumanStyle)
    apply_default_toggle_button(styles.HumanStyle, basecolor=((220,)*3, (170,)*3, "v"))
    ToggleButton.style_pressed.bck_color = ((170,)*3, (220,)*3, "v")
    p.current_theme = "human"
    if not color:
        color = styles.HumanStyle.bck_color
    for s in Button.iter_styles():
        s.bck_color = color
    Button.style_pressed.bck_color = (color[1], color[0], color[-1])
    for s in Line.iter_styles():
        s.bck_color = graphics.get_main_color(s.bck_color)

def theme_simple():
    p.current_theme = "simple"
    #Button
    Button.style_normal = styles.TextStyle()
    Button.style_hover = Button.style_normal.copy()
    Button.style_hover.bck_color = (100,100,255)
    # Button.style_hover.font_color = (100,100,255)
    Button.style_pressed = Button.style_hover.copy()
    apply_default_locked()
    apply_default_dragger()
    _DraggerButton.style_normal.bck_color = (200,200,200,255)
    #Box and boxes-like
    apply_default_box(styles.SimpleStyle)
    Box.style_normal.bck_color = (220,220,220,220)
    Box.style_locked.bck_color = darken(Box.style_normal.bck_color)
    Button.style_locked.font_color = darken(Button.style_normal.bck_color)
    apply_default_titlebox(styles.TitleBoxSimpleStyle)
    #DropDownList
    apply_default_ddl(styles.SimpleStyle)
    DropDownList.style_normal.bck_color = change_alpha(Box.style_normal.bck_color, 255)
    apply_default_input(styles.SimpleStyle)
    #Text
    Text.style_normal = styles.TextStyle()
    Text.style_normal.font_color = (50,)*3
    apply_default_label()
    #Lines
    apply_default_line(styles.SimpleStyle, thickness=0)
    #Sliders
    apply_default_slider(styles.SimpleStyle, darken(Box.style_normal.bck_color))
    #Images
    apply_default_image_style()
    #Helpers
    apply_default_helper()
    #Checkboxes and radios
    apply_default_toggle_button(styles.SimpleStyle, ((220,)*3, (150,)*3, "v"))
    ToggleButton.style_pressed.bck_color = ((150,)*3, (220,)*3, "v")
    apply_default_checkbox(styles.SimpleStyle)
    apply_default_radio(styles.CircleStyle)
    apply_default_switch()
    for s in SwitchButton.iter_styles():
        s.bck_color = (255,255,255)
    SwitchButton.style_hover.border_color = (0,0,255)
    SwitchButton.style_hover.border_thickness = 1
    SwitchButton.style_pressed = SwitchButton.style_hover.copy()
    #
    assign_styles()


def theme_text():
    p.current_theme = "text"
    #Button
    Button.style_normal = styles.TextStyle()
    Button.style_normal.font_color = (245,)*3
    Button.style_hover = Button.style_normal.copy()
    Button.style_hover.font_color = (255,255,255)
    Button.style_pressed = Button.style_hover.copy()
    apply_default_locked()
    apply_default_dragger(bck_color=Button.style_normal.font_color)
    _DraggerButton.style_hover.bck_color = Button.style_hover.font_color
    #Box
    apply_default_box(styles.SimpleStyle)
    Box.style_normal.bck_color = (200,200,200,200)
    Box.style_locked.bck_color = darken(Box.style_normal.bck_color)
    Button.style_locked.font_color = darken(Box.style_locked.bck_color)
    apply_default_titlebox(styles.TitleBoxSimpleStyle)
    TitleBox.style_normal.bck_color = Box.style_normal.bck_color
    #DropDownList
    apply_default_ddl(styles.SimpleStyle)
    DropDownList.style_normal.bck_color = change_alpha(Box.style_normal.bck_color, 200)
    apply_default_input(styles.SimpleStyle)
    #Text
    Text.style_normal = styles.TextStyle()
    Text.style_normal.font_color = Button.style_normal.font_color
    apply_default_label()
    #Lines
    apply_default_line(styles.SimpleStyle)
    #Sliders
    apply_default_slider(styles.SimpleStyle, darken(Box.style_normal.bck_color))
    #Images
    apply_default_image_style()
    #Helpers
    apply_default_helper()
    #Checkboxes and radios
    apply_default_toggle_button(styles.SimpleStyle, ((220,)*3, (150,)*3, "v"))
    ToggleButton.style_pressed.bck_color = ((150,)*3, (220,)*3, "v")
    apply_default_checkbox(styles.SimpleStyle)
    apply_default_radio(styles.CircleStyle)
    apply_default_switch()
    SwitchButton.style_normal.bck_color = (255,)*3
    #
    assign_styles()


def theme_text_dark():
    p.current_theme = "text_dark"
    #Button
    Button.style_normal = styles.TextStyle()
    Button.style_normal.font_color = (170,)*3
    Button.style_hover = Button.style_normal.copy()
    # Button.style_hover = styles.OscillatingTextStyle()
    Button.style_hover.font_color = (220,220,220)
    Button.style_pressed = Button.style_hover.copy()
    Button.style_pressed.font_color = darken(Button.style_hover.font_color)
    apply_default_locked()
    apply_default_dragger(bck_color=Button.style_normal.font_color)
    _DraggerButton.style_hover.bck_color = Button.style_hover.font_color
    #Box
    apply_default_box(styles.SimpleStyle)
    Box.style_normal.bck_color = (20,20,20,200)
    Box.style_locked.bck_color = enlighten(Box.style_normal.bck_color)
    Button.style_locked.font_color = enlighten(Box.style_locked.bck_color)
    apply_default_titlebox(styles.TitleBoxSimpleStyle)
    TitleBox.style_normal.bck_color = Box.style_normal.bck_color
    #DDL
    apply_default_ddl(styles.SimpleStyle)
    DropDownList.style_hover.bck_color = (255,255,255)
    DropDownList.style_normal.bck_color=(50,)*3 #pk DDL prend le style de box et pas de DDL ??
    _DropDownButton.style_normal = Button.style_normal.copy()
    _DropDownButton.style_hover = Button.style_hover.copy()
    _DropDownButton.style_pressed = Button.style_pressed.copy()
    _DropDownButton.style_locked = Button.style_locked.copy()
    apply_default_input(styles.SimpleStyle, (50,50,50), Button.style_normal.font_color)
    TextInput.style_locked.bck_color = darken(TextInput.style_normal.bck_color)
    #Text
    Text.style_normal = styles.TextStyle()
    Text.style_normal.font_color = Button.style_normal.font_color
    apply_default_label()
    #Lines
    apply_default_line(styles.SimpleStyle)
    #Sliders
    apply_default_slider(styles.SimpleStyle, enlighten(Box.style_normal.bck_color))
    #Images
    apply_default_image_style()
    #Helpers
    apply_default_helper()
    #Checkboxes and radios
    # apply_default_toggle_button(styles.SimpleStyle, (50,)*3)
    apply_default_toggle_button(styles.SimpleStyle, ((90,)*3, (30,)*3, "v"))
    set_style_attr("font_color", Button.style_normal.font_color, "all", only_to_cls=[ToggleButton])
    ToggleButton.style_pressed.bck_color = ((30,)*3, (90,)*3, "v")
    ToggleButton.style_pressed.font_color = darken(ToggleButton.style_normal.font_color)
    apply_default_checkbox(styles.SimpleStyle)
    apply_default_radio(styles.CircleStyle, bck_color=(200,)*3, colorkey=(0,0,0))
    apply_default_switch()
    #
    assign_styles()


def theme_game1(base_style=None,
                color1=(100,100,100),
                color2=(255,165,0),
                color3=(200,)*3):
    p.current_theme = "game1"
    if base_style is None:
        base_style = styles.GameStyle1
    def apply_variation_hover(cls):
        cls.style_hover.border_color = color2
        cls.style_hover.border_color2 = color2
        cls.style_hover.nframes = 20
        cls.style_hover.frame_mod = 2
        cls.style_hover.bck_color2 = enlighten(cls.style_hover.bck_color)
        cls.style_hover.thickness = 3
    #Button
    Button.style_normal = base_style()
    Button.style_normal.shadowgen = propose_shadowgen(Button.style_normal, fast=False)
    Button.style_normal.shadowgen.offset = (2,2)
    Button.style_normal.bck_color = color1
    Button.style_normal.bck_color2 = color1
    Button.style_normal.font_color = color3
    Button.style_normal.font_color2 = enlighten(Button.style_normal.font_color, 1.1)
    Button.style_normal.border_color2 = color1
    Button.style_normal.nframes = 20
    Button.style_normal.frame_mod = 2
    Button.style_hover = Button.style_normal.copy()
    Button.style_hover.font_color = color2
    Button.style_hover.font_color2 = color2
    apply_variation_hover(Button)
    Button.style_pressed = Button.style_hover.copy()
    Button.style_pressed.font_color = color2
    Button.style_pressed.bck_color = darken(Button.style_normal.bck_color)
    Button.style_pressed.offset = (2,2)
    apply_default_locked()
    apply_default_dragger()
    #Box and boxes-like
    # apply_default_box(base_style)
    apply_default_box(styles.RoundStyle)
    for s in Box.iter_styles():
        s.radius = 0
        s.bck_color = (0,0,0,127)
    # apply_default_titlebox(styles.TitleBoxGameStyle)
    apply_default_titlebox(styles.TitleBoxRoundStyle)
    TitleBox.style_normal.bck_color = Box.style_normal.bck_color
    TitleBox.style_normal.font_color = color2
    TitleBox.style_normal.line_color = color2
    TitleBox.style_normal.radius = 0
    #DropDownList
    apply_default_ddl(base_style)
    # apply_variation(_DropDownButton)
    _DropDownButton.style_hover.bck_color = color2
    #Text input
    apply_default_input(base_style)
    TextInput.style_hover.border_color = color2
    # TextInput.style_normal.bck_color = enlighten(Button.style_hover.bck_color)
    # TextInput.style_normal.font_color = Button.style_hover.bck_color
    #Text
    Text.style_normal = styles.TextStyle()
    # Text.style_normal.font_color = (50,)*3
    Text.style_normal.font_color = (250,)*3
    Text.style_hover = Text.style_normal
    Text.style_pressed = Text.style_normal
    Text.style_locked = Text.style_normal
    apply_default_label()
    #Lines
    apply_default_line(base_style)
    Line.style_normal.bck_color = Button.style_locked.bck_color
    #Sliders
    # apply_default_slider(base_style, (220,)*3) 
    apply_default_slider(base_style, Button.style_hover.bck_color)
    _SliderBar.style_normal = styles.RoundStyle()
    _SliderBar.style_normal.bck_color = enlighten(Button.style_hover.bck_color)
    # apply_variation(_SliderBar)
    #Images
    apply_default_image_style()
    #Helpers
    apply_default_helper()
    #Checkboxes and radios
    # ToggleButton.multi_shadows = True
    ToggleButton.style_normal = Button.style_normal.copy()
    ToggleButton.style_hover = Button.style_hover.copy()
    ToggleButton.style_pressed = Button.style_pressed.copy()
    ToggleButton.style_pressed.shadowgen = None
    # ToggleButton.style_pressed.border_color = (50,)*3
    ToggleButton.style_locked = Button.style_locked.copy()
    #
    apply_default_checkbox(base_style, radius=0.25, bck=enlighten(Button.style_normal.bck_color))
    Checkbox.style_hover.border_color = color2
    Checkbox.style_hover.font_color = color2
    Checkbox.style_pressed.font_color = color2
    Checkbox.style_hover.border_color = color2
    # apply_variation(Checkbox)
    apply_default_radio(styles.CircleStyle, bck_color=(200,)*3, colorkey=(0,0,0))
    apply_default_switch(bck=enlighten(Button.style_normal.bck_color))
    SwitchButton.style_hover.bck_color = SwitchButton.style_normal.bck_color
    # set_style_attr("shadowgen", None, "all", only_to_cls=SwitchButton)
    apply_variation_hover(SwitchButton)
    #Colorpickers
    apply_default_colorpickers()
    #
    assign_styles()

def theme_game2():
    p.current_theme = "game2"
    #Button
    base_style = styles.RoundStyle
    Button.style_normal = base_style()
    Button.style_normal.radius = 0
    Button.style_normal.border_thickness = 2
    # Button.style_normal.bck_color = (220,220,220,127)
    alpha = 180
    Button.style_normal.bck_color = ((180,180,180,alpha), (250,250,250,alpha), "v")
    Button.style_normal.border_color = (255,255,255,255)
    Button.style_normal.font_color = (255,255,255,255)
    Button.style_normal.border_thickness = 3
    Button.style_normal.has_second_draw = True
    Button.style_hover = Button.style_normal.copy()
    Button.style_hover.border_color = (255,127,0,255)
    Button.style_pressed = Button.style_hover.copy()
    Button.style_pressed.font_color = Button.style_pressed.border_color
    apply_default_locked()
    apply_default_dragger()
    #Box and boxes-like
    base_style = styles.SimpleStyle
    apply_default_box(base_style)
    Box.style_normal.bck_color = (220,220,220,127)
    # Box.style_normal.border_color = (220,220,220,127)
    apply_default_titlebox(styles.TitleBoxRoundStyle)
    TitleBox.style_normal.bck_color = Box.style_normal.bck_color
    TitleBox.style_normal.radius = 0
    # TitleBox.has_second_draw = True
    #DropDownList
    apply_default_ddl(base_style)
    DropDownList.style_normal.bck_color = ((180,180,180,255), (250,250,250,255), "v")
    # apply_variation(_DropDownButton)
    _DropDownButton.style_hover.bck_color = Button.style_hover.bck_color
    #Text input
    apply_default_input(base_style)
    # TextInput.style_hover.border_color = color2
    # TextInput.style_normal.bck_color = enlighten(Button.style_hover.bck_color)
    TextInput.style_locked = TextInput.style_normal.copy()
    #Text
    Text.style_normal = styles.TextStyle()
    Text.style_normal.font_color = (50,)*3
    Text.style_hover = Text.style_normal
    Text.style_pressed = Text.style_normal
    Text.style_locked = Text.style_normal
    apply_default_label()
    #Lines
    apply_default_line(base_style)
    Line.style_normal.bck_color = Button.style_locked.bck_color
    #Sliders
    apply_default_slider(base_style, Button.style_hover.bck_color)
    # _SliderBar.style_normal.bck_color = enlighten(Button.style_hover.bck_color)
    # apply_variation(_SliderBar)
    #Images
    apply_default_image_style()
    #Helpers
    apply_default_helper()
    #Checkboxes and radios
    # ToggleButton.multi_shadows = True
    ToggleButton.style_normal = Button.style_normal.copy()
    ToggleButton.style_hover = Button.style_hover.copy()
    ToggleButton.style_pressed = Button.style_pressed.copy()
    ToggleButton.style_pressed.font_color = ToggleButton.style_normal.font_color
    # ToggleButton.style_pressed.border_color = (50,)*3
    ToggleButton.style_locked = Button.style_locked.copy()
    #
    apply_default_checkbox(base_style)
    # apply_variation(Checkbox)
    apply_default_radio(styles.CircleStyle)
    apply_default_switch(bck=enlighten(Button.style_normal.bck_color))
    SwitchButton.style_hover.bck_color = SwitchButton.style_normal.bck_color
    # set_style_attr("shadowgen", None, "all", only_to_cls=SwitchButton)
    #Colorpickers
    apply_default_colorpickers()
    #
    assign_styles()


def set_style_attr(attr, value, states=None, exceptions_cls=None, only_to_cls=None):
    """Set a given style attribute for a group of element classes.
    ***Mandatory arguments***
    <attr> : (str) the name of the attribute.
    <value> : the value of the attribute.
    ***Optional arguments***
    <states> : either a string specifying the state concerned (e.g. 'hover') or 'all' for all states,
    or a sequence of states (e.g. ['hover', 'pressed']).
    <exception_cls> : a sequence of classes that are NOT concerned by the modification.
    <only_to_cls> : a sequence of classes to which retrain the application of the modification.
    """
    if states is None or states == "all":
        states = ["normal", "pressed", "hover", "locked"]
    elif isinstance(states, str):
        states = [states]
    if exceptions_cls is None:
        exceptions_cls = []
    if only_to_cls:
        classes = only_to_cls
    else:
        classes = all_classes
    for cls in classes:
        if not cls in exceptions_cls:
            for state in states:
                style = getattr(cls, "style_" + state)
                setattr(style, attr, value)

def refresh_all_states_style(element, recursive=True):
    for stylename in element.styles.keys():
        attr_name = "style_" + stylename
        new_style = getattr(element.__class__, attr_name)
        element.set_style(new_style, stylename)
    if recursive:
        for e in element.children:
            refresh_all_states_style(e, recursive=True)


def refresh_all_elements_style(root=None):
    if root is None:
        root = thorpy.get_current_loop().element
        if not root:
            raise Exception("Couldn't detect a root element. You should indicate one.")
    for e in root.get_all_descendants():
        refresh_all_states_style(e)

def get_theme_bck_color():
    """Returns current Button theme color."""
    return Button.style_normal.bck_color

def get_theme_main_bck_color():
    """Returns current Button theme color.
    The difference with get_theme_bck_color is that the latter can return gradient color, whereas
    get_theme_main_bck_color necessarily returns either a single RGB tuple, a single RGBA tuple or None."""
    return graphics.get_main_color(Button.style_normal.bck_color)

