from enum import IntEnum
import math
import heapq
from sortedcontainers import SortedDict
import numpy as np
import pandas as pd

MOVEMENT_TIME = 10
TIME_WITH_PATIENT = 20
REACTION_TIME = 1

class NurseMovement(IntEnum):
    REACTING = 1
    TO_PATIENT = 2
    WITH_PATIENT = 3
    FROM_PATIENT = 4

class Event:
    def __init__(self, time):
        self.time = time
        self.log = {}
    
    def handle_event(self, nurses, free_nurses, busy_nurses):
        raise NotImplementedError()

class Request(Event):
    def __init__(self, time, patient, req_id):
        super().__init__(time)
        self.patient = patient
        self.id = req_id

    def handle_event(self, nurses, free_nurses, busy_nurses):
        print(self.time, "request from patient {}".format(self.patient.id))
        nurse_id = self.patient.nurse_id
        assigned_nurse = nurses[nurse_id]
        
        if len(free_nurses) == 0:
            min_busy_end = math.inf
            for busy_nurse_id in busy_nurses: #could just iterate over nurses at this point
                busy_nurse = nurses[busy_nurse_id] 
                if busy_nurse.busy_end_time < min_busy_end:
                    min_busy_end = busy_nurse.busy_end_time
            print(self.time, "all nurses busy, request pushed back to {}".format(min_busy_end))
            self.log = {'time' : self.time, 'type' : "request", "request_id" : self.id, 'patient_id' : self.patient.id, 'patient_dst:' : self.patient.office_dst, 'requested_nurse_id' : self.patient.nurse_id, 'pushed_back' : True, 'pushed_back_time' : min_busy_end}
            return Request(min_busy_end, self.patient, self.id)
        else:
            if not assigned_nurse.is_free:
                nurse_id = free_nurses.pop() 
                assigned_nurse = nurses[nurse_id]
                print(self.time, "nurse {} chosen for patient {} because nurse {} is busy".format(nurse_id, self.patient.id, self.patient.nurse_id))
                self.log = {'time' : self.time, 'type' : "request", "request_id" : self.id, 'patient_id' : self.patient.id, 'patient_dst:' : self.patient.office_dst, 'requested_nurse_id' : self.patient.nurse_id, 'chosen_nurse_id' : nurse_id, 'pushed_back' : False}
            else:
                free_nurses.remove(nurse_id)
                print(self.time, "nurse {} chosen for patient {}".format(nurse_id, self.patient.id))
                self.log = {'time' : self.time, 'type' : "request", "request_id" : self.id, 'patient_id' : self.patient.id, 'patient_dst:' : self.patient.office_dst, 'requested_nurse_id' : nurse_id, 'chosen_nurse_id' : nurse_id, 'pushed_back' : False}
            nextPhaseStart = assigned_nurse.start_request(self.patient, self.time, self)
            busy_nurses.add(nurse_id)
            return NursePhase(nextPhaseStart, assigned_nurse)

class NursePhase(Event):
    def __init__(self, time, nurse):
        super().__init__(time)
        self.nurse = nurse
    def handle_event(self, nurses, free_nurses, busy_nurses):
        self.log = self.nurse.next_phase(self.time)
        if self.nurse.is_free:
            nurse_id = self.nurse.id
            busy_nurses.remove(nurse_id)
            free_nurses.add(nurse_id)
            return None
        else:
            return NursePhase(self.nurse.nextPhaseStart, self.nurse)


class Patient:
    def __init__(self, id, nurse_id, office_dst):
        self.id = id
        self.nurse_id = nurse_id
        self.office_dst = office_dst
        

class Nurse:
    def __init__(self, id):
        self.id = id
        self.is_free = True
    
    def start_request(self, patient, time, request):
        self.assigned_req = request
        self.is_free = False
        self.move_phase = NurseMovement.REACTING
        self.patient_id = patient.id
        self.nextPhaseStart = time + REACTION_TIME
        self.patient_dst = patient.office_dst
        self.busy_end_time = time + REACTION_TIME + self.patient_dst * 2 + TIME_WITH_PATIENT
        return self.nextPhaseStart
    
    def next_phase(self, time):
        if self.move_phase == NurseMovement.FROM_PATIENT:
            self.is_free = True
            print(time, "nurse {} returned from patient {}".format(self.id, self.patient_id))
            return {'time' : time, 'type' : "nurse_phase", "request_id" : self.assigned_req.id, 'nurse_id' : self.id, 'patient_id' : self.patient_id, 'patient_dst:' : self.patient_dst, 'nurse_phase' : "returned"}
        else:
            self.move_phase += 1
            if self.move_phase == NurseMovement.TO_PATIENT:
                self.nextPhaseStart = time + self.patient_dst
                print(time, "nurse {} departing to patient {}".format(self.id, self.patient_id))
                return {'time' : time, 'type' : "nurse_phase", "request_id" : self.assigned_req.id, 'nurse_id' : self.id, 'patient_id' : self.patient_id, 'patient_dst:' : self.patient_dst, 'nurse_phase' : "departing"}
            elif self.move_phase == NurseMovement.FROM_PATIENT:
                self.nextPhaseStart = time + self.patient_dst
                print(time, "nurse {} dealt with request from patient {}".format(self.id, self.patient_id))
                return {'time' : time, 'type' : "nurse_phase", "request_id" : self.assigned_req.id, 'nurse_id' : self.id, 'patient_id' : self.patient_id, 'patient_dst:' : self.patient_dst, 'nurse_phase' : "dealt with request"}
            else:
                self.nextPhaseStart = time + TIME_WITH_PATIENT
                print(time, "nurse {} arrived at patient {}".format(self.id, self.patient_id))
                return {'time' : time, 'type' : "nurse_phase", "request_id" : self.assigned_req.id, 'nurse_id' : self.id, 'patient_id' : self.patient_id, 'patient_dst:' : self.patient_dst, 'nurse_phase' : "arrived"}
        
