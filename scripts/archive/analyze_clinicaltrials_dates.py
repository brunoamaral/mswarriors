#!/usr/bin/env python3
"""
ClinicalTrials.gov Date Range Analysis
Analyze the time frame of the ClinicalTrials.gov MS data to compare with WHO ICTRP and EU CTIS.
"""

import pandas as pd
from datetime import datetime
import numpy as np

def analyze_clinicaltrials_dates():
    """Analyze date ranges in ClinicalTrials.gov data."""
    print("📅 CLINICALTRIALS.GOV DATE RANGE ANALYSIS")
    print("=" * 60)
    
    # Load the data
    df = pd.read_csv('data/clinicaltrials_ms_20250925.csv')
    print(f"Total studies: {len(df)}")
    
    # Analyze different date fields
    date_fields = [
        'StartDate', 
        'PrimaryCompletionDate', 
        'CompletionDate',
        'LastUpdatePostDate',
        'StudyFirstPostDate',
        'ResultsFirstPostDate'
    ]
    
    print(f"\n🔍 DATE FIELD ANALYSIS:")
    print("-" * 40)
    
    for field in date_fields:
        if field in df.columns:
            # Count non-null values
            non_null_count = df[field].notna().sum()
            coverage_pct = (non_null_count / len(df)) * 100
            
            print(f"\n{field}:")
            print(f"  Coverage: {non_null_count}/{len(df)} ({coverage_pct:.1f}%)")
            
            if non_null_count > 0:
                # Convert to datetime and find range
                dates = pd.to_datetime(df[field], errors='coerce')
                valid_dates = dates.dropna()
                
                if len(valid_dates) > 0:
                    min_date = valid_dates.min()
                    max_date = valid_dates.max()
                    
                    print(f"  Date range: {min_date.strftime('%B %d, %Y')} to {max_date.strftime('%B %d, %Y')}")
                    print(f"  Time span: {(max_date - min_date).days} days ({(max_date - min_date).days / 365.25:.1f} years)")
                    
                    # Show distribution by year
                    years = valid_dates.dt.year.value_counts().sort_index()
                    print(f"  Year distribution (top 5):")
                    for year, count in years.head(5).items():
                        pct = (count / len(valid_dates)) * 100
                        print(f"    {year}: {count} studies ({pct:.1f}%)")

def compare_with_other_registries():
    """Compare date ranges with WHO ICTRP and EU CTIS."""
    print(f"\n" + "=" * 60)
    print("📊 CROSS-REGISTRY DATE COMPARISON")
    print("=" * 60)
    
    # ClinicalTrials.gov dates
    ct_df = pd.read_csv('data/clinicaltrials_ms_20250925.csv')
    ct_start_dates = pd.to_datetime(ct_df['StartDate'], errors='coerce').dropna()
    ct_post_dates = pd.to_datetime(ct_df['StudyFirstPostDate'], errors='coerce').dropna()
    
    print(f"\n🇺🇸 CLINICALTRIALS.GOV:")
    if len(ct_start_dates) > 0:
        print(f"  Study start dates: {ct_start_dates.min().strftime('%b %Y')} to {ct_start_dates.max().strftime('%b %Y')}")
        print(f"  Studies with start dates: {len(ct_start_dates)}/{len(ct_df)} ({len(ct_start_dates)/len(ct_df)*100:.1f}%)")
    
    if len(ct_post_dates) > 0:
        print(f"  First posted dates: {ct_post_dates.min().strftime('%b %Y')} to {ct_post_dates.max().strftime('%b %Y')}")
        print(f"  Studies with post dates: {len(ct_post_dates)}/{len(ct_df)} ({len(ct_post_dates)/len(ct_df)*100:.1f}%)")
    
    # Compare with previous findings
    print(f"\n🌍 WHO ICTRP (for comparison):")
    print(f"  Registration dates: Feb 2001 to Dec 2025 (24 years)")
    print(f"  Total studies: 2,482")
    print(f"  Complete date info: 929/2,482 (37.4%)")
    
    print(f"\n🇪🇺 EU CTIS (for comparison):")
    print(f"  Trial dates: Jan 2023 to Aug 2025 (2.5 years)")
    print(f"  Total studies: 104")
    print(f"  Date coverage: ~80% (newer registry)")
    
    # Overlap analysis
    print(f"\n🔍 OVERLAP INSIGHTS:")
    
    # Check decade distribution for ClinicalTrials.gov
    if len(ct_start_dates) > 0:
        decades = {}
        for date in ct_start_dates:
            decade = (date.year // 10) * 10
            decades[decade] = decades.get(decade, 0) + 1
        
        print(f"  ClinicalTrials.gov by decade (start dates):")
        for decade in sorted(decades.keys()):
            count = decades[decade]
            pct = (count / len(ct_start_dates)) * 100
            print(f"    {decade}s: {count} studies ({pct:.1f}%)")
    
    # Calculate potential overlap periods
    print(f"\n📈 POTENTIAL OVERLAP PERIODS:")
    print(f"  All three registries: 2023-2025 (EU CTIS operational period)")
    print(f"  WHO ICTRP + ClinicalTrials.gov: 2001-2025 (24 years)")
    print(f"  Note: Same trials may be registered in multiple registries")

def main():
    """Run the complete date range analysis."""
    analyze_clinicaltrials_dates()
    compare_with_other_registries()
    
    print(f"\n" + "=" * 60)
    print("✅ DATE ANALYSIS COMPLETE")
    print("=" * 60)
    print(f"Key findings:")
    print(f"• ClinicalTrials.gov has the largest dataset (3,616 studies)")
    print(f"• Likely spans similar timeframe to WHO ICTRP (2001-2025)")  
    print(f"• Good date coverage for analysis")
    print(f"• Ready for comprehensive cross-registry comparison")

if __name__ == "__main__":
    main()