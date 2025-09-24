#!/usr/bin/env python3
"""
Clinical Trials Sponsor Analysis
Analyzes clinical trial data from WHO ICTRP to identify top sponsors and funding patterns.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import xml.etree.ElementTree as ET
from collections import Counter
import numpy as np
import os

def ensure_charts_directory():
    """Create charts directory if it doesn't exist."""
    charts_dir = "charts"
    if not os.path.exists(charts_dir):
        os.makedirs(charts_dir)
        print(f"Created {charts_dir} directory")
    return charts_dir

def load_xml_data(file_path):
    """Load and parse XML data into a pandas DataFrame."""
    print("Loading XML data...")
    
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # Extract data from each trial
    trials_data = []
    
    for trial in root.findall('Trial'):
        trial_dict = {}
        for element in trial:
            # Clean up the text content
            text = element.text.strip() if element.text else ''
            trial_dict[element.tag] = text
        trials_data.append(trial_dict)
    
    df = pd.DataFrame(trials_data)
    print(f"Loaded {len(df)} trials from XML file")
    return df

def load_excel_data(file_path):
    """Load Excel data into a pandas DataFrame."""
    print("Loading Excel data...")
    
    try:
        df = pd.read_excel(file_path)
        print(f"Loaded {len(df)} trials from Excel file")
        return df
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return None

def explore_data_structure(df, data_source=""):
    """Explore the structure and content of the DataFrame."""
    print(f"\n=== {data_source} Data Structure ===")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    
    print(f"\nColumn data types:")
    print(df.dtypes)
    
    print(f"\nFirst few rows:")
    print(df.head())
    
    # Look for sponsor-related columns
    sponsor_columns = [col for col in df.columns if 'sponsor' in col.lower()]
    print(f"\nSponsor-related columns: {sponsor_columns}")
    
    # Look for funding-related columns
    funding_columns = [col for col in df.columns if any(word in col.lower() for word in ['fund', 'support', 'financ'])]
    print(f"Funding-related columns: {funding_columns}")
    
    return sponsor_columns, funding_columns

def clean_sponsor_data(df):
    """Clean and standardize sponsor names."""
    print("\n=== Cleaning Sponsor Data ===")
    
    # Focus on primary sponsors first
    primary_sponsors = df['Primary_sponsor'].fillna('Unknown')
    
    # Clean sponsor names (remove extra whitespace, standardize)
    primary_sponsors = primary_sponsors.str.strip()
    
    # Look at some examples
    print(f"Total unique primary sponsors: {primary_sponsors.nunique()}")
    print(f"\nTop 15 primary sponsors by frequency:")
    sponsor_counts = primary_sponsors.value_counts().head(15)
    for sponsor, count in sponsor_counts.items():
        print(f"  {count:3d}: {sponsor}")
    
    # Also check secondary sponsors
    secondary_sponsors = df['Secondary_Sponsor'].fillna('')
    secondary_sponsors = secondary_sponsors.str.strip()
    non_empty_secondary = secondary_sponsors[secondary_sponsors != '']
    
    print(f"\nSecondary sponsors info:")
    print(f"  Trials with secondary sponsors: {len(non_empty_secondary)}")
    if len(non_empty_secondary) > 0:
        print(f"  Top 10 secondary sponsors:")
        sec_counts = non_empty_secondary.value_counts().head(10)
        for sponsor, count in sec_counts.items():
            print(f"    {count:2d}: {sponsor}")
    
    return primary_sponsors, secondary_sponsors

def analyze_top_sponsors(df, top_n=10):
    """Analyze and identify top sponsors."""
    print(f"\n=== Analyzing Top {top_n} Sponsors ===")
    
    primary_sponsors, _ = clean_sponsor_data(df)
    
    # Get top sponsors
    top_sponsors = primary_sponsors.value_counts().head(top_n)
    
    print(f"\nTop {top_n} Primary Sponsors:")
    print("-" * 50)
    for i, (sponsor, count) in enumerate(top_sponsors.items(), 1):
        percentage = (count / len(df)) * 100
        print(f"{i:2d}. {sponsor:<40} {count:3d} trials ({percentage:.1f}%)")
    
    return top_sponsors

