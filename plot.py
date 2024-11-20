import pygame
from pygame.locals import *
import sys
import basic_example2 as be
import pandas as pd
import math
from time import sleep

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
        self.requested_nurse_id	 = self.to_int(event_from_table['requested_nurse_id'])
        self.chosen_nurse_id = self.to_int(event_from_table['chosen_nurse_id'])
        self.nurse_id = self.to_int(event_from_table['nurse_id'])
        self.pushed_back = event_from_table['pushed_back']
        self.nurse_phase = event_from_table['nurse_phase']

    def to_int(self, num):
        #TODO some less hacky solution
        if math.isnan(num):
            return -1
        else:
            return int(num)

class NursePos:
    def __init__(self, colour: pygame.Color):
        self.pos = 0
        self.patient = None
        self.dir = 0 #1 forward, -1 back, 0 nothing
        self.at_patient = False
        self.phase_time_left = 0 #maybe useless
        self.colour = colour
    def move(self):
        if self.patient != None and self.at_patient == False:
            self.pos += self.dir
            self.phase_time_left -= 1

class PatientInfo:
    def __init__(self, colour: pygame.Color, office_dst: int):
        self.req_cnt = 0
        self.colour = colour
        self.office_dst = office_dst

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
                nurse_pos.patient = None

    
    def display(self, surf: pygame.Surface):
        #nurse dots
        free_nurses = 0
        for nurse_pos in self.nurse_positions:
            patient = nurse_pos.patient
            if patient != None:
                pos = nurse_pos.pos
                pygame.draw.circle(surf, nurse_pos.colour, (OFFICE_WIDTH + DST_OFFSET*pos, patient * PATIENT_OFFSET + PATIENT_OFFSET // 2), 5)
            else:
                pygame.draw.circle(surf, nurse_pos.colour, (30, 30 + free_nurses * 30), 10)
                free_nurses += 1

        #TODO: display something to show patient waiting for request fulfilment



class Plot:
    def __init__(self, events: list[dict], nurse_amount: int, patient_amount: int, patient_dsts: list[int], patient_nurses: list[int]):
        self.events = []
        for event in events:
            self.events.append(Event(event))

        #create states or accept them as arguments
        self.nurse_amount = nurse_amount
        self.patient_amount = patient_amount
        self.patient_dsts = patient_dsts
        
        nurse_positions = []
        for i in range(self.nurse_amount):
            colour = self.int_to_colour(i, nurse_amount)
            nurse_positions.append(NursePos(colour))
        patient_infos = []
        for i in range(self.patient_amount):
            colour = self.int_to_colour(patient_nurses[i], nurse_amount)
            patient_infos.append(PatientInfo(colour, patient_dsts[i]))
        self.state = State(nurse_positions, patient_infos)

        self.rect_height = max(self.nurse_amount, self.patient_amount) * PATIENT_OFFSET
        self.nurse_rect = pygame.Rect(0, 0, OFFICE_WIDTH, self.rect_height)

    def int_to_colour(self, num: int, total_colours: int) -> pygame.Color:
        step = 360 // total_colours
        colour = pygame.Color(0, 0, 0, 0)
        colour.hsva = (step * num, 100, 100, 50)
        return colour

    def display_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.info_surf = pygame.Surface((200, 100))
        self.image_surf = pygame.Surface((SCREEN_WIDTH - 300, SCREEN_HEIGHT))
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.clock = pygame.time.Clock()
        self.display_static()
        pygame.display.flip()

    def display_static(self):
        self.image_surf.fill(BLACK)
        pygame.draw.rect(surface=self.image_surf, color=WHITE, rect=self.nurse_rect)
        for i, patient_info in enumerate(self.state.patient_infos):
            pygame.draw.circle(self.image_surf, patient_info.colour, (OFFICE_WIDTH + DST_OFFSET*patient_info.office_dst, i * PATIENT_OFFSET + PATIENT_OFFSET // 2), 15)

            for j in range(1, patient_info.office_dst + 1):
                pygame.draw.circle(self.image_surf, WHITE, (OFFICE_WIDTH + DST_OFFSET*j, i * PATIENT_OFFSET + PATIENT_OFFSET // 2), 5)
        
        self.screen.blit(self.image_surf, (50, 50))
        # pygame.display.flip() #fixes dots staying on office edge. Probably eventually put static stuff on a different surface and just blit it
        

    def display_info(self, time: int):
        self.info_surf.fill(WHITE)
        text = self.font.render("time: " + str(time), True, BLACK)
        self.info_surf.blit(text, (5, 5))  # Position: (50, 50)
        self.screen.blit(self.info_surf, (SCREEN_WIDTH - 200, 0))

    def run(self):
        time = 0
        event_num = 0
        self.display_init()
        sleep(2)
        print("here")
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
            self.display_static() #maybe only overwrite the parts that need to be
            self.display_info(time)

            self.state.display(self.image_surf)
            self.screen.blit(self.image_surf, (50, 50)) #this is being blitted in 2 different places!!
            pygame.display.flip()
            time += 1
            self.clock.tick(1)



def main():
    #TODO sort out how to run this from jupyter
    nurse_amount = 5
    patient_amount = 8
    nurses, patients = be.create_nurses_and_patients(nurseAmount=nurse_amount, patientAmount=patient_amount)
    requests = [(1, 0), (25, 2), (26, 1), (50, 0)] #time, patient id
    patient_dsts = []
    patient_nurses = []
    for patient in patients:
        patient_dsts.append(patient.office_dst)
        patient_nurses.append(patient.nurse_id)
    sim = be.Simulator(requests, nurses, patients)
    out = sim.simulate()
    df2 = pd.DataFrame(out) #TODO design some structure to not have to go through df to keep NaNs
    outDict = df2.to_dict(orient='records') 
    plot = Plot(outDict, nurse_amount, patient_amount, patient_dsts, patient_nurses)
    plot.run()

if __name__ == "__main__":
    main()