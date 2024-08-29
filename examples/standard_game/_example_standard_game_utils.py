"""Helper file for _example_standard_game_menu.
Not designed to be part of any tutorial (dirty code disclosure)"""

import pygame, thorpy
from random import randint

def play_game(screen, difficulty, hero_color):
    difficulty_multiplier = {"Beginner":1, "Intermediate":2, "Pro":4}.get(difficulty, 1)
    W,H = screen.get_size()
    x,y = W//2, H//2 #position of the hero
    hero_rect = pygame.Rect(x,y,100,100)
    vx, vy = 5, 0 #velocity of the hero
    MAX_X = 2*W #size of the world
    S = 20 * difficulty_multiplier #obstacle size (obstacles are square)
    N_OBS = 20 #number of obstacles
    G = 0.5  #gravity
    MAX_VY = 8
    duration = 500 * difficulty_multiplier #duration of the game
    #get an image for the sky (blue gradient):
    gradient = thorpy.graphics.color_gradient(((50,50,255), (255,255,255)), (W,H), "v")
    img = pygame.Surface((S,S)) #image of the obstacles
    #generate the obstacles (rects)
    obstacles = [pygame.Rect(randint(0,MAX_X), randint(S,H-S), S,S) for i in range(N_OBS)]
    obstacles = [r for r in obstacles if not r.colliderect(hero_rect)]
    hero_rect.size = (20,20)
    #generate HUD elements ######################################################################
    # text_vel = thorpy.Text(str(vx)+" km/h")
    text_vel = thorpy.OutlinedText(str(vx)+" km/h", font_size=30)
    bar_dist = thorpy.Lifebar("Distance: 100%", 300, #text and length
                               bck_color=((255,80,80), (50,0,0), "v"), #vertical red to black
                               font_color=(50,0,0))
    group = thorpy.Group([bar_dist, text_vel], "h")
    group.stick_to(screen,"bottom","bottom")
    game_over = False
    def draw():
        screen.blit(gradient, (0,0)) #redraw sky, clearing the previous frame
        pygame.draw.rect(screen, hero_color, hero_rect)
        for rect in obstacles:
            screen.blit(img, rect)
        group.draw() #draw HUD
        if game_over:
            txt = thorpy.Text("Game Over")
            txt.set_font_size(72)
            txt.center_on(screen)
            txt.draw()
        pygame.display.flip()
    clock = pygame.time.Clock()
    for i in range(duration):
        clock.tick(60)
        #Refresh display ################################################
        text_vel.set_text(str(round(vx,1))+" km/h")
        bar_dist.set_value(1-i/duration)
        bar_dist.life_text.set_text("Distance: " + bar_dist.get_str_value_times() + "%")
        draw()
        #Game logics ###############################################
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT: #quit immediately, bypassing the rest
                pygame.quit()
                exit()
            elif e.type == pygame.KEYDOWN: #jump
                vy = -15*G
        vy += G #apply gravity
        vy = min(MAX_VY, vy)
        hero_rect.y += vy #hero doesn't move on x-axis ; the level moves towards him
        for rect in obstacles:
            rect.x -= vx
            if rect.right < 0:
                rect.x += MAX_X
            if rect.colliderect(hero_rect):
                game_over = True
        if not screen.get_rect().contains(hero_rect): #collision with border of screen
            game_over = True
        if game_over:
            t = thorpy.Alert("Game over", "You did not survive for the required duration")
            t.launch_alone()
            return False
        vx = 5 + 5 * i/1000
    t = thorpy.Alert("Congratulations", "You won this level")
    t.launch_alone()
    return True

