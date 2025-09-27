#!/usr/bin/env python3
"""
ClinicalTrials.gov MS Analysis Script
Analyzes Multiple Sclerosis clinical trial data from ClinicalTrials.gov
following the same timeframe as WHO ICTRP (Feb 2001 - Dec 2025) for fair comparison.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from datetime import datetime, date

def ensure_charts_directory():
    """Create charts directory if it doesn't exist."""
    charts_dir = "charts"
    if not os.path.exists(charts_dir):
        os.makedirs(charts_dir)
        print(f"Created {charts_dir} directory")
    return charts_dir

def load_and_filter_clinicaltrials_data():
    """
    Load ClinicalTrials.gov data and filter to WHO ICTRP timeframe.
    Filter: Feb 4, 2001 to Dec 5, 2025 (matching WHO ICTRP exactly)
    """
    print("Loading ClinicalTrials.gov data...")
    df = pd.read_csv("data/clinicaltrials_ms_20250925.csv")
    print(f"Original dataset: {len(df)} studies")
    
    # WHO ICTRP timeframe boundaries
    WHO_START_DATE = pd.Timestamp('2001-02-04')  # Exact WHO ICTRP start
    WHO_END_DATE = pd.Timestamp('2025-12-05')    # Exact WHO ICTRP end
    
    print(f"\nFiltering to WHO ICTRP timeframe:")
    print(f"Start: {WHO_START_DATE.strftime('%B %d, %Y')}")
    print(f"End: {WHO_END_DATE.strftime('%B %d, %Y')}")
    
    # Convert StudyFirstPostDate to datetime for filtering
    df['StudyFirstPostDate_dt'] = pd.to_datetime(df['StudyFirstPostDate'], errors='coerce')
    
    # Count studies before filtering
    studies_with_dates = df['StudyFirstPostDate_dt'].notna().sum()
    print(f"Studies with valid registration dates: {studies_with_dates}/{len(df)} ({studies_with_dates/len(df)*100:.1f}%)")
    
    # Apply WHO ICTRP timeframe filter
    mask = (
        (df['StudyFirstPostDate_dt'] >= WHO_START_DATE) & 
        (df['StudyFirstPostDate_dt'] <= WHO_END_DATE) &
        df['StudyFirstPostDate_dt'].notna()
    )
    
    filtered_df = df[mask].copy()
    
    print(f"After WHO timeframe filter: {len(filtered_df)} studies")
    print(f"Filtered out: {len(df) - len(filtered_df)} studies")
    print(f"Retention rate: {len(filtered_df)/len(df)*100:.1f}%")
    
    # Show date range of filtered data
    if len(filtered_df) > 0:
        min_date = filtered_df['StudyFirstPostDate_dt'].min()
        max_date = filtered_df['StudyFirstPostDate_dt'].max()
        print(f"Filtered date range: {min_date.strftime('%B %d, %Y')} to {max_date.strftime('%B %d, %Y')}")
        print(f"Time span: {(max_date - min_date).days / 365.25:.1f} years")
    
    return filtered_df

def analyze_clinicaltrials_sponsors(df):
    """Analyze sponsor patterns in filtered ClinicalTrials.gov data."""
    print(f"\n=== CLINICALTRIALS.GOV SPONSOR ANALYSIS ===")
    print(f"Analyzing {len(df)} studies (WHO ICTRP timeframe)")
    
    # Lead sponsor analysis
    sponsor_counts = df['LeadSponsorName'].value_counts()
    unique_sponsors = df['LeadSponsorName'].nunique()
    missing_sponsors = df['LeadSponsorName'].isna().sum()
    
    print(f"\nLead Sponsor Statistics:")
    print(f"• Total unique sponsors: {unique_sponsors}")
    print(f"• Missing sponsor data: {missing_sponsors} ({missing_sponsors/len(df)*100:.1f}%)")
    print(f"• Data completeness: {(1-missing_sponsors/len(df))*100:.1f}%")
    
    print(f"\nTop 10 Lead Sponsors in ClinicalTrials.gov:")
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

