"""
Entry point for source data generator
Generates encounter events for admissions and discharges
Captures operational data for downstream analytics
"""
import admission as adm

# --------------------------------------------------
# Entry Point
# --------------------------------------------------

def main():
    adm.generate_admissions()

if __name__ == "__main__":
    main()