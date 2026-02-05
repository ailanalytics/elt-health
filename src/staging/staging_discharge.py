import pyarrow as pa
import pyarrow.json as paj
import pyarrow.parquet as pap
import pyarrow.compute as pac
import json
from src.staging.staging_utils import *
from collections import defaultdict

# --------------------------------------------------
# Discharge Schema
# --------------------------------------------------

discharge_schema = pa.schema([
    # Event
    pa.field("event_type", pa.string(), nullable=False),

    # Patient
    pa.field("patient_id", pa.int64(), nullable=False),
    pa.field("patient_gender", pa.string(), nullable=True),

    # Encounter
    pa.field("department_name", pa.string(), nullable=False),
    pa.field("waiting_list", pa.bool_(), nullable=False),
    pa.field("waiting_time", pa.int16(), nullable=False),

    # Metadata
    pa.field("event_ts", pa.timestamp("ms", tz="UTC"), nullable=False),
    pa.field("ingestion_ts", pa.timestamp("ms", tz="UTC"), nullable=False),
    pa.field("source_system", pa.string(), nullable=False),
])

# --------------------------------------------------
# Group Monthly Discharge Prefixes From S3
# --------------------------------------------------

def get_discharge_prefixes() -> defaultdict[str: list[str]]:

    """
    Returns a dictionary of prefixes grouped by date: YYYY-MM
    
    :return: Grouped prefixes
    :rtype: defaultdict
    """

    prefixes = list_daily_prefixes("health-data-raw-elt", "raw/discharge/")

    return group_prefixes_by_month(prefixes)

# --------------------------------------------------
# Build Monthly Discharge Parquet
# --------------------------------------------------

def build_monthly_discharge_parquet(bucket: str, daily_prefixes: list[str], month: str):

    """
    Creates parquet file for laoding into S3 staging
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

            flat_cast = flat.cast(discharge_schema)

            tables.append(flat_cast)

    monthly = pa.concat_tables(tables)

    output_path = (
        f"s3://{bucket}/staging/discharge/"
        f"event_month={month}/discharge.parquet"
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

    monthly_prefixes = get_discharge_prefixes()

    for month, prefixes in monthly_prefixes.items():
        build_monthly_discharge_parquet(
            "health-data-raw-elt",
            prefixes,
            month
        )


if __name__ == "__main__":
    main()