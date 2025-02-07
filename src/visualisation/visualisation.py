import pygame
import sys

from src import Graph
from src.importer import Importer
from src.visualisation import Map
from .constants import *


class Visualiser:
    def __init__(self, dept_map: Map):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.map_surf = pygame.surface.Surface((MAP_SURF_WIDTH, MAP_SURF_HEIGHT))
        self.map = dept_map
        self.pixels_per_meter = self.pixel_ratio()

    def pixel_ratio(self):
        width_ratio = MAP_SURF_WIDTH / self.map.width
        height_ratio = MAP_SURF_HEIGHT / self.map.height
        return min(width_ratio, height_ratio)

    def scale_point(self, point):
        return tuple(map(lambda x: x * self.pixels_per_meter, point))

    def display_map(self):
        self.map_surf.fill('white')

        for corridor in self.map.corridors:
            pygame.draw.line(self.map_surf, 'red', self.scale_point(corridor.one_end),
                             self.scale_point(corridor.other_end), 5)

        for room in self.map.rooms + [self.map.nurse_office]:
            rect = pygame.Rect(self.scale_point((room.x - ROOM_SIDE_METERS / 2, room.y - ROOM_SIDE_METERS / 2)) ,
                               self.scale_point((ROOM_SIDE_METERS, ROOM_SIDE_METERS)))
            pygame.draw.rect(self.map_surf, 'blue', rect)

        self.screen.blit(self.map_surf, (0, 0))

    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        pass

    def display(self):
        self.screen.fill('black')
        self.display_map()
        pygame.display.flip()
        self.clock.tick(60)

    def run(self):
        while True:
            self.process_input()
            self.update()
            self.display()


def main():
    # graph = Importer("input/layouts/testLayout.json").import_graphit_graph()
    # visualiser = Visualiser(graph)
    # visualiser.run()
    ...

if __name__ == "__main__":
    main()