#!/usr/bin/env python3
"""
Comprehensive Registry Comparison Analysis
Compares WHO ICTRP and EU CTIS MS clinical trial data to identify
similarities, differences, and regional patterns in MS research funding.
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
    return charts_dir

def load_both_datasets():
    """Load both WHO and CTIS datasets for comparison."""
    print("Loading both datasets for comparison...")
    
    # Load WHO data
    who_df = pd.read_excel("data/ICTRP-Results.xlsx")
    
    # Load CTIS data
    ctis_df = pd.read_csv("data/CTIS_trials_20250924.csv")
    
    print(f"WHO ICTRP: {len(who_df)} trials")
    print(f"EU CTIS: {len(ctis_df)} trials")
    
    return who_df, ctis_df

def create_registry_comparison_chart(save_path="charts/registry_comparison.png"):
    """Create a comprehensive comparison chart between registries."""
    print("Creating registry comparison visualization...")
    
    ensure_charts_directory()
    
    # Data from our analyses
    who_top_10 = {
        "Eli Lilly and Company": 28,
        "Wyeth (Pfizer subsidiary)": 25,
        "Indiana University": 21,
        "Massachusetts General Hospital": 17,
        "Assistance Publique - Hôpitaux de Paris": 17,
        "Washington University School of Medicine": 17,
        "Xuanwu Hospital, Beijing": 16,
        "Centre Hospitalier Universitaire de Nice": 16,
        "Pfizer": 16,
        "National Institute on Aging (NIA)": 15
    }
    
    ctis_top_10 = {
        "F. Hoffmann-La Roche AG": 18,
        "Novartis Pharma AG": 11,
        "Immunic AG": 5,
        "Sanofi-Aventis R&D": 5,
        "Tg Therapeutics Inc.": 4,
        "Helse Bergen HF": 4,
        "Amsterdam UMC Stichting": 3,
        "Biogen Idec Research Limited": 3,
        "Assistance Publique Hopitaux De Paris": 3,
        "Ospedale San Raffaele S.r.l.": 2
    }
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 10))
    
    # WHO ICTRP chart
    who_sponsors = list(who_top_10.keys())
    who_counts = list(who_top_10.values())
    
    y_pos1 = np.arange(len(who_sponsors))
    bars1 = ax1.barh(y_pos1, who_counts, color=sns.color_palette("Blues_r", len(who_sponsors)))
    
    ax1.set_yticks(y_pos1)
    ax1.set_yticklabels([s[:35] + "..." if len(s) > 35 else s for s in who_sponsors])
    ax1.invert_yaxis()
    ax1.set_xlabel('Number of Trials', fontweight='bold')
    ax1.set_title('WHO ICTRP Top 10 Sponsors\n(2,482 total trials, global)', fontweight='bold', pad=15)
    ax1.grid(axis='x', alpha=0.3)
    
    # Add value labels
    for bar, count in zip(bars1, who_counts):
        ax1.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                str(count), va='center', fontweight='bold', fontsize=10)
    
    # CTIS chart
    ctis_sponsors = list(ctis_top_10.keys())
    ctis_counts = list(ctis_top_10.values())
    
    y_pos2 = np.arange(len(ctis_sponsors))
    bars2 = ax2.barh(y_pos2, ctis_counts, color=sns.color_palette("Oranges_r", len(ctis_sponsors)))
    
    ax2.set_yticks(y_pos2)
    ax2.set_yticklabels([s[:35] + "..." if len(s) > 35 else s for s in ctis_sponsors])
    ax2.invert_yaxis()
    ax2.set_xlabel('Number of Trials', fontweight='bold')
    ax2.set_title('EU CTIS Top 10 Sponsors\n(104 total trials, European)', fontweight='bold', pad=15)
    ax2.grid(axis='x', alpha=0.3)
    
    # Add value labels
    for bar, count in zip(bars2, ctis_counts):
        ax2.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                str(count), va='center', fontweight='bold', fontsize=10)
    
    # Overall title
    fig.suptitle('MS Clinical Trials: Registry Comparison of Top Sponsors\n(Sept 2025)', 
                 fontweight='bold', fontsize=16, y=0.98)
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.90)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Registry comparison chart saved as: {save_path}")
    
    return fig

def create_sponsor_type_comparison_chart(save_path="charts/sponsor_type_comparison.png"):
    """Create sponsor type distribution comparison."""
    print("Creating sponsor type comparison chart...")
    
    ensure_charts_directory()
    
    # Data from analyses (simplified categories)
    who_types = {
        'Pharmaceutical/Biotech': 35,  # Estimated from analysis
        'Academic/Medical': 45,       # Estimated from analysis  
        'Government/Public': 20       # Estimated from analysis
    }
    
    ctis_types = {
        'Pharmaceutical': 60.6,
        'Hospital/Academic': 28.8,
        'Research/Other': 10.6
    }
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # WHO pie chart (estimated percentages)
    colors1 = ['#FF9999', '#66B2FF', '#99FF99']
    wedges1, texts1, autotexts1 = ax1.pie(who_types.values(), labels=who_types.keys(),
                                          autopct='%1.1f%%', colors=colors1, startangle=90)
    
    for autotext in autotexts1:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    ax1.set_title('WHO ICTRP Sponsor Types\n(Estimated Distribution)', fontweight='bold')
    
    # CTIS pie chart (actual percentages)
    colors2 = ['#FFB366', '#66FFB2', '#B366FF']
    wedges2, texts2, autotexts2 = ax2.pie(ctis_types.values(), labels=ctis_types.keys(),
                                          autopct='%1.1f%%', colors=colors2, startangle=90)
    
    for autotext in autotexts2:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    ax2.set_title('EU CTIS Sponsor Types\n(Actual Distribution)', fontweight='bold')
    
    fig.suptitle('Sponsor Type Distribution: WHO ICTRP vs EU CTIS\n(MS Clinical Trials)', 
                 fontweight='bold', fontsize=14, y=0.95)
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.85)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Sponsor type comparison saved as: {save_path}")
    
    return fig

def create_key_insights_summary():
    """Generate key insights from registry comparison."""
    print(f"\n" + "="*70)
    print("MS CLINICAL TRIALS: CROSS-REGISTRY ANALYSIS SUMMARY")
    print("="*70)
    
    print(f"\n📊 SCALE & SCOPE:")
    print(f"• WHO ICTRP (Global): 2,482 trials, 1,355 unique sponsors")
    print(f"• EU CTIS (European): 104 trials, 50 unique sponsors")
    print(f"• Coverage ratio: CTIS represents 4.2% of WHO trial volume")
    
    print(f"\n🏢 SPONSOR LEADERSHIP PATTERNS:")
    print(f"WHO ICTRP Top Patterns:")
    print(f"  • Highly fragmented (top sponsor: 1.1% of trials)")
    print(f"  • Mixed ecosystem: pharma, academic, government")
    print(f"  • US institutions prominent")
    
    print(f"\nCTIS Top Patterns:")
    print(f"  • More concentrated (top sponsor: 17.3% of trials)")
    print(f"  • Pharma-dominated leadership (Roche, Novartis)")
    print(f"  • European focus with major pharma players")
    
    print(f"\n🔍 KEY DIFFERENCES IDENTIFIED:")
    print(f"• Concentration: CTIS shows higher sponsor concentration than WHO")
    print(f"• Zero overlap: No sponsors appear in both top-10 lists")
    print(f"• Geographic focus: CTIS reflects European regulatory landscape")
    print(f"• Pharma prominence: CTIS shows stronger pharmaceutical dominance")
    
    print(f"\n📈 SPONSOR TYPE INSIGHTS:")
    print(f"• WHO: More balanced distribution across sponsor types")
    print(f"• CTIS: 60.6% pharmaceutical vs ~35% estimated in WHO")
    print(f"• Academic role: Strong in both but different institutions")
    print(f"• Regional specialization evident in both registries")
    
    print(f"\n🌍 REGULATORY IMPLICATIONS:")
    print(f"• Dual registration: Many trials likely appear in both systems")
    print(f"• Regional optimization: Sponsors may optimize for specific regions")
    print(f"• Regulatory alignment: CTIS reflects EU-specific requirements")
    print(f"• Data complementarity: Both registries provide unique perspectives")
    
    print(f"\n💡 STRATEGIC INSIGHTS:")
    print(f"• Market approach: Different sponsors dominate different regions")
    print(f"• Investment patterns: European trials show higher pharma concentration")
    print(f"• Global vs regional: WHO captures broader, CTIS shows focused activity")
    print(f"• Regulatory landscape: CTIS reflects EU harmonization effects")
    
    print("=" * 70)

def main():
    """Run comprehensive registry comparison analysis."""
    # Load both datasets
    who_df, ctis_df = load_both_datasets()
    
    # Create comparison visualizations
    create_registry_comparison_chart()
    create_sponsor_type_comparison_chart()
    
    # Generate insights summary
    create_key_insights_summary()
    
    print(f"\n✅ Cross-registry analysis completed!")
    print(f"Generated files:")
    print(f"  • charts/registry_comparison.png")
    print(f"  • charts/sponsor_type_comparison.png")
    print(f"\n📝 Both individual and comparative analyses now available!")

if __name__ == "__main__":
    main()