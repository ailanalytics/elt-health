"""
PyArrow Staging Schemas
"""

import pyarrow as pa

# --------------------------------------------------
# Encounter Schema
# --------------------------------------------------

encounter_schema = pa.schema([
    pa.field("event_type", pa.string(), nullable=False),
    pa.field("patient_id", pa.int64(), nullable=False),
    pa.field("patient_gender", pa.string(), nullable=True),
    pa.field("department_name", pa.string(), nullable=False),
    pa.field("waiting_list", pa.bool_(), nullable=False),
    pa.field("waiting_time", pa.int16(), nullable=False),
    pa.field("event_ts", pa.timestamp("ms", tz="UTC"), nullable=False),
    pa.field("ingestion_ts", pa.timestamp("ms", tz="UTC"), nullable=False),
    pa.field("source_system", pa.string(), nullable=False),
])

# --------------------------------------------------
# Waiting List Snapshot Schema
# --------------------------------------------------

waiting_schema = pa.schema([
    pa.field("event_type", pa.string(), nullable=False),
    pa.field("waiting_count", pa.int32(), nullable=False),
    pa.field("phase", pa.string(), nullable=False),
    pa.field("event_ts", pa.timestamp("ms", tz="UTC"), nullable=False),
    pa.field("ingestion_ts", pa.timestamp("ms", tz="UTC"), nullable=False),
    pa.field("source_system", pa.string(), nullable=False),
])

# --------------------------------------------------
# Department Snapshot Schema
# --------------------------------------------------

department_schema = pa.schema([
    pa.field("event_type", pa.string(), nullable=False),
    pa.field("ward_name", pa.string(), nullable=False),
    pa.field("beds_total", pa.int16(), nullable=False),
    pa.field("beds_occupied", pa.int16(), nullable=False),
    pa.field("beds_available", pa.int16(), nullable=False),
    pa.field("phase", pa.string(), nullable=False),
    pa.field("event_ts", pa.timestamp("ms", tz="UTC"), nullable=False),
    pa.field("source_system", pa.string(), nullable=False),
    pa.field("ingestion_ts", pa.timestamp("ms", tz="UTC"), nullable=False),
])