"""We show here how to add Thorpy elements to an existing code without any intrusive changes."""
#tags: get_updater, events handling, update, existing code, existing, loop, manual , events, events handling, update, draw, get_updater, integration, include

import pygame, thorpy as tp

pygame.init()
screen = pygame.display.set_mode((1200, 700))

def my_stuff(): #do what you want with the display like in any pygame code you write
    screen.fill((255,255,255))

#Now let's pretend the UI elements below are what you need for your app:
tp.init(screen, tp.theme_game2) #bind screen to gui elements and set theme
button = tp.Button("Hello, world (this button has no effect)")
ddl = tp.DropDownListButton(("Blah", "Blah", "Blah blah"), "My list", bck_func=my_stuff)
my_ui_elements = tp.Group([button, ddl])
updater = my_ui_elements.get_updater() #this will be used to update the UI elements

#Here is a very standard loop that includes only one line to update UI elements.
clock = pygame.time.Clock()
playing = True
while playing:
    clock.tick(60)
    events = pygame.event.get()
    mouse_rel = pygame.mouse.get_rel()
    for e in events:
        if e.type == pygame.QUIT:
            playing = False
        else:
            ... #do your stuff with events
    my_stuff() #do your stuff with display
    #update Thorpy elements and draw them
    updater.update(events=events,
                   mouse_rel=mouse_rel) #if you dont give a mouse_rel, Thorpy will call pygame mouse_rel() !
    pygame.display.flip()
pygame.quit()