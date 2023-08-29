"""We show here how to move an object from point A to point B in a smooth, animated way.
Note that you can pass either a rect or an element to the MovementManager instance."""
#tags: movement, smooth movement, smooth, animation, MovementManager


import sys, pygame, thorpy as tp

pygame.init()
W,H = 1200, 700
screen = pygame.display.set_mode((W, H))
tp.init(screen, tp.theme_human) #bind screen to gui elements and set theme

text = tp.Text("Click anywhere and the button will move to this location")
button = tp.Button("My button")
group = tp.Group([text, button])
player = group.get_updater()

mm = tp.gametools.MovementManager() #this data structures handles smooth movements

playing = True
while playing:
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            playing = False
        if e.type == pygame.MOUSEBUTTONDOWN:
            if button.state != "pressed" and button.state != "hover":
                mm.add(button, e.pos, vmax=1) #vmax is 1 by default
        else:
            ... #do your stuff with events
    screen.fill((250,)*3)
    mm.update()
    player.update(events=events) #update Thorpy elements
    pygame.display.flip()
pygame.quit()
