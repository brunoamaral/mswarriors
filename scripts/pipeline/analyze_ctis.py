#!/usr/bin/env python3
"""
EU Clinical Trials Information System (CTIS) Analysis
Analyzes MS clinical trial data from CTIS to identify sponsors and funding patterns
for comparison with WHO ICTRP findings.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from datetime import datetime

def ensure_charts_directory():
    """Create charts directory if it doesn't exist."""
    charts_dir = "charts"
    if not os.path.exists(charts_dir):
        os.makedirs(charts_dir)
        print(f"Created {charts_dir} directory")
    return charts_dir

def load_ctis_data():
    """Load the CTIS data and explore its structure."""
    print("Loading CTIS data...")
    df = pd.read_csv("data/CTIS_trials_20250924.csv")
    print(f"Loaded {len(df)} trials from CTIS")
    return df

def analyze_ctis_structure(df):
    """Analyze the CTIS data structure and key fields."""
    print(f"\n=== CTIS Data Structure ===")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    
    # Check key sponsor fields
    print(f"\nSponsor field analysis:")
    print(f"Sponsor/Co-Sponsors - Unique values: {df['Sponsor/Co-Sponsors'].nunique()}")
    print(f"Sponsor/Co-Sponsors - Missing values: {df['Sponsor/Co-Sponsors'].isna().sum()}")
    
    print(f"\nSponsor type analysis:")
    sponsor_types = df['Sponsor type'].value_counts()
    print(f"Sponsor types available:")
    for stype, count in sponsor_types.items():
        print(f"  {stype}: {count} trials")
    
    # Check date fields
    date_fields = ['Decision date', 'Start date', 'End date', 'Last updated']
    for field in date_fields:
        if field in df.columns:
            non_null = df[field].notna().sum()
            print(f"{field} - Non-null values: {non_null}/{len(df)} ({non_null/len(df)*100:.1f}%)")
    
    return sponsor_types

def analyze_ctis_sponsors(df):
    """Analyze CTIS sponsor data and identify top sponsors."""
    print(f"\n=== CTIS Sponsor Analysis ===")
    
    # Clean sponsor names
    sponsors = df['Sponsor/Co-Sponsors'].fillna('Unknown').str.strip()
    
    # Get top sponsors
    top_sponsors = sponsors.value_counts()
    
    print(f"Total unique sponsors: {sponsors.nunique()}")
    print(f"\nTop 10 sponsors in CTIS:")
    print("-" * 60)
    for i, (sponsor, count) in enumerate(top_sponsors.head(10).items(), 1):
        percentage = (count / len(df)) * 100
        print(f"{i:2d}. {sponsor:<45} {count:2d} trials ({percentage:.1f}%)")
    
    return top_sponsors

def create_ctis_sponsor_chart(top_sponsors, save_path="charts/ctis_top_sponsors.png"):
    """Create visualization of top CTIS sponsors."""
    print(f"\n=== Creating CTIS Sponsor Visualization ===")
    
    ensure_charts_directory()
    
    # Take top 10 for visualization
    top_10 = top_sponsors.head(10)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create horizontal bar chart
    y_pos = np.arange(len(top_10))
    sponsors = top_10.index.tolist()
    counts = top_10.values.tolist()
    
    # Shorten long sponsor names for better display
    shortened_sponsors = []
    for sponsor in sponsors:
        if len(sponsor) > 45:
            shortened_sponsors.append(sponsor[:42] + "...")
        else:
            shortened_sponsors.append(sponsor)
    
    bars = ax.barh(y_pos, counts, color=sns.color_palette("viridis", len(sponsors)))
    
    # Customize the chart
    ax.set_yticks(y_pos)
    ax.set_yticklabels(shortened_sponsors)
    ax.invert_yaxis()  # Top sponsor at the top
    ax.set_xlabel('Number of Clinical Trials', fontsize=12, fontweight='bold')
    ax.set_ylabel('Primary Sponsor', fontsize=12, fontweight='bold')
    ax.set_title('Top 10 Sponsors of MS Clinical Trials in EU CTIS\n(131 total trials, exported Sept 2025)', 
                 fontsize=14, fontweight='bold', pad=20)
    
    # Add value labels on bars
    for i, (bar, count) in enumerate(zip(bars, counts)):
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                str(count), va='center', fontweight='bold')
    
    # Add grid for better readability
    ax.grid(axis='x', alpha=0.3)
    ax.set_axisbelow(True)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the chart
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"CTIS sponsors chart saved as: {save_path}")
    
    return fig

