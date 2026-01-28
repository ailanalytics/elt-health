"""
Raw Data Generator
Writes json to local dev data folder
"""

import random

# --------------------------------------------------
# Define Variables
# --------------------------------------------------

def generate_encounter_event(ts, patient_id, encounter_type, department):
    return {
        "event_type": encounter_type,
        "patient": {
            "patient_id": patient_id,
        },
        "encounter": {
            "department": department,
        },
        "event_ts": ts,
        "source_system": "ehr",
    }