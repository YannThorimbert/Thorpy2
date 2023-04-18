"""
In this example, we let the user choose a font amongst the available system fonts.
"""

import pygame
import thorpy as tp

pygame.init()
screen = pygame.display.set_mode((1200, 700))


tp.init(screen, tp.theme_human) #bind screen to gui elements and set theme


fonts = sorted(pygame.font.get_fonts())
buttons = []
style = tp.styles.SimpleStyle()
style_hover = style.copy()
style_hover.bck_color = (100,100,255)
for font_name in fonts:
    button = tp.Button(text=font_name, style_normal=style, all_styles_as_normal=True,
                           generate_surfaces=False)
    button.set_style(style_hover, "hover", refresh=False)
    button.set_font_name(font_name)
    buttons.append(button)

ddl = tp.DropDownListButton(buttons,
                                title=tp.get_default_font(),
                                size_limit=("auto",300),
                                launch_nonblocking=True)
choose_font = tp.Labelled("Choose a font ("+str(len(fonts))+" fonts detected)", ddl )
choose_font.set_value(tp.get_default_font())
font_size = tp.SliderWithText("Font size", 8, 30, 20, "h", 100)
text = tp.Text("Lorem ipsum dolor sit amet, consectetur adipiscing elit.")
text.set_max_text_width(400)
text.set_font_color((150,)*3)

group = tp.TitleBox("Choose a font", [choose_font, font_size, text])
group.center_on(screen)

def at_refresh():
    screen.fill((255,)*3)
    font = choose_font.get_value()
    if font or font_size.get_value() != text.get_current_style().font_size:
        group.set_font_name(font, apply_to_children=True)
        group.set_font_size(font_size.get_value(), apply_to_children=True)
        font_size.sort_children("h")
        choose_font.sort_children("h")
        group.sort_children()
group.get_updater().launch(at_refresh)
pygame.quit()