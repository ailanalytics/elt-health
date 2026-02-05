import pyarrow as pa
import pyarrow.json as paj
import pyarrow.parquet as pap
import json
from src.staging.staging_utils import *
from collections import defaultdict

# --------------------------------------------------
# Group Monthly Encounter Prefixes From S3
# --------------------------------------------------

def get_encounter_prefixes(encounter_type: str) -> defaultdict[str: list[str]]:

    """
    Returns a dictionary of prefixes grouped by date: YYYY-MM
    
    :return: Grouped prefixes
    :rtype: defaultdict
    """

    prefixes = list_daily_prefixes("health-data-raw-elt", f"raw/{encounter_type}/")

    return group_prefixes_by_month(prefixes)

# --------------------------------------------------
# Build Monthly Parquet
# --------------------------------------------------

def build_monthly_encounter_parquet(bucket: str, daily_prefixes: list[str], month: str, encounter_type: str):

    """
    Creates parquet file for loading into S3 staging
    Retrieves json objects at bucket prefix
    Enforces types
    Normalises timestamps before casting in PyArrow
    
    :param bucket: Prefix and target bucket
    :type bucket: str
    :param daily_prefixes: List of daily prefixes
    :type daily_prefixes: list[str]
    :param month: Target month, used in S3 key
    :type month: str
    """

    tables = []

    fs = S3FileSystem()

    for prefix in daily_prefixes:

        s3_prefix = f"{bucket}/{prefix}"

        objects_at_prefix = get_objects_at_prefix(s3_prefix)

        for object in objects_at_prefix:

            with fs.open_input_file(object) as f:
                payload = json.loads(f.read().decode("utf-8"))

            payload["event_ts"] = normalize_timestamp(payload["event_ts"])
            payload["ingestion_ts"] = normalize_timestamp(payload["ingestion_ts"])

            raw = paj.read_json(
                pa.py_buffer(json.dumps(payload).encode("utf-8"))
            )

            flat = (
                raw
                .flatten()
                .select([
                    "event_type",
                    "patient.patient_id",
                    "patient.gender",
                    "encounter.department",
                    "encounter.waiting_list",
                    "encounter.waiting_time",
                    "event_ts",
                    "ingestion_ts",
                    "source_system",
                ])
                .rename_columns([
                    "event_type",
                    "patient_id",
                    "patient_gender",
                    "department_name",
                    "waiting_list",
                    "waiting_time",
                    "event_ts",
                    "ingestion_ts",
                    "source_system",
                ])
            )

            flat_cast = flat.cast(event_schema)

            tables.append(flat_cast)

    monthly = pa.concat_tables(tables)

    output_path = (
        f"s3://{bucket}/staging/{encounter_type}/"
        f"event_month={month}/{encounter_type}.parquet"
    )

    pap.write_table(
        monthly,
        output_path,
        compression="snappy",
        use_dictionary=True
    )

# --------------------------------------------------
# Entry Point
# --------------------------------------------------

def main():

    admission_prefixes = get_encounter_prefixes("admission")
    discharge_prefixes = get_encounter_prefixes("discharge")

    for month, prefixes in admission_prefixes.items():
        build_monthly_encounter_parquet(
            "health-data-raw-elt",
            prefixes,
            month,
            "admission"
        )

    for month, prefixes in discharge_prefixes.items():
        build_monthly_encounter_parquet(
            "health-data-raw-elt",
            prefixes,
            month,
            "discharge"
        )


if __name__ == "__main__":
    main()