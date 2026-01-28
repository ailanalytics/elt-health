"""
Raw Lab Data Generator
Writes json to local dev data folder
"""

import json
import copy
import random
from utils import *

# --------------------------------------------------
# Define Variables
# --------------------------------------------------

LAB_TEST_PATH = "src/raw/lab_tests.json"

with open(LAB_TEST_PATH, "r", encoding="utf-8") as f:
    lab_tests = json.load(f)

def generate_lab_result_event(ts, gender, patient_id, department):

    data = lab_tests["data"]

    data_name, tests = random.choice(list(data.items()))

    data_with_values = copy.deepcopy(tests)

    for test in data_with_values:
        test_range = test["range"]

        if gender in test_range:
            low = test_range[gender]["low"]
            high = test_range[gender]["high"]
        else:
            low = test_range.get("low")
            high = test_range.get("high")

        test["value"] = random_value(low, high)

    return {
        "event_type": "lab_result",
        "patient": {
            "patient_id": patient_id
        },
        "lab_results": {
            "result_set": data_name,
            "tests": data_with_values,
        },
        "department": department,
        "event_ts": ts,
        "source_system": "lab",
    }

if __name__ == "__main__":
    results = generate_lab_result_event("male", 10000)
    print(results)