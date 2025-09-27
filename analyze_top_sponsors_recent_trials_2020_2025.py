#!/usr/bin/env python3
"""
Top Sponsors and Their Most Recent Trials Analysis - 2020-2025 Period
Identifies top 5 sponsors from each registry and their 5 most recent clinical trials.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from datetime import datetime

def ensure_output_directory():
    """Create output directory if it doesn't exist."""
    output_dir = "analysis_2020_2025/reports"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

def load_and_filter_clinicaltrials_data():
    """Load and filter ClinicalTrials.gov data to 2020-2025 timeframe."""
    print("Loading ClinicalTrials.gov data...")
    df = pd.read_csv("data/clinicaltrials_ms_20250925.csv")
    
    # Convert date and filter
    df['StudyFirstPostDate_dt'] = pd.to_datetime(df['StudyFirstPostDate'], errors='coerce')
    
    start_date = pd.Timestamp('2020-01-01')
    end_date = pd.Timestamp('2025-12-31')
    
    filtered = df[
        (df['StudyFirstPostDate_dt'] >= start_date) & 
        (df['StudyFirstPostDate_dt'] <= end_date) &
        df['StudyFirstPostDate_dt'].notna()
    ].copy()
    
    print(f"ClinicalTrials.gov filtered to {len(filtered):,} studies (2020-2025)")
    return filtered

def load_and_filter_ictrp_data():
    """Load and filter WHO ICTRP data to 2020-2025 timeframe."""
    print("Loading WHO ICTRP data...")
    df = pd.read_excel("data/ICTRP-Results.xlsx")
    
    # Convert date and filter
    df['Date_registration_dt'] = pd.to_datetime(df['Date_registration'], errors='coerce')
    
    start_date = pd.Timestamp('2020-01-01')
    end_date = pd.Timestamp('2025-12-31')
    
    filtered = df[
        (df['Date_registration_dt'] >= start_date) & 
        (df['Date_registration_dt'] <= end_date) &
        df['Date_registration_dt'].notna()
    ].copy()
    
    print(f"WHO ICTRP filtered to {len(filtered):,} studies (2020-2025)")
    return filtered

def load_and_filter_ctis_data():
    """Load and filter EU CTIS data to 2020-2025 timeframe."""
    print("Loading EU CTIS data...")
    df = pd.read_csv("data/CTIS_trials_20250924.csv")
    
    # Convert date and filter
    df['Decision_date_dt'] = pd.to_datetime(df['Decision date'], errors='coerce')
    
    start_date = pd.Timestamp('2020-01-01')
    end_date = pd.Timestamp('2025-12-31')
    
    filtered = df[
        (df['Decision_date_dt'] >= start_date) & 
        (df['Decision_date_dt'] <= end_date) &
        df['Decision_date_dt'].notna()
    ].copy()
    
    print(f"EU CTIS filtered to {len(filtered):,} studies (2020-2025)")
    return filtered

def analyze_top_sponsors_clinicaltrials(df):
    """Find top 5 sponsors from ClinicalTrials.gov and their recent trials."""
    print("\n=== CLINICALTRIALS.GOV TOP 5 SPONSORS ===")
    
    # Get top 5 sponsors
    sponsor_counts = df['LeadSponsorName'].value_counts()
    top_5_sponsors = sponsor_counts.head(5)
    
    print("Top 5 Sponsors:")
    for i, (sponsor, count) in enumerate(top_5_sponsors.items(), 1):
        print(f"{i:2d}. {sponsor:<50} {count:3d} trials")
    
    # For each top sponsor, get their 5 most recent trials
    sponsor_recent_trials = {}
    
    for sponsor in top_5_sponsors.index:
        sponsor_trials = df[df['LeadSponsorName'] == sponsor].copy()
        
        # Sort by registration date (most recent first)
        sponsor_trials_sorted = sponsor_trials.sort_values('StudyFirstPostDate_dt', ascending=False)
        
        # Get top 5 most recent
        recent_5 = sponsor_trials_sorted.head(5)
        
        sponsor_recent_trials[sponsor] = recent_5[['NCTId', 'BriefTitle', 'StudyFirstPostDate', 'Phase', 'OverallStatus']].copy()
    
    return top_5_sponsors, sponsor_recent_trials

