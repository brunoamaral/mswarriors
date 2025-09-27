#!/usr/bin/env python3
"""
ClinicalTrials.gov API Data Fetcher
Fetches Multiple Sclerosis clinical trials data from ClinicalTrials.gov API v2
and saves it for analysis alongside WHO ICTRP and EU CTIS data.
"""

import requests
import json
import pandas as pd
import time
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

# API Configuration
CLINICALTRIALS_API_BASE = "https://clinicaltrials.gov/api/v2"
MS_CONDITION_QUERY = "multiple sclerosis"
OUTPUT_DIR = "data"

def ensure_data_directory():
    """Create data directory if it doesn't exist."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created {OUTPUT_DIR} directory")

def fetch_studies_page(page_token: Optional[str] = None, page_size: int = 1000) -> Dict[str, Any]:
    """
    Fetch a single page of studies from ClinicalTrials.gov API.
    
    Args:
        page_token: Token for pagination (None for first page)
        page_size: Number of studies per page (max 1000)
    
    Returns:
        API response as dictionary
    """
    url = f"{CLINICALTRIALS_API_BASE}/studies"
    
    # Parameters for MS clinical trials
    params = {
        "query.cond": MS_CONDITION_QUERY,
        "format": "json",
        "pageSize": page_size,
        "countTotal": "true" if not page_token else "false",  # Only count total on first page
        # Note: Not specifying fields to get all available data initially
    }
    
    if page_token:
        params["pageToken"] = page_token
    
    print(f"Fetching page {'(first)' if not page_token else f'(token: {page_token[:20]}...)'}")
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        studies_count = len(data.get("studies", []))
        print(f"  Retrieved {studies_count} studies")
        
        return data
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from ClinicalTrials.gov API: {e}")
        raise
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        raise

def fetch_all_ms_studies() -> List[Dict[str, Any]]:
    """
    Fetch all Multiple Sclerosis studies from ClinicalTrials.gov API.
    
    Returns:
        List of all MS studies
    """
    print("Starting to fetch Multiple Sclerosis trials from ClinicalTrials.gov...")
    print(f"Condition query: '{MS_CONDITION_QUERY}'")
    
    all_studies = []
    page_token = None
    page_count = 0
    
    while True:
        page_count += 1
        print(f"\nFetching page {page_count}...")
        
        try:
            # Add delay to be respectful to the API
            if page_count > 1:
                time.sleep(1)  # 1 second delay between requests
            
            page_data = fetch_studies_page(page_token)
            
            studies = page_data.get("studies", [])
            all_studies.extend(studies)
            
            # Show total count from first page
            if page_count == 1:
                total_count = page_data.get("totalCount")
                if total_count:
                    print(f"Total studies available: {total_count}")
            
            # Check for next page
            page_token = page_data.get("nextPageToken")
            if not page_token:
                print("No more pages to fetch")
                break
                
        except Exception as e:
            print(f"Error on page {page_count}: {e}")
            break
    
    print(f"\n✅ Completed fetching {len(all_studies)} studies across {page_count} pages")
    return all_studies

def flatten_study_data(study: Dict[str, Any]) -> Dict[str, Any]:
    """
    Flatten nested study data structure for easier analysis.
    
    Args:
        study: Raw study data from API
    
    Returns:
        Flattened study data dictionary
    """
    flat_data = {}
    
    # Helper function to safely get nested values
    def safe_get(obj, *keys):
        for key in keys:
            if isinstance(obj, dict) and key in obj:
                obj = obj[key]
            else:
                return None
        return obj
    
    # Basic identification
    flat_data["NCTId"] = safe_get(study, "protocolSection", "identificationModule", "nctId")
    flat_data["BriefTitle"] = safe_get(study, "protocolSection", "identificationModule", "briefTitle")
    flat_data["OfficialTitle"] = safe_get(study, "protocolSection", "identificationModule", "officialTitle")
    
    # Status and dates
    flat_data["OverallStatus"] = safe_get(study, "protocolSection", "statusModule", "overallStatus")
    flat_data["StartDate"] = safe_get(study, "protocolSection", "statusModule", "startDateStruct", "date")
    flat_data["PrimaryCompletionDate"] = safe_get(study, "protocolSection", "statusModule", "primaryCompletionDateStruct", "date")
    flat_data["CompletionDate"] = safe_get(study, "protocolSection", "statusModule", "completionDateStruct", "date")
    flat_data["LastUpdatePostDate"] = safe_get(study, "protocolSection", "statusModule", "lastUpdatePostDateStruct", "date")
    flat_data["StudyFirstPostDate"] = safe_get(study, "protocolSection", "statusModule", "studyFirstPostDateStruct", "date")
    
    # Study design
    flat_data["StudyType"] = safe_get(study, "protocolSection", "designModule", "studyType")
    phases = safe_get(study, "protocolSection", "designModule", "phases")
    flat_data["Phase"] = "|".join(phases) if phases else None
    
    # Enrollment
    flat_data["EnrollmentCount"] = safe_get(study, "protocolSection", "designModule", "enrollmentInfo", "count")
    flat_data["EnrollmentType"] = safe_get(study, "protocolSection", "designModule", "enrollmentInfo", "type")
    
    # Sponsors
    flat_data["LeadSponsorName"] = safe_get(study, "protocolSection", "sponsorCollaboratorsModule", "leadSponsor", "name")
    flat_data["LeadSponsorClass"] = safe_get(study, "protocolSection", "sponsorCollaboratorsModule", "leadSponsor", "class")
    
    # Collaborators
    collaborators = safe_get(study, "protocolSection", "sponsorCollaboratorsModule", "collaborators")
    if collaborators:
        collab_names = [c.get("name") for c in collaborators if c.get("name")]
        flat_data["Collaborators"] = "|".join(collab_names) if collab_names else None
        collab_classes = [c.get("class") for c in collaborators if c.get("class")]
        flat_data["CollaboratorClasses"] = "|".join(collab_classes) if collab_classes else None
    else:
        flat_data["Collaborators"] = None
        flat_data["CollaboratorClasses"] = None
    
    # Conditions
    conditions = safe_get(study, "protocolSection", "conditionsModule", "conditions")
    flat_data["Conditions"] = "|".join(conditions) if conditions else None
    
    # Keywords
    keywords = safe_get(study, "protocolSection", "conditionsModule", "keywords")
    flat_data["Keywords"] = "|".join(keywords) if keywords else None
    
    # Locations (first location for country/city/state)
    locations = safe_get(study, "protocolSection", "contactsLocationsModule", "locations")
    if locations and len(locations) > 0:
        first_location = locations[0]
        flat_data["LocationCountry"] = safe_get(first_location, "country")
        flat_data["LocationCity"] = safe_get(first_location, "city") 
        flat_data["LocationState"] = safe_get(first_location, "state")
        flat_data["TotalLocations"] = len(locations)
    else:
        flat_data["LocationCountry"] = None
        flat_data["LocationCity"] = None
        flat_data["LocationState"] = None
        flat_data["TotalLocations"] = 0
    
    # Interventions
    interventions = safe_get(study, "protocolSection", "armsInterventionsModule", "interventions")
    if interventions:
        intervention_names = [i.get("name") for i in interventions if i.get("name")]
        intervention_types = [i.get("type") for i in interventions if i.get("type")]
        flat_data["InterventionNames"] = "|".join(intervention_names) if intervention_names else None
        flat_data["InterventionTypes"] = "|".join(intervention_types) if intervention_types else None
    else:
        flat_data["InterventionNames"] = None
        flat_data["InterventionTypes"] = None
    
    # Outcomes
    primary_outcomes = safe_get(study, "protocolSection", "outcomesModule", "primaryOutcomes")
    if primary_outcomes:
        primary_measures = [o.get("measure") for o in primary_outcomes if o.get("measure")]
        flat_data["PrimaryOutcomeMeasures"] = "|".join(primary_measures) if primary_measures else None
    else:
        flat_data["PrimaryOutcomeMeasures"] = None
    
    secondary_outcomes = safe_get(study, "protocolSection", "outcomesModule", "secondaryOutcomes")
    if secondary_outcomes:
        secondary_measures = [o.get("measure") for o in secondary_outcomes if o.get("measure")]
        flat_data["SecondaryOutcomeMeasures"] = "|".join(secondary_measures) if secondary_measures else None
    else:
        flat_data["SecondaryOutcomeMeasures"] = None
    
    # Results availability
    flat_data["HasResults"] = study.get("hasResults", False)
    flat_data["ResultsFirstPostDate"] = safe_get(study, "protocolSection", "statusModule", "resultsFirstPostDateStruct", "date")
    
    return flat_data

def save_data(studies: List[Dict[str, Any]], format_type: str = "both") -> str:
    """
    Save fetched studies data to files.
    
    Args:
        studies: List of study dictionaries
        format_type: "json", "csv", or "both"
    
    Returns:
        Path to saved file(s)
    """
    ensure_data_directory()
    
    # Generate timestamp for filename
    timestamp = datetime.now().strftime("%Y%m%d")
    
    saved_files = []
    
    if format_type in ["json", "both"]:
        json_filename = f"{OUTPUT_DIR}/clinicaltrials_ms_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(studies, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved raw JSON data: {json_filename}")
        saved_files.append(json_filename)
    
    if format_type in ["csv", "both"]:
        # Flatten all studies for CSV
        print("Flattening study data for CSV format...")
        flat_studies = [flatten_study_data(study) for study in studies]
        
        df = pd.DataFrame(flat_studies)
        csv_filename = f"{OUTPUT_DIR}/clinicaltrials_ms_{timestamp}.csv"
        df.to_csv(csv_filename, index=False, encoding='utf-8')
        
        print(f"✅ Saved flattened CSV data: {csv_filename}")
        print(f"CSV contains {len(df)} studies with {len(df.columns)} columns")
        print(f"Columns: {list(df.columns)}")
        saved_files.append(csv_filename)
    
    return saved_files

def main():
    """Main execution function."""
    print("🏥 ClinicalTrials.gov MS Data Fetcher")
    print("=" * 50)
    
    try:
        # Fetch all MS studies
        studies = fetch_all_ms_studies()
        
        if not studies:
            print("❌ No studies retrieved. Exiting.")
            return
        
        # Save data in both formats
        saved_files = save_data(studies, format_type="both")
        
        # Summary statistics
        print(f"\n📊 FETCH SUMMARY:")
        print(f"• Total MS studies retrieved: {len(studies)}")
        print(f"• Data source: ClinicalTrials.gov API v2")
        print(f"• Search query: '{MS_CONDITION_QUERY}'")
        print(f"• Files saved: {len(saved_files)}")
        for file_path in saved_files:
            print(f"  - {file_path}")
        
        print(f"\n✅ ClinicalTrials.gov data fetch completed successfully!")
        print(f"Ready for analysis alongside WHO ICTRP and EU CTIS data.")
        
    except Exception as e:
        print(f"❌ Error during data fetch: {e}")
        raise

if __name__ == "__main__":
    main()