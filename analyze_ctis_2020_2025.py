#!/usr/bin/env python3
"""
EU CTIS MS Analysis Script - Recent Period (2020-2025)
Analyzes Multiple Sclerosis clinical trial data from EU CTIS
focusing on the recent 2020-2025 timeframe (though CTIS started in 2023).
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from datetime import datetime

def ensure_output_directory():
    """Create output directory if it doesn't exist."""
    output_dir = "analysis_2020_2025/charts"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created {output_dir} directory")
    return output_dir

def load_and_filter_ctis_data():
    """
    Load EU CTIS data and filter to 2020-2025 timeframe.
    Note: CTIS only started in 2023, so we'll only have 2023-2025 data.
    Filter: January 1, 2020 to December 31, 2025
    """
    print("Loading EU CTIS data...")
    df = pd.read_csv("data/CTIS_trials_20250924.csv")
    print(f"Original dataset: {len(df)} studies")
    
    # 2020-2025 timeframe boundaries
    START_DATE = pd.Timestamp('2020-01-01')
    END_DATE = pd.Timestamp('2025-12-31')
    
    print(f"\nFiltering to recent timeframe:")
    print(f"Start: {START_DATE.strftime('%B %d, %Y')}")
    print(f"End: {END_DATE.strftime('%B %d, %Y')}")
    print(f"Note: EU CTIS only started in 2023, so effective range is 2023-2025")
    
    # Convert Decision date to datetime (this represents when the trial was approved/decided)
    df['application_date_dt'] = pd.to_datetime(df['Decision date'], errors='coerce')
    
    # Count studies before filtering
    studies_with_dates = df['application_date_dt'].notna().sum()
    print(f"Studies with valid application dates: {studies_with_dates}/{len(df)} ({studies_with_dates/len(df)*100:.1f}%)")
    
    # Apply 2020-2025 timeframe filter (effectively 2023-2025 for CTIS)
    mask = (
        (df['application_date_dt'] >= START_DATE) & 
        (df['application_date_dt'] <= END_DATE) &
        df['application_date_dt'].notna()
    )
    
    filtered_df = df[mask].copy()
    
    print(f"After 2020-2025 filter: {len(filtered_df)} studies")
    print(f"Filtered out: {len(df) - len(filtered_df)} studies")
    print(f"Retention rate: {len(filtered_df)/len(df)*100:.1f}%")
    
    # Show date range of filtered data
    if len(filtered_df) > 0:
        min_date = filtered_df['application_date_dt'].min()
        max_date = filtered_df['application_date_dt'].max()
        print(f"Filtered date range: {min_date.strftime('%B %d, %Y')} to {max_date.strftime('%B %d, %Y')}")
        print(f"Time span: {(max_date - min_date).days / 365.25:.1f} years")
    
    return filtered_df

