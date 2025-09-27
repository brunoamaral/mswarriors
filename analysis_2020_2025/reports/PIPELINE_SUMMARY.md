# MS Clinical Trials Analysis Pipeline Summary

**Timeframe:** 2020-2025
**Execution Time:** 2025-09-27 13:44:01
**Success Rate:** 5/5 (100.0%)

## Execution Results

| Script | Description | Status |
|--------|-------------|---------|
| `scripts/pipeline/analyze_ictrp_2020_2025.py` | WHO ICTRP Analysis (2020-2025) | ✅ SUCCESS |
| `scripts/pipeline/analyze_ctis_2020_2025.py` | EU CTIS Analysis (2020-2025) | ✅ SUCCESS |
| `scripts/pipeline/analyze_clinicaltrials_2020_2025.py` | ClinicalTrials.gov Analysis (2020-2025) | ✅ SUCCESS |
| `scripts/pipeline/create_cross_registry_charts_2020_2025.py` | Cross-Registry Comparison Charts | ✅ SUCCESS |
| `scripts/pipeline/analyze_top_sponsors_recent_trials_2020_2025.py` | Top Sponsors & Recent Trials Analysis | ✅ SUCCESS |

## Generated Outputs

### Charts
- Individual registry analyses with comprehensive visualizations
- Cross-registry comparison charts
- Geographic distribution analyses
- Sponsor analysis and trends
- Timeline and recruitment patterns

### Reports
- Detailed markdown reports for each analysis
- Cross-registry comparison insights
- Top sponsors and recent trials analysis
- Pipeline execution summary

## File Structure
```
analysis_2020_2025/
├── charts/          # All visualization outputs
├── reports/         # Markdown reports and summaries
└── data/           # Processed data outputs (if any)
```