def create_sponsor_visualization(top_sponsors, save_path="charts/top_sponsors_chart.png"):
    """Create a professional visualization of top sponsors."""
    print(f"\n=== Creating Visualization ===")
    
    # Ensure charts directory exists
    ensure_charts_directory()
    
    # Set up the plot style
    plt.style.use('default')
    sns.set_palette("husl")
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create horizontal bar chart
    y_pos = np.arange(len(top_sponsors))
    sponsors = top_sponsors.index.tolist()
    counts = top_sponsors.values.tolist()
    
    # Shorten long sponsor names for better display
    shortened_sponsors = []
    for sponsor in sponsors:
        if len(sponsor) > 45:
            shortened_sponsors.append(sponsor[:42] + "...")
        else:
            shortened_sponsors.append(sponsor)
    
    bars = ax.barh(y_pos, counts, color=sns.color_palette("husl", len(sponsors)))
    
    # Customize the chart
    ax.set_yticks(y_pos)
    ax.set_yticklabels(shortened_sponsors)
    ax.invert_yaxis()  # Top sponsor at the top
    ax.set_xlabel('Number of Clinical Trials', fontsize=12, fontweight='bold')
    ax.set_ylabel('Primary Sponsor', fontsize=12, fontweight='bold')
    ax.set_title('Top 10 Sponsors of Multiple Sclerosis Clinical Trials\n(WHO ICTRP Database - 2,482 total trials, exported Sept 2025)', 
                 fontsize=14, fontweight='bold', pad=20)
    
    # Add value labels on bars
    for i, (bar, count) in enumerate(zip(bars, counts)):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, 
                str(count), va='center', fontweight='bold')
    
    # Add grid for better readability
    ax.grid(axis='x', alpha=0.3)
    ax.set_axisbelow(True)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the chart
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Chart saved as: {save_path}")
    
    return fig

def explore_funding_patterns(df):
    """Explore various funding and trial patterns."""
    print(f"\n=== Exploring Funding Patterns ===")
    
    # Phase distribution
    phases = df['Phase'].fillna('Not specified')
    print(f"\nTrial phases distribution:")
    phase_counts = phases.value_counts()
    for phase, count in phase_counts.head(10).items():
        percentage = (count / len(df)) * 100
        print(f"  {phase:<25} {count:3d} trials ({percentage:.1f}%)")
    
    # Countries analysis
    countries = df['Countries'].fillna('Not specified')
    print(f"\nTop 10 countries by number of trials:")
    country_counts = countries.value_counts().head(10)
    for country, count in country_counts.items():
        percentage = (count / len(df)) * 100
        print(f"  {country:<25} {count:3d} trials ({percentage:.1f}%)")
    
    # Study type analysis
    study_types = df['Study_type'].fillna('Not specified')
    print(f"\nStudy types:")
    type_counts = study_types.value_counts()
    for study_type, count in type_counts.items():
        percentage = (count / len(df)) * 100
        print(f"  {study_type:<25} {count:3d} trials ({percentage:.1f}%)")
    
    # Recruitment status
    recruitment = df['Recruitment_Status'].fillna('Not specified')
    print(f"\nRecruitment status:")
    recruitment_counts = recruitment.value_counts()
    for status, count in recruitment_counts.items():
        percentage = (count / len(df)) * 100
        print(f"  {status:<25} {count:3d} trials ({percentage:.1f}%)")
    
    return {
        'phases': phase_counts,
        'countries': country_counts,
        'study_types': type_counts,
        'recruitment_status': recruitment_counts
    }

def main():
    # File paths - we'll use Excel for better data type handling
    excel_file = "data/ICTRP-Results.xlsx"
    
    # Load data
    print("Loading clinical trials data...")
    df = load_excel_data(excel_file)
    
    if df is None:
        print("Failed to load data. Exiting.")
        return
    
    print(f"Successfully loaded {len(df)} clinical trials for Multiple Sclerosis")
    
    # Analyze top sponsors
    top_sponsors = analyze_top_sponsors(df, top_n=10)
    
    # Create visualization
    create_sponsor_visualization(top_sponsors)
    
    # Explore additional patterns
    patterns = explore_funding_patterns(df)
    
    # Summary
    print(f"\n=== Summary ===")
    print(f"Total trials analyzed: {len(df):,}")
    print(f"Total unique primary sponsors: {df['Primary_sponsor'].nunique()}")
    print(f"Top sponsor represents {(top_sponsors.iloc[0] / len(df) * 100):.1f}% of all trials")
    print(f"Top 10 sponsors represent {(top_sponsors.sum() / len(df) * 100):.1f}% of all trials")

if __name__ == "__main__":
    main()