def create_ctis_sponsor_type_chart(df, save_path="charts/ctis_sponsor_types.png"):
    """Create visualization of sponsor types in CTIS with grouped categories."""
    print("Creating CTIS sponsor type visualization with grouped categories...")
    
    ensure_charts_directory()
    
    # Get raw sponsor types
    raw_sponsor_types = df['Sponsor type'].value_counts()
    
    # Group small categories and clean duplicates
    grouped_types = {}
    
    for sponsor_type, count in raw_sponsor_types.items():
        percentage = (count / len(df)) * 100
        
        # Clean up pharmaceutical duplicates
        if 'Pharmaceutical company' in sponsor_type:
            if 'Pharmaceutical Company' not in grouped_types:
                grouped_types['Pharmaceutical Company'] = 0
            grouped_types['Pharmaceutical Company'] += count
        
        # Clean up hospital/clinic duplicates  
        elif 'Hospital/Clinic/Other health care facility' in sponsor_type:
            if 'Hospital/Clinic/Healthcare' not in grouped_types:
                grouped_types['Hospital/Clinic/Healthcare'] = 0
            grouped_types['Hospital/Clinic/Healthcare'] += count
            
        # Group small categories (under 3%)
        elif percentage < 3.0:
            if 'Academic/Research/Other' not in grouped_types:
                grouped_types['Academic/Research/Other'] = 0
            grouped_types['Academic/Research/Other'] += count
            
        else:
            grouped_types[sponsor_type] = count
    
    # Convert to series for consistent handling
    import pandas as pd
    sponsor_types = pd.Series(grouped_types).sort_values(ascending=False)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create pie chart with better colors
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57'][:len(sponsor_types)]
    wedges, texts, autotexts = ax.pie(sponsor_types.values, labels=sponsor_types.index, 
                                      autopct='%1.1f%%', colors=colors, startangle=90)
    
    # Customize text
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(12)
    
    for text in texts:
        text.set_fontsize(11)
        text.set_fontweight('bold')
    
    ax.set_title('Distribution by Sponsor Type - EU CTIS MS Trials\n(104 total trials, Sept 2025)', 
                 fontweight='bold', fontsize=14, pad=20)
    
    # Add summary text
    total_trials = len(df)
    pharma_pct = (sponsor_types.get('Pharmaceutical Company', 0) / total_trials) * 100
    textstr = f'Pharmaceutical dominance: {pharma_pct:.1f}% of trials'
    ax.text(0.02, 0.02, textstr, transform=ax.transAxes, fontsize=10,
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgray', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"CTIS sponsor types chart saved as: {save_path}")
    
    return fig, sponsor_types

def analyze_ctis_trial_phases(df):
    """Analyze trial phases in CTIS data."""
    phases = df['Trial phase'].fillna('Not specified')
    phase_counts = phases.value_counts()
    
    print(f"\nTrial phases in CTIS:")
    for phase, count in phase_counts.items():
        percentage = (count / len(df)) * 100
        print(f"  {phase:<40} {count:2d} trials ({percentage:.1f}%)")
    
    return phase_counts

def analyze_ctis_dates(df):
    """Analyze date ranges in CTIS data."""
    print(f"\n=== CTIS Date Analysis ===")
    
    # Convert date columns
    df_dates = df.copy()
    date_columns = ['Decision date', 'Start date', 'End date', 'Last updated']
    
    for col in date_columns:
        if col in df_dates.columns:
            df_dates[col] = pd.to_datetime(df_dates[col], errors='coerce')
    
    # Analyze start dates
    if 'Start date' in df_dates.columns:
        valid_starts = df_dates.dropna(subset=['Start date'])
        if len(valid_starts) > 0:
            earliest = valid_starts['Start date'].min()
            latest = valid_starts['Start date'].max()
            
            print(f"Trial start dates:")
            print(f"  Earliest: {earliest.strftime('%B %d, %Y') if pd.notna(earliest) else 'N/A'}")
            print(f"  Latest: {latest.strftime('%B %d, %Y') if pd.notna(latest) else 'N/A'}")
            print(f"  Trials with start dates: {len(valid_starts)}/{len(df)} ({len(valid_starts)/len(df)*100:.1f}%)")
    
    return df_dates

def compare_with_who_data(ctis_sponsors, who_top_sponsors=None):
    """Compare CTIS findings with WHO ICTRP data."""
    print(f"\n=== Comparison: CTIS vs WHO ICTRP ===")
    
    # Sample WHO top sponsors for comparison (from previous analysis)
    who_top_10 = [
        "Eli Lilly and Company", "Wyeth is now a wholly owned subsidiary of Pfizer",
        "Indiana University", "Massachusetts General Hospital", "Assistance Publique - Hôpitaux de Paris",
        "Washington University School of Medicine", "Xuanwu Hospital, Beijing", 
        "Centre Hospitalier Universitaire de Nice", "Pfizer", "National Institute on Aging (NIA)"
    ]
    
    ctis_top_10 = ctis_sponsors.head(10).index.tolist()
    
    print("CTIS Top 10 vs WHO ICTRP Top 10 Comparison:")
    print("-" * 60)
    print(f"{'CTIS Rank':<5} {'CTIS Sponsor':<30} {'Trials':<8} {'In WHO Top 10?'}")
    print("-" * 60)
    
    overlap_count = 0
    for i, sponsor in enumerate(ctis_top_10, 1):
        count = ctis_sponsors[sponsor]
        # Check for potential matches (accounting for name variations)
        in_who = any(who_sponsor.lower() in sponsor.lower() or 
                    sponsor.lower() in who_sponsor.lower() 
                    for who_sponsor in who_top_10)
        if in_who:
            overlap_count += 1
            status = "✓ Yes"
        else:
            status = "✗ No"
        
        short_sponsor = sponsor[:28] + "..." if len(sponsor) > 28 else sponsor
        print(f"{i:<5} {short_sponsor:<30} {count:<8} {status}")
    
    print(f"\nOverlap Analysis:")
    print(f"Sponsors appearing in both top 10 lists: {overlap_count}/10")
    print(f"Registry-specific sponsors in CTIS: {10 - overlap_count}/10")

def generate_ctis_summary(df, top_sponsors, sponsor_types, phase_counts):
    """Generate comprehensive CTIS summary."""
    print(f"\n" + "="*60)
    print("EU CTIS MULTIPLE SCLEROSIS TRIALS ANALYSIS")
    print("="*60)
    
    total_trials = len(df)
    unique_sponsors = df['Sponsor/Co-Sponsors'].nunique()
    
    print(f"\nKEY FINDINGS:")
    print(f"• Total MS trials in CTIS: {total_trials}")
    print(f"• Unique sponsors: {unique_sponsors}")
    print(f"• Most active sponsor: {top_sponsors.index[0]} ({top_sponsors.iloc[0]} trials)")
    print(f"• Top sponsor represents {(top_sponsors.iloc[0]/total_trials*100):.1f}% of CTIS trials")
    
    print(f"\nSPONSOR TYPE DISTRIBUTION:")
    for stype, count in sponsor_types.items():
        percentage = (count/total_trials*100)
        print(f"• {stype}: {count} trials ({percentage:.1f}%)")
    
    print(f"\nTRIAL CHARACTERISTICS:")
    print(f"• Most common phase: {phase_counts.index[0]} ({phase_counts.iloc[0]} trials)")
    print(f"• Registry focus: European regulatory framework (CTIS)")
    
    print(f"\nDATA COMPARISON:")
    print(f"• CTIS trials: {total_trials} (EU regulatory focus)")
    print(f"• WHO ICTRP trials: 2,482 (global overview)")
    print(f"• Ratio: 1 CTIS trial per {2482/total_trials:.1f} WHO trials")
    
    print("=" * 60)

def main():
    """Run complete CTIS analysis."""
    # Load and analyze CTIS data
    df = load_ctis_data()
    
    # Analyze structure
    sponsor_types = analyze_ctis_structure(df)
    
    # Analyze sponsors
    top_sponsors = analyze_ctis_sponsors(df)
    
    # Analyze trial phases
    phase_counts = analyze_ctis_trial_phases(df)
    
    # Analyze dates
    df_with_dates = analyze_ctis_dates(df)
    
    # Create visualizations
    create_ctis_sponsor_chart(top_sponsors)
    fig_types, sponsor_types = create_ctis_sponsor_type_chart(df)
    
    # Compare with WHO data
    compare_with_who_data(top_sponsors)
    
    # Generate summary
    generate_ctis_summary(df, top_sponsors, sponsor_types, phase_counts)
    
    print(f"\n✅ CTIS analysis completed!")
    print(f"Generated files:")
    print(f"  • charts/ctis_top_sponsors.png")
    print(f"  • charts/ctis_sponsor_types.png")

if __name__ == "__main__":
    main()