from __future__ import annotations
from typing import Sequence, Literal
import pygame
from pygame.math import Vector2 as V2


Coord = tuple[float|int, float|int]
Size = tuple[float|int, float|int]

V2orCoord = Coord|V2

# RGB = Tuple[int, int, int]
# RGBA = Tuple[int, int, int, int]
RGB = tuple[float|int, float|int, float|int]
RGBA = tuple[float|int, float|int, float|int,float|int]
RGB_OR_RGBA = RGB|RGBA
RGB_OR_RGBA_OR_NONE = RGB|RGBA|None

RGB_OR_RGBA_SEQ = RGB_OR_RGBA|Sequence[RGB_OR_RGBA]

# A sequence of exactly two RGB_OR_RGBA elements
ColorPair = tuple[RGB_OR_RGBA, RGB_OR_RGBA] | Sequence[RGB_OR_RGBA]  # Assuming the list has exactly two elements

ColorsAndOrientation = tuple[RGB_OR_RGBA_SEQ, str]
ColorAndNone = tuple[RGB_OR_RGBA_SEQ, None]
ProcessedGradient = ColorsAndOrientation|ColorAndNone

PygameAcceptedColor = RGB_OR_RGBA | pygame.Color

GradientColor = RGB_OR_RGBA | tuple[RGB_OR_RGBA_SEQ, str] | RGB_OR_RGBA_SEQ

PygCol = Literal['P', 'RGB', 'RGBX', 'RGBA', 'ARGB', 'BGRA', 'RGBA_PREMULT', 'ARGB_PREMULT']
PygCol2 = Literal['P', 'RGB', 'RGBX', 'RGBA', 'ARGB', 'BGRA']

RectOrElement = pygame.Rect | "Element"