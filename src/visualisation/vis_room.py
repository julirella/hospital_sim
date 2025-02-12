import pygame

from src.constants import *
from .vis_nurse import VisNurse
from .. import Room
from src.visualisation.vis_patient import VisPatient


class VisRoom:
    def __init__(self, orig_room: Room, pixels_per_meter: int, patients: list[VisPatient]):
        self._x = orig_room.x
        self._y = orig_room.y
        self._pixels_per_meter = pixels_per_meter
        self._width_pixels = ROOM_SIDE_METERS * pixels_per_meter
        self._height_pixels = ROOM_SIDE_METERS * pixels_per_meter
        self._room_surf = pygame.surface.Surface((self._width_pixels, self._height_pixels))
        self._patients = patients
        self._rect = pygame.Rect(0, 0, self._width_pixels, self._height_pixels)
        # patient bed width is the same as width of gap between beds and beds and walls
        self._patient_width = self._width_pixels / (2 * len(self._patients) + 1)
        self._patient_height = self._height_pixels / 2 - self._height_pixels / 6
        pygame.font.init() #maybe initialise globally somehow?
        self._font = pygame.font.Font(None, 36) #sort out adaptive size

        self._nurses: list[VisNurse] = []

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def add_nurse(self, nurse: VisNurse):
        self._nurses.append(nurse)

    def remove_nurses(self):
        self._nurses.clear()

    def surface(self, time: float):
        pygame.draw.rect(self._room_surf, 'white', self._rect) #background
        pygame.draw.rect(self._room_surf, 'blue', self._rect, 1) #rim

        #draw patients
        for i, patient in enumerate(self._patients):
            x = self._patient_width + i * 2 * self._patient_width
            y = self._height_pixels * 2 / 3
            patient_rect = (x, y, self._patient_width, self._patient_height)
            pygame.draw.rect(self._room_surf, patient.colour, patient_rect)
            text = self._font.render(str(patient.waiting_requests(time)), True, 'black')
            # self._room_surf.blit(text, (x, y))
            self._room_surf.blit(text, patient_rect) #maybe put it in center of rectangle to make it nicer

        #draw nurses
        nurse_radius = self._width_pixels / (2 * len(self._nurses) + 1)
        for i, nurse in enumerate(self._nurses):
            x = nurse_radius + i * 2 * nurse_radius + nurse_radius / 2
            y = self._height_pixels / 6 + nurse_radius / 2
            # pygame.draw.circle(self._room_surf, nurse.colour, (x, y), nurse_radius)
            nurse.draw(self._room_surf, (x, y), self._pixels_per_meter)


        return self._room_surf