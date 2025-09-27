#!/usr/bin/env python3
"""
Cross-Registry Comparison Charts - 2020-2025 Period
Creates integrated comparison charts combining WHO ICTRP, EU CTIS, and ClinicalTrials.gov data.
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
    return output_dir

def load_all_filtered_data():
    """Load and filter all three datasets to 2020-2025 timeframe."""
    print("Loading all registry datasets for comparison...")
    
    # Load ClinicalTrials.gov data
    print("- Loading ClinicalTrials.gov data...")
    ct_df = pd.read_csv("data/clinicaltrials_ms_20250925.csv")
    ct_df['StudyFirstPostDate_dt'] = pd.to_datetime(ct_df['StudyFirstPostDate'], errors='coerce')
    
    # Load WHO ICTRP data  
    print("- Loading WHO ICTRP data...")
    ictrp_df = pd.read_excel("data/ICTRP-Results.xlsx")
    ictrp_df['Date_registration_dt'] = pd.to_datetime(ictrp_df['Date_registration'], errors='coerce')
    
    # Load EU CTIS data
    print("- Loading EU CTIS data...")
    ctis_df = pd.read_csv("data/CTIS_trials_20250924.csv")
    ctis_df['Decision_date_dt'] = pd.to_datetime(ctis_df['Decision date'], errors='coerce')
    
    # Filter to 2020-2025
    start_date = pd.Timestamp('2020-01-01')
    end_date = pd.Timestamp('2025-12-31')
    
    print(f"\nFiltering to timeframe: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    
    # Apply filters
    ct_filtered = ct_df[
        (ct_df['StudyFirstPostDate_dt'] >= start_date) & 
        (ct_df['StudyFirstPostDate_dt'] <= end_date) &
        ct_df['StudyFirstPostDate_dt'].notna()
    ].copy()
    
    ictrp_filtered = ictrp_df[
        (ictrp_df['Date_registration_dt'] >= start_date) & 
        (ictrp_df['Date_registration_dt'] <= end_date) &
        ictrp_df['Date_registration_dt'].notna()
    ].copy()
    
    ctis_filtered = ctis_df[
        (ctis_df['Decision_date_dt'] >= start_date) & 
        (ctis_df['Decision_date_dt'] <= end_date) &
        ctis_df['Decision_date_dt'].notna()
    ].copy()
    
    print(f"Filtered datasets:")
    print(f"  ClinicalTrials.gov: {len(ct_filtered):,} studies")
    print(f"  WHO ICTRP: {len(ictrp_filtered):,} studies") 
    print(f"  EU CTIS: {len(ctis_filtered):,} studies")
    print(f"  Total: {len(ct_filtered) + len(ictrp_filtered) + len(ctis_filtered):,} studies")
    
    return ct_filtered, ictrp_filtered, ctis_filtered

def create_registry_comparison_chart(ct_df, ictrp_df, ctis_df):
    """Create comprehensive registry comparison chart."""
    print("\nCreating registry comparison chart...")
    ensure_output_directory()
    
    # Registry data
    registries = ['ClinicalTrials.gov', 'WHO ICTRP', 'EU CTIS']
    study_counts = [len(ct_df), len(ictrp_df), len(ctis_df)]
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Bar chart
    bars = ax1.bar(registries, study_counts, color=colors, alpha=0.8, edgecolor='white', linewidth=2)
    ax1.set_ylabel('Number of Studies', fontweight='bold', fontsize=12)
    ax1.set_title('MS Clinical Trials by Registry\n(2020-2025 Period)', fontweight='bold', fontsize=14)
    
    # Add value labels on bars
    for bar, count in zip(bars, study_counts):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
                f'{count:,}', ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    ax1.grid(axis='y', alpha=0.3)
    ax1.set_axisbelow(True)
    
    # Pie chart
    wedges, texts, autotexts = ax2.pie(study_counts, labels=registries, autopct='%1.1f%%',
                                       colors=colors, startangle=90)
    ax2.set_title('Registry Distribution\n(2020-2025 Period)', fontweight='bold', fontsize=14)
    
    # Enhance pie chart text
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(11)
    
    # Add summary statistics
    total_studies = sum(study_counts)
    summary_text = f'Total Studies: {total_studies:,}\nPeriod: 2020-2025 (6 years)\nActive Registries: 3'
    
    plt.figtext(0.02, 0.02, summary_text, fontsize=10, 
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgray', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig("analysis_2020_2025/charts/registry_comparison_2020_2025.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Registry comparison chart saved")

def create_sponsor_type_comparison_chart(ct_df, ctis_df):
    """Create sponsor type comparison between ClinicalTrials.gov and EU CTIS."""
    print("Creating sponsor type comparison chart...")
    
    # ClinicalTrials.gov sponsor classes
    ct_classes = ct_df['LeadSponsorClass'].value_counts()
    
    # Map to standardized categories
    ct_mapped = {
        'Industry': ct_classes.get('INDUSTRY', 0),
        'Academic/Other': ct_classes.get('OTHER', 0),
        'Government': ct_classes.get('NIH', 0) + ct_classes.get('OTHER_GOV', 0) + ct_classes.get('FED', 0),
        'Network': ct_classes.get('NETWORK', 0)
    }
    
    # EU CTIS sponsor types (simplified)
    ctis_types = ctis_df['Sponsor type'].value_counts()
    ctis_mapped = {
        'Industry': ctis_types.get('Pharmaceutical company', 0),
        'Academic/Other': (ctis_types.get('Hospital/Clinic/Other health care facility', 0) + 
                          ctis_types.get('University/Research institute', 0)),
        'Government': 0,  # Not clearly distinguished in CTIS
        'Network': 0
    }
    
    # Create comparison
    categories = list(ct_mapped.keys())
    ct_values = [ct_mapped[cat] for cat in categories]
    ctis_values = [ctis_mapped[cat] for cat in categories]
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    x = np.arange(len(categories))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, ct_values, width, label='ClinicalTrials.gov', color='#1f77b4', alpha=0.8)
    bars2 = ax.bar(x + width/2, ctis_values, width, label='EU CTIS', color='#2ca02c', alpha=0.8)
    
    ax.set_xlabel('Sponsor Type', fontweight='bold', fontsize=12)
    ax.set_ylabel('Number of Studies', fontweight='bold', fontsize=12)
    ax.set_title('Sponsor Type Comparison\n(ClinicalTrials.gov vs EU CTIS, 2020-2025)', fontweight='bold', fontsize=14, pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                        f'{int(height)}', ha='center', va='bottom', fontweight='bold')
    
    ax.grid(axis='y', alpha=0.3)
    ax.set_axisbelow(True)
    
    plt.tight_layout()
    plt.savefig("analysis_2020_2025/charts/sponsor_type_comparison_2020_2025.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Sponsor type comparison chart saved")

def create_combined_geographic_chart(ct_df, ictrp_df):
    """Create combined geographic distribution chart."""
    print("Creating combined geographic distribution chart...")
    
    # Analyze ClinicalTrials.gov countries
    ct_countries = []
    if 'LocationCountry' in ct_df.columns:
        for countries_str in ct_df['LocationCountry'].dropna():
            if isinstance(countries_str, str):
                countries = [c.strip() for c in str(countries_str).split(',')]
                ct_countries.extend(countries)
    
    # Analyze WHO ICTRP countries
    ictrp_countries = []
    if 'Countries' in ictrp_df.columns:
        for countries_str in ictrp_df['Countries'].dropna():
            if isinstance(countries_str, str):
                countries = [c.strip() for c in str(countries_str).split(';')]
                ictrp_countries.extend(countries)
    
    # Combine and count
    all_countries = ct_countries + ictrp_countries
    country_counts = pd.Series(all_countries).value_counts()
    
    # Get top 15 countries
    top_countries = country_counts.head(15)
    
    fig, ax = plt.subplots(figsize=(14, 10))
    
    colors = sns.color_palette("viridis", len(top_countries))
    y_pos = np.arange(len(top_countries))
    
    bars = ax.barh(y_pos, top_countries.values, color=colors, alpha=0.8, edgecolor='white', linewidth=1)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(top_countries.index, fontweight='bold')
    ax.invert_yaxis()
    ax.set_xlabel('Number of Studies', fontweight='bold', fontsize=12)
    ax.set_title('Combined Geographic Distribution of MS Clinical Trials\n(ClinicalTrials.gov + WHO ICTRP, Top 15 Countries, 2020-2025)', fontweight='bold', fontsize=14, pad=20)
    
    # Add value labels
    for bar, count in zip(bars, top_countries.values):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                str(count), va='center', fontweight='bold', fontsize=10)
    
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    # Add summary
    total_countries = len(country_counts)
    total_studies = sum(top_countries.values)
    summary_text = f'Showing top 15 of {total_countries} countries\nCombined studies: {total_studies:,}'
    ax.text(0.02, 0.98, summary_text, transform=ax.transAxes, 
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.8),
            verticalalignment='top', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig("analysis_2020_2025/charts/geographic_distribution_2020_2025.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Combined geographic distribution chart saved")

def create_combined_sponsor_data_completeness_chart(ct_df, ictrp_df, ctis_df):
    """Create combined sponsor data completeness comparison."""
    print("Creating combined sponsor data completeness chart...")
    
    # Calculate completeness rates
    registries = ['ClinicalTrials.gov', 'WHO ICTRP', 'EU CTIS']
    
    # ClinicalTrials.gov
    ct_completeness = (1 - ct_df['LeadSponsorName'].isna().sum() / len(ct_df)) * 100
    
    # WHO ICTRP
    ictrp_completeness = (1 - ictrp_df['Primary_sponsor'].isna().sum() / len(ictrp_df)) * 100
    
    # EU CTIS
    ctis_completeness = (1 - ctis_df['Sponsor/Co-Sponsors'].isna().sum() / len(ctis_df)) * 100
    
    completeness_rates = [ct_completeness, ictrp_completeness, ctis_completeness]
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    bars = ax.bar(registries, completeness_rates, color=colors, alpha=0.8, edgecolor='white', linewidth=2)
    
    ax.set_ylabel('Sponsor Data Completeness (%)', fontweight='bold', fontsize=12)
    ax.set_title('Sponsor Data Completeness by Registry\n(2020-2025 Period)', fontweight='bold', fontsize=14, pad=20)
    ax.set_ylim(0, 105)
    
    # Add value labels on bars
    for bar, rate in zip(bars, completeness_rates):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{rate:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    # Add horizontal reference lines
    ax.axhline(y=100, color='green', linestyle='--', alpha=0.5, label='100% Complete')
    ax.axhline(y=90, color='orange', linestyle='--', alpha=0.5, label='90% Threshold')
    
    ax.grid(axis='y', alpha=0.3)
    ax.set_axisbelow(True)
    ax.legend()
    
    plt.tight_layout()
    plt.savefig("analysis_2020_2025/charts/sponsor_data_completeness_2020_2025.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Combined sponsor data completeness chart saved")

def main():
    """Generate cross-registry comparison charts for 2020-2025 period."""
    print("🎨 Creating Cross-Registry Comparison Charts (2020-2025)")
    print("="*65)
    
    try:
        # Load filtered datasets
        ct_df, ictrp_df, ctis_df = load_all_filtered_data()
        
        # Create comprehensive comparison charts
        create_registry_comparison_chart(ct_df, ictrp_df, ctis_df)
        create_sponsor_type_comparison_chart(ct_df, ctis_df)
        create_combined_geographic_chart(ct_df, ictrp_df)
        create_combined_sponsor_data_completeness_chart(ct_df, ictrp_df, ctis_df)
        
        print(f"\n✅ Cross-registry comparison charts completed!")
        print(f"All charts saved to: analysis_2020_2025/charts/")
        
        # Show final count
        chart_count = len([f for f in os.listdir("analysis_2020_2025/charts") if f.endswith('.png')])
        print(f"Total charts in 2020-2025 analysis: {chart_count}")
        
    except Exception as e:
        print(f"❌ Error during chart generation: {e}")
        raise

if __name__ == "__main__":
    main()