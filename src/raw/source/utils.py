import random
from datetime import datetime, timezone, date, timedelta, time

PATIENT_DATE_TRACKING = {}

def create_timestamp(patient_id, date):
    encounter_date = date
    tracking_date = track_date(patient_id)
    t = generate_time()
    ts = datetime.combine(encounter_date, t)
    return ts.replace(tzinfo=timezone.utc)


def track_date(patient_id, date):

    if (patient_id) not in PATIENT_DATE_TRACKING:
        PATIENT_DATE_TRACKING[patient_id] = date
        return date
    else:
        previous_date = PATIENT_DATE_TRACKING[patient_id]
        next_admit_date = previous_date + timedelta(days=random.randint(1, 180))
        PATIENT_DATE_TRACKING[patient_id] = next_admit_date
        return next_admit_date


# def generate_date():
#     start = date(2024, 1, 28)
#     end = date(2025, 1, 28)

#     delta_days = (end - start).days
#     random_date = start + timedelta(days=random.randint(0, delta_days))

#     return random_date

def generate_time():
    return time(
        hour=random.randint(0, 23),
        minute=random.randint(0, 59),
        second=random.randint(0, 59)
    )

def date_from_timestamp(ts):
    ts_string = str(ts)
    dt = datetime.fromisoformat(ts_string)
    return dt.date()

def random_value(low, high, decimals=2):
    if low is None or high is None:
        return None
    value = random.uniform(low, high)
    return round(value, decimals)