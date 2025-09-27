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

def create_geographic_distribution_chart(df):
    """Create geographic distribution chart for WHO ICTRP data."""
    print("Creating geographic distribution chart...")
    ensure_output_directory()
    
    # Extract countries from the Countries column
    countries = []
    for countries_str in df['Countries'].dropna():
        if isinstance(countries_str, str):
            # Split by semicolon and clean
            country_list = [c.strip() for c in str(countries_str).split(';')]
            countries.extend(country_list)
    
    if not countries:
        print("No country data available")
        return
    
    # Count countries and get top 15
    country_counts = pd.Series(countries).value_counts().head(15)
    
    fig, ax = plt.subplots(figsize=(14, 10))
    
    colors = sns.color_palette("viridis", len(country_counts))
    y_pos = np.arange(len(country_counts))
    
    bars = ax.barh(y_pos, country_counts.values, color=colors, alpha=0.8, edgecolor='white', linewidth=1)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(country_counts.index, fontweight='bold')
    ax.invert_yaxis()
    ax.set_xlabel('Number of Studies', fontweight='bold', fontsize=12)
    ax.set_title('Geographic Distribution of MS Clinical Trials\n(WHO ICTRP, Top 15 Countries, 2020-2025)', 
                fontweight='bold', fontsize=14, pad=20)
    
    # Add value labels
    for bar, count in zip(bars, country_counts.values):
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                str(count), va='center', fontweight='bold', fontsize=10)
    
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    # Add summary
    total_countries = len(pd.Series(countries).value_counts())
    total_studies = sum(country_counts.values)
    summary_text = f'Showing top 15 of {total_countries} countries\nTotal studies: {total_studies}'
    ax.text(0.02, 0.98, summary_text, transform=ax.transAxes, 
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.8),
            verticalalignment='top', fontweight='bold')
    
    plt.tight_layout()
    output_path = "analysis_2020_2025/charts/ictrp_geographic_distribution_2020_2025.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Geographic distribution chart saved: {output_path}")

def create_phase_distribution_chart(df):
    """Create phase distribution chart for WHO ICTRP data."""
    print("Creating phase distribution chart...")
    ensure_output_directory()
    
    # Analyze Study type column for phase information
    if 'Study_type' not in df.columns:
        print("No study type data available for phase analysis")
        return
    
    # Count study types
    phase_counts = df['Study_type'].value_counts()
    
    # Filter out very small categories (less than 2 studies)
    phase_counts = phase_counts[phase_counts >= 2]
    
    if phase_counts.empty:
        print("No sufficient phase data for visualization")
        return
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    colors = sns.color_palette("Set2", len(phase_counts))
    y_pos = np.arange(len(phase_counts))
    
    bars = ax.barh(y_pos, phase_counts.values, color=colors, alpha=0.8, edgecolor='white', linewidth=1)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(phase_counts.index, fontweight='bold')
    ax.invert_yaxis()
    ax.set_xlabel('Number of Studies', fontweight='bold', fontsize=12)
    ax.set_title('Study Type Distribution\n(WHO ICTRP, 2020-2025)', fontweight='bold', fontsize=14, pad=20)
    
    # Add value labels
    total = phase_counts.sum()
    for bar, count in zip(bars, phase_counts.values):
        percentage = (count / total) * 100
        ax.text(bar.get_width() + total * 0.01, bar.get_y() + bar.get_height()/2,
                f'{count} ({percentage:.1f}%)', va='center', fontweight='bold', fontsize=10)
    
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    plt.tight_layout()
    output_path = "analysis_2020_2025/charts/ictrp_phase_distribution_2020_2025.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Phase distribution chart saved: {output_path}")

