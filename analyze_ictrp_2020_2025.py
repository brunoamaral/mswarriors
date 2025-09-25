#!/usr/bin/env python3
"""
WHO ICTRP MS Analysis Script - Recent Period (2020-2025)
Analyzes Multiple Sclerosis clinical trial data from WHO ICTRP
focusing on the recent 2020-2025 timeframe for contemporary insights.
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

def load_and_filter_ictrp_data():
    """
    Load WHO ICTRP data and filter to 2020-2025 timeframe.
    Filter: January 1, 2020 to December 31, 2025
    """
    print("Loading WHO ICTRP data...")
    df = pd.read_excel("data/ICTRP-Results.xlsx")
    print(f"Original dataset: {len(df)} studies")
    
    # 2020-2025 timeframe boundaries
    START_DATE = pd.Timestamp('2020-01-01')
    END_DATE = pd.Timestamp('2025-12-31')
    
    print(f"\nFiltering to recent timeframe:")
    print(f"Start: {START_DATE.strftime('%B %d, %Y')}")
    print(f"End: {END_DATE.strftime('%B %d, %Y')}")
    
    # Convert Date_registration to datetime  
    df['date_registration_dt'] = pd.to_datetime(df['Date_registration'], errors='coerce')
    
    # Count studies before filtering
    studies_with_dates = df['date_registration_dt'].notna().sum()
    print(f"Studies with valid registration dates: {studies_with_dates}/{len(df)} ({studies_with_dates/len(df)*100:.1f}%)")
    
    # Apply 2020-2025 timeframe filter
    mask = (
        (df['date_registration_dt'] >= START_DATE) & 
        (df['date_registration_dt'] <= END_DATE) &
        df['date_registration_dt'].notna()
    )
    
    filtered_df = df[mask].copy()
    
    print(f"After 2020-2025 filter: {len(filtered_df)} studies")
    print(f"Filtered out: {len(df) - len(filtered_df)} studies")
    print(f"Retention rate: {len(filtered_df)/len(df)*100:.1f}%")
    
    # Show date range of filtered data
    if len(filtered_df) > 0:
        min_date = filtered_df['date_registration_dt'].min()
        max_date = filtered_df['date_registration_dt'].max()
        print(f"Filtered date range: {min_date.strftime('%B %d, %Y')} to {max_date.strftime('%B %d, %Y')}")
        print(f"Time span: {(max_date - min_date).days / 365.25:.1f} years")
    
    return filtered_df

def analyze_ictrp_sponsors_2020(df):
    """Analyze sponsor patterns in 2020-2025 WHO ICTRP data."""
    print(f"\n=== WHO ICTRP SPONSOR ANALYSIS (2020-2025) ===")
    print(f"Analyzing {len(df)} recent studies")
    
    # Primary sponsor analysis
    sponsor_counts = df['Primary_sponsor'].value_counts()
    unique_sponsors = df['Primary_sponsor'].nunique()
    missing_sponsors = df['Primary_sponsor'].isna().sum()
    
    print(f"\nPrimary Sponsor Statistics:")
    print(f"• Total unique sponsors: {unique_sponsors}")
    print(f"• Missing sponsor data: {missing_sponsors} ({missing_sponsors/len(df)*100:.1f}%)")
    print(f"• Data completeness: {(1-missing_sponsors/len(df))*100:.1f}%")
    
    print(f"\nTop 10 Primary Sponsors in WHO ICTRP (2020-2025):")
    print("-" * 70)
    for i, (sponsor, count) in enumerate(sponsor_counts.head(10).items(), 1):
        percentage = (count / len(df)) * 100
        print(f"{i:2d}. {sponsor:<45} {count:3d} trials ({percentage:.1f}%)")
    
    # Sponsor concentration analysis
    top_10_total = sponsor_counts.head(10).sum()
    top_10_percentage = (top_10_total / len(df)) * 100
    print(f"\nConcentration Analysis:")
    print(f"• Top 10 sponsors represent: {top_10_total}/{len(df)} studies ({top_10_percentage:.1f}%)")
    print(f"• Sponsor fragmentation: {unique_sponsors} sponsors for {len(df)} studies")
    print(f"• Average trials per sponsor: {len(df)/unique_sponsors:.1f}")
    
    return sponsor_counts

def create_ictrp_sponsor_chart_2020(sponsor_counts, save_path="analysis_2020_2025/charts/ictrp_top_sponsors_2020_2025.png"):
    """Create top sponsors visualization for WHO ICTRP 2020-2025."""
    print("Creating WHO ICTRP top sponsors chart (2020-2025)...")
    
    ensure_output_directory()
    
    # Get top 10 sponsors
    top_sponsors = sponsor_counts.head(10)
    
    # Create horizontal bar chart
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Create bars with color gradient
    colors = sns.color_palette("plasma", len(top_sponsors))
    y_pos = np.arange(len(top_sponsors))
    
    bars = ax.barh(y_pos, top_sponsors.values, color=colors)
    
    # Customize chart
    ax.set_yticks(y_pos)
    ax.set_yticklabels([name[:50] + "..." if len(name) > 50 else name for name in top_sponsors.index])
    ax.invert_yaxis()
    ax.set_xlabel('Number of Clinical Trials', fontweight='bold', fontsize=12)
    ax.set_title('Top 10 Primary Sponsors - WHO ICTRP MS Trials\n(Recent Period: 2020 - 2025)', 
                 fontweight='bold', fontsize=14, pad=20)
    
    # Add value labels on bars
    for bar, count in zip(bars, top_sponsors.values):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                str(count), va='center', fontweight='bold', fontsize=10)
    
    # Add grid for better readability
    ax.grid(axis='x', alpha=0.3)
    ax.set_axisbelow(True)
    
    # Add summary text
    total_studies = sponsor_counts.sum()
    top_10_pct = (top_sponsors.sum() / total_studies) * 100
    textstr = f'Top 10 represent {top_10_pct:.1f}% of {total_studies:,} total studies\nRecent period focus: 2020-2025'
    props = dict(boxstyle='round', facecolor='lightgreen', alpha=0.5)
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=props)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"WHO ICTRP sponsors chart (2020-2025) saved as: {save_path}")
    
    return fig

def analyze_yearly_trends_2020(df):
    """Analyze yearly registration trends in the 2020-2025 period."""
    print(f"\n=== YEARLY TRENDS ANALYSIS (2020-2025) ===")
    
    # Extract year from registration date
    df['registration_year'] = df['date_registration_dt'].dt.year
    
    yearly_counts = df['registration_year'].value_counts().sort_index()
    
    print("Annual MS Trial Registrations (WHO ICTRP):")
    for year, count in yearly_counts.items():
        print(f"  {year}: {count:3d} trials")
    
    # Create yearly trends chart
    fig, ax = plt.subplots(figsize=(12, 8))
    
    years = yearly_counts.index
    counts = yearly_counts.values
    
    # Create bar chart with trend line
    bars = ax.bar(years, counts, color='skyblue', alpha=0.7, edgecolor='navy')
    
    # Add trend line
    z = np.polyfit(years, counts, 1)
    p = np.poly1d(z)
    ax.plot(years, p(years), "r--", linewidth=2, label=f'Trend: {z[0]:+.1f} trials/year')
    
    # Customize chart
    ax.set_xlabel('Registration Year', fontweight='bold', fontsize=12)
    ax.set_ylabel('Number of Trials', fontweight='bold', fontsize=12)
    ax.set_title('Annual MS Trial Registrations - WHO ICTRP\n(Recent Period: 2020-2025)', 
                 fontweight='bold', fontsize=14, pad=20)
    
    # Add value labels on bars
    for bar, count in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                str(count), ha='center', va='bottom', fontweight='bold')
    
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    ax.set_axisbelow(True)
    
    # Set x-axis to show all years
    ax.set_xticks(years)
    
    plt.tight_layout()
    plt.savefig("analysis_2020_2025/charts/ictrp_yearly_trends_2020_2025.png", dpi=300, bbox_inches='tight')
    print("Yearly trends chart saved as: analysis_2020_2025/charts/ictrp_yearly_trends_2020_2025.png")
    
    return yearly_counts

def generate_summary_report_2020(df, sponsor_counts, yearly_counts):
    """Generate comprehensive summary for 2020-2025 period."""
    print(f"\n" + "="*70)
    print("WHO ICTRP MS ANALYSIS SUMMARY (2020-2025)")
    print("="*70)
    
    # Basic stats
    total_studies = len(df)
    unique_sponsors = sponsor_counts.nunique()
    top_sponsor_count = sponsor_counts.iloc[0] if len(sponsor_counts) > 0 else 0
    top_sponsor_name = sponsor_counts.index[0] if len(sponsor_counts) > 0 else "N/A"
    top_sponsor_pct = (top_sponsor_count / total_studies) * 100 if total_studies > 0 else 0
    
    print(f"\n📊 KEY FINDINGS (RECENT PERIOD):")
    print(f"• Total MS studies (2020-2025): {total_studies:,}")
    print(f"• Unique primary sponsors: {unique_sponsors:,}")
    print(f"• Top sponsor: {top_sponsor_name} ({top_sponsor_count} studies, {top_sponsor_pct:.1f}%)")
    print(f"• Sponsor concentration: Top 10 = {sponsor_counts.head(10).sum()/total_studies*100:.1f}%")
    
    # Yearly trends
    if len(yearly_counts) > 1:
        trend_change = yearly_counts.iloc[-1] - yearly_counts.iloc[0]
        avg_annual = yearly_counts.mean()
        print(f"\n📈 TEMPORAL TRENDS:")
        print(f"• Average annual registrations: {avg_annual:.1f}")
        print(f"• Change from 2020 to latest: {trend_change:+d} trials")
        print(f"• Peak year: {yearly_counts.idxmax()} ({yearly_counts.max()} trials)")
        print(f"• Lowest year: {yearly_counts.idxmin()} ({yearly_counts.min()} trials)")
    
    # Timeline context
    print(f"\n📅 TEMPORAL CONTEXT:")
    print(f"• Timeframe: January 1, 2020 - December 31, 2025")
    print(f"• Duration: 6 years (recent period focus)")
    print(f"• Registry: WHO ICTRP (International)")
    print(f"• COVID-19 impact period included")

def main():
    """Run the complete WHO ICTRP 2020-2025 analysis."""
    print("🏥 WHO ICTRP MS Analysis - Recent Period (2020-2025)")
    print("="*60)
    
    try:
        # Load and filter data to 2020-2025
        df = load_and_filter_ictrp_data()
        
        if len(df) == 0:
            print("❌ No studies remain after filtering. Check date ranges.")
            return
        
        # Analyze sponsors
        sponsor_counts = analyze_ictrp_sponsors_2020(df)
        
        # Create sponsor visualization
        create_ictrp_sponsor_chart_2020(sponsor_counts)
        
        # Analyze yearly trends
        yearly_counts = analyze_yearly_trends_2020(df)
        
        # Generate summary
        generate_summary_report_2020(df, sponsor_counts, yearly_counts)
        
        print(f"\n✅ WHO ICTRP analysis (2020-2025) completed!")
        print(f"Generated files:")
        print(f"  • analysis_2020_2025/charts/ictrp_top_sponsors_2020_2025.png")
        print(f"  • analysis_2020_2025/charts/ictrp_yearly_trends_2020_2025.png")
        print(f"\n📝 Focused on recent MS clinical trial landscape!")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        raise

if __name__ == "__main__":
    main()