from enum import IntEnum

MOVEMENT_TIME = 10
TIME_WITH_PATIENT = 20
REACTION_TIME = 1

class NurseMovement(IntEnum):
    REACTING = 1
    TO_PATIENT = 2
    WITH_PATIENT = 3
    FROM_PATIENT = 4


class Nurse:
    def __init__(self, id):
        self.id = id
        self.is_free = True
    
    def start_request(self, patient_id):
        self.is_free = False
        self.move_phase = NurseMovement.REACTING
        self.move_time = REACTION_TIME
        self.patient_id = patient_id

    def next_move_phase(self, time):
        #update 
        if self.move_phase == NurseMovement.FROM_PATIENT:
            self.is_free = True
            print(time, "nurse {} returned from patient {}".format(self.id, self.patient_id))
        else:
            self.move_phase += 1
            if self.move_phase == NurseMovement.TO_PATIENT:
                self.move_time = MOVEMENT_TIME
                print(time, "nurse {} departing to patient {}".format(self.id, self.patient_id))
            elif self.move_phase == NurseMovement.FROM_PATIENT:
                self.move_time = MOVEMENT_TIME
                print(time, "nurse {} dealt with request from patient {}".format(self.id, self.patient_id))
            else:
                self.move_time = TIME_WITH_PATIENT
                print(time, "nurse {} arrived at patient {}".format(self.id, self.patient_id))


    def move(self, time_steps, end_time):
        while not self.is_free:
            steps_remaining = self.move_time - time_steps
            if steps_remaining > 0:
                self.move_time = steps_remaining
                break
            elif steps_remaining == 0:
                self.next_move_phase(end_time)
                break
            else:
                time_steps -= self.move_time #move to end of phase
                self.next_move_phase(end_time - time_steps)


class Patient:
    def __init__(self, id, nurse_id):
        self.id = id
        self.nurse_id = nurse_id

def move_nurses(time_steps, nurses, free_nurses, busy_nurses, end_time):
    #move each nurse 
    busy_nurses_cp = busy_nurses.copy() #imperfect fix for elements being removed from set during iteration
    for nurse_id in busy_nurses_cp: 
        nurse = nurses[nurse_id]
        nurse.move(time_steps, end_time)
        #check if they have become free
        if nurse.is_free:
            busy_nurses.remove(nurse_id)
            free_nurses.add(nurse_id)


def choose_nurse(patient, nurses, free_nurses, busy_nurses, time):
    print(time, "request from patient {}".format(patient.id))
    nurse_id = patient.nurse_id
    assigned_nurse = nurses[nurse_id]

    if not assigned_nurse.is_free:
        nurse_id = free_nurses.pop_front() #problem if there are no free nurses. Also this isn't fair to the nurses cause it picks an arbitrary free nurse
        assigned_nurse = nurses[nurse_id]
        print(time, "nurse {} chosen for patient {} because nurse {} is busy".format(nurse_id, patient.id, patient.nurse_id))
    else:
        free_nurses.remove(nurse_id)
        print(time, "nurse {} chosen for patient {}".format(nurse_id, patient.id))

    assigned_nurse.start_request(patient.id)
    busy_nurses.add(nurse_id)



def simulate(requests, nurses, patients):
    busy_nurses = set()
    free_nurses = set()
    for nurse in nurses:
        free_nurses.add(nurse.id)
    
    prev_time = 0

    for req in requests:
        time = req[0] #time of next request
        time_steps = time - prev_time #time until next request

        #move nurses until request time
        move_nurses(time_steps, nurses, free_nurses, busy_nurses, time)

        # deal with request
        patient_id = req[1]
        patient = patients[patient_id]
        choose_nurse(patient, nurses, free_nurses, busy_nurses, time)
        prev_time = time

    #make sure everyone finishes what they're doing before the end
    sim_end_time = 100
    move_nurses(sim_end_time - time, nurses, free_nurses, busy_nurses, sim_end_time) 

print("Test 1") #one patient, one nurse
nurses = []
for i in range(1):
    nurses.append(Nurse(i))
patients = []
for i in range(1):
    patients.append(Patient(i, i % len(nurses)))
requests = [(1, 0)] #time, patient id
events = simulate(requests, nurses, patients)

print("Test 2")
requests = [(1, 0), (50, 0)] #time, patient id
events = simulate(requests, nurses, patients)

print("Test 3")
requests = [(1, 0), (42, 0)] #time, patient id
events = simulate(requests, nurses, patients)

print("Test 4") #multiple patients
nurses = []
for i in range(1):
    nurses.append(Nurse(i))
patients = []
for i in range(3):
    patients.append(Patient(i, i % len(nurses)))

requests = [(1, 0), (50, 1)] #time, patient id
events = simulate(requests, nurses, patients)

print("Test 5")
requests = [(1, 0), (42, 1)] #time, patient id
events = simulate(requests, nurses, patients)

print("Test 6") #multiple nurses
nurses = []
for i in range(2):
    nurses.append(Nurse(i))
patients = []
for i in range(3):
    patients.append(Patient(i, i % len(nurses)))

requests = [(1, 0), (50, 1)] #time, patient id
events = simulate(requests, nurses, patients)

print("Test 7") #overlapping request times
requests = [(1, 0), (25, 1)] #time, patient id
events = simulate(requests, nurses, patients)

print("Test 8") #nurse reassignment
requests = [(1, 0), (25, 2)] #time, patient id
events = simulate(requests, nurses, patients)

# print("Test 9") #no nurses free when a request comes - currently doesn't work
# requests = [(1, 0), (25, 2), (26, 1)] #time, patient id
# events = simulate(requests, nurses, patients)