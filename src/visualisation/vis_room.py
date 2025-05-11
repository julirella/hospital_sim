import pygame

from src.constants import *
from .vis_nurse import VisNurse
from .. import Room, NurseOffice
from src.visualisation.vis_patient import VisPatient


class VisRoom:
    """
    class representing a room for visualisation
    """
    def __init__(self, orig_room: Room, pixels_per_meter: int, patients: list[VisPatient]) -> None:
        """
        :param orig_room: the corresponding simulation Room object
        :param pixels_per_meter: how many pixels does it take to draw a meter in the visualisation
        :param patients: list of visualisation patients
        """
        self._x = orig_room.x
        self._y = orig_room.y

        if type(orig_room) is NurseOffice:
            self._rim_colour = 'red'
        else: # it's a patient room
            self._rim_colour = 'blue'

        self._pixels_per_meter = pixels_per_meter
        self._patients = patients

        # create the room surface
        self._width_pixels = ROOM_SIDE_METERS * pixels_per_meter
        self._height_pixels = ROOM_SIDE_METERS * pixels_per_meter
        self._room_surf = pygame.surface.Surface((self._width_pixels, self._height_pixels))

        # create room rectangle to be drawn onto surface later
        self._rect = pygame.Rect(0, 0, self._width_pixels, self._height_pixels)

        # calculate dimensions of beds so that they fit in the room
        # patient bed width is the same as width of gap between beds and beds and walls
        self._patient_width = self._width_pixels / (2 * len(self._patients) + 1)
        self._patient_height = self._height_pixels / 2 - self._height_pixels / 6

        # prepare font for printing request counts on beds
        pygame.font.init()
        self._font = pygame.font.Font(None, int(self._patient_height))

        self._nurses: list[VisNurse] = []

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def add_nurse(self, nurse: VisNurse) -> None:
        """
        move nurse into the room
        :param nurse: the nurse that has entered the room
        """
        self._nurses.append(nurse)

    def remove_nurses(self) -> None:
        """
        remove all nurses from the room
        """
        self._nurses.clear()

    def surface(self, time: float) -> pygame.Surface:
        """
        draw room state at given time onto the surface
        :param time: the given time
        :return: the prepared room surface
        """
        # draw the room
        pygame.draw.rect(self._room_surf, 'white', self._rect) #background
        pygame.draw.rect(self._room_surf, self._rim_colour, self._rect, 1) #rim

        #draw patients
        for i, patient in enumerate(self._patients):
            x = self._patient_width + i * 2 * self._patient_width
            y = self._height_pixels * 2 / 3 - self._patient_height / 10
            patient_rect = (x, y, self._patient_width, self._patient_height)
            pygame.draw.rect(self._room_surf, patient.colour, patient_rect)
            text = self._font.render(str(patient.waiting_requests(time)), True, 'black')
            self._room_surf.blit(text, (x + self._patient_width / 10, y + self._patient_height / 10))

        #draw nurses
        nurse_radius = self._width_pixels / (2 * len(self._nurses) + 1)
        for i, nurse in enumerate(self._nurses):
            x = nurse_radius + i * 2 * nurse_radius + nurse_radius / 2
            y = self._height_pixels / 6 + nurse_radius / 2
            nurse.draw(self._room_surf, (x, y), self._pixels_per_meter)

        return self._room_surf