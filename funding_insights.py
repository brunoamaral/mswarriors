#!/usr/bin/env python3
"""
Additional funding analysis visualizations
Creates comprehensive charts for blog post use
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

def ensure_charts_directory():
    """Create charts directory if it doesn't exist."""
    charts_dir = "charts"
    if not os.path.exists(charts_dir):
        os.makedirs(charts_dir)
        print(f"Created {charts_dir} directory")
    return charts_dir

def load_data():
    """Load the clinical trials data."""
    df = pd.read_excel("data/ICTRP-Results.xlsx")
    return df

def create_geographic_distribution_chart(df, save_path="charts/geographic_distribution.png"):
    """Create a chart showing geographic distribution of trials."""
    print("Creating geographic distribution chart...")
    
    # Ensure charts directory exists
    ensure_charts_directory()
    
    # Get top 10 countries
    countries = df['Countries'].fillna('Not specified')
    top_countries = countries.value_counts().head(10)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create bar chart
    colors = sns.color_palette("viridis", len(top_countries))
    bars = ax.bar(range(len(top_countries)), top_countries.values, color=colors)
    
    # Customize
    ax.set_xticks(range(len(top_countries)))
    ax.set_xticklabels([country.replace('(Islamic Republic of)', '(IR)') for country in top_countries.index], 
                       rotation=45, ha='right')
    ax.set_ylabel('Number of Clinical Trials', fontweight='bold')
    ax.set_title('Geographic Distribution of Multiple Sclerosis Clinical Trials\n(Top 10 Countries - 2,482 total trials, WHO ICTRP, Sept 2025)', 
                 fontweight='bold', pad=20)
    
    # Add value labels
    for bar, count in zip(bars, top_countries.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                str(count), ha='center', va='bottom', fontweight='bold')
    
    # Add grid
    ax.grid(axis='y', alpha=0.3)
    ax.set_axisbelow(True)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Geographic distribution chart saved as: {save_path}")
    return fig

def create_phase_distribution_chart(df, save_path="charts/phase_distribution.png"):
    """Create a pie chart showing trial phase distribution."""
    print("Creating trial phase distribution chart...")
    
    phases = df['Phase'].fillna('Not specified')
    phase_counts = phases.value_counts()
    
    # Group smaller phases together
    main_phases = phase_counts.head(7)
    other_count = phase_counts.iloc[7:].sum()
    if other_count > 0:
        main_phases['Others'] = other_count
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create pie chart
    colors = sns.color_palette("Set3", len(main_phases))
    wedges, texts, autotexts = ax.pie(main_phases.values, labels=main_phases.index, 
                                      autopct='%1.1f%%', colors=colors, startangle=90)
    
    # Customize text
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(10)
    
    for text in texts:
        text.set_fontsize(10)
    
    ax.set_title('Distribution of Multiple Sclerosis Clinical Trial Phases\n(2,482 total trials, WHO ICTRP, Sept 2025)', 
                 fontweight='bold', fontsize=14, pad=20)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Phase distribution chart saved as: {save_path}")
    return fig

def create_sponsor_type_analysis(df, save_path="charts/sponsor_types.png"):
    """Analyze and visualize sponsor types (pharmaceutical, academic, government)."""
    print("Creating sponsor type analysis...")
    
    primary_sponsors = df['Primary_sponsor'].fillna('Unknown').str.strip()
    
    # Categorize sponsors
    pharmaceutical_keywords = ['Pfizer', 'Lilly', 'Novartis', 'Roche', 'Merck', 'Bristol', 'Johnson', 
                               'Wyeth', 'Biogen', 'Genentech', 'Sanofi', 'GlaxoSmithKline', 'AbbVie',
                               'Pharma', 'Pharmaceutical', 'Biotechnology', 'Biotech', 'AG', 'Inc.', 
                               'Corporation', 'Corp', 'Ltd', 'Limited', 'SA', 'SpA', 'GmbH']
    
    academic_keywords = ['University', 'College', 'Hospital', 'Medical Center', 'Institut', 'Center',
                         'Centre', 'School of Medicine', 'Research Institute', 'Foundation',
                         'Clinic', 'Clinique', 'Ospedale', 'Universitaire', 'Universidad']
    
    government_keywords = ['National Institute', 'Ministry', 'Department', 'Government', 'Public Health',
                           'VA Medical', 'Veterans', 'NIH', 'NIA', 'NIMH', 'NHS', 'Health Service']
    
    def categorize_sponsor(sponsor):
        sponsor_lower = sponsor.lower()
        
        # Check pharmaceutical first (more specific)
        for keyword in pharmaceutical_keywords:
            if keyword.lower() in sponsor_lower:
                return 'Pharmaceutical/Biotech'
        
        # Check government
        for keyword in government_keywords:
            if keyword.lower() in sponsor_lower:
                return 'Government/Public'
        
        # Check academic/medical
        for keyword in academic_keywords:
            if keyword.lower() in sponsor_lower:
                return 'Academic/Medical'
        
        return 'Other/Unknown'
    
    sponsor_types = primary_sponsors.apply(categorize_sponsor)
    type_counts = sponsor_types.value_counts()
    
    # Create visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Pie chart
    colors = sns.color_palette("husl", len(type_counts))
    wedges, texts, autotexts = ax1.pie(type_counts.values, labels=type_counts.index, 
                                       autopct='%1.1f%%', colors=colors, startangle=90)
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    ax1.set_title('Distribution by Sponsor Type\n(2,482 MS trials, WHO ICTRP, Sept 2025)', fontweight='bold')
    
    # Top sponsors by category
    top_pharma = primary_sponsors[sponsor_types == 'Pharmaceutical/Biotech'].value_counts().head(5)
    top_academic = primary_sponsors[sponsor_types == 'Academic/Medical'].value_counts().head(5)
    
    # Bar chart for top pharmaceutical sponsors
    y_pos = np.arange(len(top_pharma))
    bars = ax2.barh(y_pos, top_pharma.values, color=colors[0], alpha=0.8)
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels([sponsor[:30] + "..." if len(sponsor) > 30 else sponsor 
                         for sponsor in top_pharma.index])
    ax2.invert_yaxis()
    ax2.set_xlabel('Number of Trials')
    ax2.set_title('Top 5 Pharmaceutical/Biotech Sponsors', fontweight='bold')
    
    # Add value labels
    for bar, count in zip(bars, top_pharma.values):
        ax2.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                 str(count), va='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Sponsor types analysis saved as: {save_path}")
    
    return fig, type_counts, top_pharma, top_academic

