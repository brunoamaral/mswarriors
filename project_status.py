#!/usr/bin/env python3
"""
Project Status Summary
Shows the current organization and status of the MS Clinical Trials Analysis project.
"""

import os
from pathlib import Path

def count_files_in_directory(path, extensions=None):
    """Count files in a directory with optional extension filtering."""
    if not os.path.exists(path):
        return 0
    
    count = 0
    for file in os.listdir(path):
        if extensions:
            if any(file.endswith(ext) for ext in extensions):
                count += 1
        else:
            if os.path.isfile(os.path.join(path, file)):
                count += 1
    return count

def main():
    """Display project status summary."""
    print("📊 MS Clinical Trials Analysis Project Status")
    print("=" * 50)
    
    # Main pipeline
    print("🚀 Main Pipeline:")
    if os.path.exists("ms_analysis_pipeline.py"):
        print("   ✅ ms_analysis_pipeline.py - Main orchestrator")
    else:
        print("   ❌ ms_analysis_pipeline.py - Missing")
    
    # Active analysis scripts
    print("\n📈 Active Analysis Scripts:")
    active_scripts = [
        "scripts/pipeline/analyze_ictrp_2020_2025.py",
        "scripts/pipeline/analyze_ctis_2020_2025.py",
        "scripts/pipeline/analyze_clinicaltrials_2020_2025.py",
        "scripts/pipeline/create_cross_registry_charts_2020_2025.py",
        "scripts/pipeline/analyze_top_sponsors_recent_trials_2020_2025.py",
        "scripts/pipeline/analyze_clinicaltrials.py",
        "scripts/pipeline/analyze_ctis.py",
        "scripts/pipeline/analyze_registry_comparison.py"
    ]
    
    for script in active_scripts:
        script_name = os.path.basename(script)
        if os.path.exists(script):
            print(f"   ✅ {script_name}")
        else:
            print(f"   ❌ {script_name} - Missing")
    
    # Data files
    print("\n📊 Data Files:")
    data_files = [
        "data/ICTRP-Results.xlsx",
        "data/CTIS_trials_20250924.csv", 
        "data/clinicaltrials_ms_20250925.csv"
    ]
    
    for data_file in data_files:
        if os.path.exists(data_file):
            size_mb = os.path.getsize(data_file) / (1024 * 1024)
            print(f"   ✅ {data_file} ({size_mb:.1f}MB)")
        else:
            print(f"   ❌ {data_file} - Missing")
    
    # Output directories and counts
    print("\n📁 Output Directories:")
    
    # 2020-2025 Analysis
    charts_2020 = count_files_in_directory("analysis_2020_2025/charts", [".png", ".jpg", ".jpeg"])
    reports_2020 = count_files_in_directory("analysis_2020_2025/reports", [".md", ".txt"])
    print(f"   📈 analysis_2020_2025/")
    print(f"      📊 charts/: {charts_2020} files")  
    print(f"      📋 reports/: {reports_2020} files")
    
    # 2001-2025 Analysis
    charts_2001 = count_files_in_directory("analysis_2001_2025/charts", [".png", ".jpg", ".jpeg"])
    reports_2001 = count_files_in_directory("analysis_2001_2025/reports", [".md", ".txt"])
    print(f"   📉 analysis_2001_2025/")
    print(f"      📊 charts/: {charts_2001} files")
    print(f"      📋 reports/: {reports_2001} files")
    
    # Script organization
    print("\n🛠️  Script Organization:")
    pipeline_count = count_files_in_directory("scripts/pipeline", [".py"])
    archive_count = count_files_in_directory("scripts/archive", [".py"])
    utils_count = count_files_in_directory("scripts/utils", [".py"])
    
    print(f"   📦 scripts/pipeline/: {pipeline_count} scripts")
    print(f"   🗄️  scripts/archive/: {archive_count} scripts")  
    print(f"   🔧 scripts/utils/: {utils_count} scripts")
    
    # Summary statistics
    total_charts = charts_2020 + charts_2001
    total_reports = reports_2020 + reports_2001
    total_archived = archive_count
    
    print(f"\n📊 Summary Statistics:")
    print(f"   • Total Charts Generated: {total_charts}")
    print(f"   • Total Reports Generated: {total_reports}")
    print(f"   • Scripts Archived: {total_archived}")
    print(f"   • Active Pipeline Scripts: {len(active_scripts)}")
    
    # Quick start reminder
    print(f"\n🚀 Quick Start:")
    print(f"   uv run ms_analysis_pipeline.py --timeframe 2020-2025")
    print(f"   uv run ms_analysis_pipeline.py --list-scripts")

if __name__ == "__main__":
    main()