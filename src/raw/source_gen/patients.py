"""
Patient Class
"""

import random
from datetime import date

# --------------------------------------------------
# Patient Class
# --------------------------------------------------

class Patient:
    
    def __init__(self, patient_id: int):

        """
        Initialise patient class
        
        :param self: References class
        :param patient_id: Patient identifier
        :type patient_id: int
        """

        self.patient_id = patient_id
        self.gender = random.choice(["male", "female"])
        self.admission_date: date | None = None
        self.discharge_date: date | None = None
        self.waiting_list: bool = False
        self.waiting_time: int = 0

    def patient_on_waiting_list(self) -> bool:

        """
        Is patient present on waiting list
        
        :param self: References class
        :return: True if on waiting list
        :rtype: bool
        """

        return self.waiting_list

    def can_admit(self, admit_date: date) -> bool:

        """
        Determines if patient can be admitted:
            Never admitted -> True
            Currently admitted -> False
            Admit on same day -> False
            Only admit after discharge -> True
        
        :param self: References class
        :param admit_date: Date of admission
        :type admit_date: date
        :return: True/False
        :rtype: bool
        """

        if self.admission_date is None and self.discharge_date is None:
            return True

        if self.admission_date is not None and self.discharge_date is None:
            return False

        if self.admission_date == admit_date:
            return False

        return admit_date > self.discharge_date