"""
Orchestration for creating waiting list snapshot parquet
S3 raw json parsed into rows before passing to PyArrow
Appended to S3 staging partitioned by YYYY-MM
"""

from src.staging.staging_utils import get_prefixes, build_parquet
from src.staging.schemas import waiting_schema

# --------------------------------------------------
# Entry Point
# --------------------------------------------------

def main():

    waiting_select = [
        "event_type",
        "waiting_count",
        "phase",
        "event_ts",
        "ingestion_ts",
        "source_system",
    ]

    waiting_prefixes = get_prefixes("wait_snapshot", "month")

    for month, prefixes in waiting_prefixes.items():
        build_parquet(
            "health-data-raw-elt",
            prefixes,
            month,
            "waiting_list_snapshot",
            waiting_schema,
            waiting_select,
            waiting_select,
            False
        )


if __name__ == "__main__":
    main()