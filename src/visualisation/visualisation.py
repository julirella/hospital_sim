import pygame
import sys
import pandas as pd
import numpy as np

from src.visualisation import Map
from src.constants import *


class Visualiser:
    def __init__(self, dept_map: Map, nurse_logs: list[pd.DataFrame], sim_end_time: float):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.prev_increment = pygame.time.get_ticks()

        self.map_surf = pygame.surface.Surface((MAP_SURF_WIDTH, MAP_SURF_HEIGHT))
        self.map = dept_map
        self.pixels_per_meter = self.pixel_ratio()

        pygame.font.init()
        self._font = pygame.font.Font(None, 50)

        self.nurse_logs = nurse_logs

        self.increment_ms = 500 # how often to increment in milliseconds
        self.sim_time = 0
        self.increment = 1

        self.paused = True

        self.end_time = sim_end_time

    def pixel_ratio(self):
        width_ratio = MAP_SURF_WIDTH / self.map.width
        height_ratio = MAP_SURF_HEIGHT / self.map.height
        return min(width_ratio, height_ratio)

    def scale_point(self, point):
        return tuple(map(lambda x: x * self.pixels_per_meter, point))

    def display_map(self):
        map_surf = self.map.surface(self.sim_time)
        self.screen.blit(map_surf, (0, 0))

    def display_text(self):
        formatted_time = "{:.2f}".format(self.sim_time).rstrip('0').rstrip('.')
        formatted_increment = "{:.2f}".format(self.increment)

        time_text = self._font.render(formatted_time, True, 'black')
        self.screen.blit(time_text, (MAP_SURF_WIDTH, 20))

        time_text = self._font.render(formatted_increment + "x", True, 'black')
        self.screen.blit(time_text, (MAP_SURF_WIDTH, 80))

        if self.paused:
            time_text = self._font.render("pause" ,True, 'red')
            self.screen.blit(time_text, (MAP_SURF_WIDTH, 140))

    def update_sim_time(self, diff):
        self.sim_time += diff
        if self.sim_time < 0:
            self.sim_time = 0
        elif self.sim_time > self.end_time:
            self.sim_time = self.end_time

    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.paused:
                        self.prev_increment = pygame.time.get_ticks() # to wait before jumping after unpause
                    self.paused = not self.paused
                elif event.key == pygame.K_RIGHT:
                    self.update_sim_time(self.increment)
                elif event.key == pygame.K_LEFT:
                    self.update_sim_time(-self.increment)
                elif event.key == pygame.K_d:
                    self.increment += 0.1
                elif event.key == pygame.K_s:
                    self.increment -= 0.1
                elif event.key == pygame.K_r:
                    self.sim_time = 0

        # if not self.paused:
        #     self.time += self.increment

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
        time_since_start = self.sim_time - prev_row['time'].item()
        speed = self.map.nurse_by_id(nurse_id).speed
        nurse_pos = self.point_on_line(start, end, time_since_start, speed)
        self.map.put_nurse_in_corridor(nurse_id, nurse_pos)

    def update_nurses(self):
        # nurses:
        # if nurse is moving, just calculate exact position
        # otherwise figure out what room they're in and put them in the room to be displayed there

        for nurse_id, nurse_log in enumerate(self.nurse_logs):
            if self.sim_time <= nurse_log.iloc[0]['time']:
                # put nurse in nurse office - assuming nurses always start in office
                self.map.put_nurse_in_office(nurse_id)
            elif self.sim_time > nurse_log.iloc[-1]['time']:
                # assuming nurse always ends in room because all events end in room - this will fail if there's a time cut off
                self.put_nurse_in_room(nurse_id, nurse_log.iloc[-1])

            else:
                row_after_time = nurse_log[nurse_log['time'] >= self.sim_time].iloc[0]
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
        current_time = pygame.time.get_ticks()
        if current_time - self.prev_increment >= self.increment_ms:
            if not self.paused:
                self.update_sim_time(self.increment)
                self.prev_increment = current_time

        self.map.reset()
        self.update_nurses()
        # self.update_patients()

    def display(self):
        self.screen.fill('white')
        self.display_map() #including everyone in rooms
        self.display_text()
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