def analyze_ctis_sponsors_2020(df):
    """Analyze sponsor patterns in 2020-2025 EU CTIS data."""
    print(f"\n=== EU CTIS SPONSOR ANALYSIS (2020-2025) ===")
    print(f"Analyzing {len(df)} recent studies")
    
    # Group small sponsor types to reduce clutter
    def group_sponsor_type(sponsor_type):
        """Group small sponsor types for cleaner visualization."""
        if pd.isna(sponsor_type):
            return 'Unknown'
        
        sponsor_type = str(sponsor_type).strip()
        
        # Major categories (keep separate)
        major_categories = {
            'Commercial sponsor': 'Commercial',
            'Non-commercial sponsor': 'Academic/Non-commercial'
        }
        
        # Return grouped category or original if major
        return major_categories.get(sponsor_type, 'Other/Mixed')

    # Apply grouping
    df['grouped_sponsor_type'] = df['Sponsor type'].apply(group_sponsor_type)
    
    # Sponsor type analysis
    sponsor_type_counts = df['grouped_sponsor_type'].value_counts()
    unique_types = df['grouped_sponsor_type'].nunique()
    
    print(f"\nSponsor Type Statistics:")
    print(f"• Total sponsor types (grouped): {unique_types}")
    
    print(f"\nSponsor Type Distribution in EU CTIS (2020-2025):")
    print("-" * 70)
    for i, (stype, count) in enumerate(sponsor_type_counts.items(), 1):
        percentage = (count / len(df)) * 100
        print(f"{i:2d}. {stype:<35} {count:3d} trials ({percentage:.1f}%)")
    
    # Individual sponsor analysis (top organizations)
    sponsor_counts = df['Sponsor/Co-Sponsors'].value_counts()
    unique_sponsors = df['Sponsor/Co-Sponsors'].nunique()
    missing_sponsors = df['Sponsor/Co-Sponsors'].isna().sum()
    
    print(f"\nIndividual Sponsor Statistics:")
    print(f"• Total unique sponsors: {unique_sponsors}")
    print(f"• Missing sponsor data: {missing_sponsors} ({missing_sponsors/len(df)*100:.1f}%)")
    
    if len(sponsor_counts) > 0:
        print(f"\nTop 10 Individual Sponsors in EU CTIS (2020-2025):")
        print("-" * 70)
        for i, (sponsor, count) in enumerate(sponsor_counts.head(10).items(), 1):
            percentage = (count / len(df)) * 100
            print(f"{i:2d}. {sponsor:<45} {count:3d} trials ({percentage:.1f}%)")
    
    return sponsor_type_counts, sponsor_counts

def create_ctis_sponsor_charts_2020(sponsor_type_counts, sponsor_counts):
    """Create sponsor visualizations for EU CTIS 2020-2025."""
    print("Creating EU CTIS sponsor charts (2020-2025)...")
    
    ensure_output_directory()
    
    # 1. Sponsor Type Distribution (Bar Chart)
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Sort by count for better visualization
    sorted_types = sponsor_type_counts.sort_values(ascending=True)
    
    colors = sns.color_palette("viridis", len(sorted_types))
    y_pos = np.arange(len(sorted_types))
    
    bars = ax.barh(y_pos, sorted_types.values, color=colors, alpha=0.8, edgecolor='white', linewidth=1)
    
    # Customize chart
    ax.set_yticks(y_pos)
    ax.set_yticklabels(sorted_types.index, fontsize=11, fontweight='bold')
    ax.set_xlabel('Number of Clinical Trials', fontweight='bold', fontsize=12)
    ax.set_title('Sponsor Type Distribution - EU CTIS MS Trials\n(Recent Period: 2020-2025, effectively 2023-2025)', 
                 fontweight='bold', fontsize=14, pad=20)
    
    # Add value labels on bars with percentages
    total = sponsor_type_counts.sum()
    for bar, count in zip(bars, sorted_types.values):
        percentage = (count / total) * 100
        ax.text(bar.get_width() + total * 0.01, bar.get_y() + bar.get_height()/2,
                f'{count} ({percentage:.1f}%)', va='center', fontweight='bold', fontsize=11)
    
    # Add grid for better readability
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    # Add summary
    commercial_pct = (sponsor_type_counts.get('Commercial', 0) / total) * 100
    academic_pct = (sponsor_type_counts.get('Academic/Non-commercial', 0) / total) * 100
    
    summary_text = (f'Summary (2020-2025 timeframe):\n'
                   f'• Commercial: {commercial_pct:.1f}%\n'
                   f'• Academic/Non-commercial: {academic_pct:.1f}%\n'
                   f'• Total Studies: {total}')
    
    ax.text(0.02, 0.98, summary_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.4", facecolor='lightblue', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig("analysis_2020_2025/charts/ctis_sponsor_types_2020_2025.png", dpi=300, bbox_inches='tight')
    print("EU CTIS sponsor types chart saved as: analysis_2020_2025/charts/ctis_sponsor_types_2020_2025.png")
    
    # 2. Top Individual Sponsors (if we have enough data)
    if len(sponsor_counts) > 0:
        fig, ax = plt.subplots(figsize=(14, 10))
        
        # Get top sponsors (max 10 or all if fewer)
        top_sponsors = sponsor_counts.head(min(10, len(sponsor_counts)))
        
        colors = sns.color_palette("plasma", len(top_sponsors))
        y_pos = np.arange(len(top_sponsors))
        
        bars = ax.barh(y_pos, top_sponsors.values, color=colors)
        
        # Customize chart
        ax.set_yticks(y_pos)
        ax.set_yticklabels([name[:50] + "..." if len(name) > 50 else name for name in top_sponsors.index])
        ax.invert_yaxis()
        ax.set_xlabel('Number of Clinical Trials', fontweight='bold', fontsize=12)
        ax.set_title('Top Individual Sponsors - EU CTIS MS Trials\n(Recent Period: 2020-2025, effectively 2023-2025)', 
                     fontweight='bold', fontsize=14, pad=20)
        
        # Add value labels on bars
        for bar, count in zip(bars, top_sponsors.values):
            ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
                    str(count), va='center', fontweight='bold', fontsize=10)
        
        # Add grid for better readability
        ax.grid(axis='x', alpha=0.3)
        ax.set_axisbelow(True)
        
        # Add summary text
        total_studies = sponsor_counts.sum()
        top_pct = (top_sponsors.sum() / total_studies) * 100
        textstr = f'Top {len(top_sponsors)} represent {top_pct:.1f}% of {total_studies} total studies\nEU CTIS: 2023-2025 active period'
        props = dict(boxstyle='round', facecolor='lightcoral', alpha=0.5)
        ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=10,
                verticalalignment='top', bbox=props)
        
        plt.tight_layout()
        plt.savefig("analysis_2020_2025/charts/ctis_top_sponsors_2020_2025.png", dpi=300, bbox_inches='tight')
        print("EU CTIS top sponsors chart saved as: analysis_2020_2025/charts/ctis_top_sponsors_2020_2025.png")

