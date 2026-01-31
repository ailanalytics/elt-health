"""
Annual admissions ~30000
Daily mean ~82
"""

import numpy as np
import random
from utils import *
from datetime import timedelta
from utils import *
import raw.source.encounter as enc
import raw.source.lab as lab
from raw.source.patients import PatientRegistry

DEP = [
    {"dep": "icu", "range": {"min": 1, "max": 20}},
    {"dep": "surgery", "range": {"min": 1, "max": 24}},
    {"dep": "a&e", "range": {"min": 1, "max": 24}},
    {"dep": "ward1", "range": {"min": 1, "max": 180}},
    {"dep": "ward2", "range": {"min": 1, "max": 180}},
    {"dep": "ward3", "range": {"min": 1, "max": 180}},
    {"dep": "ward4", "range": {"min": 1, "max": 180}},    
]

PRESSURE_MULTIPLIER = { # By month 1 = Jan
    1: 1.25,
    2: 1.20,
    3: 1.10,
    4: 1.05,
    5: 0.95,
    6: 0.90,
    7: 0.90,
    8: 0.92,
    9: 1.00,
    10: 1.05,
    11: 1.15,
    12: 1.20,
}

def admissions_for_day(date, baseline=82):
    month = date.month
    multiplier = PRESSURE_MULTIPLIER[month]

    mean = baseline * multiplier

    return np.random.poisson(mean)

def generate_admissions():

    registry = PatientRegistry(range(10000, 30000))

    start = date(2024, 1, 28)
    end = date(2024, 1, 28)

    for date in range(start, end):

        admissions_per_day = admissions_for_day(date)
        created_admissions = 0

        while created_admissions < admissions_per_day:

            patient = registry.get_random_admittable(date)

            if patient:

                department = random.choice(DEP)
                dep_name = department["dep"]

                # Generate event timestamps
                ts = create_timestamp(patient.patient_id, date)

                stay_min = department["range"]["min"]
                stay_max = department["range"]["max"]
                
                if dep_name == "surgery" or dep_name == "a&e":
                    ts_discharge = ts + timedelta(hours=random.randint(stay_min, stay_max), minutes=random.randint(0, 60))
                else:
                    ts_discharge = ts + timedelta(days=random.randint(stay_min, stay_max), hours=random.randint(0, 24), minutes=random.randint(0, 60))

                lab_ts = ts + timedelta(hours=random.randint(1, 4))

                # Generate events
                encounter_admit = enc.generate_encounter_event(ts.isoformat(), patient.patient_id, patient.gender, "admission", dep_name)
                encounter_discharge = enc.generate_encounter_event(ts_discharge.isoformat(), patient.patient_id, patient.gender, "discharge", dep_name)
                lab_result = lab.generate_lab_result_event(lab_ts.isoformat(), patient.gender, patient.patient_id, dep_name)

                patient.admission_date = date
                patient.discharge_date = date_from_timestamp(ts_discharge)

                created_admissions += 1

            else:
                continue

            