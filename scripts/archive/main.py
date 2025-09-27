#!/usr/bin/env python3
"""
MS Warriors Clinical Trials Analysis - Main Orchestrator
Runs the complete analysis pipeline for Multiple Sclerosis clinical trials data.
Cross-registry analysis covering WHO ICTRP and EU CTIS datasets.
"""

import subprocess
import sys
import os

def run_analysis_script(script_name, description):
    """Run an analysis script and handle any errors."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Script: {script_name}")
    print("="*60)
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, check=True)
        print("✅ Analysis completed successfully!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {script_name}:")
        print(f"Exit code: {e.returncode}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False
    except FileNotFoundError:
        print(f"❌ Script not found: {script_name}")
        return False

def main():
    """Run the complete MS clinical trials analysis pipeline."""
    print("🧬 MS Warriors Cross-Registry Clinical Trials Analysis Pipeline")
    print("Analyzing Multiple Sclerosis clinical trials funding patterns...")
    print("Datasets: WHO ICTRP (Global) + EU CTIS (European)")
    
    # Ensure charts directory exists
    os.makedirs("charts", exist_ok=True)
    
    # Define analysis pipeline
    analyses = [
        ("analyze_trials.py", "WHO ICTRP Analysis & Top 10 Sponsors"),
        ("funding_insights.py", "WHO Extended Analysis - Geographic, Timeline & Types"),
        ("analyze_dates.py", "WHO Date Range & Temporal Analysis"),
        ("analyze_ctis.py", "EU CTIS Analysis & Regional Patterns"),
        ("analyze_registry_comparison.py", "Cross-Registry Comparative Analysis"),
    ]
    
    successful = 0
    total = len(analyses)
    
    # Run each analysis
    for script, description in analyses:
        if run_analysis_script(script, description):
            successful += 1
        else:
            print(f"⚠️  Continuing with remaining analyses...")
    
    # Final summary
    print(f"\n{'='*60}")
    print(f"🏁 CROSS-REGISTRY ANALYSIS PIPELINE COMPLETE")
    print(f"{'='*60}")
    print(f"✅ Successful: {successful}/{total} analyses")
    
    if successful == total:
        print(f"🎉 All analyses completed successfully!")
        print(f"\n� Generated Charts:")
        chart_files = [f for f in os.listdir("charts") if f.endswith('.png')]
        for chart in sorted(chart_files):
            print(f"   • charts/{chart}")
        
        print(f"\n📋 Analysis Report: ANALYSIS_REPORT.md")
        print(f"\n💡 Key Cross-Registry Findings:")
        print(f"   • WHO ICTRP: 2,482 trials, 1,355 sponsors (24 years)")
        print(f"   • EU CTIS: 104 trials, 50 sponsors (2.5 years)")
        print(f"   • Zero overlap in top 10 sponsors between registries")
        print(f"   • WHO top: Eli Lilly (28 trials, 1.1%)")
        print(f"   • CTIS top: F. Hoffmann-La Roche AG (18 trials, 17.3%)")
        print(f"   • CTIS shows 15x higher sponsor concentration")
        print(f"   • European registry: 60.6% pharmaceutical dominance")
        
    else:
        print(f"⚠️  Some analyses failed. Check error messages above.")
        
    print(f"\n🔬 Cross-registry MS research funding analysis complete!")
    print(f"🌍 Global and European regulatory perspectives analyzed!")

if __name__ == "__main__":
    main()
