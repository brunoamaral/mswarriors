#!/usr/bin/env python3
"""
MS Clinical Trials Analysis Pipeline
====================================

Unified pipeline for comprehensive analysis of Multiple Sclerosis clinical trials
across three registries: ClinicalTrials.gov, WHO ICTRP, and EU CTIS.

This pipeline supports both historical (2001-2025) and recent (2020-2025) timeframe analyses.

Usage:
    python ms_analysis_pipeline.py --timeframe 2020-2025
    python ms_analysis_pipeline.py --timeframe 2001-2025
    python ms_analysis_pipeline.py --timeframe both

Features:
- Individual registry analyses with comprehensive charts
- Cross-registry comparisons
- Top sponsors and recent trials analysis
- Automated report generation
- Organized output structure
"""

import argparse
import subprocess
import sys
import os
from datetime import datetime
import json

class MSAnalysisPipeline:
    """Main pipeline orchestrator for MS clinical trials analysis."""
    
    def __init__(self, timeframe="2020-2025"):
        self.timeframe = timeframe
        self.output_base = f"analysis_{timeframe.replace('-', '_')}"
        self.ensure_output_directories()
        
    def ensure_output_directories(self):
        """Create necessary output directories."""
        dirs = [
            f"{self.output_base}/charts",
            f"{self.output_base}/reports",
            f"{self.output_base}/data"
        ]
        for dir_path in dirs:
            os.makedirs(dir_path, exist_ok=True)
        print(f"✓ Output directories ready for {self.timeframe} analysis")
    
    def run_script(self, script_name, description):
        """Run a Python script and handle errors."""
        print(f"\\n🔄 {description}...")
        try:
            result = subprocess.run([sys.executable, script_name], 
                                 capture_output=True, text=True, check=True)
            print(f"✅ {description} completed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ {description} failed:")
            print(f"Error: {e.stderr}")
            return False
        except FileNotFoundError:
            print(f"❌ Script {script_name} not found")
            return False
    
    def get_2020_2025_scripts(self):
        """Get list of scripts for 2020-2025 analysis."""
        return [
            ("scripts/pipeline/analyze_ictrp_2020_2025.py", "WHO ICTRP Analysis (2020-2025)"),
            ("scripts/pipeline/analyze_ctis_2020_2025.py", "EU CTIS Analysis (2020-2025)"), 
            ("scripts/pipeline/analyze_clinicaltrials_2020_2025.py", "ClinicalTrials.gov Analysis (2020-2025)"),
            ("scripts/pipeline/create_cross_registry_charts_2020_2025.py", "Cross-Registry Comparison Charts"),
            ("scripts/pipeline/analyze_top_sponsors_recent_trials_2020_2025.py", "Top Sponsors & Recent Trials Analysis")
        ]
    
    def run_2020_2025_analysis(self):
        """Run complete 2020-2025 analysis pipeline."""
        print(f"🚀 Starting MS Clinical Trials Analysis Pipeline - 2020-2025")
        print("=" * 70)
        
        scripts_to_run = self.get_2020_2025_scripts()
        
        results = []
        for script, description in scripts_to_run:
            success = self.run_script(script, description)
            results.append((script, description, success))
        
        self.generate_pipeline_summary(results, "2020-2025")
        return results
    
    def run_2001_2025_analysis(self):
        """Run complete 2001-2025 analysis pipeline."""
        print(f"🚀 Starting MS Clinical Trials Analysis Pipeline - 2001-2025")
        print("=" * 70)
        
        # For 2001-2025, we need to use the original analysis scripts
        scripts_to_run = [
            ("scripts/pipeline/analyze_clinicaltrials.py", "ClinicalTrials.gov Analysis (2001-2025)"),
            ("scripts/pipeline/analyze_ctis.py", "EU CTIS Analysis (2001-2025)"),
            ("scripts/pipeline/analyze_registry_comparison.py", "Registry Comparison Analysis (2001-2025)")
        ]
        
        results = []
        for script, description in scripts_to_run:
            success = self.run_script(script, description)
            results.append((script, description, success))
        
        self.generate_pipeline_summary(results, "2001-2025")
        return results
    
    def generate_pipeline_summary(self, results, timeframe):
        """Generate a summary report of the pipeline execution."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        summary = {
            "pipeline_execution": {
                "timeframe": timeframe,
                "execution_time": timestamp,
                "total_scripts": len(results),
                "successful": sum(1 for _, _, success in results if success),
                "failed": sum(1 for _, _, success in results if not success)
            },
            "script_results": [
                {
                    "script": script,
                    "description": desc,
                    "status": "SUCCESS" if success else "FAILED"
                }
                for script, desc, success in results
            ]
        }
        
        # Save JSON summary
        summary_path = f"analysis_{timeframe.replace('-', '_')}/reports/pipeline_summary.json"
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        # Generate markdown summary
        md_content = self.create_markdown_summary(summary, timeframe)
        md_path = f"analysis_{timeframe.replace('-', '_')}/reports/PIPELINE_SUMMARY.md"
        with open(md_path, 'w') as f:
            f.write(md_content)
        
        print(f"\\n📊 Pipeline Summary:")
        print(f"   • Total scripts: {summary['pipeline_execution']['total_scripts']}")
        print(f"   • Successful: {summary['pipeline_execution']['successful']}")
        print(f"   • Failed: {summary['pipeline_execution']['failed']}")
        print(f"   • Summary saved: {md_path}")
    
    def create_markdown_summary(self, summary, timeframe):
        """Create a markdown summary of pipeline execution."""
        content = [
            f"# MS Clinical Trials Analysis Pipeline Summary",
            f"",
            f"**Timeframe:** {timeframe}",
            f"**Execution Time:** {summary['pipeline_execution']['execution_time']}",
            f"**Success Rate:** {summary['pipeline_execution']['successful']}/{summary['pipeline_execution']['total_scripts']} ({(summary['pipeline_execution']['successful']/summary['pipeline_execution']['total_scripts']*100):.1f}%)",
            f"",
            f"## Execution Results",
            f"",
            f"| Script | Description | Status |",
            f"|--------|-------------|---------|"
        ]
        
        for result in summary['script_results']:
            status_emoji = "✅" if result['status'] == "SUCCESS" else "❌"
            content.append(f"| `{result['script']}` | {result['description']} | {status_emoji} {result['status']} |")
        
        content.extend([
            f"",
            f"## Generated Outputs",
            f"",
            f"### Charts",
            f"- Individual registry analyses with comprehensive visualizations",
            f"- Cross-registry comparison charts", 
            f"- Geographic distribution analyses",
            f"- Sponsor analysis and trends",
            f"- Timeline and recruitment patterns",
            f"",
            f"### Reports",
            f"- Detailed markdown reports for each analysis",
            f"- Cross-registry comparison insights",
            f"- Top sponsors and recent trials analysis",
            f"- Pipeline execution summary",
            f"",
            f"## File Structure",
            f"```",
            f"analysis_{timeframe.replace('-', '_')}/",
            f"├── charts/          # All visualization outputs",
            f"├── reports/         # Markdown reports and summaries", 
            f"└── data/           # Processed data outputs (if any)",
            f"```"
        ])
        
        return "\\n".join(content)
    
    def run_full_pipeline(self):
        """Run the appropriate analysis pipeline based on timeframe."""
        if self.timeframe == "2020-2025":
            return self.run_2020_2025_analysis()
        elif self.timeframe == "2001-2025":
            return self.run_2001_2025_analysis()
        elif self.timeframe == "both":
            print("🚀 Running Both Timeframe Analyses")
            print("=" * 50)
            
            # Run 2020-2025 analysis
            self.timeframe = "2020-2025"
            self.output_base = "analysis_2020_2025"
            self.ensure_output_directories()
            results_2020 = self.run_2020_2025_analysis()
            
            print("\\n" + "="*50)
            
            # Run 2001-2025 analysis
            self.timeframe = "2001-2025" 
            self.output_base = "analysis_2001_2025"
            self.ensure_output_directories()
            results_2001 = self.run_2001_2025_analysis()
            
            return results_2020 + results_2001
        else:
            print(f"❌ Unsupported timeframe: {self.timeframe}")
            print("Supported timeframes: 2020-2025, 2001-2025, both")
            return []

def main():
    """Main entry point for the pipeline."""
    parser = argparse.ArgumentParser(
        description="MS Clinical Trials Analysis Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python ms_analysis_pipeline.py --timeframe 2020-2025
  python ms_analysis_pipeline.py --timeframe 2001-2025  
  python ms_analysis_pipeline.py --timeframe both
        """
    )
    
    parser.add_argument(
        "--timeframe", 
        choices=["2020-2025", "2001-2025", "both"],
        default="2020-2025",
        help="Analysis timeframe (default: 2020-2025)"
    )
    
    parser.add_argument(
        "--list-scripts",
        action="store_true", 
        help="List all available analysis scripts"
    )
    
    args = parser.parse_args()
    
    if args.list_scripts:
        print("Available Analysis Scripts:")
        print("=" * 30)
        print("2020-2025 Timeframe:")
        scripts_2020 = [
            "analyze_ictrp_2020_2025.py - WHO ICTRP Analysis",
            "analyze_ctis_2020_2025.py - EU CTIS Analysis", 
            "analyze_clinicaltrials_2020_2025.py - ClinicalTrials.gov Analysis",
            "create_cross_registry_charts_2020_2025.py - Cross-Registry Comparisons",
            "analyze_top_sponsors_recent_trials_2020_2025.py - Top Sponsors Analysis"
        ]
        for script in scripts_2020:
            print(f"  • {script}")
        
        print("\\n2001-2025 Timeframe:")
        scripts_2001 = [
            "analyze_clinicaltrials.py - ClinicalTrials.gov Analysis",
            "analyze_ctis.py - EU CTIS Analysis",
            "analyze_registry_comparison.py - Registry Comparison"
        ]
        for script in scripts_2001:
            print(f"  • {script}")
        return
    
    # Run the pipeline
    pipeline = MSAnalysisPipeline(args.timeframe)
    results = pipeline.run_full_pipeline()
    
    # Final summary
    successful = sum(1 for _, _, success in results if success)
    total = len(results)
    
    print(f"\\n🎉 Pipeline Execution Complete!")
    print(f"📊 Results: {successful}/{total} scripts executed successfully")
    
    if successful < total:
        print("⚠️  Some scripts failed - check the logs above for details")
        sys.exit(1)
    else:
        print("✅ All analyses completed successfully!")

if __name__ == "__main__":
    main()