import pygame

fallback_font_name = "arial"
fallback_font_size = 20

auto_shadow_threshold = 300*300

current_theme = "default"

current_func_before = None

screen = None

cursor = None

element_being_dragged = None

waiting_bar = None

def refresh():
    global element_being_dragged
    if not pygame.mouse.get_pressed()[0]:
        element_being_dragged = None

def refresh_waiting_bar():
    if waiting_bar:
        waiting_bar.refresh()