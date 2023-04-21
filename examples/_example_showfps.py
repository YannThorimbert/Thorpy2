"""
We show here how to instanciate an element that displays the framerate of your app.
"""
#tags: FPS, ShowFPS, get_updater

import pygame, random
import thorpy as tp

pygame.init()
W,H = 1200, 700
screen = pygame.display.set_mode((W, H))
tp.init(screen, tp.theme_human) #bind screen to gui elements and set theme

def refresh():#some function that you call once per frame
    for i in range(n.get_value()):
        x = random.randint(0, W-60)
        y = random.randint(0, H-60)
        color = (random.randint(50,255),0,0)
        points = (x+10, y), (x+50,y), (x+50, y+40), (x+40,y+50), (x,y+50), (x,y+10)
        pygame.draw.polygon(screen, color, points)
        pygame.draw.aalines(screen, (0,0,0), True, points, 1)
    

clock = pygame.time.Clock()
max_fps = 120

fps = tp.ShowFPS(clock, pre="FPS:")
help_text = """Indicate below the number of new rectangles to blit each frame (to put pressure on FPS)"""
n = tp.SliderWithText("Number of rects", 0, 800, 0, 400)
descr = tp.Text(help_text, max_width=1000)
box = tp.TitleBox("Show FPS example", [fps, descr, n])
box.center_on(screen)

thorpy_updater = box.get_updater(max_fps)

playing = True
while playing:
    clock.tick(max_fps)
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            playing = False
        else:
            ... #do your stuff
    thorpy_updater.update(func_before=refresh, events=events)
    pygame.display.flip()
pygame.quit()

