import pygame
from typing import Optional, List, Dict, Callable, Tuple

from . import parameters as p


class Loop:

    def __init__(self, element:Optional["Element"]=None,
                 fps:int=60,
                 manually_updated:bool=True):
        """
        <element> : parent of all elements that are handled by this loop.
        <manually_updated> : set to True if this Loop's update method is called
        by you (end-user).
        """
        self.element:Optional["Element"] = element
        self.to_update:List["Element"] = [] #!!! List of elements to visually update
        self.fps:int = fps
        self.clock:pygame.time.Clock = pygame.time.Clock()
        self.iteration:int = 0
        self.playing:bool = True
        self.click_outside_cancel:bool = True
        if manually_updated:
            self.click_outside_cancel = False
        self.esc_quit:bool = True
        self.min_iterations_between_clicks:int = self.fps // 2 #set to 0 if not needed
        # self.last_click = -float("inf")
        if manually_updated:
            loops.append(self)
        self.manually_updated:bool = manually_updated
        # self.reactions = {}

    # def user_is_allowed_to_click_again(self):
    #     dt = self.iteration - self.last_click
    #     if dt >= self.min_iterations_between_clicks:
    #         self.last_click = self.iteration
    #         return True
    #     return False

    def reaction(self, e)->None: #event e
        pass

    def update(self,
               func_before:Optional[Callable]=None,
               no_state_change:bool=True,
               events:Optional[List[pygame.event.Event]]=None,
               func_after:Optional[Callable]=None,
               mouse_rel:Optional[Tuple[int,int]]=None)->None:
        """Update and draw the thorpy elements.
        Method to call each frame of the game if you do not use automatic thorpy loops
        (typically, use this method in your own main loop, after drawing everything on the screen).
        ***Optional arguments***
        <events> : list of the events to handle from your pygame loop.
        <func_before> : function that is called before updating and drawing the elements.
        <func_after> : function that is called after updating and drawing the elements.
        <mouse_rel> : the change in position of the mouse since last call. If you dont indicate it,
        then Thorpy must call it. Otherwise, it just uses the value you give.
        """
        assert self.element
        if self.fps > 0:
            self.clock.tick(self.fps)
        if func_before:
            func_before()
        if mouse_rel is None:
            mouse_rel = pygame.mouse.get_rel()
        if events is None:
            events = pygame.event.get()
        else:
            assert self.manually_updated
        for e in events:
            self.reaction(e)
            if e.type == pygame.QUIT:
                quit_all_loops()
                pygame.event.post(pygame.event.Event(pygame.QUIT))
                return
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if self.click_outside_cancel:
                    if not self.element.rect.collidepoint(pygame.mouse.get_pos()):
                        if self.element.at_cancel:
                            self.element.at_cancel()
                        if self.element.loop_give_back:
                            self.element.remove_from_loop()
                        else:
                            quit_current_loop()
                self.element.react_button(e.button)
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE and self.esc_quit:
                    quit_current_loop()
            
        if no_state_change:
            for e in self.to_update: #reminder : to_update is not necessarily part of self.element's children
                e.update_no_state_change(mouse_rel)
                e.draw()
        else:
            for e in self.to_update:
                e.update(mouse_rel)
                e.draw()
        self.element.update(mouse_rel)
        self.element.draw()
        if func_after:
            func_after()
        p.refresh()
        self.iteration += 1

    def launch(self,
               func_before:Optional[Callable]=None,
               func_after:Optional[Callable]=None)->None:
        if self.fps < 0:
            self.fps = 60
        if self.manually_updated:
            loops.remove(self)
            self.manually_updated = False
        self.playing = True
        loops.append(self)
        if func_before is None and p.current_func_before:
            func_before = p.current_func_before
        while self.playing:
            self.clock.tick(self.fps)
            self.update(func_before, func_after=func_after)
            pygame.display.flip()
            self.iteration += 1


loops: List[Loop] = []


def pause(debug_msg:str="Thorpy pause - press a key to continue")->None:
    print(debug_msg)
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN or e.type == pygame.MOUSEBUTTONDOWN:
                return
            elif e.type == pygame.QUIT:
                quit_all_loops()
                pygame.event.post(pygame.event.Event(pygame.QUIT))
                return


def get_current_loop()->Optional[Loop]:
    if loops:
        return loops[-1]
    return None

def quit_current_loop()->Loop:
    loop = loops.pop()
    loop.playing = False
    # new_loop = get_current_loop()
    # if new_loop:
    #     new_loop.last_click = loop.iteration - loop.last_click
    return loop

def quit_all_loops()->None:
    for i in range(len(loops)):
        quit_current_loop()

def exit_app()->None:
    quit_all_loops()
    pygame.quit()
    exit()


#this is the function that elements will call to launch themselves.
#it wraps the functionnalities of Loop.
def loop_elements(main_element:"Element",
                    others:List["Element"],
                    func_before:Optional[Callable]=None,
                    click_outside_cancel:bool=True,
                    reaction:Optional[pygame.event.Event]=None,
                    esc_quit:bool=True,
                    func_after:Optional[Callable]=None)->None:
    loop = Loop(main_element, manually_updated=False)
    if reaction:
        loop.reaction = reaction #type:ignore #sorry for that
    loop.click_outside_cancel = click_outside_cancel
    loop.esc_quit = True
    loop.to_update = others
    # old = get_current_loop()
    # if old:
    #     dt = old.iteration - old.last_click
    #     loop.last_click = loop.iteration - dt
    loop.launch(func_before)