def create_clinicaltrials_sponsor_chart(sponsor_counts, save_path="charts/clinicaltrials_top_sponsors.png"):
    """Create top sponsors visualization for ClinicalTrials.gov."""
    print("Creating ClinicalTrials.gov top sponsors chart...")
    
    ensure_charts_directory()
    
    # Get top 10 sponsors
    top_sponsors = sponsor_counts.head(10)
    
    # Create horizontal bar chart
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Create bars with color gradient
    colors = sns.color_palette("viridis", len(top_sponsors))
    y_pos = np.arange(len(top_sponsors))
    
    bars = ax.barh(y_pos, top_sponsors.values, color=colors)
    
    # Customize chart
    ax.set_yticks(y_pos)
    ax.set_yticklabels([name[:50] + "..." if len(name) > 50 else name for name in top_sponsors.index])
    ax.invert_yaxis()
    ax.set_xlabel('Number of Clinical Trials', fontweight='bold', fontsize=12)
    ax.set_title('Top 10 Sponsors - ClinicalTrials.gov MS Trials\n(WHO ICTRP Timeframe: Feb 2001 - Dec 2025)', 
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
    textstr = f'Top 10 represent {top_10_pct:.1f}% of {total_studies:,} total studies\nTimeframe matches WHO ICTRP for comparison'
    props = dict(boxstyle='round', facecolor='lightblue', alpha=0.5)
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=props)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"ClinicalTrials.gov sponsors chart saved as: {save_path}")
    
    return fig

def analyze_sponsor_classes(df):
    """Analyze sponsor class distribution."""
    print(f"\n=== SPONSOR CLASS ANALYSIS ===")
    
    class_counts = df['LeadSponsorClass'].value_counts()
    
    print(f"Sponsor Class Distribution:")
    for sclass, count in class_counts.items():
        percentage = (count / len(df)) * 100
        print(f"  {sclass:<15} {count:4d} studies ({percentage:.1f}%)")
    
    return class_counts

def create_sponsor_class_chart(class_counts, save_path="charts/clinicaltrials_sponsor_classes.png"):
    """Create sponsor class distribution chart using horizontal bar chart for better readability."""
    print("Creating ClinicalTrials.gov sponsor class chart...")
    
    ensure_charts_directory()
    
    # Group small categories to reduce clutter
    total = class_counts.sum()
    
    # Map class codes to readable names
    class_name_map = {
        'OTHER': 'Academic/Other',
        'INDUSTRY': 'Industry', 
        'NIH': 'NIH',
        'OTHER_GOV': 'Other Government',
        'FED': 'Federal',
        'NETWORK': 'Network',
        'INDIV': 'Individual'
    }
    
    # Separate major categories (>=1%) from minor ones
    major_categories = {}
    minor_total = 0
    minor_details = []
    
    for class_code, count in class_counts.items():
        percentage = (count / total) * 100
        readable_name = class_name_map.get(class_code, class_code)
        
        if percentage >= 1.0:  # Major categories
            major_categories[readable_name] = count
        else:  # Minor categories - group them
            minor_total += count
            minor_details.append(f"{readable_name} ({count})")
    
    # Add grouped minor categories if any
    if minor_total > 0:
        minor_label = f"Other Categories\n({', '.join(minor_details[:3])}{'...' if len(minor_details) > 3 else ''})"
        major_categories[minor_label] = minor_total
    
    # Create horizontal bar chart for better readability
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Sort by count for better visualization
    sorted_categories = dict(sorted(major_categories.items(), key=lambda x: x[1], reverse=True))
    
    categories = list(sorted_categories.keys())
    counts = list(sorted_categories.values())
    
    # Create horizontal bars with color gradient
    colors = sns.color_palette("viridis", len(categories))
    y_pos = np.arange(len(categories))
    
    bars = ax.barh(y_pos, counts, color=colors, alpha=0.8, edgecolor='white', linewidth=1)
    
    # Customize chart
    ax.set_yticks(y_pos)
    ax.set_yticklabels(categories, fontsize=11, fontweight='bold')
    ax.invert_yaxis()
    ax.set_xlabel('Number of Clinical Trials', fontweight='bold', fontsize=12)
    ax.set_title('Sponsor Class Distribution - ClinicalTrials.gov MS Trials\n(WHO ICTRP Timeframe: Feb 2001 - Dec 2025)', 
                 fontweight='bold', fontsize=14, pad=20)
    
    # Add value labels on bars with percentages
    for i, (bar, count) in enumerate(zip(bars, counts)):
        percentage = (count / total) * 100
        ax.text(bar.get_width() + total * 0.01, bar.get_y() + bar.get_height()/2,
                f'{count:,} ({percentage:.1f}%)', va='center', fontweight='bold', fontsize=11)
    
    # Add grid for better readability
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    # Add summary statistics box
    industry_count = class_counts.get('INDUSTRY', 0)
    other_count = class_counts.get('OTHER', 0)
    govt_count = class_counts.get('NIH', 0) + class_counts.get('OTHER_GOV', 0) + class_counts.get('FED', 0)
    
    industry_pct = (industry_count / total) * 100
    other_pct = (other_count / total) * 100
    govt_pct = (govt_count / total) * 100
    
    summary_text = (f'Summary Statistics:\n'
                   f'• Industry: {industry_pct:.1f}% ({industry_count:,} studies)\n'
                   f'• Academic/Other: {other_pct:.1f}% ({other_count:,} studies)\n'
                   f'• Government (All): {govt_pct:.1f}% ({govt_count} studies)\n'
                   f'• Total Studies: {total:,}')
    
    ax.text(0.02, 0.98, summary_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.4", facecolor='lightblue', alpha=0.8))
    
    # Set x-axis limit to accommodate labels
    ax.set_xlim(0, max(counts) * 1.25)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"ClinicalTrials.gov sponsor class chart saved as: {save_path}")
    
    return fig

