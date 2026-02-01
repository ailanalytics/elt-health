"""
Coordinates admissions, discharges, waiting list
"""

import numpy as np
import random
from datetime import timedelta
import src.raw.source_gen.encounter as enc
from src.raw.source_gen.department import Department
from src.raw.source_gen.waiting_list import WaitingList
from src.raw.ingestion.s3_write import write_to_bucket
from src.raw.source_gen.utils import *
from src.raw.source_gen.patient_registry import PatientRegistry
from src.raw.source_gen.constants import PRESSURE_MULTIPLIER, DAILY_ADMISSION_BASELINE, PATIENT_REGISTRY_MAX, DEPARTMENT_CONFIG

# --------------------------------------------------
# Discharges
# --------------------------------------------------

def process_discharges(active_admissions: list, current_date: date) -> list:

    """
    Receives list of active admissions,
    returns filtered list of active admissions
    
    :param active_admissions: List of active admissions
    :type active_admissions: list
    :param current_date: Current date
    :type current_date: date
    """

    remaining = []

    for entry in active_admissions:
        discharge_date = entry["discharge_date"]

        if discharge_date is not None and discharge_date <= current_date:
            # discharge happens
            entry["department"].discharge()
        else:
            remaining.append(entry)

    return remaining

# --------------------------------------------------
# Daily Admissions
# --------------------------------------------------

def admissions_for_day(date: date, baseline: int) -> int:

    """
    Calculates number of admissions for day
    and poisson mean determined by monthly pressure multiplier
    
    :param date: Current date
    :type date: date
    :param baseline: Baseline admissions constant
    :type baseline: int
    :return: Poisson adjusted admissions
    :rtype: int
    """

    month = date.month
    multiplier = PRESSURE_MULTIPLIER[month]
    mean = baseline * multiplier

    return np.random.poisson(mean)

# --------------------------------------------------
# Department Snapshot
# --------------------------------------------------

def department_snapshot(ts: datetime, departments: dict, phase: str):

    """
    Generates department snapshot
    Writes to S3
    
    :param ts: Snapshot timestamp
    :type ts: datetime
    :param departments: Dict of all departments
    :type departments: dict
    :param phase: Start Of Day/End Of Day
    :type phase: str
    """

    snapshot = {
        "event_type": "dep_snapshot",
        "departments": {
            name: dep.to_dict()
            for name, dep in departments.items()
        },
        "phase": phase,
        "event_ts": ts,
        "source_system": "department",
    }

    write_to_bucket(snapshot)

# --------------------------------------------------
# Admission/Discharge/Waiting List Coordinator
# --------------------------------------------------

def generate_admissions():

    """
    Coordinate admissions, discharges, waiting list
    Creates departments from DEPARTMENT_CONFIG constant
    Creates daily snapshot of number of patients on waiting list
    Daily discharges prioritised, followed by patients in waiting list
    Selects each day in range, creates number of admissions for the day
    Creates timestamp for admission and discharge json
    Calls generator functions to create json for S3
    Breaks inner loop if no patient is admittable or department has capacity
    """

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

        current_date_ts = create_timestamp(current_date)
        sod_ts = current_date_ts.replace(hour=0, minute=0, second=1)
        waitinglist.waiting_list_snapshot(str(sod_ts.isoformat()), "SOD")
        department_snapshot(str(sod_ts.isoformat()), departments, "SOD")

        active_admissions = process_discharges(active_admissions, current_date)
        admissions_per_day = admissions_for_day(current_date, DAILY_ADMISSION_BASELINE)
        created_admissions = 0

        while created_admissions < admissions_per_day:

            if waitinglist.has_waiting():
                entry = waitinglist.peek()
                patient = entry["patient"]
                request_date = entry["request_date"]
            else:
                patient = registry.get_random_admittable(current_date)
                request_date = current_date

            if not patient:
                break 

            dep_with_capacity = [
                d for d in departments.values()
                if d.has_capacity()
            ]

            if not dep_with_capacity:
                if not waitinglist.has_patient(patient):
                    waitinglist.add(patient, current_date)
                    patient.waiting_list = True
                break

            dep = random.choice(dep_with_capacity)
            dep.admit()

            los_days = dep.generate_length_of_stay()

            admit_ts = create_timestamp(current_date)

            discharge_time = random_time_between(8, 22)
            discharge_date = admit_ts + timedelta(
                days=los_days
            )
            discharge_ts = datetime.combine(
                discharge_date.date(),
                discharge_time,
                tzinfo=admit_ts.tzinfo
            )

            patient.admission_date = current_date
            patient.discharge_date = date_from_timestamp(discharge_ts)

            active_admissions.append({
                "patient": patient,
                "department": dep,
                "discharge_date": patient.discharge_date
            })

            if waitinglist.has_waiting() and waitinglist.peek()["patient"] == patient:
                waitinglist.pop_patient()
                patient.waiting_time = (current_date - request_date).days
            else:
                patient.waiting_time = 0

            created_admissions += 1

            enc.generate_encounter_event(
                admit_ts.isoformat(), 
                patient.patient_id, 
                patient.gender, 
                "admission", 
                dep.name, 
                patient.waiting_list,
                patient.waiting_time
            )

            enc.generate_encounter_event(
                discharge_ts.isoformat(), 
                patient.patient_id, 
                patient.gender, 
                "discharge", 
                dep.name
            )

        eod_ts = current_date_ts.replace(hour=23, minute=59, second=59)
        waitinglist.waiting_list_snapshot(str(eod_ts.isoformat()), "EOD")
        department_snapshot(str(eod_ts.isoformat()), departments, "EOD")
        current_date += timedelta(days=1)