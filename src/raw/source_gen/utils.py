"""
Helper functions
"""

import random
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