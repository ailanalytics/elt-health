"""
Raw Data Generator
Writes json to local dev data folder
"""

import json
import copy
import random

# --------------------------------------------------
# Define Variables
# --------------------------------------------------

def generate_vital_signs_event(ts, patient_id):
    return {
        "event_type": "vital_signs",
        "patient": {
            "patient_id": patient_id
        },
        "vitals": {
            "heart_rate": random.randint(40, 200),
            "systolic_bp": random.randint(90, 200),
            "diastolic_bp": random.randint(40, 120),
            "spo2": random.randint(60, 100),
        },
        "event_ts": ts,
        "source_system": "monitor",
    }
