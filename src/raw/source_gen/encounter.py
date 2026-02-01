"""
Encounter Generator
Encounter data for S3
"""

from src.raw.ingestion.s3_write import write_to_bucket

# --------------------------------------------------
# Generate Encounters
# --------------------------------------------------

def generate_encounter_event(
        ts: str, 
        patient_id: int, 
        gender: str, 
        encounter_type: str, 
        department: str, 
        waiting_list: bool=False, 
        wait_time: int=0
        ):

    """
    Generates encounter event for patient
    
    :param ts: Encounter timestamp
    :type ts: str
    :param patient_id: Patient identifier
    :type patient_id: int
    :param gender: Patient gender
    :type gender: str
    :param encounter_type: Admission/Discharge
    :type encounter_type: str
    :param department: Department name
    :type department: str
    :param waiting_list: Patient was on waiting list
    :type waiting_list: bool
    :param wait_time: Waiting time length in days, default 0
    :type wait_time: int
    """

    event = {
        "event_type": encounter_type,
        "patient": {
            "patient_id": patient_id,
            "gender": gender
        },
        "encounter": {
            "department": department,
            "waiting_list": waiting_list,
            "waiting_time": wait_time
        },
        "event_ts": ts,
        "source_system": "ehr",
    }

    write_to_bucket(event)
