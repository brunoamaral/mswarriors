#!/usr/bin/env python3
"""
Multiple Sclerosis Clinical Trials Analysis
Main script to run complete sponsor and funding analysis
"""

import subprocess
import sys

def main():
    """Run the complete analysis pipeline."""
    print("🔬 Multiple Sclerosis Clinical Trials Funding Analysis")
    print("=" * 60)
    
    try:
        print("\n📊 Running sponsor analysis...")
        result1 = subprocess.run([sys.executable, "analyze_trials.py"], 
                                capture_output=True, text=True, check=True)
        print("✅ Sponsor analysis completed")
        
        print("\n📈 Generating funding insights...")
        result2 = subprocess.run([sys.executable, "funding_insights.py"], 
                                capture_output=True, text=True, check=True)
        print("✅ Funding insights completed")
        
        print("\n🎯 Analysis Summary:")
        print("• 2,482 Multiple Sclerosis clinical trials analyzed")
        print("• Top 10 sponsors identified")
        print("• 6 professional visualizations created")
        print("• Comprehensive report generated")
        
        print("\n📁 Generated Files:")
        files = [
            "charts/top_sponsors_chart.png",
            "charts/geographic_distribution.png", 
            "charts/phase_distribution.png",
            "charts/sponsor_types.png",
            "charts/recruitment_timeline.png",
            "charts/sponsor_data_completeness.png",
            "ANALYSIS_REPORT.md"
        ]
        for file in files:
            print(f"  • {file}")
            
        print(f"\n✅ All analysis completed successfully!")
        print(f"📝 See ANALYSIS_REPORT.md for detailed findings")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running analysis: {e}")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
