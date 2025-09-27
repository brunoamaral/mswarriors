#!/usr/bin/env python3
"""
Analyze the date range of clinical trials in our dataset
"""

import pandas as pd
import numpy as np
from datetime import datetime

def analyze_trial_dates():
    """Analyze the registration date range of trials in our dataset."""
    print("Analyzing trial registration dates...")
    
    # Load the data
    df = pd.read_excel("data/ICTRP-Results.xlsx")
    
    # Convert date columns to datetime
    df_dates = df.copy()
    df_dates['Date_registration'] = pd.to_datetime(df_dates['Date_registration'], errors='coerce')
    df_dates['Date_registration3'] = pd.to_datetime(df_dates['Date_registration3'].astype(str), format='%Y%m%d', errors='coerce')
    
    # Use the primary date registration column
    valid_dates = df_dates.dropna(subset=['Date_registration'])
    
    print(f"\nDate Analysis Results:")
    print(f"=" * 50)
    print(f"Total trials: {len(df):,}")
    print(f"Trials with valid registration dates: {len(valid_dates):,}")
    print(f"Trials with missing dates: {len(df) - len(valid_dates):,}")
    
    if len(valid_dates) > 0:
        earliest_date = valid_dates['Date_registration'].min()
        latest_date = valid_dates['Date_registration'].max()
        
        print(f"\nDate Range:")
        print(f"Earliest trial registration: {earliest_date.strftime('%B %d, %Y')}")
        print(f"Latest trial registration: {latest_date.strftime('%B %d, %Y')}")
        print(f"Time span: {(latest_date - earliest_date).days:,} days ({(latest_date - earliest_date).days // 365} years)")
        
        # Show distribution by decade
        valid_dates['Year'] = valid_dates['Date_registration'].dt.year
        valid_dates['Decade'] = (valid_dates['Year'] // 10) * 10
        
        print(f"\nTrials by Decade:")
        decade_counts = valid_dates['Decade'].value_counts().sort_index()
        for decade, count in decade_counts.items():
            decade_end = decade + 9
            percentage = (count / len(valid_dates)) * 100
            print(f"{decade}s ({decade}-{decade_end}): {count:4d} trials ({percentage:5.1f}%)")
        
        # Recent activity (last 5 years)
        recent_cutoff = datetime.now() - pd.DateOffset(years=5)
        recent_trials = valid_dates[valid_dates['Date_registration'] >= recent_cutoff]
        
        print(f"\nRecent Activity (since {recent_cutoff.strftime('%Y')}):")
        print(f"Trials registered in last 5 years: {len(recent_trials):,} ({(len(recent_trials)/len(valid_dates)*100):.1f}%)")
        
        # Show some sample early and recent trials
        print(f"\nSample Early Trials:")
        early_trials = valid_dates.nsmallest(3, 'Date_registration')[['Date_registration', 'Public_title', 'Primary_sponsor']]
        for idx, row in early_trials.iterrows():
            print(f"  {row['Date_registration'].strftime('%Y-%m-%d')}: {row['Public_title'][:60]}... (Sponsor: {row['Primary_sponsor'][:40]}...)")
        
        print(f"\nSample Recent Trials:")
        recent_trials_sample = valid_dates.nlargest(3, 'Date_registration')[['Date_registration', 'Public_title', 'Primary_sponsor']]
        for idx, row in recent_trials_sample.iterrows():
            print(f"  {row['Date_registration'].strftime('%Y-%m-%d')}: {row['Public_title'][:60]}... (Sponsor: {row['Primary_sponsor'][:40]}...)")
        
        return {
            'earliest_date': earliest_date,
            'latest_date': latest_date,
            'total_with_dates': len(valid_dates),
            'decade_counts': decade_counts
        }
    else:
        print("No valid dates found in the dataset")
        return None

if __name__ == "__main__":
    results = analyze_trial_dates()