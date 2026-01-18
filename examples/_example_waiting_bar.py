"""We show here how to use a WaitingBar to indicate to the user he has to wait."""
#tags: wait, waiting bar, loading, loading bar, bar, progress bar, set_waiting_bar, WaitingBar, refresh_waiting_bar


import pygame, thorpy as tp

pygame.init()

screen = pygame.display.set_mode((1200, 700))
tp.init(screen, tp.theme_human) #bind screen to gui elements and set theme


#First, we prepare a WaitingBar object to show when needed:
waiting_bar = tp.WaitingBar("", #text is let empty here as we want a thin bar (see height argument)
                            length=200, #length of the bar in pixels
                            rect_color=(100,100,255), #color of the moving rect in the bar
                            speed=2.5, #speed of the moving rect in the bar
                            rel_width=0.2, #width of the moving rect in the bar, relatively to bar length
                            height=10, #height (thickness) of the bar
                            font_color=None) #keep default font color

#Then we indicate Thorpy that a waiting bar should be shown next time refresh_waiting_bar() is called.
tp.set_waiting_bar(waiting_bar)
# tp.set_waiting_bar("Loading stuff...") #if you indicate text, default waiting bar is used

#Now we define a button that will mimic a loading moment where the user has to wait a little bit.
button = tp.Button("Click to wait\n(yes, it's a bit weird)")
button.center_on(screen)

def load_heavy_stuff():
    for i in range(10000000//4): 
        import random #let's pretend we load some heavy stuff here
        x = (random.random()**0.4219) / (random.random()+1.) #random computation
        if i % 10000 == 0: #its up to you to decide how often you want to refresh
            tp.refresh_waiting_bar()
    print("Finished waiting !")
        
button.at_unclick = load_heavy_stuff #type:ignore

def before_gui(): #add here the things to do each frame before blitting gui elements
    screen.fill((200,)*3)
tp.call_before_gui(before_gui) #tells thorpy to call before_gui() before drawing gui.

#For the sake of brevity, the main loop is replaced here by a shorter but blackbox-like method
button.get_updater().launch()
pygame.quit()

