"""
Orchestration for creating department snapshot parquet
S3 raw json parsed into rows before passing to PyArrow
Appended to S3 staging partitioned by YYYY-MM
"""

from src.staging.staging_utils import get_prefixes, build_parquet
from src.staging.schemas import department_schema

# --------------------------------------------------
# Explode Department Snapshot Json
# --------------------------------------------------

def explode_department_snapshot(event: dict) -> list[dict]:

    """
    Explodes department snapshot json from
    nested objects to single row
    
    :param event: Event json
    :type event: dict
    :return: List of rows by department
    :rtype: list[dict]
    """

    rows = []

    for ward_name, ward in event["departments"].items():
        rows.append({
            "event_type": event["event_type"],
            "ward_name": ward_name,
            "beds_total": ward["beds_total"],
            "beds_occupied": ward["beds_occupied"],
            "beds_available": ward["beds_available"],
            "phase": event["phase"],
            "event_ts": event["event_ts"],
            "source_system": event["source_system"],
            "ingestion_ts": event["ingestion_ts"],
        })

    return rows

# --------------------------------------------------
# Entry Point
# --------------------------------------------------

def main():

    department_select = [
        "event_type",
        "ward_name",
        "beds_total",
        "beds_occupied",
        "beds_available",
        "phase",
        "event_ts",
        "source_system",
        "ingestion_ts",
    ]

    department_prefixes = get_prefixes("dep_snapshot", "month")

    for month, prefixes in department_prefixes.items():
        build_parquet(
            "health-data-raw-elt",
            prefixes,
            month,
            "department_snapshot",
            department_schema,
            department_select,
            department_select,
            True
        )


if __name__ == "__main__":
    main()