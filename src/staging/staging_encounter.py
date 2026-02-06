"""
Orchestration for encounter data
Admission and discharge raw S3 data
Creation of parquet
Appended to S3 staging
Partitioned by YYYY-MM
"""

from src.staging.staging_utils import get_prefixes, build_parquet
from src.staging.schemas import encounter_schema

# --------------------------------------------------
# Entry Point
# --------------------------------------------------

def main():

    select = [
        "event_type",
        "patient.patient_id",
        "patient.gender",
        "encounter.department",
        "encounter.waiting_list",
        "encounter.waiting_time",
        "event_ts",
        "ingestion_ts",
        "source_system",
    ]
    rename = [
        "event_type",
        "patient_id",
        "patient_gender",
        "department_name",
        "waiting_list",
        "waiting_time",
        "event_ts",
        "ingestion_ts",
        "source_system",
    ]

    admission_prefixes = get_prefixes("admission", "month")
    discharge_prefixes = get_prefixes("discharge", "month")

    for month, prefixes in admission_prefixes.items():
        build_parquet(
            "health-data-raw-elt",
            prefixes,
            month,
            "admission",
            encounter_schema,
            select,
            rename,
            False
        )

    for month, prefixes in discharge_prefixes.items():
        build_parquet(
            "health-data-raw-elt",
            prefixes,
            month,
            "discharge",
            encounter_schema,
            select,
            rename,
            False
        )


if __name__ == "__main__":
    main()