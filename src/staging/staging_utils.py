import re
from src.raw.ingestion.s3config import client

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
# Group by Month
# --------------------------------------------------

def group_prefixes_by_month(prefixes: list[str]):

    for prefix in prefixes:

        date = re.search(r'\d{4}-\d{2}', prefix)

        print(date.group())

# prefixes = list_daily_prefixes("health-data-raw-elt", "raw/admission/")

# group_prefixes_by_month(prefixes)