import pygame
from pygame.locals import *
import sys

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PATIENT_OFFSET = 100
IMG_TOP = 50
IMG_LEFT = 50
OFFICE_WIDTH = 100
DST_OFFSET = 20

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Event:
    def __init__(self, event_from_table: dict):
        self.time  = event_from_table['time']
        self.type = event_from_table['type']
        self.request_id = event_from_table['request_id']
        self.patient_id = event_from_table['patient_id']
        self.patient_dst = event_from_table['patient_dst']
        self.requested_nurse_id	 = event_from_table['requested_nurse_id']
        self.chosen_nurse_id = event_from_table['chosen_nurse_id']
        self.nurse_id = event_from_table['nurse_id']
        self.pushed_back = event_from_table['pushed_back']
        self.nurse_phase = event_from_table['nurse_phase']

class NursePos:
    def __init__(self):
        self.pos = 0
        self.patient = None
        self.dir = 0 #1 forward, -1 back, 0 nothing
        self.at_patient = False
        self.phase_time_left = 0 #maybe useless
    def move(self):
        if self.patient != None and self.at_patient == False:
            self.pos += self.dir
            self.phase_time_left -= 1

class PatientInfo:
    def __init__(self):
        self.req_cnt = 0

class State:
    def __init__(self, nurse_positions: list[NursePos], patient_infos: list[PatientInfo]):
        self.nurse_positions = nurse_positions
        self.patient_infos = patient_infos
    
    def tick_clock(self):
        for nurse_pos in self.nurse_positions:
                nurse_pos.move()
    
    def handle_event(self, event: Event):
        if event.type == 'request': #patient assigned but not moving yet
            nurse_id = event.chosen_nurse_id
            nurse_pos = self.nurse_positions[nurse_id]
            nurse_pos.patient = event.patient_id
            self.patient_infos[event.patient_id].req_cnt += 1
        elif event.type == 'nurse_phase':
            nurse_id = event.nurse_id
            nurse_pos = self.nurse_positions[nurse_id]

            if event.nurse_phase == 'departing':
                nurse_pos.dir = 1
                nurse_pos.phase_time_left = event.patient_dst
            elif event.nurse_phase == 'arrived':
                nurse_pos.at_patient = True
                nurse_pos.dir = 0
                nurse_pos.phase_time_left = 20 #TODO: have this as some global variable
                self.patient_infos[event.patient_id].req_cnt -= 1
            elif event.nurse_phase == 'dealt with request':
                nurse_pos.at_patient = False
                nurse_pos.dir = -1
                nurse_pos.phase_time_left = event.patient_dst
            elif event.nurse_phase == 'returned':
                nurse_pos.dir = 0

    
    def display(self):
        #nurse dots
        for nurse_pos in self.nurse_positions:
            patient = nurse_pos.patient
            if patient != None:
                pos = nurse_pos.pos
                pygame.draw.circle(self.screen, WHITE, (IMG_LEFT + OFFICE_WIDTH + DST_OFFSET*pos, patient * PATIENT_OFFSET + IMG_TOP), 5)

        #TODO: display something to show patient waiting for request fulfilment



class Plot:
    def __init__(self, events: list[dict] = None):
        self.events = []
        if events != None:
            for event in events:
                self.events.append(Event(event))

        #create states or accept them as arguments
        self.nurse_amount = 3
        self.patient_amount = 4
        self.patient_dsts = [10, 15, 20, 25]
        
        nurse_positions = []
        for _ in range(self.nurse_amount):
            nurse_positions.append(NursePos)
        patient_infos = []
        for _ in range(self.patient_amount):
            patient_infos.append(PatientInfo())
        self.state = State(nurse_positions, patient_infos)

        self.rect_height = max(self.nurse_amount, self.patient_amount) * PATIENT_OFFSET
        self.nurse_rect = pygame.Rect(IMG_LEFT, IMG_TOP, OFFICE_WIDTH, self.rect_height)

    def display_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
        self.clock = pygame.time.Clock()
        self.display_static()
        pygame.display.flip()

    def display_static(self):
        # self.screen.fill(WHITE)
        pygame.draw.rect(surface=self.screen, color=WHITE, rect=self.nurse_rect)
        for i, dst in enumerate(self.patient_dsts):
            pygame.draw.circle(self.screen, RED, (IMG_LEFT + OFFICE_WIDTH + DST_OFFSET*dst, i * PATIENT_OFFSET + IMG_TOP), 15)

            for j in range(1, dst + 1):
                pygame.draw.circle(self.screen, WHITE, (IMG_LEFT + OFFICE_WIDTH + DST_OFFSET*j, i * PATIENT_OFFSET + IMG_TOP), 5)
                  


    def display_state(self, state: State):
        ...

    def run(self):
        time = 0
        event_num = 0
        self.display_init()
        while True:
            for event in pygame.event.get():              
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            #handle all events in last second
            while self.events[event_num].time <= time:
                self.state.handle_event(self.events[event_num])
                event_num += 1 #will probably go out of range after last event
            self.state.tick_clock()
            self.state.display()
            time += 1
            self.clock.tick(1)



def main():
    plot = Plot()
    plot.run()

if __name__ == "__main__":
    main()