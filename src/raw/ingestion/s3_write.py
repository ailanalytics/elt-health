"""
Writes generator data to S3 bucket
"""

import json
import uuid
from datetime import datetime, timezone
from src.raw.source_gen.source_gen_utils import date_from_timestamp
from src.raw.ingestion.s3config import client, s3_bucket

# --------------------------------------------------
# Write Encounter to S3
# --------------------------------------------------

def write_to_bucket(payload: dict):

    """
    Writes event to S3
    
    :param payload: Payload data
    :type payload: dict
    """

    ingestion_ts = str(datetime.now(timezone.utc))
    event_ts = str(datetime.fromisoformat(payload["event_ts"]))
    event_date = str(date_from_timestamp(event_ts))
    event_type = payload["event_type"]
    payload["ingestion_ts"] = ingestion_ts

    key = (
        f"{event_type}/event_date={event_date}/{event_type}_{uuid.uuid4().hex}.json"
    )

    client.put_object(
        Bucket=s3_bucket,
        Key=key,
        Body=json.dumps(payload).encode("utf-8"),
        ContentType="application/json"
    )