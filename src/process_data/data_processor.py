import pandas as pd
from math import sqrt
from itertools import chain
import numpy as np

from src.importer.gen_importer import GenImporter

class DataProcessor:
    def __init__(self, nurse_log_path, event_log_path, people_path) -> None:
        self.nurse_df = pd.read_csv(nurse_log_path)
        self.event_df = pd.read_csv(event_log_path)
        gen_importer = GenImporter("", people_path) #it would be better to create a separate importer for people only
        gen_importer.import_people()
        self.nurse_patients = gen_importer.nurse_patients
        self.patient_cnt = gen_importer.patient_cnt
        

    def row_diff(self, row_num: int, df: pd.DataFrame, col_name: str):
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
        move_rows = self.nurse_df[(self.nurse_df['nurse'] == nurse_id) & (self.nurse_df['action'] == "move to")].index.tolist()
        total_dst = 0
        for row in move_rows:
            x_dst = self.row_diff(row, self.nurse_df, "x")
            y_dst = self.row_diff(row, self.nurse_df, "y")
            distance = sqrt(x_dst ** 2 + y_dst ** 2)
            total_dst += distance
        
        return total_dst
    
    def nurse_time_walked(self, nurse_id):
        move_rows = self.nurse_df[(self.nurse_df['nurse'] == nurse_id) & (self.nurse_df['action'] == "move to")].index.tolist()
        total_time = 0
        for row in move_rows:
            total_time += self.row_diff(row, self.nurse_df, "time")
        return total_time
    
    def nurse_time_at_patient(self, nurse_id, patient_id):
        #assuming the df is sorted by nurse_id first and time second
        time_rows = self.nurse_df[(self.nurse_df['nurse'] == nurse_id) & (self.nurse_df['patient'] == patient_id) & (self.nurse_df['action'] == "time at patient")].index.tolist()
        total_time = 0
        for row in time_rows:
            total_time += self.row_diff(row, self.nurse_df, "time")
        return total_time
    
    def nurse_time_at_patients(self, nurse_id, patient_ids):
        total_time = 0
        for patient_id in patient_ids:
            total_time += self.nurse_time_at_patient(nurse_id, patient_id)
        return total_time
    
    def nurse_time_at_own_patients(self, nurse_id):
        this_nurses_patients = self.nurse_patients[nurse_id]
        return self.nurse_time_at_patients(nurse_id, this_nurses_patients)
    
    def nurse_time_at_other_patients(self, nurse_id):
        other_patients = []
        for i, patient_lst in enumerate(self.nurse_patients):
            if i != nurse_id:
                other_patients += patient_lst
        
        return self.nurse_time_at_patients(nurse_id, other_patients)
    
    def nurse_time_at_all_patients(self, nurse_id):
        flattened_patients_lst =  list(chain.from_iterable(self.nurse_patients))
        return self.nurse_time_at_patients(nurse_id, flattened_patients_lst)
    
    def nurse_time_resting(self, nurse_id):
        end_time = self.nurse_df["time"].max() #assuming it started at time 0
        resting_time = end_time - self.nurse_time_at_all_patients(nurse_id) - self.nurse_time_walked(nurse_id)
        return resting_time
    
    def patient_time_waiting_per_event(self, patient_id, request_level=None) -> list[float]:
        if request_level is None:
            request_events = self.event_df[(self.event_df['patient'] == patient_id) & (self.event_df['type'] == 'request')]
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
        return sum(self.patient_time_waiting_per_event(patient_id, request_level))
    
    def patient_avg_time_waiting(self, patient_id, request_level=None):
        return np.average(self.patient_time_waiting_per_event(patient_id, request_level))