def create_recruitment_timeline_chart(df):
    """Create recruitment timeline chart showing registration trends."""
    print("Creating recruitment timeline chart...")
    ensure_output_directory()
    
    # Group by year and month
    df_copy = df.copy()
    df_copy['year'] = df_copy['date_registration_dt'].dt.year
    df_copy['year_month'] = df_copy['date_registration_dt'].dt.to_period('M')
    
    # Remove missing dates
    df_copy = df_copy.dropna(subset=['year_month'])
    
    if df_copy.empty:
        print("No date data available for timeline")
        return
    
    # Monthly counts
    monthly_counts = df_copy['year_month'].value_counts().sort_index()
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Monthly timeline
    monthly_counts.plot(kind='line', ax=ax1, color='#2E86AB', marker='o', markersize=4, linewidth=2)
    ax1.set_title('MS Clinical Trial Registrations Timeline\n(WHO ICTRP, 2020-2025)', 
                  fontweight='bold', fontsize=14, pad=20)
    ax1.set_ylabel('Monthly Registrations', fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.set_axisbelow(True)
    
    # Yearly summary
    yearly_counts = df_copy['year'].value_counts().sort_index()
    bars = ax2.bar(yearly_counts.index, yearly_counts.values, 
                   color='#A23B72', alpha=0.8, edgecolor='white', linewidth=2)
    
    ax2.set_title('Annual Registration Summary', fontweight='bold', fontsize=12)
    ax2.set_ylabel('Annual Registrations', fontweight='bold')
    ax2.set_xlabel('Year', fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    ax2.set_axisbelow(True)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{int(height)}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    output_path = "analysis_2020_2025/charts/ictrp_recruitment_timeline_2020_2025.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Recruitment timeline chart saved: {output_path}")

def create_sponsor_data_completeness_chart(df):
    """Create sponsor data completeness chart."""
    print("Creating sponsor data completeness chart...")
    ensure_output_directory()
    
    # Calculate completeness rates for different fields
    fields = {
        'Primary Sponsor': 'Primary_sponsor',
        'Secondary Sponsors': 'Secondary_sponsor',
        'Funding Source': 'Source_funding',
        'Countries': 'Countries',
        'Study Type': 'Study_type'
    }
    
    completeness_rates = {}
    for field_name, column_name in fields.items():
        if column_name in df.columns:
            rate = (1 - df[column_name].isna().sum() / len(df)) * 100
            completeness_rates[field_name] = rate
    
    if not completeness_rates:
        print("No completeness data available")
        return
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    fields_list = list(completeness_rates.keys())
    rates_list = list(completeness_rates.values())
    
    colors = sns.color_palette("viridis", len(rates_list))
    bars = ax.bar(fields_list, rates_list, color=colors, alpha=0.8, edgecolor='white', linewidth=2)
    
    ax.set_ylabel('Data Completeness (%)', fontweight='bold', fontsize=12)
    ax.set_title('WHO ICTRP Data Completeness by Field\n(2020-2025 Period)', 
                fontweight='bold', fontsize=14, pad=20)
    ax.set_ylim(0, 105)
    
    # Add value labels on bars
    for bar, rate in zip(bars, rates_list):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{rate:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    # Add horizontal reference lines
    ax.axhline(y=100, color='green', linestyle='--', alpha=0.5, label='100% Complete')
    ax.axhline(y=90, color='orange', linestyle='--', alpha=0.5, label='90% Threshold')
    ax.axhline(y=75, color='red', linestyle='--', alpha=0.5, label='75% Threshold')
    
    ax.grid(axis='y', alpha=0.3)
    ax.set_axisbelow(True)
    ax.legend()
    
    # Rotate x-axis labels if needed
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    output_path = "analysis_2020_2025/charts/ictrp_sponsor_data_completeness_2020_2025.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Sponsor data completeness chart saved: {output_path}")

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
        
        # Create additional comprehensive charts
        create_geographic_distribution_chart(df)
        create_phase_distribution_chart(df)
        create_recruitment_timeline_chart(df)
        create_sponsor_data_completeness_chart(df)
        
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