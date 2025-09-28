#!/usr/bin/env python3
"""
Simple sponsor analysis - shows unique sponsor values and counts for each registry.
"""

import pandas as pd

def main():
    print("🔍 Sponsor Unique Values Analysis")
    print("=" * 50)
    
    # ClinicalTrials.gov
    print("\n📊 CLINICALTRIALS.GOV")
    try:
        df = pd.read_csv("data/clinicaltrials_ms_20250925.csv")
        sponsors = df['LeadSponsorName'].value_counts()
        print(f"Total unique sponsors: {len(sponsors)}")
        for sponsor, count in sponsors.head(20).items():
            print(f"{count:4d} - {sponsor}")
    except Exception as e:
        print(f"Error: {e}")
    
    # WHO ICTRP  
    print("\n📊 WHO ICTRP")
    try:
        df = pd.read_excel("data/ICTRP-Results.xlsx")
        sponsors = df['Primary_sponsor'].value_counts()
        print(f"Total unique sponsors: {len(sponsors)}")
        for sponsor, count in sponsors.head(20).items():
            print(f"{count:4d} - {sponsor}")
    except Exception as e:
        print(f"Error: {e}")
    
    # EU CTIS
    print("\n📊 EU CTIS")
    try:
        df = pd.read_csv("data/CTIS_trials_20250924.csv")
        sponsors = df['Sponsor/Co-Sponsors'].value_counts()
        print(f"Total unique sponsors: {len(sponsors)}")
        for sponsor, count in sponsors.items():
            print(f"{count:4d} - {sponsor}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()