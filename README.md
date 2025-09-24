# Multiple Sclerosis Clinical Trials Analysis

Analysis of clinical trials registered on the WHO International Clinical Trials Registry Platform (ICTRP) to identify top sponsors and funding patterns in Multiple Sclerosis research.

## Data Sources

### WHO ICTRP

Data was extracted from the WHO International Clinical Trials Registry Platform (ICTRP) using the Trial Search portal (https://trialsearch.who.int/).

**Search Parameters:**
- **Search URL**: https://trialsearch.who.int/AdvSearch.aspx
- **Condition field**: Multiple Sclerosis
- **Status field**: ALL
- **Recruiting Status**: ALL
- **Export date**: 09/23/2025 01:00:09
- **Results**: 2,482 studies

The exported files are:
- `data/ICTRP-Results.xml` (XML format)
- `data/ICTRP-Results.xlsx` (Excel format)

### EU CTIS

**Search Parameters:**
- **Search URL**: https://euclinicaltrials.eu/search-for-clinical-trials/?lang=en
- **Condition field**: multiple sclerosis




## Quick Start

This project uses [uv](https://docs.astral.sh/uv/) for Python package management.

### Run Complete Analysis

```bash
uv run main.py
```

This will:
1. Analyze all 2,482 clinical trials
2. Identify top 10 sponsors
3. Generate 5 professional visualizations
4. Create a comprehensive analysis report

### Run Individual Analyses

```bash
# Basic sponsor analysis
uv run analyze_trials.py

# Comprehensive funding insights
uv run funding_insights.py
```

## Key Findings

- **2,482 total trials** analyzed across 1,355 unique sponsors
- **Eli Lilly and Company** is the top sponsor (28 trials)
- **United States** leads geographically (745 trials, 30%)
- **High fragmentation**: Top 10 sponsors represent only 7.6% of trials
- **474 trials** registered since 2020, showing continued research investment

## Generated Visualizations

The analysis creates 6 publication-ready charts in the `charts/` directory:

1. **`charts/top_sponsors_chart.png`** - Top 10 clinical trial sponsors
2. **`charts/geographic_distribution.png`** - Global distribution by country
3. **`charts/phase_distribution.png`** - Trial phases breakdown
4. **`charts/sponsor_types.png`** - Analysis by sponsor category
5. **`charts/recruitment_timeline.png`** - Registration trends over time
6. **`charts/sponsor_data_completeness.png`** - Data quality assessment

## Dependencies

The project automatically manages dependencies using uv:

- pandas (data manipulation)
- matplotlib (plotting) 
- seaborn (statistical visualization)
- openpyxl (Excel file handling)
- lxml (XML parsing)

## Project Structure

```
mswarriors/
├── charts/                        # Generated visualizations
│   ├── top_sponsors_chart.png          # Top 10 sponsors bar chart
│   ├── geographic_distribution.png     # Country distribution
│   ├── phase_distribution.png          # Trial phases pie chart
│   ├── sponsor_types.png               # Sponsor category analysis
│   ├── recruitment_timeline.png        # Registration timeline
│   └── sponsor_data_completeness.png   # Data quality assessment
├── data/
│   ├── ICTRP-Results.xml          # Raw XML data
│   └── ICTRP-Results.xlsx         # Raw Excel data
├── main.py                        # Main analysis runner
├── analyze_trials.py              # Core sponsor analysis
├── funding_insights.py            # Extended funding patterns
├── ANALYSIS_REPORT.md             # Comprehensive findings report
└── pyproject.toml                 # Project configuration
```

## Usage for Blog Posts

All generated PNG files in the `charts/` directory are high-resolution (300 DPI) and optimized for web publication. The `ANALYSIS_REPORT.md` contains detailed findings, methodology, and insights suitable for blog content.

## Technical Notes

- Built with Python 3.13 and uv package management
- Handles both XML and Excel data formats (Excel preferred for analysis)
- Implements robust data cleaning and sponsor name standardization
- Includes comprehensive error handling and progress reporting