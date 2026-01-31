"""
Raw Lab Data Generator
Writes json to local dev data folder
"""

import json
import copy
import random
from utils import *
from constants import LAB_TEST_PATH

# --------------------------------------------------
# Define Variables
# --------------------------------------------------

with open(LAB_TEST_PATH, "r", encoding="utf-8") as f:
    lab_tests = json.load(f)

def generate_lab_result_event(ts, gender, patient_id, department):

    data = lab_tests["data"]

    data_name, tests = random.choice(list(data.items()))

    data_with_values = copy.deepcopy(tests)

    for test in data_with_values:
        test_range = test["test_range"]
        low = test_range.get("low")
        high = test_range.get("high")
        test["value"] = random_value(low, high)

    event = {
        "event_type": "lab_result",
        "patient": {
            "patient_id": patient_id,
            "gender": gender
        },
        "lab_results": {
            "result_set": data_name,
            "tests": data_with_values,
        },
        "department": department,
        "event_ts": ts,
        "source_system": "lab",
    }

    # print(event)

if __name__ == "__main__":
    results = generate_lab_result_event("male", 10000)
