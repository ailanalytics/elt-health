"""
Helper functions
"""

import random
import statistics
from datetime import datetime, timezone, time, date

# --------------------------------------------------
# Time
# --------------------------------------------------

def create_timestamp(date: date) -> datetime:

    """
    Create timestamp from date
    
    :param date: Date
    :type date: date
    :return: Timestamp
    :rtype: datetime
    """

    encounter_date = date
    t = generate_time()
    ts = datetime.combine(encounter_date, t)

    return ts.replace(tzinfo=timezone.utc)

def generate_time():

    """
    Generate random time
    """

    return time(
        hour=random.randint(0, 23),
        minute=random.randint(0, 59),
        second=random.randint(0, 59)
    )

def date_from_timestamp(ts: datetime) -> date:

    """
    Create date from timestamp
    
    :param ts: Timestamp
    :type ts: datetime
    :return: date
    :rtype: date
    """

    ts_string = str(ts)
    dt = datetime.fromisoformat(ts_string)

    return dt.date()

def random_time_between(start_hour: int, end_hour: int) -> time:

    """
    Create random time between hours 24hr format
    
    :param start_hour: Start time
    :type start_hour: int
    :param end_hour: End time
    :type end_hour: int
    :return: Random time
    :rtype: time
    """

    hour = random.randint(start_hour, end_hour - 1)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)

    return time(hour, minute, second)

# --------------------------------------------------
# Statistics
# --------------------------------------------------

def validate_queue_dynamics(wait_times: list):

    """
    Validates queue dynamics, prints results
    
    :param wait_times: List of accumulated wait times across entire date range
    :type wait_times: list(int)
    """
    
    avg = sum(wait_times) / len(wait_times)
    median = statistics.median(wait_times)
    mode = statistics.mode(wait_times)
    max_wait = max(wait_times)
    min_wait = min(wait_times)
    p90 = statistics.quantiles(wait_times, n=10)[8]
    p95 = statistics.quantiles(wait_times, n=20)[18]

    print(
    f"""
    WAIT TIME STATISTICS
    -------------------
    Average : {avg:.2f} days
    Median  : {median} days
    Mode    : {mode} days
    Min     : {min_wait} days
    P90     : {p90} days
    P95     : {p95} days
    Max     : {max_wait} days
    """
    )