"""We show here how to directly launch an element, without having to click another one for that."""
#tags: text input, input, direct launch, direct, launch, integration


import pygame, thorpy as tp

pygame.init()
screen = pygame.display.set_mode((800, 600))

def launch_my_prompt():
    prompt = tp.TextInput("", "Enter your nickname")
    def on_validation():
        nickname.set_text(prompt.get_value())
    prompt.on_validation = on_validation
    box_around_prompt = tp.TitleBox("My Dialog Box", [prompt])
    box_around_prompt.center_on(screen)
    prompt.direct_launch(box_around_prompt)


def draw(): #do what you want with the display like in any pygame code you write
    screen.fill((255,255,255))

#Now let's pretend the UI elements below are what you need for your app:
tp.init(screen, tp.theme_round) #bind screen to gui elements and set theme

text = tp.Text("Press #RGB(0,200,0)<k># to launch a prompt") #fancy text with green color around '<k>'
text.set_font_rich_text_tag("#")
text2 = tp.Text("Current nickname set:")
nickname = tp.Text("Bob", font_color=(255,0,0), font_size=20)
group_nickname = tp.Group([text2, nickname], "h")
group = tp.Group([text, group_nickname])
group.center_on(screen)
updater = group.get_updater()

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
        else: #do your stuff with events
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_k:
                    launch_my_prompt()
    draw() #do your stuff with display
    #update Thorpy elements and draw them
    updater.update(events=events, mouse_rel=mouse_rel) 
    pygame.display.flip()
pygame.quit()