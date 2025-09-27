#!/usr/bin/env python3
"""
Check unique sponsor class values in ClinicalTrials.gov data
to diagnose pie chart labeling issues.
"""

import pandas as pd

def analyze_sponsor_classes():
    """Analyze sponsor class distribution in detail."""
    print("🔍 ClinicalTrials.gov Sponsor Class Analysis")
    print("="*50)
    
    # Load data
    df = pd.read_csv("data/clinicaltrials_ms_20250925.csv")
    
    print(f"Total studies: {len(df)}")
    print(f"Lead Sponsor Class column exists: {'LeadSponsorClass' in df.columns}")
    
    if 'LeadSponsorClass' in df.columns:
        print(f"\nUnique sponsor classes:")
        class_counts = df['LeadSponsorClass'].value_counts()
        
        print(f"Number of unique classes: {len(class_counts)}")
        print("\nDetailed breakdown:")
        print("-" * 60)
        
        for i, (class_name, count) in enumerate(class_counts.items(), 1):
            percentage = (count / len(df)) * 100
            print(f"{i:2d}. '{class_name}' -> {count:4d} studies ({percentage:.1f}%)")
            # Show raw value to check for special characters
            print(f"    Raw value: {repr(class_name)}")
            print(f"    Length: {len(str(class_name))} characters")
            print()
        
        # Check for null values
        null_count = df['LeadSponsorClass'].isna().sum()
        print(f"Null/missing values: {null_count}")
        
        # Show some example data
        print(f"\nFirst 10 sponsor class values:")
        for i, value in enumerate(df['LeadSponsorClass'].head(10), 1):
            print(f"{i:2d}. {repr(value)}")
    
    else:
        print("LeadSponsorClass column not found!")
        print("Available columns:")
        for col in df.columns:
            print(f"  - {col}")

if __name__ == "__main__":
    analyze_sponsor_classes()