import pyarrow as pa

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
    pa.field("event_ts", pa.timestamp("ms"), nullable=False),
    pa.field("ingestion_ts", pa.timestamp("ms"), nullable=False),
    pa.field("source_system", pa.string(), nullable=False),
])