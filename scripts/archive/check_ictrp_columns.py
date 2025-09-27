#!/usr/bin/env python3
"""
Check column names in WHO ICTRP data
"""

import pandas as pd

def check_ictrp_columns():
    """Check the actual column names in WHO ICTRP data."""
    print("🔍 WHO ICTRP Data Structure Analysis")
    print("="*50)
    
    # Load data
    df = pd.read_excel("data/ICTRP-Results.xlsx")
    
    print(f"Total studies: {len(df)}")
    print(f"Total columns: {len(df.columns)}")
    
    print(f"\nColumn names:")
    print("-" * 60)
    
    for i, col in enumerate(df.columns, 1):
        print(f"{i:2d}. '{col}'")
    
    # Look for date-related columns
    date_columns = [col for col in df.columns if 'date' in col.lower()]
    print(f"\nDate-related columns:")
    for col in date_columns:
        print(f"  - {col}")
        # Show sample values
        sample = df[col].dropna().head(3)
        print(f"    Sample values: {list(sample)}")
        
    # Look for sponsor-related columns
    sponsor_columns = [col for col in df.columns if 'sponsor' in col.lower()]
    print(f"\nSponsor-related columns:")
    for col in sponsor_columns:
        print(f"  - {col}")

if __name__ == "__main__":
    check_ictrp_columns()