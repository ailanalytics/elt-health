"""
Waiting list queue Class
FIFO
"""

from collections import deque
from datetime import date, datetime

# --------------------------------------------------
# Waiting List
# --------------------------------------------------

class WaitingList:

    def __init__(self):

        """
        Docstring for __init__
        
        Initialise queue
        """

        self.queue = deque()

    def add(self, patient, request_date: date):

        """
        Add patient instance to queue
        
        :param self: References class
        :param patient: Patient class
        :param request_date: ISO Date of insertion
        :type request_date: date
        """
        
        self.queue.append({
            "patient": patient,
            "request_date": request_date
        })

    def has_waiting(self) -> bool:

        """
        Returns true if waiting list is > 0
        
        :param self: References class
        :return: True if > 0
        :rtype: bool
        """

        return len(self.queue) > 0
    
    def has_patient(self, patient) -> bool:

        """
        Is patient present in queue
        
        :param self: References class
        :param patient: Patient class
        :return: True if present
        :rtype: bool
        """

        return any(
            entry["patient"] == patient
            for entry in self.queue
        )

    def peek(self):

        """
        Returns first element of queue
        
        :param self: References class
        """

        return self.queue[0]

    def pop_patient(self):

        """
        Removes first element
        
        :param self: References class
        """
        
        return self.queue.popleft()

    def __len__(self):

        """
        Returns length of queue
        
        :param self: References class
        """
        
        return len(self.queue)
    
    def waiting_list_snapshot(self, ts: datetime, phase: str):

        snapshot = {
        "event_type": "wait_snapshot",
        "waiting_count": self.__len__,
        "phase": phase,
        "event_ts": ts,
        "source_system": "waiting_list",
        }
