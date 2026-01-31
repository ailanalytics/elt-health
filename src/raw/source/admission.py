"""
Annual admissions ~30000
Daily mean ~82
"""

import numpy as np
import random
import encounter as enc
import lab
from department import Department
from collections import deque
from utils import *
from datetime import timedelta
from utils import *
from patients import PatientRegistry
from constants import PRESSURE_MULTIPLIER, DAILY_ADMISSION_BASELINE, PATIENT_REGISTRY_MAX, DEPARTMENT_CONFIG

class WaitingList:
    def __init__(self):
        self.queue = deque()

    def add(self, patient, request_date: date):
        self.queue.append({
            "patient": patient,
            "request_date": request_date
        })
        print(len(self.queue))

    def has_waiting(self) -> bool:
        return len(self.queue) > 0
    
    def has_patient(self, patient) -> bool:
        return any(
            entry["patient"] == patient
            for entry in self.queue
        )

    def peek(self):
        return self.queue[0]

    def pop(self):
        return self.queue.popleft()

    def __len__(self):
        return len(self.queue)

def process_discharges(active_admissions, current_date):

    remaining = []

    for entry in active_admissions:
        discharge_date = entry["discharge_date"]
        if discharge_date is not None and discharge_date <= current_date:
            # discharge happens
            entry["department"].discharge()
        else:
            remaining.append(entry)

    return remaining

def admissions_for_day(date, baseline=DAILY_ADMISSION_BASELINE):

    month = date.month
    multiplier = PRESSURE_MULTIPLIER[month]

    mean = baseline * multiplier

    return np.random.poisson(mean)

def generate_admissions():

    registry = PatientRegistry(range(10000, PATIENT_REGISTRY_MAX))
    waitinglist = WaitingList()
    active_admissions = []

    departments = {
        d["name"]: Department(
            name=d["name"],
            beds=d["beds"],
            stay_min=d["min"],
            stay_max=d["max"]
        )
        for d in DEPARTMENT_CONFIG
    }

    start = date(2025, 1, 28)
    end = date(2026, 1, 28)

    current_date = start

    while current_date <= end:

        active_admissions = process_discharges(active_admissions, current_date)

        admissions_per_day = admissions_for_day(current_date)
        created_admissions = 0

        while created_admissions <= admissions_per_day:

            # Choose patient (backlog first)
            if waitinglist.has_waiting():
                entry = waitinglist.peek()
                patient = entry["patient"]
                request_date = entry["request_date"]
            else:
                patient = registry.get_random_admittable(current_date)
                request_date = current_date

            if not patient:
                print("no patients")
                break  # no eligible patients today

            # Check capacity
            dep_with_capacity = [
                d for d in departments.values()
                if d.has_capacity()
            ]

            if not dep_with_capacity:
                # No beds → backlog
                if not waitinglist.has_patient(patient):
                    waitinglist.add(patient, current_date)
                # print("No beds")
                break  # stop trying today

            # Admit patient
            dep = random.choice(dep_with_capacity)
            dep.admit()

            active_admissions.append({
                "patient": patient,
                "department": dep,
                "discharge_date": patient.discharge_date
            })

            admit_ts = create_timestamp(current_date)

            los_days = dep.generate_length_of_stay()

            discharge_time = random_time_between(8, 22)

            discharge_date = admit_ts + timedelta(
                days=los_days
            )

            discharge_ts = datetime.combine(
                discharge_date.date(),
                discharge_time,
                tzinfo=admit_ts.tzinfo
            )

            lab_ts = admit_ts + timedelta(
                hours=random.randint(0, 6),
                minutes=random.randint(0, 59)
            )

            patient.admission_date = current_date
            patient.discharge_date = date_from_timestamp(discharge_ts)

            # Remove from waiting list if applicable
            if waitinglist.has_waiting() and waitinglist.peek()["patient"] == patient:
                waitinglist.pop()
                patient.waiting_time = (current_date - request_date).days
            else:
                patient.waiting_time = 0

            created_admissions += 1

            print(current_date)

            # Generate events
            enc.generate_encounter_event(
                admit_ts.isoformat(), 
                patient.patient_id, 
                patient.gender, 
                "admission", 
                dep.name, 
                patient.waiting_time
            )

            enc.generate_encounter_event(
                discharge_ts.isoformat(), 
                patient.patient_id, 
                patient.gender, 
                "discharge", 
                dep.name
            )

            lab.generate_lab_result_event(
                lab_ts.isoformat(), 
                patient.gender, 
                patient.patient_id, 
                dep.name
            )

        current_date += timedelta(days=1)

    # for entry in departments.values():
    #     print(entry.get_beds_occupied())