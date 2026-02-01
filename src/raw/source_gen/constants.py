LAB_TEST_PATH = "src/raw/source/lab_tests.json"

DAILY_ADMISSION_BASELINE = 20

PATIENT_REGISTRY_MAX = 15000

DEPARTMENT_MAX_STAY = 30

DEPARTMENT_CONFIG = [
    {"name": "ward1",   "beds": 20, "min": 1, "max": DEPARTMENT_MAX_STAY},
    {"name": "ward2",   "beds": 20, "min": 1, "max": DEPARTMENT_MAX_STAY},
    {"name": "ward3",   "beds": 10, "min": 1, "max": DEPARTMENT_MAX_STAY},
    {"name": "ward4",   "beds": 32, "min": 1, "max": DEPARTMENT_MAX_STAY},
    {"name": "ward5",   "beds": 18, "min": 1, "max": DEPARTMENT_MAX_STAY},
    {"name": "ward6",   "beds": 24, "min": 1, "max": DEPARTMENT_MAX_STAY},
]

PRESSURE_MULTIPLIER = { # By month 1 = Jan
    1: 1.25,
    2: 1.20,
    3: 1.10,
    4: 1.05,
    5: 0.95,
    6: 0.90,
    7: 0.90,
    8: 0.92,
    9: 1.00,
    10: 1.05,
    11: 1.15,
    12: 1.20,
}