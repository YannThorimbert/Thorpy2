import os
from . import elements
from . import styles
from . import loops
from .loops import Loop
from . import parameters
from . import graphics
from . import sound
from . import shadows
from .shadows import Shadow
from . import gametools
from .monitoring import Monitor

from .canonical import arrow_cursor, hand_cursor

#Import elements classes
from .elements import Alert, AlertWithChoices, ArrowButton, Box, Button, DropDownList, Image, Line
from .elements import Slider, SliderWithText, Text, TextInput, TitleBox, ToggleButton, Helper
from .elements import Checkbox, Radio, SwitchButton, SwitchButtonWithText, DropDownListButton
from .elements import ColorPicker, ColorPickerRGB, ColorPickerPredefined, ImageButton, HeterogeneousTexts
from .elements import TextAndImageButton, Lifebar, DeadButton, AnimatedGif, WaitingBar
from .elements import TogglablesPool, Labelled, LabelledColorPicker, Group, ShowFPS, TkDialog

#Import styling functions
from .themes import theme_classic, theme_human, theme_round, theme_simple, theme_text, theme_game2
from .themes import theme_round_gradient, theme_round2
from .themes import theme_text_dark, theme_game1, set_style_attr, refresh_all_elements_style, get_theme_bck_color, get_theme_main_bck_color
from .styles import get_default_font, set_default_font, get_text_size, get_text_height

__version__ = "2.0.92"

def set_screen(screen):
    """Set the default surface display for all elements that will be created after this call."""
    parameters.screen = screen

def get_screen():
    """Get the default surface display for elements that will be created after this call."""
    return parameters.screen

def init(screen, theme=None):
    """Initialize the display surface for the elements that will be created and set the default theme.
    ***Mandatory arguments***
    <screen> : Pygame surface used as default display surface for the element to draw.
    ***Optional arguments***
    <theme> : a thorpy theme function (e.g. thorpy.theme_classic). If no theme is passed, 'human' theme is used."""
    set_screen(screen)
    if theme:
        theme()
    else:
        themes.theme_human()

def fn(fn):
    """Refers a filename from Thorpy location on the disk. Mostly used for the examples, you should not use it."""
    return os.path.join(module_directory, fn)

def call_before_gui(func):
    """Sets the function to call by default before gui is drawn on screen, when using Thorpy's Updater object.
    If you integrate Thorpy element into your own loop, this must probably won't affect your code."""
    parameters.current_func_before = func

def set_waiting_bar(text_or_bar):
    """Sets the global waiting bar that will be shown to the user when he has to wait.
    <text_or_bar> : either a string or a WaitingBar. If it's a string, then Thorpy automatically
    generates a WaitingBar instance with this string as the text."""
    if isinstance(text_or_bar, str):
        parameters.waiting_bar = WaitingBar(text_or_bar)
    else:
        parameters.waiting_bar = text_or_bar

def refresh_waiting_bar():
    """Function to call each time the waiting bar has to be updated and drawn to the screen."""
    parameters.refresh_waiting_bar()

def pause():
    """Pauses the application until user press a key."""
    loops.pause()

get_current_loop = loops.get_current_loop
quit_current_loop = loops.quit_current_loop
quit_all_loops = loops.quit_all_loops
exit_app = loops.exit_app

module_path = os.path.abspath(__file__)
module_directory = os.path.dirname(module_path)