import pygame
import sys
import pandas as pd
import numpy as np

from src.visualisation import Map
from src.constants import *


class Visualiser:
    def __init__(self, dept_map: Map, nurse_logs: list[pd.DataFrame]):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.map_surf = pygame.surface.Surface((MAP_SURF_WIDTH, MAP_SURF_HEIGHT))
        self.map = dept_map
        self.pixels_per_meter = self.pixel_ratio()

        self.nurse_logs = nurse_logs



        self.time = 15


    def pixel_ratio(self):
        width_ratio = MAP_SURF_WIDTH / self.map.width
        height_ratio = MAP_SURF_HEIGHT / self.map.height
        return min(width_ratio, height_ratio)

    def scale_point(self, point):
        return tuple(map(lambda x: x * self.pixels_per_meter, point))

    def display_map(self):
        map_surf = self.map.surface()
        self.screen.blit(map_surf, (0, 0))

    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def point_on_line(self, start: tuple[float, float], end: tuple[float, float], time_since_start: float, speed: float):
        dst_covered = time_since_start * speed
        start = np.array(start)
        end = np.array(end)
        direction = end - start
        unit_direction = direction / np.linalg.norm(direction)
        point = start + unit_direction * dst_covered
        return point.tolist()

    def update(self):
        self.map.reset()
        #nurses:
        #if nurse is moving, just calculate exact position
        #otherwise figure out what room they're in and put them in the room to be displayed there

        for nurse_id, nurse_log in enumerate(self.nurse_logs):
            row_after_time = nurse_log[nurse_log['time'] >= self.time].iloc[0]
            action = row_after_time['action']
            if action == 'time at patient':
                #figure out room and put nurse there
                pass
            elif action == 'move to':
                index_after_time = row_after_time.name.item()
                prev_row = nurse_log.iloc[index_after_time - 1]
                start = prev_row['x'].item(), prev_row['y'].item()
                end = row_after_time['x'].item(), row_after_time['y'].item()
                time_since_start = self.time - prev_row['time'].item()
                speed = self.map.nurse_by_id(nurse_id).speed
                nurse_pos = self.point_on_line(start, end, time_since_start, speed)
                self.map.put_nurse_in_corridor(nurse_id, nurse_pos)

            elif action == 'assign event':
                #???
                pass
            elif action == 'unassign event':
                #???
                pass
            else:
                raise Exception('unknown action') #finish action should probably not come up


    def display(self):
        self.screen.fill('black')
        self.display_map() #including everyone in rooms
        #display moving nurses
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