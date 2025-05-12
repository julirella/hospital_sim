import pandas as pd
from math import sqrt
from itertools import chain
import numpy as np
import csv

from src.importer.gen_importer import GenImporter

class DataProcessor:
    """
    class for processing data and calculating statistics from nurse and event logs
    """
    def __init__(self, nurse_log_path, event_log_path, people_path) -> None:
        """
        :param nurse_log_path: path to nurse log file
        :param event_log_path: path to event log file
        :param people_path: path to the sim input file specifying nurses and patients
        """

        # create dataframes
        self.nurse_df = pd.read_csv(nurse_log_path)
        self.event_df = pd.read_csv(event_log_path)

        # import people from file (it would be better to create a separate importer for people only)
        gen_importer = GenImporter("", people_path)
        gen_importer.import_people()
        self.nurse_patients = gen_importer.nurse_patients
        self.patient_cnt = gen_importer.patient_cnt
        

    def __row_diff__(self, row_num: int, df: pd.DataFrame, col_name: str):
        #calculates difference between items in col_name in df on rows row_num and the one before it
        #the column must be of a numerical type
        if row_num < 1:
            raise Exception("Row_num must be at least 1 (second row)")
        start_row = df.loc[row_num - 1]
        end_row = df.loc[row_num]
        start_item = start_row[col_name]
        end_item = end_row[col_name]
        return end_item - start_item
    
    def nurse_dst_walked(self, nurse_id):
        """
        calculate the total distance the nurse walked
        :param nurse_id: ID of the nurse
        :return: total distance walked
        """
        move_rows = self.nurse_df[(self.nurse_df['nurse'] == nurse_id) & (self.nurse_df['action'] == "move to")].index.tolist()
        total_dst = 0
        for row in move_rows:
            x_dst = self.__row_diff__(row, self.nurse_df, "x")
            y_dst = self.__row_diff__(row, self.nurse_df, "y")
            distance = sqrt(x_dst ** 2 + y_dst ** 2)
            total_dst += distance
        
        return total_dst
    
    def nurse_time_walked(self, nurse_id):
        """
        calculate the total time the nurse spent walking
        :param nurse_id: ID of the nurse
        :return: total time spent walking
        """
        move_rows = self.nurse_df[(self.nurse_df['nurse'] == nurse_id) & (self.nurse_df['action'] == "move to")].index.tolist()
        total_time = 0
        for row in move_rows:
            total_time += self.__row_diff__(row, self.nurse_df, "time")
        return total_time

    def nurse_time_at_patient(self, nurse_id, patient_id):
        """
        calculates total time the given nurse spent caring for the given patient
        :param nurse_id: ID of the nurse
        :param patient_id: ID of the patient
        :return: the resulting time
        """

        #assuming the df is sorted by nurse_id first and time second
        events = self.nurse_df[(self.nurse_df['nurse'] == nurse_id) & (self.nurse_df['patient'] == patient_id) & (self.nurse_df['action'] == "time at patient")].event.tolist()
        total_time = 0
        for event in events:
            total_event_time = 0
            event_df = self.nurse_df[self.nurse_df['event'] == event].reset_index(drop=True)
            time_at_patient_idx = event_df[event_df['action'] == 'time at patient'].index[0]
            int_end_time = event_df.loc[time_at_patient_idx].time  # end of current calculated interval
            int_calculated = False

            #go back through all pauses
            for idx in range(time_at_patient_idx - 1, -1, -1):
                line = event_df.loc[idx]
                action = line["action"]
                if idx == 0: #so start of first interval. If idx is 0, the nurse never had to move
                    if not int_calculated:
                        total_event_time += int_end_time - line["time"]
                    break
                if action == 'unassign event':
                    int_end_time = line["time"]
                    int_calculated = False
                elif not int_calculated:
                    total_event_time += int_end_time - line["time"]
                    int_calculated = True

            total_time += total_event_time

        return total_time
    
    def nurse_time_at_patients(self, nurse_id, patient_ids):
        """
        :param nurse_id: ID of the nurse
        :param patient_ids: ID of patients to calculate time spent at
        :return: time the nurse spent caring for patients specified in list
        """
        total_time = 0
        for patient_id in patient_ids:
            total_time += self.nurse_time_at_patient(nurse_id, patient_id)
        return total_time
    
    def nurse_time_at_own_patients(self, nurse_id):
        """
        :param nurse_id: ID of nurse
        :return: time the nurse spent caring for their assigned patients
        """
        this_nurses_patients = self.nurse_patients[nurse_id]
        return self.nurse_time_at_patients(nurse_id, this_nurses_patients)
    
    def nurse_time_at_other_patients(self, nurse_id):
        """
        :param nurse_id: ID of the nurse
        :return: time the nurse spent caring for the other nurses' patients
        """
        other_patients = []
        for i, patient_lst in enumerate(self.nurse_patients):
            if i != nurse_id:
                other_patients += patient_lst
        
        return self.nurse_time_at_patients(nurse_id, other_patients)
    
    def nurse_time_at_all_patients(self, nurse_id):
        """
        nurse time spent caring for all patients
        :param nurse_id: ID of the nurse
        :return: time the nurse spent caring for all patients
        """
        flattened_patients_lst =  list(chain.from_iterable(self.nurse_patients))
        return self.nurse_time_at_patients(nurse_id, flattened_patients_lst)
    
    def nurse_time_resting(self, nurse_id):
        """
        time nurse spent resting, ie not walking and not caring for patients (so this includes time spent in patient
        rooms not doing anything)
        :param nurse_id: ID of the nurse
        :return: nurse time spent resting
        """
        end_time = self.nurse_df["time"].max() #assuming it started at time 0
        resting_time = end_time - self.nurse_time_at_all_patients(nurse_id) - self.nurse_time_walked(nurse_id)
        return resting_time
    
    def patient_time_waiting_per_event(self, patient_id, request_level=None) -> list[float]:
        """
        for a given patient, returns list of time spent waiting for each event
        :param patient_id: ID of the patient
        :param request_level: level of events to look at. If 1, looks at plans. If None, looks at all events.
        :return: list of time spent waiting for each event
        """
        if request_level is None: # we want plans too but not return to office
            request_events = self.event_df[(self.event_df['patient'] == patient_id) & ((self.event_df['type'] == 'request') | (self.event_df['type'] == 'plan'))]
        elif request_level == 1:
            request_events = self.event_df[(self.event_df['patient'] == patient_id) &
                                           (((self.event_df['type'] == 'request') & (self.event_df['request_level'] == 1)) | (self.event_df['type'] == 'plan'))]
        else: 
            request_events = self.event_df[(self.event_df['patient'] == patient_id) & (self.event_df['type'] == 'request') & (self.event_df['request_level'] == request_level)]
        event_times = []
        for _, event in request_events.groupby('event'):
            planned_start = event[event['action'] == 'planned start']['time']
            end_time = event[event['action'] == 'end']['time']
            wait_time = end_time.values[0] - planned_start.values[0]
            event_times.append(wait_time)
        return event_times
    
    def patient_total_time_waiting(self, patient_id, request_level=None) -> float:
        """
        For a given patient, returns sum of all time spent waiting for events. If in a given time interval the patient
        has multiple events, that interval is counted multiple times
        :param patient_id: ID of the patient
        :param request_level: level of events to look at. If 1, looks at plans. If None, looks at all events.
        :return: sum of all time spent waiting for events of the given level
        """
        return sum(self.patient_time_waiting_per_event(patient_id, request_level))
    
    def patient_avg_time_waiting(self, patient_id, request_level=None):
        """
        for a given patient, returns average time spent waiting for a request of specified level
        :param patient_id: ID of the patient
        :param request_level: level of events to look at. If 1, looks at plans. If None, looks at all events
        :return: average time waiting for a single request
        """
        times_lst = self.patient_time_waiting_per_event(patient_id, request_level)
        if times_lst == []:
            return 0
        else:
            return np.average(times_lst)