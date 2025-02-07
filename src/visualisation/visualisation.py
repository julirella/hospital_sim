import pygame
import sys

from src import Graph
from src.importer import Importer


class Visualiser:
    def __init__(self, graph: Graph):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()

        self.graph_surf = pygame.surface.Surface((600, 400))

        self.graph = graph

    def display_graph(self):


    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        pass

    def display(self):
        self.screen.fill('black')
        pygame.display.flip()
        self.clock.tick(60)

    def run(self):
        while True:
            self.process_input()
            self.update()
            self.display()


def main():
    graph = Importer("input/layouts/testLayout.json").import_graphit_graph()
    visualiser = Visualiser(graph)
    visualiser.run()

if __name__ == "__main__":
    main()