"""
Helper functions for orchestration, normalising fields,
returning S3 prefixes, grouping prefixes
"""

import re
import pyarrow as pa
import pyarrow.parquet as pap
import json
from pyarrow.fs import S3FileSystem, FileSelector
from src.raw.ingestion.s3config import client
from src.staging.staging_department_snapshot import explode_department_snapshot
from collections import defaultdict
from datetime import datetime, timezone

# --------------------------------------------------
# List Daily Prefixes
# --------------------------------------------------

def list_daily_prefixes(bucket: str, prefix: str) -> list[str]:

    """
    Return S3 prefixes
    
    :param bucket: Bucket name
    :type bucket: str
    :param prefix: Prefix path
    :type prefix: str
    :return: List of partitions
    :rtype: list[str]
    """

    paginator = client.get_paginator("list_objects_v2")

    prefixes = set()

    for page in paginator.paginate(Bucket=bucket, Prefix=prefix, Delimiter="/"):
        
        for prefix in page.get("CommonPrefixes", []):
            prefixes.add(prefix["Prefix"])

    return sorted(prefixes)

# --------------------------------------------------
# Group Prefixes by Date
# --------------------------------------------------

def group_prefixes_by_date(prefixes: list[str], date_type: str) -> defaultdict[str: list[str]]:

    """
    Groups prefixes by date: YYYY-MM/YYYY
    
    :param prefixes: List of prefixes from S3 
    :type prefixes: list[str]
    :param date_type: month or year
    :type date_type: str
    :return: Dict of date prefixes
    :rtype: defaultdict
    """

    grouped_prefix = defaultdict(list)

    for prefix in prefixes:

        if date_type == "month":    
            date = re.search(r'\d{4}-\d{2}', prefix).group()
        else:
            date = re.search(r'\d{4}', prefix).group()

        grouped_prefix[date].append(prefix)

    return grouped_prefix

# --------------------------------------------------
# Get Objects at S3 Prefix
# --------------------------------------------------

def get_objects_at_prefix(prefix: str) -> list[str]:

    """
    Returns list of objects at given prefix
    
    :param prefix: Prefix
    :type prefix: str
    :return: List of objects
    :rtype: list[str]
    """

    fs = S3FileSystem()

    selector = FileSelector(
        base_dir = prefix,
        recursive = True
    )

    files = fs.get_file_info(selector)

    keys = [
        f.path for f in files
        if f.path.endswith(".json")
    ]

    return keys

# --------------------------------------------------
# Return PyArrow Table
# --------------------------------------------------

def get_raw_object(fs: S3FileSystem, object: str, isDepartment: bool) -> pa.Table:

    """
    Get raw json from S3
    Normalise timestamps 
    Explode if department snapshot
    
    :param fs: S3 Filesystem
    :type fs: S3FileSystem
    :param object: Raw json object
    :type object: str
    :param isDepartment: isDepartment -> explode nested objects
    :type isDepartment: bool
    :return: PyArrow table
    :rtype: Any
    """

    with fs.open_input_file(object) as f:
        payload = json.loads(f.read().decode("utf-8"))

    payload["event_ts"] = normalise_timestamp(payload["event_ts"])
    payload["ingestion_ts"] = normalise_timestamp(payload["ingestion_ts"])

    if isDepartment:
        rows = explode_department_snapshot(payload) 
    else:
        rows = [payload]                              

    return pa.Table.from_pylist(rows)

# --------------------------------------------------
# Group Event Prefixes From S3
# --------------------------------------------------

def get_prefixes(event_type: str, date_type: str) -> defaultdict[str: list[str]]:

    """
    Returns a dictionary of prefixes grouped by date
    
    :return: Grouped prefixes
    :rtype: defaultdict
    """

    prefixes = list_daily_prefixes("health-data-raw-elt", f"raw/{event_type}/")

    return group_prefixes_by_date(prefixes, date_type)

# --------------------------------------------------
# Build Parquet
# --------------------------------------------------

def build_parquet(
        bucket: str, 
        daily_prefixes: list[str], 
        date: str, 
        event_type: str,
        schema: pa.schema,
        select: list[str],
        rename: list[str],
        isDepartment: bool
        ):
    
    """
    Takes list of daily prefixes, gets S3 raw objects 
    Parses raw json object, normalises timestamps, 
    explodes nested json for department snapshots
    Flattens raw json object for parquet
    Casts to parquet schema, enforcing types
    Creates tables and appends to S3 staging
    
    :param bucket: S3 Bucket
    :type bucket: str
    :param daily_prefixes: List of prefixes returned from S3 raw
    :type daily_prefixes: list[str]
    :param date: Partition date - YYYY-MM || YYYY
    :type date: str
    :param event_type: Used for S3 staging partition 
    :type event_type: str
    :param schema: PyArrow schema
    :type schema: pa.schema
    :param select: Json fields to select from raw
    :type select: list[str]
    :param rename: Rename raw fields
    :type rename: list[str]
    :param isDepartment: Determine if event is a department snapshot
    :type isDepartment: bool
    """

    tables = []

    fs = S3FileSystem()

    for prefix in daily_prefixes:

        s3_prefix = f"{bucket}/{prefix}"
        objects_at_prefix = get_objects_at_prefix(s3_prefix)

        for object in objects_at_prefix:

            raw = get_raw_object(fs, object, isDepartment)

            flat = (
                raw
                .flatten()
                .select(select)
                .rename_columns(rename)
            ).cast(schema)

            tables.append(flat)

    parquet_tables = pa.concat_tables(tables)

    output_path = (
        f"s3://{bucket}/staging/{event_type}/"
        f"event_date={date}/{event_type}.parquet"
    )

    pap.write_table(
        parquet_tables,
        output_path,
        compression="snappy",
        use_dictionary=True
    )

    print(f"[OK] Writing Parquet To S3 for {event_type} {date}")

# --------------------------------------------------
# Normalise Timestamps
# --------------------------------------------------

def normalise_timestamp(value: str) -> str:

    """
    Normalize timestamp to ISO-8601 UTC string.

    :param value: Input string
    :type value: str
    :return: Formatted timestamp
    :rtype: str
    """

    dt = datetime.fromisoformat(value)

    return (
        dt.astimezone(timezone.utc)
          .isoformat(timespec="milliseconds")
          .replace("+00:00", "Z")
    )