import json
import copy
import random
from datetime import datetime, timezone, date, timedelta, time

PATIENT_DATE_TRACKING = set()

def create_timestamp(patient_id):
    encounter_date = create_unused_date(patient_id)
    t = generate_time()
    ts = datetime.combine(encounter_date, t)
    return ts.replace(tzinfo=timezone.utc)


def create_unused_date(patient_id):
    attempts = 0

    MAX_ATTEMPTS = 40

    while attempts < MAX_ATTEMPTS:

        find_date = generate_date()

        if (patient_id, find_date) not in PATIENT_DATE_TRACKING:
            PATIENT_DATE_TRACKING.add((patient_id, find_date))
            return find_date

        attempts += 1

    raise ValueError("No unused date found")

def generate_date() -> date:
    start = date(2024, 1, 28)
    end = date(2025, 1, 28)

    delta_days = (end - start).days
    random_date = start + timedelta(days=random.randint(0, delta_days))

    return random_date

def generate_time():
    return time(
        hour=random.randint(0, 23),
        minute=random.randint(0, 59),
        second=random.randint(0, 59)
    )

def random_value(low, high, decimals=2):
    if low is None or high is None:
        return None
    value = random.uniform(low, high)
    return round(value, decimals)