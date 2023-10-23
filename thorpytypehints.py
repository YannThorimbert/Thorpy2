from typing import Union, Tuple, List, Sequence, Literal
import pygame
from pygame.math import Vector2 as V2


FloatOrInt = Union[float, int]
Coord = Tuple[FloatOrInt, FloatOrInt]
Size = Tuple[FloatOrInt, FloatOrInt]

V2orCoord = Union[Coord, V2]

# RGB = Tuple[int, int, int]
# RGBA = Tuple[int, int, int, int]
RGB = Tuple[FloatOrInt, FloatOrInt, FloatOrInt]
RGBA = Tuple[FloatOrInt, FloatOrInt, FloatOrInt, FloatOrInt]
RGB_OR_RGBA = Union[RGB, RGBA]
RGB_OR_RGBA_OR_NONE = Union[RGB_OR_RGBA, None]

RGB_OR_RGBA_SEQ = Union[RGB_OR_RGBA,Sequence[RGB_OR_RGBA]]

# A sequence of exactly two RGB_OR_RGBA elements
ColorPair = Union[
    Tuple[RGB_OR_RGBA, RGB_OR_RGBA],
    List[RGB_OR_RGBA]  # Assuming the list has exactly two elements
]

ColorsAndOrientation = Tuple[RGB_OR_RGBA_SEQ, str]
ColorAndNone = Tuple[RGB_OR_RGBA_SEQ, None]
ProcessedGradient = Union[ColorsAndOrientation, ColorAndNone]

PygameAcceptedColor = Union[RGB_OR_RGBA, pygame.Color]

GradientColor = Union[RGB_OR_RGBA,
                      Tuple[RGB_OR_RGBA_SEQ, str],
                      RGB_OR_RGBA_SEQ]

PygCol = Literal['P', 'RGB', 'RGBX', 'RGBA', 'ARGB', 'BGRA', 'RGBA_PREMULT', 'ARGB_PREMULT']
PygCol2 = Literal['P', 'RGB', 'RGBX', 'RGBA', 'ARGB', 'BGRA']

RectOrElement = Union[pygame.Rect,"Element"]