def analyze_yearly_trends_2020(df):
    """Analyze yearly application trends in the 2020-2025 period."""
    print(f"\n=== YEARLY TRENDS ANALYSIS (2020-2025) ===")
    
    # Extract year from application date
    df['application_year'] = df['application_date_dt'].dt.year
    
    yearly_counts = df['application_year'].value_counts().sort_index()
    
    print("Annual MS Trial Applications (EU CTIS):")
    for year, count in yearly_counts.items():
        print(f"  {year}: {count:3d} trials")
    
    # Create yearly trends chart
    fig, ax = plt.subplots(figsize=(12, 8))
    
    years = yearly_counts.index
    counts = yearly_counts.values
    
    # Create bar chart with trend line (if we have multiple years)
    bars = ax.bar(years, counts, color='coral', alpha=0.7, edgecolor='darkred')
    
    if len(years) > 1:
        # Add trend line
        z = np.polyfit(years, counts, 1)
        p = np.poly1d(z)
        ax.plot(years, p(years), "r--", linewidth=2, label=f'Trend: {z[0]:+.1f} trials/year')
        ax.legend()
    
    # Customize chart
    ax.set_xlabel('Application Year', fontweight='bold', fontsize=12)
    ax.set_ylabel('Number of Trials', fontweight='bold', fontsize=12)
    ax.set_title('Annual MS Trial Applications - EU CTIS\n(Recent Period: 2020-2025, effectively 2023-2025)', 
                 fontweight='bold', fontsize=14, pad=20)
    
    # Add value labels on bars
    for bar, count in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                str(count), ha='center', va='bottom', fontweight='bold')
    
    ax.grid(axis='y', alpha=0.3)
    ax.set_axisbelow(True)
    
    # Set x-axis to show all years
    ax.set_xticks(years)
    
    # Add note about CTIS start date
    ax.text(0.02, 0.95, 'Note: EU CTIS launched in Jan 2023', 
            transform=ax.transAxes, fontsize=10, style='italic',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='yellow', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig("analysis_2020_2025/charts/ctis_yearly_trends_2020_2025.png", dpi=300, bbox_inches='tight')
    print("Yearly trends chart saved as: analysis_2020_2025/charts/ctis_yearly_trends_2020_2025.png")
    
    return yearly_counts

def generate_summary_report_2020(df, sponsor_type_counts, sponsor_counts, yearly_counts):
    """Generate comprehensive summary for 2020-2025 period."""
    print(f"\n" + "="*70)
    print("EU CTIS MS ANALYSIS SUMMARY (2020-2025)")
    print("="*70)
    
    # Basic stats
    total_studies = len(df)
    unique_sponsors = sponsor_counts.nunique()
    
    print(f"\n📊 KEY FINDINGS (RECENT PERIOD):")
    print(f"• Total MS studies (2020-2025): {total_studies:,}")
    print(f"• Unique sponsors: {unique_sponsors:,}")
    print(f"• Registry operational period: 2023-2025 (CTIS launch)")
    
    # Sponsor type breakdown
    commercial_count = sponsor_type_counts.get('Commercial', 0)
    academic_count = sponsor_type_counts.get('Academic/Non-commercial', 0)
    commercial_pct = (commercial_count / total_studies) * 100 if total_studies > 0 else 0
    academic_pct = (academic_count / total_studies) * 100 if total_studies > 0 else 0
    
    print(f"\n🏢 SPONSOR COMPOSITION:")
    print(f"• Commercial sponsors: {commercial_count} studies ({commercial_pct:.1f}%)")
    print(f"• Academic/Non-commercial: {academic_count} studies ({academic_pct:.1f}%)")
    
    # Top sponsor
    if len(sponsor_counts) > 0:
        top_sponsor_count = sponsor_counts.iloc[0]
        top_sponsor_name = sponsor_counts.index[0]
        top_sponsor_pct = (top_sponsor_count / total_studies) * 100
        print(f"• Top sponsor: {top_sponsor_name} ({top_sponsor_count} studies, {top_sponsor_pct:.1f}%)")
    
    # Yearly trends
    if len(yearly_counts) > 0:
        peak_year = yearly_counts.idxmax()
        peak_count = yearly_counts.max()
        avg_annual = yearly_counts.mean()
        
        print(f"\n📈 TEMPORAL TRENDS:")
        print(f"• Average annual applications: {avg_annual:.1f}")
        print(f"• Peak year: {peak_year} ({peak_count} trials)")
        
        if len(yearly_counts) > 1:
            trend_change = yearly_counts.iloc[-1] - yearly_counts.iloc[0]
            print(f"• Change from first to latest year: {trend_change:+d} trials")
    
    # Timeline context
    print(f"\n📅 TEMPORAL CONTEXT:")
    print(f"• Requested timeframe: January 1, 2020 - December 31, 2025")
    print(f"• Actual data period: 2023-2025 (EU CTIS operational)")
    print(f"• Registry: EU CTIS (European Union)")
    print(f"• Note: Newest of the three registries analyzed")

def main():
    """Run the complete EU CTIS 2020-2025 analysis."""
    print("🏥 EU CTIS MS Analysis - Recent Period (2020-2025)")
    print("="*60)
    
    try:
        # Load and filter data to 2020-2025
        df = load_and_filter_ctis_data()
        
        if len(df) == 0:
            print("❌ No studies remain after filtering.")
            print("Note: EU CTIS only started in 2023, so no data before that.")
            return
        
        # Analyze sponsors
        sponsor_type_counts, sponsor_counts = analyze_ctis_sponsors_2020(df)
        
        # Create sponsor visualizations
        create_ctis_sponsor_charts_2020(sponsor_type_counts, sponsor_counts)
        
        # Analyze yearly trends
        yearly_counts = analyze_yearly_trends_2020(df)
        
        # Generate summary
        generate_summary_report_2020(df, sponsor_type_counts, sponsor_counts, yearly_counts)
        
        print(f"\n✅ EU CTIS analysis (2020-2025) completed!")
        print(f"Generated files:")
        print(f"  • analysis_2020_2025/charts/ctis_sponsor_types_2020_2025.png")
        print(f"  • analysis_2020_2025/charts/ctis_top_sponsors_2020_2025.png")
        print(f"  • analysis_2020_2025/charts/ctis_yearly_trends_2020_2025.png")
        print(f"\n📝 Focused on EU CTIS operational period!")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        raise

if __name__ == "__main__":
    main()