class EventQueue:
    def __init__(self, request_tuples, patients):
        #for now, constructs Request objects from tuples
        #later maybe accept list of requests instead
        self.events = SortedDict()
        for i, req_tuple in enumerate(request_tuples):
            time = req_tuple[0] 
            patient_id = req_tuple[1]
            req = Request(time, patients[patient_id], i)
            self.insert(req)

    def first_time(self):
        return next(iter(self.events.items())) #returns first (time, events)
    def first(self):
        time, events = self.first_time()
        return time, events[0]

    def insert(self, event):
        #insert a constructed Event object if event is not None
        if event is not None:
            time = event.time
            if time in self.events:
                self.events[time].append(event)
            else:
                self.events[time] = [event]
    def empty(self):
        return len(self.events) == 0

    def popFirst(self):
        time, events = self.first_time()
        if len(events) == 1:
            event = self.events.pop(time)[0]
        else:
            event = events.pop(0)
        return time, event


class Simulator:
    def __init__(self, requests, nurses, patients):
        self.events = EventQueue(requests, patients)
        # print(self.events.items())
        self.patients = patients
        self.nurses = nurses #.copy() ?
        self.busy_nurses = set()
        self.free_nurses = set()
        for nurse in nurses:
            self.free_nurses.add(nurse.id)

        self.log = []
    def simulate(self):
        while not self.events.empty():
            _, event = self.events.popFirst()
            newEvent = event.handle_event(self.nurses, self.free_nurses, self.busy_nurses)
            self.events.insert(newEvent)
            self.log.append(event.log)
        
        return self.log
        # df.to_csv('out.csv')

def generate_requests(patientAmount: int) -> list[float, int]:
    requests = []
    for patient_id in range(patientAmount):
        request_amount = np.random.randint(30, 70)
        for _ in range(request_amount):
            req_time = np.random.uniform(0, 3600)
            requests.append((req_time, patient_id))
    
    requests.sort()
    print(requests)
    print(len(requests))
    return requests

def create_nurses_and_patients(nurseAmount: int, patientAmount: int, randomNurses=False):
    nurses = []
    for i in range(nurseAmount):
        nurses.append(Nurse(i))

    patients = []
    for i in range(patientAmount):
        office_dst = (i+1)*5 #first patient is 5s away, each following is 5s further than the previous
        if(randomNurses):
            nurse_id = np.random.randint(0, nurseAmount)
        else:
            nurse_id = i % len(nurses)        
        patients.append(Patient(i, nurse_id, office_dst))
    
    return nurses, patients

def main():
    # print("Test 1") #one patient, one nurse
    # nurses = []
    # for i in range(1):
    #     nurses.append(Nurse(i))
    # patients = []
    # for i in range(1):
    #     patients.append(Patient(i, i % len(nurses)))
    # requests = [(1, 0)]
    # # requests = [(1, 0), (2, 1), (1, 1)]

    # generate_requests(2)
    # sim = Simulator(requests, nurses, patients)
    # sim.simulate()

    # print("Test 2")
    # requests = [(1, 0), (50, 0)] #time, patient id
    # sim = Simulator(requests, nurses, patients)
    # sim.simulate()

    # print("Test 3")
    # requests = [(1, 0), (42, 0)] #time, patient id
    # sim = Simulator(requests, nurses, patients)
    # sim.simulate()

    # print("Test 4") #multiple patients
    # nurses = []
    # for i in range(1):
    #     nurses.append(Nurse(i))
    # patients = []
    # for i in range(3):
    #     patients.append(Patient(i, i % len(nurses)))

    # requests = [(1, 0), (50, 1)] #time, patient id
    # sim = Simulator(requests, nurses, patients)
    # sim.simulate()

    # print("Test 5")
    # requests = [(1, 0), (42, 1)] #time, patient id
    # sim = Simulator(requests, nurses, patients)
    # sim.simulate()

    # print("Test 6") #multiple nurses
    nurses = []
    for i in range(2):
        nurses.append(Nurse(i))
    patients = []
    for i in range(3):
        patients.append(Patient(i, i % len(nurses)))

    # requests = [(1, 0), (50, 1)] #time, patient id
    # sim = Simulator(requests, nurses, patients)
    # sim.simulate()

    # print("Test 7") #overlapping request times
    # requests = [(1, 0), (25, 1)] #time, patient id
    # sim = Simulator(requests, nurses, patients)
    # sim.simulate()

    # print("Test 8") #nurse reassignment
    # requests = [(1, 0), (25, 2)] #time, patient id
    # sim = Simulator(requests, nurses, patients)
    # sim.simulate()

    print("Test 9") #no nurses free when a request comes
    requests = [(1, 0), (25, 2), (26, 1)] #time, patient id
    sim = Simulator(requests, nurses, patients)
    sim.simulate()

    # print("Test 10") #no nurses free when a request comes
    # requests = generate_requests(len(patients))
    # sim = Simulator(requests, nurses, patients)
    # sim.simulate()


if __name__ == "__main__":
    main()