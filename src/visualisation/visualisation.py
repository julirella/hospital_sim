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

        pygame.font.init()
        self._font = pygame.font.Font(None, 50)

        self.nurse_logs = nurse_logs

        self.time = 0
        self.increment = 1

        self.paused = False


    def pixel_ratio(self):
        width_ratio = MAP_SURF_WIDTH / self.map.width
        height_ratio = MAP_SURF_HEIGHT / self.map.height
        return min(width_ratio, height_ratio)

    def scale_point(self, point):
        return tuple(map(lambda x: x * self.pixels_per_meter, point))

    def display_map(self):
        map_surf = self.map.surface(self.time)
        self.screen.blit(map_surf, (0, 0))

    def display_text(self):
        time_text = self._font.render(str(self.time), True, 'white')
        self.screen.blit(time_text, (MAP_SURF_WIDTH + 20, 20))

    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused


        if not self.paused:
            self.time += self.increment

    def point_on_line(self, start: tuple[float, float], end: tuple[float, float], time_since_start: float, speed: float):
        dst_covered = time_since_start * speed
        start = np.array(start)
        end = np.array(end)
        direction = end - start
        unit_direction = direction / np.linalg.norm(direction)
        point = start + unit_direction * dst_covered
        return point.tolist()

    def put_nurse_in_room(self, nurse_id, row):
        patient_id = row['patient']
        self.map.put_nurse_in_room(nurse_id, patient_id)

    def put_nurse_in_corridor(self, nurse_id, prev_row, row_after_time):
        start = prev_row['x'].item(), prev_row['y'].item()
        end = row_after_time['x'].item(), row_after_time['y'].item()
        time_since_start = self.time - prev_row['time'].item()
        speed = self.map.nurse_by_id(nurse_id).speed
        nurse_pos = self.point_on_line(start, end, time_since_start, speed)
        self.map.put_nurse_in_corridor(nurse_id, nurse_pos)

    def update_nurses(self):
        # nurses:
        # if nurse is moving, just calculate exact position
        # otherwise figure out what room they're in and put them in the room to be displayed there

        for nurse_id, nurse_log in enumerate(self.nurse_logs):
            if self.time <= nurse_log.iloc[0]['time']:
                # put nurse in nurse office - assuming nurses always start in office
                self.map.put_nurse_in_office(nurse_id)
            elif self.time > nurse_log.iloc[-1]['time']:
                # assuming nurse always ends in room because all events end in room - this will fail if there's a time cut off
                self.put_nurse_in_room(nurse_id, nurse_log.iloc[-1])

            else:
                row_after_time = nurse_log[nurse_log['time'] >= self.time].iloc[0]
                action = row_after_time['action']

                if action == 'time at patient':
                    self.put_nurse_in_room(nurse_id, row_after_time)
                elif action == 'move to':
                    index_after_time = row_after_time.name.item()
                    prev_row = nurse_log.iloc[index_after_time - 1]
                    self.put_nurse_in_corridor(nurse_id, prev_row, row_after_time)
                elif action == 'unassign event' or action == 'assign event':
                    index_after_time = row_after_time.name.item()
                    prev_row = nurse_log.iloc[index_after_time - 1]
                    prev_pos = prev_row['x'].item(), prev_row['y'].item()
                    next_pos = row_after_time['x'].item(), row_after_time['y'].item()
                    if prev_pos == next_pos:  # TODO: check for float problems
                        # nurse is in room
                        self.put_nurse_in_room(nurse_id, prev_row)
                    else:
                        # nurse is walking in corridor
                        self.put_nurse_in_corridor(nurse_id, prev_row, row_after_time)
                else:
                    raise Exception('unknown action')  # finish action should probably not come up

    # def update_patients(self):
    #     #for each patient, figure out how many events they're waiting for
    #     ...

    def update(self):
        self.map.reset()
        self.update_nurses()
        # self.update_patients()

    def display(self):
        self.screen.fill('black')
        self.display_map() #including everyone in rooms
        self.display_text()
        pygame.display.flip()
        self.clock.tick(2)

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