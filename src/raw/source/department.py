
import random

DEPARTMENT_CONFIG = [
    {"name": "ward1",   "beds": 20, "min": 1, "max": 30},
    {"name": "ward2",   "beds": 20, "min": 1, "max": 30},
    {"name": "ward3",   "beds": 10, "min": 1, "max": 30},
    {"name": "ward4",   "beds": 32, "min": 1, "max": 30},
    {"name": "ward5",   "beds": 18, "min": 1, "max": 30},
    {"name": "ward6",   "beds": 24, "min": 1, "max": 30},
]

    # 124 Beds

class Department:

    def __init__(
        self,
        name: str,
        beds: int,
        stay_min: int,
        stay_max: int,
    ):
        self.name = name
        self.beds_total = beds
        self.beds_occupied = 0

        self.stay_min = stay_min
        self.stay_max = stay_max

    # ---------- Bed state ----------

    def has_capacity(self) -> bool:
        return self.beds_occupied <= self.beds_total

    def admit(self) -> bool:
        if not self.has_capacity():
            return False
        self.beds_occupied += 1
        return True

    def discharge(self):
        if self.beds_occupied > 0:
            self.beds_occupied -= 1

    # ---------- Length of stay ----------

    def generate_length_of_stay(self) -> int:
        r = random.random()
        # 90% normal patients
        if r <= 0.9:
            days = random.randint(self.stay_min, self.stay_max)
        # 8% long stays
        elif r > 0.9 and r < 0.98:
            days = random.randint(15, 30)
        # 2% bed blockers
        else:
            days = random.randint(31, 90)

        return days