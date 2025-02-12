import pygame

from src.constants import NURSE_SPEED_MPS, NURSE_RADIUS_METERS


class VisNurse:
    def __init__(self, colour):
        self.x = 0
        self.y = 0
        self.colour = colour
        self.speed = NURSE_SPEED_MPS

    @property
    def pos(self):
        return self.x, self.y

    def set_pos(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def draw(self, surf, pos, pixels_per_meter):
        pygame.draw.circle(surf, self.colour, pos, NURSE_RADIUS_METERS * pixels_per_meter)