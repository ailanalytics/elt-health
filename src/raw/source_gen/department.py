"""
Department Class
Coordinates creation of departments
Manages state of each department
"""

import random

# --------------------------------------------------
# Department Class
# --------------------------------------------------

class Department:

    def __init__(self, name: str, beds: int, stay_min: int, stay_max: int,):

        """
        Initialises Department class
        
        :param self: References class
        :param name: Name of department
        :type name: str
        :param beds: Number of beds in department
        :type beds: int
        :param stay_min: Minimum length of stay in days
        :type stay_min: int
        :param stay_max: Maximum length of stay in days
        :type stay_max: int
        """

        self.name = name
        self.beds_total = beds
        self.beds_occupied = 0
        self.stay_min = stay_min
        self.stay_max = stay_max

    def get_beds_occupied(self) -> int:

        """
        Returns number of beds occupaied in department
        
        :param self: References class
        """

        return self.beds_occupied

    def has_capacity(self) -> bool:

        """
        Returns true if department has bed
        
        :param self: References class
        :return: Returns true if number of beds occupied <= total beds
        :rtype: bool
        """

        return self.beds_occupied <= self.beds_total

    def admit(self):

        """
        Incriments number of beds occupied in department
        
        :param self: References class
        """

        self.beds_occupied += 1

    def discharge(self):

        """
        Decriments number of beds occupied in department
        only if department has occupied bed
        
        :param self: References class
        """

        if self.beds_occupied > 0:
            self.beds_occupied -= 1

    def generate_length_of_stay(self) -> int:

        """
        Generates length of stay for patient in days
        Adjusts length of stay to create long-stay and bed block patients
        
        :param self: References class
        :return: Length of stay in days
        :rtype: int
        """

        r = random.random()
        
        if r <= 0.9:
            days = random.randint(self.stay_min, self.stay_max)
        elif r < 0.98:
            days = random.randint(15, 30)
        else:
            days = random.randint(31, 90)

        return days