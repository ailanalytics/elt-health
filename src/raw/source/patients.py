import random
from datetime import date

class Patient:
    
    def __init__(self, patient_id: int):
        self.patient_id = patient_id
        self.gender = random.choice(["male", "female"])
        self.admission_date: date | None = None
        self.discharge_date: date | None = None
        self.waiting_time: int = 0

    def can_admit(self, admit_date: date) -> bool:
        # Never admitted before
        if self.admission_date is None and self.discharge_date is None:
            return True

        # Currently admitted
        if self.admission_date is not None and self.discharge_date is None:
            return False

        # Prevent same-day re-admission
        if self.admission_date == admit_date:
            return False

        # Admit only after discharge
        return admit_date > self.discharge_date

class PatientRegistry:
    def __init__(self, patient_ids: range):
        self.patients = {
            pid: Patient(pid) for pid in patient_ids
        }

    def get(self, patient_id: int) -> Patient:
        return self.patients[patient_id]

    def get_random_admittable(self, admit_date: date) -> Patient | None:
        eligible = [
            p for p in self.patients.values()
            if p.can_admit(admit_date)
        ]

        if not eligible:
            return None

        return random.choice(eligible)
