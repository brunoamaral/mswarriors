# CTIS Sponsor Type Grouping Strategy

## Problem Identified
The original CTIS sponsor type pie chart had garbled text due to:
- 5 categories under 3% threshold causing cramped labels
- Duplicate entries (e.g., "Pharmaceutical company, Pharmaceutical company")
- Inconsistent naming conventions

## Original Distribution (8 categories)
1. **Pharmaceutical company**: 63 trials (60.6%)
2. **Hospital/Clinic/Other health care facility**: 30 trials (28.8%)
3. **Laboratory/Research/Testing facility**: 4 trials (3.8%)
4. **Educational Institution**: 3 trials (2.9%)
5. **Hospital/Clinic/Other health care facility, Hospital/Clinic/Other health care facility**: 1 trial (1.0%) *[duplicate]*
6. **Health care**: 1 trial (1.0%)
7. **Patient organisation/association**: 1 trial (1.0%)
8. **Pharmaceutical company, Pharmaceutical company**: 1 trial (1.0%) *[duplicate]*

## Solution: 3-Category Grouping
1. **Pharmaceutical Company**: 64 trials (61.5%)
   - Combined "Pharmaceutical company" (63) + "Pharmaceutical company, Pharmaceutical company" (1)
   
2. **Hospital/Clinic/Healthcare**: 31 trials (29.8%)
   - Combined "Hospital/Clinic/Other health care facility" (30) + duplicate entry (1)
   
3. **Academic/Research/Other**: 9 trials (8.7%)
   - Combined all categories under 3%:
     - Laboratory/Research/Testing facility (4 trials)
     - Educational Institution (3 trials)
     - Health care (1 trial)
     - Patient organisation/association (1 trial)

## Benefits Achieved
✅ **Clean visualization**: No more cramped/garbled text
✅ **Logical grouping**: Similar sponsor types combined
✅ **Clear percentages**: All categories above 8% for readable labels
✅ **Duplicate cleanup**: Removed redundant entries
✅ **Consistency**: Matches analysis narrative and conclusions

## Chart Improvements
- Better color palette for distinction
- Larger, bold text for readability
- Added summary annotation showing pharmaceutical dominance
- Corrected total count (104 trials vs previous 131 error)

The updated chart now clearly shows the 3-way split in CTIS funding with clean, readable labels.