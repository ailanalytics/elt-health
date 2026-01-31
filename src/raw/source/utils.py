import random
from datetime import datetime, timezone, date, timedelta, time

def create_timestamp(date):
    encounter_date = date
    t = generate_time()
    ts = datetime.combine(encounter_date, t)
    return ts.replace(tzinfo=timezone.utc)

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

def random_time_between(start_hour: int, end_hour: int) -> time:
    hour = random.randint(start_hour, end_hour - 1)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return time(hour, minute, second)