def compare_with_who_ictrp(ct_sponsors):
    """Compare ClinicalTrials.gov findings with WHO ICTRP."""
    print(f"\n=== COMPARISON: CLINICALTRIALS.GOV vs WHO ICTRP ===")
    
    # WHO ICTRP top sponsors (from previous analysis)
    who_top_sponsors = [
        "Eli Lilly and Company",
        "Wyeth (now Pfizer subsidiary)", 
        "Indiana University",
        "Massachusetts General Hospital",
        "Assistance Publique - Hôpitaux de Paris",
        "Washington University School of Medicine",
        "Xuanwu Hospital, Beijing",
        "Centre Hospitalier Universitaire de Nice", 
        "Pfizer",
        "National Institute on Aging (NIA)"
    ]
    
    ct_top_10 = ct_sponsors.head(10).index.tolist()
    
    print("Registry Comparison (Same Timeframe: Feb 2001 - Dec 2025):")
    print("-" * 80)
    print(f"{'Rank':<4} {'ClinicalTrials.gov Sponsor':<40} {'Count':<6} {'In WHO Top 10?'}")
    print("-" * 80)
    
    overlap_count = 0
    for i, sponsor in enumerate(ct_top_10, 1):
        count = ct_sponsors[sponsor]
        
        # Check for potential matches (accounting for name variations)
        potential_match = False
        for who_sponsor in who_top_sponsors:
            # Simple matching logic - can be refined
            if (sponsor.lower() in who_sponsor.lower() or 
                who_sponsor.lower() in sponsor.lower() or
                any(word in who_sponsor.lower() for word in sponsor.lower().split() if len(word) > 3)):
                potential_match = True
                break
        
        if potential_match:
            overlap_count += 1
            status = "✓ Possible"
        else:
            status = "✗ No"
        
        short_sponsor = sponsor[:38] + "..." if len(sponsor) > 38 else sponsor
        print(f"{i:<4} {short_sponsor:<40} {count:<6} {status}")
    
    print(f"\nCross-Registry Analysis (Same Timeframe):")
    print(f"• Potential overlaps in top 10: {overlap_count}/10")
    print(f"• Registry-specific patterns: {10 - overlap_count}/10")
    print(f"• This suggests different sponsor ecosystems despite same timeframe")