def create_recruitment_timeline_chart(df, save_path="charts/recruitment_timeline.png"):
    """Create a timeline of trial recruitment."""
    print("Creating recruitment timeline chart...")
    
    # Convert date columns
    df_copy = df.copy()
    df_copy['Date_registration'] = pd.to_datetime(df_copy['Date_registration'], errors='coerce')
    
    # Filter out invalid dates and very old dates
    valid_dates = df_copy.dropna(subset=['Date_registration'])
    valid_dates = valid_dates[valid_dates['Date_registration'] > '2000-01-01']
    
    # Group by year
    valid_dates['Year'] = valid_dates['Date_registration'].dt.year
    yearly_counts = valid_dates.groupby('Year').size()
    
    # Create the chart
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(yearly_counts.index, yearly_counts.values, marker='o', linewidth=2, markersize=6)
    ax.fill_between(yearly_counts.index, yearly_counts.values, alpha=0.3)
    
    ax.set_xlabel('Year', fontweight='bold')
    ax.set_ylabel('Number of Trials Registered', fontweight='bold')
    ax.set_title('Multiple Sclerosis Clinical Trials Registration Timeline (2001-2025)\n(2,482 total trials, WHO ICTRP, exported Sept 2025)', fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3)
    
    # Highlight recent years
    recent_years = yearly_counts.tail(5)
    ax.axvspan(recent_years.index[0], recent_years.index[-1], alpha=0.2, color='red', 
               label=f'Last 5 years\n({recent_years.sum()} trials)')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Timeline chart saved as: {save_path}")
    return fig

def create_sponsor_data_completeness_chart(df, save_path="charts/sponsor_data_completeness.png"):
    """Create a chart showing completeness of sponsor data."""
    print("Creating sponsor data completeness chart...")
    
    # Analyze primary sponsor completeness
    primary_complete = (~df['Primary_sponsor'].isna() & 
                       (df['Primary_sponsor'].str.strip() != '') & 
                       (df['Primary_sponsor'].str.strip() != 'Unknown')).sum()
    primary_missing = len(df) - primary_complete
    
    # Analyze secondary sponsor completeness
    secondary_complete = (~df['Secondary_Sponsor'].isna() & 
                         (df['Secondary_Sponsor'].str.strip() != '')).sum()
    secondary_missing = len(df) - secondary_complete
    
    # Create the visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Primary sponsor completeness pie chart
    primary_data = [primary_complete, primary_missing]
    primary_labels = [f'With Primary Sponsor\n({primary_complete:,} trials)', 
                     f'Missing/Unknown\n({primary_missing:,} trials)']
    colors1 = ['#2E8B57', '#CD5C5C']  # Sea green and Indian red
    
    wedges1, texts1, autotexts1 = ax1.pie(primary_data, labels=primary_labels, 
                                          autopct='%1.1f%%', colors=colors1, 
                                          startangle=90, explode=(0.05, 0))
    
    for autotext in autotexts1:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(11)
    
    for text in texts1:
        text.set_fontsize(10)
        text.set_fontweight('bold')
    
    ax1.set_title('Primary Sponsor Data\nCompleteness', fontweight='bold', fontsize=12, pad=15)
    
    # Secondary sponsor data bar chart
    categories = ['Trials with\nSecondary Sponsors', 'Trials without\nSecondary Sponsors']
    counts = [secondary_complete, secondary_missing]
    colors2 = ['#4682B4', '#D3D3D3']  # Steel blue and light gray
    
    bars = ax2.bar(categories, counts, color=colors2, alpha=0.8)
    ax2.set_ylabel('Number of Trials', fontweight='bold')
    ax2.set_title('Secondary Sponsor Data\nAvailability', fontweight='bold', fontsize=12, pad=15)
    
    # Add value labels on bars
    for bar, count in zip(bars, counts):
        percentage = (count / len(df)) * 100
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20,
                f'{count:,}\n({percentage:.1f}%)', ha='center', va='bottom', 
                fontweight='bold', fontsize=10)
    
    # Add grid for better readability
    ax2.grid(axis='y', alpha=0.3)
    ax2.set_axisbelow(True)
    
    # Add overall title
    fig.suptitle('Sponsor Data Completeness in MS Clinical Trials\n(2,482 total trials, WHO ICTRP, Sept 2025)', 
                 fontweight='bold', fontsize=14, y=0.98)
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.85)  # Make room for the main title
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Sponsor data completeness chart saved as: {save_path}")
    
    # Print summary statistics
    print(f"\nSponsor Data Completeness Summary:")
    print(f"• Primary sponsor data available: {primary_complete:,} trials ({(primary_complete/len(df)*100):.1f}%)")
    print(f"• Primary sponsor missing/unknown: {primary_missing:,} trials ({(primary_missing/len(df)*100):.1f}%)")
    print(f"• Secondary sponsor data available: {secondary_complete:,} trials ({(secondary_complete/len(df)*100):.1f}%)")
    print(f"• Trials with only primary sponsor: {primary_complete - secondary_complete:,} trials")
    
    return fig, {
        'primary_complete': primary_complete,
        'primary_missing': primary_missing, 
        'secondary_complete': secondary_complete,
        'secondary_missing': secondary_missing
    }

