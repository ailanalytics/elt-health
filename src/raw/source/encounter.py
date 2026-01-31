"""
Raw Data Generator
Writes json to local dev data folder
"""

# --------------------------------------------------
# Define Variables
# --------------------------------------------------

def generate_encounter_event(ts, patient_id, gender, encounter_type, department, wait_time=0):

    event = {
        "event_type": encounter_type,
        "patient": {
            "patient_id": patient_id,
            "gender": gender
        },
        "encounter": {
            "department": department,
            "waiting_time": wait_time
        },
        "event_ts": ts,
        "source_system": "ehr",
    }
    # if event["encounter"]["waiting_time"] > 0:  
    #     print(event["encounter"]["waiting_time"])