def analyze_top_sponsors_ictrp(df):
    """Find top 5 sponsors from WHO ICTRP and their recent trials."""
    print("\n=== WHO ICTRP TOP 5 SPONSORS ===")
    
    # Get top 5 sponsors
    sponsor_counts = df['Primary_sponsor'].value_counts()
    top_5_sponsors = sponsor_counts.head(5)
    
    print("Top 5 Sponsors:")
    for i, (sponsor, count) in enumerate(top_5_sponsors.items(), 1):
        print(f"{i:2d}. {sponsor:<50} {count:3d} trials")
    
    # For each top sponsor, get their 5 most recent trials
    sponsor_recent_trials = {}
    
    for sponsor in top_5_sponsors.index:
        sponsor_trials = df[df['Primary_sponsor'] == sponsor].copy()
        
        # Sort by registration date (most recent first)
        sponsor_trials_sorted = sponsor_trials.sort_values('Date_registration_dt', ascending=False)
        
        # Get top 5 most recent
        recent_5 = sponsor_trials_sorted.head(5)
        
        sponsor_recent_trials[sponsor] = recent_5[['TrialID', 'Public_title', 'Date_registration', 'Study_type', 'Recruitment_Status']].copy()
    
    return top_5_sponsors, sponsor_recent_trials

def analyze_top_sponsors_ctis(df):
    """Find top 5 sponsors from EU CTIS and their recent trials."""
    print("\n=== EU CTIS TOP 5 SPONSORS ===")
    
    # Get top 5 sponsors
    sponsor_counts = df['Sponsor/Co-Sponsors'].value_counts()
    top_5_sponsors = sponsor_counts.head(5)
    
    print("Top 5 Sponsors:")
    for i, (sponsor, count) in enumerate(top_5_sponsors.items(), 1):
        print(f"{i:2d}. {sponsor:<50} {count:3d} trials")
    
    # For each top sponsor, get their 5 most recent trials
    sponsor_recent_trials = {}
    
    for sponsor in top_5_sponsors.index:
        sponsor_trials = df[df['Sponsor/Co-Sponsors'] == sponsor].copy()
        
        # Sort by decision date (most recent first)
        sponsor_trials_sorted = sponsor_trials.sort_values('Decision_date_dt', ascending=False)
        
        # Get top 5 most recent
        recent_5 = sponsor_trials_sorted.head(5)
        
        sponsor_recent_trials[sponsor] = recent_5[['Trial number', 'Title of the trial', 'Decision date', 'Trial phase', 'Overall trial status']].copy()
    
    return top_5_sponsors, sponsor_recent_trials

