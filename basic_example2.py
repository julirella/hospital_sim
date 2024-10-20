from enum import IntEnum
import math

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
    
    def handle_event(self, nurses, free_nurses, busy_nurses):
        raise NotImplementedError()

class Request(Event):
    def __init__(self, time, patient):
        super().__init__(time)
        self.patient = patient

    def handle_event(self, nurses, free_nurses, busy_nurses):
        print(self.time, "request from patient {}".format(self.patient.id))
        nurse_id = self.patient.nurse_id
        assigned_nurse = nurses[nurse_id]
        
        if len(free_nurses) == 0:
            min_busy_end = math.inf
            for nurse in busy_nurses:
                if nurse.busy_end_time < min_busy_end:
                    min_busy_end = nurse.busy_end_time
            print(self.time, "all nurses busy, request pushed back to {}".format(min_busy_end))
            return Request(min_busy_end, self.patient)
        else:
            if not assigned_nurse.is_free:
                nurse_id = free_nurses.pop() 
                assigned_nurse = nurses[nurse_id]
                print(self.time, "nurse {} chosen for patient {} because nurse {} is busy".format(nurse_id, self.patient.id, self.patient.nurse_id))
            else:
                free_nurses.remove(nurse_id)
                print(self.time, "nurse {} chosen for patient {}".format(nurse_id, self.patient.id))
            nextPhaseStart = assigned_nurse.start_request(self.patient.id, self.time)
            busy_nurses.add(nurse_id)
            return NursePhase(nextPhaseStart, assigned_nurse)

class NursePhase(Event):
    def __init__(self, time, nurse):
        super().__init__(time)
        self.nurse = nurse
    def handle_event(self, nurses, free_nurses, busy_nurses):
        self.nurse.next_phase(self.time)
        if self.nurse.is_free:
            nurse_id = self.nurse.id
            busy_nurses.remove(nurse_id)
            free_nurses.add(nurse_id)
            return NursePhase(self.nurse.nextPhaseStart, self.nurse)
        else:
            return None

class Patient:
    def __init__(self, id, nurse_id):
        self.id = id
        self.nurse_id = nurse_id
        

class Nurse:
    def __init__(self, id):
        self.id = id
        self.is_free = True
    
    def start_request(self, patient_id, time):
        self.is_free = False
        self.move_phase = NurseMovement.REACTING
        self.patient_id = patient_id
        self.nextPhaseStart = time + REACTION_TIME
        self.busy_end_time = time + REACTION_TIME + MOVEMENT_TIME * 2 + TIME_WITH_PATIENT
        return self.nextPhaseStart
    
    def next_phase(self, time):
        if self.move_phase == NurseMovement.FROM_PATIENT:
            self.is_free = True
            print(time, "nurse {} returned from patient {}".format(self.id, self.patient_id))
        else:
            self.move_phase += 1
            if self.move_phase == NurseMovement.TO_PATIENT:
                self.nextPhaseStart = time + MOVEMENT_TIME
                print(time, "nurse {} departing to patient {}".format(self.id, self.patient_id))
            elif self.move_phase == NurseMovement.FROM_PATIENT:
                self.move_time = time + MOVEMENT_TIME
                print(time, "nurse {} dealt with request from patient {}".format(self.id, self.patient_id))
            else:
                self.move_time = time + TIME_WITH_PATIENT
                print(time, "nurse {} arrived at patient {}".format(self.id, self.patient_id))
        
class EventQueue:
    def __init__(self, requests, patients):
        self.events = {}
        for req in requests:
            # print(req[0], patients[req[1]])
            # print("\n")
            self.insert((req[0], patients[req[1]]))

    def first_time(self):
        return next(iter(self.events.items())) #returns first (time, events)
    def first(self):
        time, events = self.first_time()
        return time, events[0]

    def insert(self, item):
        if item is not None:
            time = item[0]
            patient = item[1]
            if time in self.events:
                self.events[time].append(Request(time, patient))
            else:
                self.events[time] = [Request(time, patient)]

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
    
    def simulate(self):
        while not self.events.empty():
            _, event = self.events.popFirst()
            newEvent = event.handle_event(self.nurses, self.free_nurses, self.busy_nurses)
            self.events.insert(newEvent)


print("Test 1") #one patient, one nurse
nurses = []
for i in range(1):
    nurses.append(Nurse(i))
patients = []
for i in range(1):
    patients.append(Patient(i, i % len(nurses)))
requests = [(1, 0)]
# requests = [(1, 0), (2, 1), (1, 1)]
sim = Simulator(requests, nurses, patients)
sim.simulate()

print("Test 2")
requests = [(1, 0), (50, 0)] #time, patient id
sim = Simulator(requests, nurses, patients)
sim.simulate()

print("Test 3")
requests = [(1, 0), (42, 0)] #time, patient id
sim = Simulator(requests, nurses, patients)
sim.simulate()

print("Test 4") #multiple patients
nurses = []
for i in range(1):
    nurses.append(Nurse(i))
patients = []
for i in range(3):
    patients.append(Patient(i, i % len(nurses)))

requests = [(1, 0), (50, 1)] #time, patient id
sim = Simulator(requests, nurses, patients)
sim.simulate()

print("Test 5")
requests = [(1, 0), (42, 1)] #time, patient id
sim = Simulator(requests, nurses, patients)
sim.simulate()

print("Test 6") #multiple nurses
nurses = []
for i in range(2):
    nurses.append(Nurse(i))
patients = []
for i in range(3):
    patients.append(Patient(i, i % len(nurses)))

requests = [(1, 0), (50, 1)] #time, patient id
sim = Simulator(requests, nurses, patients)
sim.simulate()

print("Test 7") #overlapping request times
requests = [(1, 0), (25, 1)] #time, patient id
sim = Simulator(requests, nurses, patients)
sim.simulate()

print("Test 8") #nurse reassignment
requests = [(1, 0), (25, 2)] #time, patient id
sim = Simulator(requests, nurses, patients)
sim.simulate()

print("Test 9") #no nurses free when a request comes - currently doesn't work
requests = [(1, 0), (25, 2), (26, 1)] #time, patient id
sim = Simulator(requests, nurses, patients)
sim.simulate()
