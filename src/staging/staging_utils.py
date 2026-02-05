import re
import pyarrow as pa
from pyarrow.fs import S3FileSystem, FileSelector
from src.raw.ingestion.s3config import client
from collections import defaultdict
from datetime import datetime, timezone

# --------------------------------------------------
# Event Schema
# --------------------------------------------------

event_schema = pa.schema([
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
# Group Prefixes by Month
# --------------------------------------------------

def group_prefixes_by_month(prefixes: list[str]) -> defaultdict[str: list[str]]:

    """
    Groups prefixes by YYYY-MM
    
    :param prefixes: List of prefixes from S3 
    :type prefixes: list[str]
    :return: Dict of key: YYYY-MM, value: list of months prefixes
    :rtype: defaultdict
    """

    grouped_prefix = defaultdict(list)

    for prefix in prefixes:

        date = re.search(r'\d{4}-\d{2}', prefix).group()

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
# Normalise Timestamps
# --------------------------------------------------

def normalize_timestamp(value: str) -> str:

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
