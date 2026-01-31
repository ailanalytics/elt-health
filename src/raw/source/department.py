
import random

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

    def get_beds_occupied(self):
        return self.beds_occupied

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
        elif r > 0.9 and r < 0.99:
            days = random.randint(15, 30)
        # 2% bed blockers
        else:
            days = random.randint(31, 90)

        return days