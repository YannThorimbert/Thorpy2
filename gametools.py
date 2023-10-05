from pygame.math import Vector2 as V2
import pygame

from typing import List
import thorpytypehints as ty

LOREM_IPSUM:List[str] = """ Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus. Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor. Cras elementum ultrices diam. Maecenas ligula massa, varius a, semper congue, euismod non, mi. Proin porttitor, orci nec nonummy molestie, enim est eleifend mi, non fermentum diam nisl sit amet erat. Duis semper. Duis arcu massa, scelerisque vitae, consequat in, pretium a, enim. Pellentesque congue. Ut in risus volutpat libero pharetra tempor. Cras vestibulum bibendum augue. Praesent egestas leo in pede. Praesent blandit odio eu enim. Pellentesque sed dui ut augue blandit sodales. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Aliquam nibh. Mauris ac mauris sed pede pellentesque fermentum. Maecenas adipiscing ante non diam sodales hendrerit.
Ut velit mauris, egestas sed, gravida nec, ornare ut, mi. Aenean ut orci vel massa suscipit pulvinar. Nulla sollicitudin. Fusce varius, ligula non tempus aliquam, nunc turpis ullamcorper nibh, in tempus sapien eros vitae ligula. Pellentesque rhoncus nunc et augue. Integer id felis. Curabitur aliquet pellentesque diam. Integer quis metus vitae elit lobortis egestas. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Morbi vel erat non mauris convallis vehicula. Nulla et sapien. Integer tortor tellus, aliquam faucibus, convallis id, congue eu, quam. Mauris ullamcorper felis vitae erat. Proin feugiat, augue non elementum posuere, metus purus iaculis lectus, et tristique ligula justo vitae magna.

Aliquam convallis sollicitudin purus. Praesent aliquam, enim at fermentum mollis, ligula massa adipiscing nisl, ac euismod nibh nisl eu lectus. Fusce vulputate sem at sapien. Vivamus leo. Aliquam euismod libero eu enim. Nulla nec felis sed leo placerat imperdiet. Aenean suscipit nulla in justo. Suspendisse cursus rutrum augue. Nulla tincidunt tincidunt mi. Curabitur iaculis, lorem vel rhoncus faucibus, felis magna fermentum augue, et ultricies lacus lorem varius purus. Curabitur eu amet.""".replace("\n","").split(".")


def lorem_ipsum(n:int=4)->str:
    n = min(len(LOREM_IPSUM), n)
    return ".".join(LOREM_IPSUM[0:n]) + "."

def get_e_or_r_topleft(e:ty.RectOrElement):
    if isinstance(e, pygame.Rect):
        return e.topleft
    else:
        return e.rect.topleft

class MovementManager:
    """Generates smooth animated movements between two coordinates for a collection of
    pygame Rects or thorpy Elements."""
    def __init__(self)->None:
        self.elements:List[ty.RectOrElement] = []
        self.target_pos:List[V2] = []
        self.current_pos:List[V2] = []
        self.vmax:List[float] = []
        # self.params = []

    def add(self,
            element:ty.RectOrElement,
            target_pos:ty.Coord,
            vmax:float=1.,
            remove_if_already_moving:bool=True)->None:
        """Register a movement for a Rect or an element. The element will move from where it is now
        up to the target_pos.
        ***Mandatory arguments***
        <element> : either a pygame Rect or a thorpy element.
        <target_pos> : (2-tuple) coordinates of the target position.
        ***Optional arguments***
        <vmax> : (float) the maximum velocity during the movement.
        <remove_if_already_moving> : (bool) if True, then an object cannot be part of two movements at the same time.
        You probably want it True !"""
        if remove_if_already_moving:
            self.remove(element)
        self.elements.append(element)
        self.current_pos.append(V2(get_e_or_r_topleft(element)))
        self.target_pos.append(V2(target_pos))
        self.vmax.append(vmax)

    def pop(self, i:int)->None:
        self.elements.pop(i)
        self.target_pos.pop(i)
        self.current_pos.pop(i)
        self.vmax.pop(i)

    def update(self)->None:
        """Function to be called each frame of the app to update objects position as
        a part of the movement animation."""
        to_remove = []
        for i,e in enumerate(self.elements):
            d = (self.target_pos[i] - self.current_pos[i])
            D = d.length()
            if D < 1:
                to_remove.append(i)
                continue
            vel = d/2
            if vel.length() > self.vmax[i]:
                vel.scale_to_length(self.vmax[i])
            if D < self.vmax[i]:
                vel = d
            self.current_pos[i] += vel
            if isinstance(e, pygame.Rect):
                e.topleft = tuple(self.current_pos[i]) # type:ignore #(we let pygame cast the floats to int)
            else:
                e.set_topleft(*tuple(self.current_pos[i]))
        for i in to_remove[::-1]:
            self.pop(i)

    def remove(self, element)->None:
        if element in self.elements:
            index = self.elements.index(element)
            self.pop(index)