def generate_summary_report(df):
    """Generate a comprehensive summary report."""
    print("\n" + "="*60)
    print("MULTIPLE SCLEROSIS CLINICAL TRIALS FUNDING ANALYSIS")
    print("="*60)
    
    # Basic stats
    total_trials = len(df)
    unique_sponsors = df['Primary_sponsor'].nunique()
    
    # Top sponsors
    top_sponsors = df['Primary_sponsor'].value_counts().head(10)
    
    # Geographic distribution
    top_countries = df['Countries'].fillna('Not specified').value_counts().head(5)
    
    # Phases
    phases = df['Phase'].fillna('Not specified').value_counts()
    
    # Timeline
    df_dates = df.copy()
    df_dates['Date_registration'] = pd.to_datetime(df_dates['Date_registration'], errors='coerce')
    recent_trials = df_dates[df_dates['Date_registration'] > '2020-01-01'].shape[0]
    
    print(f"\nKEY FINDINGS:")
    print(f"• Total Multiple Sclerosis trials analyzed: {total_trials:,}")
    print(f"• Unique primary sponsors: {unique_sponsors:,}")
    print(f"• Trials registered since 2020: {recent_trials}")
    print(f"• Most active sponsor: {top_sponsors.index[0]} ({top_sponsors.iloc[0]} trials)")
    print(f"• Leading country: {top_countries.index[0]} ({top_countries.iloc[0]} trials, {(top_countries.iloc[0]/total_trials*100):.1f}%)")
    
    print(f"\nSPONSOR CONCENTRATION:")
    print(f"• Top sponsor represents {(top_sponsors.iloc[0]/total_trials*100):.1f}% of all trials")
    print(f"• Top 5 sponsors represent {(top_sponsors.head(5).sum()/total_trials*100):.1f}% of all trials")
    print(f"• Top 10 sponsors represent {(top_sponsors.head(10).sum()/total_trials*100):.1f}% of all trials")
    
    print(f"\nTRIAL CHARACTERISTICS:")
    print(f"• Most common phase: {phases.index[0]} ({phases.iloc[0]} trials, {(phases.iloc[0]/total_trials*100):.1f}%)")
    print(f"• Interventional trials: {df[df['Study_type'].str.contains('Interventional', na=False, case=False)].shape[0]} ({(df[df['Study_type'].str.contains('Interventional', na=False, case=False)].shape[0]/total_trials*100):.1f}%)")
    
    print("\n" + "="*60)

def main():
    # Load data
    df = load_data()
    
    # Create all visualizations
    create_geographic_distribution_chart(df)
    create_phase_distribution_chart(df)
    fig, type_counts, top_pharma, top_academic = create_sponsor_type_analysis(df)
    create_recruitment_timeline_chart(df)
    fig_completeness, completeness_stats = create_sponsor_data_completeness_chart(df)
    
    # Generate summary report
    generate_summary_report(df)
    
    print(f"\n✅ All visualizations created successfully!")
    print(f"Files generated:")
    print(f"  • charts/top_sponsors_chart.png")
    print(f"  • charts/geographic_distribution.png") 
    print(f"  • charts/phase_distribution.png")
    print(f"  • charts/sponsor_types.png")
    print(f"  • charts/recruitment_timeline.png")
    print(f"  • charts/sponsor_data_completeness.png")

if __name__ == "__main__":
    main()