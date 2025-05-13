import pygame
import sys

from src.visualisation import Map
from src.constants import *


class Visualiser:
    """
    class for running the visualisation of the simulation
    """
    def __init__(self, dept_map: Map, sim_end_time: float):
        """
        :param dept_map: map of the department for visualisation
        :param sim_end_time: time at which the simulation ends
        """

        self.map = dept_map

        #init pygame, surfaces, font
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.fill('white')
        self.clock = pygame.time.Clock()
        self.text_surf = pygame.surface.Surface((TEXT_SURF_WIDTH, TEXT_SURF_HEIGHT))
        pygame.font.init()
        self.font = pygame.font.Font(None, 50)

        #set default times
        self.auto_increment_rate = 500 # how often to auto increment in milliseconds
        self.sim_time = 0 # sim time in seconds
        self.increment = 1 # how much to increment sim time by in seconds (later controlled by user)
        self.prev_increment = pygame.time.get_ticks() # time of last auto increment
        self.end_time = sim_end_time

        self.paused = True # visualisation paused flag
        self.time_updated = True # was time updated in the last iteration flag

    def __display_map__(self) -> None:
        # draw the map onto the screen

        map_surf = self.map.update_surface(self.sim_time)
        self.screen.blit(map_surf, (TEXT_SURF_WIDTH + TEXT_SURF_OFFSET, 0))

    def __display_text__(self) -> None:
        # print text containing info about visualisation progress onto the scree

        self.text_surf.fill('white')

        formatted_time = "{:.2f}".format(self.sim_time).rstrip('0').rstrip('.')
        formatted_increment = "{:.2f}".format(self.increment)

        time_text = self.font.render(formatted_time, True, 'black')
        self.text_surf.blit(time_text, (0, 0))

        time_text = self.font.render(formatted_increment + "x", True, 'black')
        self.text_surf.blit(time_text, (0, 60))

        if self.paused:
            time_text = self.font.render("pause", True, 'red')
            self.text_surf.blit(time_text, (0, 120))

        self.screen.blit(self.text_surf, (TEXT_SURF_OFFSET, TEXT_SURF_OFFSET))

    def __update_sim_time__(self, diff: float) -> None:
        # add diff to sim time and mark the change

        self.sim_time += diff
        if self.sim_time < 0:
            self.sim_time = 0
        elif self.sim_time > self.end_time:
            self.sim_time = self.end_time

        self.time_updated = True

    def __process_input__(self) -> None:
        # check for and process user input

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
                    self.__update_sim_time__(self.increment)
                elif event.key == pygame.K_LEFT:
                    self.__update_sim_time__(-self.increment)
                elif event.key == pygame.K_d:
                    self.increment += 0.1
                elif event.key == pygame.K_s:
                    self.increment -= 0.1
                elif event.key == pygame.K_r:
                    self.__update_sim_time__(-self.sim_time)

    def __update_and_display__(self) -> None:
        # increment sim time if it's time to do so and display the current state of the map

        current_time = pygame.time.get_ticks()
        if current_time - self.prev_increment >= self.auto_increment_rate:
            if not self.paused:
                self.__update_sim_time__(self.increment)
                self.prev_increment = current_time

        if self.time_updated:
            # only update map if time has changed
            self.__display_map__() #including everyone in rooms
            self.time_updated = False
        self.__display_text__()
        pygame.display.flip()
        self.clock.tick(60)

    def run(self) -> None:
        """
        run the visualisation
        """
        while True:
            self.__process_input__()
            self.__update_and_display__()