def generate_detailed_report(ct_data, ictrp_data, ctis_data, ct_total, ictrp_total, ctis_total):
    """Generate a comprehensive report of top sponsors and their recent trials."""
    print("\nGenerating detailed report...")
    ensure_output_directory()
    
    ct_sponsors, ct_trials = ct_data
    ictrp_sponsors, ictrp_trials = ictrp_data
    ctis_sponsors, ctis_trials = ctis_data
    
    report_content = []
    
    # Header
    report_content.append("# Top 5 Sponsors and Their Most Recent Trials (2020-2025)")
    report_content.append("=" * 70)
    report_content.append("")
    report_content.append(f"**Analysis Date:** {datetime.now().strftime('%B %d, %Y')}")
    report_content.append(f"**Time Period:** January 1, 2020 - December 31, 2025")
    report_content.append(f"**Registries:** ClinicalTrials.gov, WHO ICTRP, EU CTIS")
    report_content.append("")
    
    # Executive Summary
    report_content.append("## Executive Summary")
    report_content.append("")
    report_content.append("This analysis identifies the top 5 sponsors by trial count in each registry during the 2020-2025 period")
    report_content.append("and examines their 5 most recent clinical trial registrations.")
    report_content.append("")
    
    # ClinicalTrials.gov Analysis
    report_content.append("## 1. ClinicalTrials.gov Analysis")
    report_content.append("")
    report_content.append("### Top 5 Sponsors by Trial Count:")
    report_content.append("")
    
    for i, (sponsor, count) in enumerate(ct_sponsors.items(), 1):
        percentage = (count / ct_sponsors.sum()) * 100
        report_content.append(f"{i}. **{sponsor}** - {count} trials ({percentage:.1f}%)")
    report_content.append("")
    
    report_content.append("### Most Recent Trials by Top Sponsors:")
    report_content.append("")
    
    for sponsor, trials in ct_trials.items():
        report_content.append(f"#### {sponsor}")
        report_content.append("")
        report_content.append("| NCT ID | Title | Registration Date | Phase | Status |")
        report_content.append("|--------|-------|-------------------|--------|--------|")
        
        for _, trial in trials.iterrows():
            title = str(trial['BriefTitle']) if pd.notna(trial['BriefTitle']) else "N/A"
            phase = str(trial['Phase']) if pd.notna(trial['Phase']) else "N/A"
            status = str(trial['OverallStatus']) if pd.notna(trial['OverallStatus']) else "N/A"
            reg_date = str(trial['StudyFirstPostDate']) if pd.notna(trial['StudyFirstPostDate']) else "N/A"
            
            report_content.append(f"| {trial['NCTId']} | {title} | {reg_date} | {phase} | {status} |")
        
        report_content.append("")
    
    # WHO ICTRP Analysis
    report_content.append("## 2. WHO ICTRP Analysis")
    report_content.append("")
    report_content.append("### Top 5 Sponsors by Trial Count:")
    report_content.append("")
    
    for i, (sponsor, count) in enumerate(ictrp_sponsors.items(), 1):
        percentage = (count / ictrp_sponsors.sum()) * 100
        report_content.append(f"{i}. **{sponsor}** - {count} trials ({percentage:.1f}%)")
    report_content.append("")
    
    report_content.append("### Most Recent Trials by Top Sponsors:")
    report_content.append("")
    
    for sponsor, trials in ictrp_trials.items():
        report_content.append(f"#### {sponsor}")
        report_content.append("")
        report_content.append("| Trial ID | Title | Registration Date | Study Type | Status |")
        report_content.append("|----------|-------|-------------------|------------|--------|")
        
        for _, trial in trials.iterrows():
            title = str(trial['Public_title']) if pd.notna(trial['Public_title']) else "N/A"
            study_type = str(trial['Study_type']) if pd.notna(trial['Study_type']) else "N/A"
            status = str(trial['Recruitment_Status']) if pd.notna(trial['Recruitment_Status']) else "N/A"
            reg_date = str(trial['Date_registration']) if pd.notna(trial['Date_registration']) else "N/A"
            
            report_content.append(f"| {trial['TrialID']} | {title} | {reg_date} | {study_type} | {status} |")
        
        report_content.append("")
    
    # EU CTIS Analysis
    report_content.append("## 3. EU CTIS Analysis")
    report_content.append("")
    report_content.append("### Top 5 Sponsors by Trial Count:")
    report_content.append("")
    
    for i, (sponsor, count) in enumerate(ctis_sponsors.items(), 1):
        percentage = (count / ctis_sponsors.sum()) * 100
        report_content.append(f"{i}. **{sponsor}** - {count} trials ({percentage:.1f}%)")
    report_content.append("")
    
    report_content.append("### Most Recent Trials by Top Sponsors:")
    report_content.append("")
    
    for sponsor, trials in ctis_trials.items():
        report_content.append(f"#### {sponsor}")
        report_content.append("")
        report_content.append("| EudraCT Number | Title | Decision Date | Trial Phase | Status |")
        report_content.append("|----------------|-------|---------------|-------------|--------|")
        
        for _, trial in trials.iterrows():
            title = str(trial['Title of the trial']) if pd.notna(trial['Title of the trial']) else "N/A"
            trial_phase = str(trial['Trial phase']) if pd.notna(trial['Trial phase']) else "N/A"
            status = str(trial['Overall trial status']) if pd.notna(trial['Overall trial status']) else "N/A"
            decision_date = str(trial['Decision date']) if pd.notna(trial['Decision date']) else "N/A"
            
            report_content.append(f"| {trial['Trial number']} | {title} | {decision_date} | {trial_phase} | {status} |")
        
        report_content.append("")
    
    # Cross-Registry Insights
    report_content.append("## 4. Cross-Registry Insights")
    report_content.append("")
    
    # Find sponsors appearing in multiple registries
    ct_sponsor_set = set(ct_sponsors.index)
    ictrp_sponsor_set = set(ictrp_sponsors.index)
    ctis_sponsor_set = set(ctis_sponsors.index)
    
    # Check for overlaps (accounting for name variations)
    report_content.append("### Sponsor Presence Across Registries:")
    report_content.append("")
    report_content.append("**Multi-Registry Sponsors:**")
    
    # Look for similar sponsor names (basic matching)
    all_sponsors = list(ct_sponsor_set) + list(ictrp_sponsor_set) + list(ctis_sponsor_set)
    sponsor_variations = {}
    
    for sponsor in all_sponsors:
        base_name = sponsor.lower().replace('inc.', '').replace('inc', '').replace('ltd', '').replace('ag', '').replace('pharmaceuticals', '').strip()
        if base_name not in sponsor_variations:
            sponsor_variations[base_name] = []
        sponsor_variations[base_name].append(sponsor)
    
    multi_registry_sponsors = {k: v for k, v in sponsor_variations.items() if len(v) > 1}
    
    if multi_registry_sponsors:
        for base_name, variations in multi_registry_sponsors.items():
            report_content.append(f"- **{base_name.title()}**: {', '.join(variations)}")
    else:
        report_content.append("- No obvious multi-registry sponsors detected (may be due to name variations)")
    
    report_content.append("")
    
    # Summary statistics
    report_content.append("### Summary Statistics:")
    report_content.append("")
    report_content.append(f"- **Total unique top sponsors across all registries:** {len(set(all_sponsors))}")
    
    # Calculate proper percentages - top 5 sponsors as percentage of total trials in each registry
    ct_percentage = (ct_sponsors.sum() / ct_total) * 100 if ct_total > 0 else 0
    ictrp_percentage = (ictrp_sponsors.sum() / ictrp_total) * 100 if ictrp_total > 0 else 0
    ctis_percentage = (ctis_sponsors.sum() / ctis_total) * 100 if ctis_total > 0 else 0
    
    report_content.append(f"- **ClinicalTrials.gov top 5 represent:** {ct_sponsors.sum()} trials ({ct_percentage:.1f}% of {ct_total} total trials)")
    report_content.append(f"- **WHO ICTRP top 5 represent:** {ictrp_sponsors.sum()} trials ({ictrp_percentage:.1f}% of {ictrp_total} total trials)") 
    report_content.append(f"- **EU CTIS top 5 represent:** {ctis_sponsors.sum()} trials ({ctis_percentage:.1f}% of {ctis_total} total trials)")
    
    # Write report to file
    report_path = "analysis_2020_2025/reports/TOP_SPONSORS_RECENT_TRIALS_2020_2025.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_content))
    
    print(f"✓ Detailed report saved: {report_path}")
    return report_path

