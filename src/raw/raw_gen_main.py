"""
Raw Data Generator
Writes json to local dev data folder
"""

import json
import copy
import random
from datetime import datetime, timezone, date, timedelta
from utils import *
import raw_gen_encounter as enc
import raw_gen_lab as lab

# --------------------------------------------------
# Define Variables
# --------------------------------------------------

DEP = [
    {"dep": "icu", "range": {"min": 1, "max": 20}},
    {"dep": "surgery", "range": {"min": 1, "max": 24}},
    {"dep": "a&e", "range": {"min": 1, "max": 24}},
    {"dep": "ward1", "range": {"min": 1, "max": 180}},
    {"dep": "ward2", "range": {"min": 1, "max": 180}},
    {"dep": "ward3", "range": {"min": 1, "max": 180}},
    {"dep": "ward4", "range": {"min": 1, "max": 180}},    
]

GENDER = ["male", "female"]

def main():

    for i in range(0, 1):

        # Patient details

        patient_id = random.randint(10000, 10100)
        patient_gender = random.choice(GENDER)
        department = random.choice(DEP)
        dep_name = department["dep"]

        # Generate event timestamps

        ts = create_timestamp(patient_id)

        stay_min = department["range"]["min"]
        stay_max = department["range"]["max"]
        
        if dep_name == "surgery" or dep_name == "a&e":
            ts_discharge = ts + timedelta(hours=random.randint(stay_min, stay_max), minutes=random.randint(0, 60))
        else:
            ts_discharge = ts + timedelta(days=random.randint(stay_min, stay_max), hours=random.randint(0, 24), minutes=random.randint(0, 60))

        lab_ts = ts + timedelta(hours=random.randint(1, 4))

        # Generate events

        encounter_admit = enc.generate_encounter_event(ts.isoformat(), patient_id, "admission", dep_name)
        encounter_discharge = enc.generate_encounter_event(ts_discharge.isoformat(), patient_id, "discharge", dep_name)
        lab_result = lab.generate_lab_result_event(lab_ts.isoformat(), patient_gender, patient_id, dep_name)

        print(encounter_admit, encounter_discharge, lab_result)

if __name__ == "__main__":
    main()