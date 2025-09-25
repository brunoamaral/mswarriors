#!/usr/bin/env python3
"""
ClinicalTrials.gov API Test Script
Test basic API connectivity and understand the correct field names.
"""

import requests
import json

def test_api_basic():
    """Test basic API call without complex field selection."""
    url = "https://clinicaltrials.gov/api/v2/studies"
    
    # Simple test with just condition and small page size
    params = {
        "query.cond": "multiple sclerosis",
        "format": "json",
        "pageSize": 3,  # Small size for testing
        "countTotal": "true"
    }
    
    print("Testing basic API call...")
    print(f"URL: {url}")
    print(f"Params: {params}")
    
    try:
        response = requests.get(url, params=params, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success! Retrieved {len(data.get('studies', []))} studies")
            print(f"Total count: {data.get('totalCount', 'Not provided')}")
            
            # Show structure of first study
            if data.get("studies"):
                first_study = data["studies"][0]
                print(f"\nFirst study structure (top-level keys):")
                print(json.dumps(list(first_study.keys()), indent=2))
                
                # Show protocol section structure
                if "protocolSection" in first_study:
                    protocol = first_study["protocolSection"]
                    print(f"\nProtocol section keys:")
                    print(json.dumps(list(protocol.keys()), indent=2))
                    
                    # Show identification module
                    if "identificationModule" in protocol:
                        ident = protocol["identificationModule"]
                        print(f"\nIdentification module:")
                        print(json.dumps(ident, indent=2))
            
            return data
        else:
            print(f"Error: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"Exception: {e}")
        return None

def test_metadata():
    """Test the metadata endpoint to understand available fields."""
    url = "https://clinicaltrials.gov/api/v2/studies/metadata"
    
    print("\nTesting metadata endpoint...")
    
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            metadata = response.json()
            print("✅ Metadata retrieved successfully")
            print(f"Total field definitions: {len(metadata)}")
            
            # Show first few field names
            field_names = [field.get('name') for field in metadata[:10] if field.get('name')]
            print(f"Sample field names: {field_names}")
            
            return metadata
        else:
            print(f"Metadata error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Metadata exception: {e}")
        return None

if __name__ == "__main__":
    print("🧪 ClinicalTrials.gov API Test")
    print("=" * 40)
    
    # Test basic API
    data = test_api_basic()
    
    # Test metadata
    metadata = test_metadata()
    
    if data:
        print("\n✅ Basic API test successful!")
    else:
        print("\n❌ Basic API test failed!")
        
    if metadata:
        print("✅ Metadata test successful!")
    else:
        print("❌ Metadata test failed!")