def create_sponsor_comparison_chart(ct_sponsors, ictrp_sponsors, ctis_sponsors):
    """Create a comparison chart of top sponsors across registries."""
    print("Creating sponsor comparison visualization...")
    
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 8))
    
    # ClinicalTrials.gov
    ax1.barh(range(len(ct_sponsors)), ct_sponsors.values, color='#1f77b4', alpha=0.8)
    ax1.set_yticks(range(len(ct_sponsors)))
    ax1.set_yticklabels([name[:30] + "..." if len(name) > 30 else name for name in ct_sponsors.index])
    ax1.set_xlabel('Number of Trials')
    ax1.set_title('ClinicalTrials.gov\nTop 5 Sponsors', fontweight='bold')
    ax1.invert_yaxis()
    
    # Add value labels
    for i, v in enumerate(ct_sponsors.values):
        ax1.text(v + 0.5, i, str(v), va='center', fontweight='bold')
    
    # WHO ICTRP
    ax2.barh(range(len(ictrp_sponsors)), ictrp_sponsors.values, color='#ff7f0e', alpha=0.8)
    ax2.set_yticks(range(len(ictrp_sponsors)))
    ax2.set_yticklabels([name[:30] + "..." if len(name) > 30 else name for name in ictrp_sponsors.index])
    ax2.set_xlabel('Number of Trials')
    ax2.set_title('WHO ICTRP\nTop 5 Sponsors', fontweight='bold')
    ax2.invert_yaxis()
    
    # Add value labels
    for i, v in enumerate(ictrp_sponsors.values):
        ax2.text(v + 0.1, i, str(v), va='center', fontweight='bold')
    
    # EU CTIS
    ax3.barh(range(len(ctis_sponsors)), ctis_sponsors.values, color='#2ca02c', alpha=0.8)
    ax3.set_yticks(range(len(ctis_sponsors)))
    ax3.set_yticklabels([name[:30] + "..." if len(name) > 30 else name for name in ctis_sponsors.index])
    ax3.set_xlabel('Number of Trials')
    ax3.set_title('EU CTIS\nTop 5 Sponsors', fontweight='bold')
    ax3.invert_yaxis()
    
    # Add value labels
    for i, v in enumerate(ctis_sponsors.values):
        ax3.text(v + 0.2, i, str(v), va='center', fontweight='bold')
    
    plt.suptitle('Top 5 Sponsors by Registry (2020-2025)', fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    chart_path = "analysis_2020_2025/charts/top_5_sponsors_comparison_2020_2025.png"
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Sponsor comparison chart saved: {chart_path}")

def main():
    """Run the complete top sponsors and recent trials analysis."""
    print("🔍 Top 5 Sponsors and Their Most Recent Trials Analysis (2020-2025)")
    print("=" * 80)
    
    try:
        # Load and filter data from all three registries
        ct_df = load_and_filter_clinicaltrials_data()
        ictrp_df = load_and_filter_ictrp_data()
        ctis_df = load_and_filter_ctis_data()
        
        # Analyze top sponsors and their recent trials
        ct_data = analyze_top_sponsors_clinicaltrials(ct_df)
        ictrp_data = analyze_top_sponsors_ictrp(ictrp_df)
        ctis_data = analyze_top_sponsors_ctis(ctis_df)
        
        # Create comparison visualization
        create_sponsor_comparison_chart(ct_data[0], ictrp_data[0], ctis_data[0])
        
        # Generate comprehensive report
        report_path = generate_detailed_report(ct_data, ictrp_data, ctis_data, len(ct_df), len(ictrp_df), len(ctis_df))
        
        print(f"\n✅ Top sponsors analysis completed!")
        print(f"📊 Generated files:")
        print(f"   • {report_path}")
        print(f"   • analysis_2020_2025/charts/top_5_sponsors_comparison_2020_2025.png")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        raise

if __name__ == "__main__":
    main()