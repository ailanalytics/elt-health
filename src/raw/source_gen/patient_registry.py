"""
Patient registry Class
"""

import random
from datetime import date
from patients import Patient

# --------------------------------------------------
# Patient Registry Class
# --------------------------------------------------

class PatientRegistry:

    def __init__(self, patient_ids: range):

        """
        Initialise class
        
        :param self: References class
        :param patient_ids: int Range of patient identifiers
        :type patient_ids: range
        """

        self.patients = {
            pid: Patient(pid) for pid in patient_ids
        }

    def get(self, patient_id: int) -> Patient:

        """
        Returns patient class from patients dict
        
        :param self: References class
        :param patient_id: Patient identifier
        :type patient_id: int
        :return: Patient class
        :rtype: Patient
        """

        return self.patients[patient_id]

    def get_random_admittable(self, admit_date: date) -> Patient | None:

        """
        Return random patient from patients dict
        
        :param self: References class
        :param admit_date: Date of admission
        :type admit_date: date
        :return: Patient class or None
        :rtype: Patient | None
        """

        eligible = [
            p for p in self.patients.values()
            if p.can_admit(admit_date)
        ]

        if not eligible:
            return None

        return random.choice(eligible)
