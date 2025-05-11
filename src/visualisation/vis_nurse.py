import pygame
import pandas as pd

from src.constants import NURSE_SPEED_MPS, NURSE_RADIUS_METERS


class VisNurse:
    """
    class representing a nurse for visualisation
    """
    def __init__(self, colour: pygame.Color, nurse_log: pd.DataFrame) -> None:
        """
        :param colour: colour of the nurse circle
        :param nurse_log: the nurse's log from simulation
        """
        self.x = 0 # pixel x coordinate
        self.y = 0 # pixel y coordinate
        self.colour = colour
        self.nurse_log = nurse_log
        self.speed = NURSE_SPEED_MPS

    @property
    def pos(self) -> tuple[float, float]:
        return self.x, self.y

    def set_pos(self, pos: tuple[float, float]):
        self.x = pos[0]
        self.y = pos[1]

    def draw(self, surf: pygame.Surface, pos: tuple[float, float], pixels_per_meter: int) -> None:
        """
        draw a circle representing the nurse onto the surface at the given position
        :param surf: the surface to draw the nurse onto
        :param pos: x and y coordinate of the position at which to draw the nurse
        :param pixels_per_meter: how many pixels does it take to draw a meter in the visualisation
        """
        pygame.draw.circle(surf, self.colour, pos, NURSE_RADIUS_METERS * pixels_per_meter)