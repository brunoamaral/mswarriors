#!/usr/bin/env python3
"""
Quick analysis of CTIS sponsor types to identify grouping opportunities.
"""
import pandas as pd

def analyze_sponsor_types():
    df = pd.read_csv('data/CTIS_trials_20250924.csv')
    
    print("CTIS Sponsor Type Distribution:")
    print("=" * 50)
    
    sponsor_counts = df['Sponsor type'].value_counts()
    print(sponsor_counts)
    
    print("\nDetailed Analysis:")
    print("=" * 30)
    
    total_trials = len(df)
    
    for stype, count in sponsor_counts.items():
        percentage = count / total_trials * 100
        print(f"{stype}: {count} trials ({percentage:.1f}%)")
    
    print(f"\nTotal trials: {total_trials}")
    
    # Identify small categories (less than 3%)
    print("\nCategories under 3%:")
    print("-" * 25)
    small_categories = []
    for stype, count in sponsor_counts.items():
        percentage = count / total_trials * 100
        if percentage < 3.0:
            small_categories.append((stype, count, percentage))
            print(f"  {stype}: {count} trials ({percentage:.1f}%)")
    
    print(f"\nFound {len(small_categories)} categories under 3% threshold")

if __name__ == "__main__":
    analyze_sponsor_types()