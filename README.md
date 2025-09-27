# MS Clinical Trials Analysis Project

A comprehensive analysis pipeline for Multiple Sclerosis clinical trials data across three major registries: ClinicalTrials.gov, WHO ICTRP, and EU CTIS.

## Quick Start

### Run Complete Analysis Pipeline

```bash
# Run 2020-2025 analysis (recent period)
uv run ms_analysis_pipeline.py --timeframe 2020-2025

# Run 2001-2025 analysis (historical period)
uv run ms_analysis_pipeline.py --timeframe 2001-2025

# Run both timeframes
uv run ms_analysis_pipeline.py --timeframe both

# List available scripts
uv run ms_analysis_pipeline.py --list-scripts
```

### Individual Analyses (Advanced Users)

```bash
# 2020-2025 Recent Period Analysis
uv run analyze_ictrp_2020_2025.py           # WHO ICTRP analysis
uv run analyze_ctis_2020_2025.py            # EU CTIS analysis  
uv run analyze_clinicaltrials_2020_2025.py  # ClinicalTrials.gov analysis
uv run create_cross_registry_charts_2020_2025.py  # Cross-registry comparison
uv run analyze_top_sponsors_recent_trials_2020_2025.py  # Top sponsors analysis

# 2001-2025 Historical Period Analysis  
uv run analyze_clinicaltrials.py            # ClinicalTrials.gov analysis
uv run analyze_ctis.py                      # EU CTIS analysis
uv run analyze_registry_comparison.py       # Registry comparison
```

## Project Structure

```
mswarriors/
├── ms_analysis_pipeline.py              # 🚀 Main pipeline orchestrator
├── README.md                            # This file
├── pyproject.toml                       # Python project configuration
│
├── data/                                # 📊 Source datasets
│   ├── ICTRP-Results.xlsx              # WHO ICTRP data
│   ├── CTIS_trials_20250924.csv        # EU CTIS data
│   └── clinicaltrials_ms_20250925.csv  # ClinicalTrials.gov data
│
├── analysis_2020_2025/                 # 📈 Recent period outputs
│   ├── charts/                         # Generated visualizations
│   └── reports/                        # Analysis reports & summaries
│
├── analysis_2001_2025/                 # 📉 Historical period outputs  
│   ├── charts/                         # Generated visualizations
│   └── reports/                        # Analysis reports & summaries
│
└── scripts/                            # 🛠️ Script organization
    ├── pipeline/                       # Active analysis scripts
    ├── archive/                        # Archived/deprecated scripts
    └── utils/                          # Utility functions
```

## Analysis Components

### 🏥 Registry-Specific Analyses

**WHO ICTRP (International Clinical Trials Registry Platform)**
- Sponsor analysis and trends
- Geographic distribution
- Study type patterns
- Recruitment timelines
- Data completeness assessment

**EU CTIS (Clinical Trial Information System)**  
- European pharmaceutical landscape
- Sponsor type analysis
- Regulatory timeline tracking
- Member state participation

**ClinicalTrials.gov**
- US-focused clinical research
- Industry vs academic sponsors
- Phase distribution analysis  
- Geographic reach assessment

### 🔍 Cross-Registry Comparisons

- Registry size and coverage comparison
- Sponsor overlap analysis
- Geographic distribution differences
- Data quality and completeness
- Temporal trends across platforms

### 👥 Top Sponsors Analysis

- Identification of most active sponsors per registry
- Recent trial portfolio analysis
- Sponsor activity patterns
- Cross-registry sponsor presence

## Key Features

### ✅ Comprehensive Coverage
- **3 Major Registries**: ClinicalTrials.gov, WHO ICTRP, EU CTIS
- **2 Time Periods**: Historical (2001-2025) and Recent (2020-2025)  
- **20+ Visualizations**: Charts, maps, timelines, comparisons
- **Detailed Reports**: Markdown summaries with insights

### ✅ Automated Pipeline
- Single command execution for complete analysis
- Error handling and progress tracking
- Organized output structure
- Reproducible results

### ✅ Data Quality Focus
- Data completeness assessments
- Date validation and filtering
- Missing data handling
- Consistent analysis methodology

## Generated Outputs

### 📊 Charts & Visualizations
- Registry comparison charts
- Geographic distribution maps
- Sponsor analysis charts
- Timeline and trend visualizations
- Phase distribution analysis
- Data completeness assessments

### 📋 Reports & Summaries
- **Individual Registry Reports**: Detailed analysis per registry
- **Cross-Registry Comparison**: Comprehensive comparative analysis
- **Top Sponsors Report**: Most active sponsors and recent trials
- **Pipeline Summary**: Execution status and results overview

### 📈 Key Metrics
- **Total Studies Analyzed**: 6,202 studies (2001-2025)
- **Recent Period Studies**: 2,045 studies (2020-2025) 
- **Registries Covered**: 3 major platforms
- **Countries Analyzed**: 100+ countries worldwide
- **Sponsors Tracked**: 1,000+ unique sponsors

## Data Sources

| Registry | Coverage | Records | Timeframe |
|----------|----------|---------|-----------|
| **ClinicalTrials.gov** | Global (US-focused) | 3,616 MS studies | 2000-2025 |
| **WHO ICTRP** | International | 2,482 MS studies | 2005-2025 |  
| **EU CTIS** | European Union | 104 MS studies | 2023-2025 |

## Technical Requirements

- **Python 3.11+** with UV package manager
- **Required packages**: pandas, matplotlib, seaborn, numpy, openpyxl
- **Memory**: 4GB+ recommended for large datasets
- **Storage**: 1GB+ for outputs and intermediate files

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