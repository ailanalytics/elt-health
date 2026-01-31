"""
Entry point for raw data generator
Writes json to local dev data folder
"""
import admission as adm

# --------------------------------------------------
# Entry Point
# --------------------------------------------------

def main():
    adm.generate_admissions()

if __name__ == "__main__":
    main()