# MS Clinical Trials Analysis Pipeline Summary

**Timeframe:** 2001-2025
**Execution Time:** 2025-09-27 13:44:36
**Success Rate:** 3/3 (100.0%)

## Execution Results

| Script | Description | Status |
|--------|-------------|---------|
| `scripts/pipeline/analyze_clinicaltrials.py` | ClinicalTrials.gov Analysis (2001-2025) | ✅ SUCCESS |
| `scripts/pipeline/analyze_ctis.py` | EU CTIS Analysis (2001-2025) | ✅ SUCCESS |
| `scripts/pipeline/analyze_registry_comparison.py` | Registry Comparison Analysis (2001-2025) | ✅ SUCCESS |

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
analysis_2001_2025/
├── charts/          # All visualization outputs
├── reports/         # Markdown reports and summaries
└── data/           # Processed data outputs (if any)
```