def generate_summary_report(df, sponsor_counts, class_counts):
    """Generate comprehensive summary."""
    print(f"\n" + "="*70)
    print("CLINICALTRIALS.GOV MS ANALYSIS SUMMARY")
    print("(WHO ICTRP TIMEFRAME: FEB 2001 - DEC 2025)")
    print("="*70)
    
    # Basic stats
    total_studies = len(df)
    unique_sponsors = sponsor_counts.nunique()
    top_sponsor_count = sponsor_counts.iloc[0]
    top_sponsor_name = sponsor_counts.index[0]
    top_sponsor_pct = (top_sponsor_count / total_studies) * 100
    
    print(f"\n📊 KEY FINDINGS:")
    print(f"• Total MS studies (WHO timeframe): {total_studies:,}")
    print(f"• Unique lead sponsors: {unique_sponsors:,}")
    print(f"• Top sponsor: {top_sponsor_name} ({top_sponsor_count} studies, {top_sponsor_pct:.1f}%)")
    print(f"• Sponsor concentration: Top 10 = {sponsor_counts.head(10).sum()/total_studies*100:.1f}%")
    
    # Class distribution
    industry_count = class_counts.get('INDUSTRY', 0)
    other_count = class_counts.get('OTHER', 0)
    industry_pct = (industry_count / total_studies) * 100
    other_pct = (other_count / total_studies) * 100
    
    print(f"\n🏢 SPONSOR COMPOSITION:")
    print(f"• Industry sponsors: {industry_count} studies ({industry_pct:.1f}%)")
    print(f"• Academic/Other: {other_count} studies ({other_pct:.1f}%)")
    print(f"• Government/NIH: {class_counts.get('NIH', 0)} studies")
    
    # Timeline context
    print(f"\n📅 TEMPORAL CONTEXT:")
    print(f"• Timeframe: February 4, 2001 - December 5, 2025")
    print(f"• Duration: 24.8 years (matching WHO ICTRP exactly)")
    print(f"• Registry: ClinicalTrials.gov (US-focused)")
    
    print(f"\n🔍 COMPARATIVE INSIGHTS:")
    print(f"• Dataset size: Larger than WHO ICTRP (2,482 studies)")
    print(f"• Lead sponsor dominance: {top_sponsor_pct:.1f}% vs WHO's 1.1% (Eli Lilly)")
    print(f"• Industry focus: {industry_pct:.1f}% vs WHO's estimated ~35%")
    print(f"• Ready for cross-registry comparison analysis")

def main():
    """Run the complete ClinicalTrials.gov analysis."""
    print("🏥 ClinicalTrials.gov MS Analysis")
    print("Filtered to WHO ICTRP Timeframe for Fair Comparison")
    print("="*60)
    
    try:
        # Load and filter data to WHO timeframe
        df = load_and_filter_clinicaltrials_data()
        
        if len(df) == 0:
            print("❌ No studies remain after filtering. Check date ranges.")
            return
        
        # Analyze sponsors
        sponsor_counts = analyze_clinicaltrials_sponsors(df)
        
        # Analyze sponsor classes  
        class_counts = analyze_sponsor_classes(df)
        
        # Create visualizations
        create_clinicaltrials_sponsor_chart(sponsor_counts)
        create_sponsor_class_chart(class_counts)
        
        # Compare with WHO ICTRP
        compare_with_who_ictrp(sponsor_counts)
        
        # Generate summary
        generate_summary_report(df, sponsor_counts, class_counts)
        
        print(f"\n✅ ClinicalTrials.gov analysis completed!")
        print(f"Generated files:")
        print(f"  • charts/clinicaltrials_top_sponsors.png")
        print(f"  • charts/clinicaltrials_sponsor_classes.png")
        print(f"\n📝 Analysis used WHO ICTRP timeframe for fair comparison!")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        raise

if __name__ == "__main__":
    main()