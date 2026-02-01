"""
Entry point for source data generator
Generates encounter events for admissions and discharges
Captures operational data for downstream analytics
"""
from src.raw.source_gen.admission import generate_admissions

# --------------------------------------------------
# Entry Point
# --------------------------------------------------

def main():
    generate_admissions()

if __name__ == "__main__":
    main()