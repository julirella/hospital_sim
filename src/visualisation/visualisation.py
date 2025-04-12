import pygame
import sys

from src.visualisation import Map
from src.constants import *


class Visualiser:
    def __init__(self, dept_map: Map, sim_end_time: float):
        self.map = dept_map

        #init pygame, surfaces, font
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.fill('white')
        self.clock = pygame.time.Clock()
        # self.map_surf = pygame.surface.Surface((MAP_SURF_WIDTH, MAP_SURF_HEIGHT))
        self.text_surf = pygame.surface.Surface((TEXT_SURF_WIDTH, TEXT_SURF_HEIGHT))
        pygame.font.init()
        self._font = pygame.font.Font(None, 50)

        #set default times
        self.auto_increment_rate = 500 # how often to auto increment in milliseconds
        self.sim_time = 0 # sim time in seconds
        self.increment = 1 # how much to increment sim time by in seconds
        self.prev_increment = pygame.time.get_ticks() # time of last auto increment
        self.end_time = sim_end_time

        self.paused = True
        self.time_updated = True

    def display_map(self):
        map_surf = self.map.update_surface(self.sim_time)
        self.screen.blit(map_surf, (TEXT_SURF_WIDTH + TEXT_SURF_OFFSET, 0))

    def display_text(self):
        self.text_surf.fill('white')

        formatted_time = "{:.2f}".format(self.sim_time).rstrip('0').rstrip('.')
        formatted_increment = "{:.2f}".format(self.increment)

        time_text = self._font.render(formatted_time, True, 'black')
        self.text_surf.blit(time_text, (0, 0))

        time_text = self._font.render(formatted_increment + "x", True, 'black')
        self.text_surf.blit(time_text, (0, 60))

        if self.paused:
            time_text = self._font.render("pause" ,True, 'red')
            self.text_surf.blit(time_text, (0, 120))

        self.screen.blit(self.text_surf, (TEXT_SURF_OFFSET, TEXT_SURF_OFFSET))

    def update_sim_time(self, diff):
        self.sim_time += diff
        if self.sim_time < 0:
            self.sim_time = 0
        elif self.sim_time > self.end_time:
            self.sim_time = self.end_time

        self.time_updated = True

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

    def update_and_display(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.prev_increment >= self.auto_increment_rate:
            if not self.paused:
                self.update_sim_time(self.increment)
                self.prev_increment = current_time

        if self.time_updated:
            # only update map if time has changed
            self.display_map() #including everyone in rooms
            self.time_updated = False
        self.display_text()
        pygame.display.flip()
        self.clock.tick(60)

    def run(self):
        while True:
            self.process_input()
            self.update_and_display()


def main():
    # graph = Importer("input/layouts/testLayout.json").import_graphit_graph()
    # visualiser = Visualiser(graph)
    # visualiser.run()
    ...

if __name__ == "__main__":
    main()