import pygame

from typing import Optional, Callable, TYPE_CHECKING
if TYPE_CHECKING:
    from .canonical import Element #type: ignore
    from .elements import WaitingBar #type: ignore

fallback_font_name:str = "arial"
fallback_font_size:int = 20

auto_shadow_threshold:int = 300*300

current_theme:str = "default"

current_func_before:Optional[Callable] = None

screen:Optional[pygame.Surface] = None

cursor:Optional[pygame.Cursor] = None

element_being_dragged:Optional["Element"] = None

waiting_bar:Optional["WaitingBar"] = None

def refresh()->None:
    global element_being_dragged
    if not pygame.mouse.get_pressed()[0]:
        element_being_dragged = None

def refresh_waiting_bar()->None:
    """Refreshes the waiting bar state, if any global waiting bar is set."""
    if waiting_bar:
        waiting_bar.refresh()