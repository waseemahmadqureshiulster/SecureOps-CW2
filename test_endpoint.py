import urllib.request
import json
import os
import ssl

def allowSelfSignedHttps(allowed):
    # Bypass certificate verification (useful for some dev environments)
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True)

# ---------------------------------------------------------
# 1. CONFIGURATION (Paste your details here)
# ---------------------------------------------------------

# Run this in terminal to get URL: 
# az ml online-endpoint show --name secureops-endpoint-xheik01 --query scoring_uri -o tsv
url = 'https://secureops-endpoint-xheik01.germanywestcentral.inference.ml.azure.com/score'

# Run this in terminal to get Key: 
# az ml online-endpoint get-credentials --name secureops-endpoint-xheik01 --query primaryKey -o tsv
api_key = '799HB9HKOCtYuDvLJNW6X41iILBbikPRTIVDjEZTbQMJYhX74XLMJQQJ99BLAAAAAAAAAAAAINFRAZML3N47' 

# ---------------------------------------------------------
# 2. PREPARE DATA
# ---------------------------------------------------------

# This data mimics a single row from your CIDDS dataset.
# The model expects: Duration, Packets, Bytes, Proto, Flags
data = {
    "data": [
        {
            "Duration": 0.25,
            "Packets": 10,
            "Bytes": 1000,
            "Proto": "TCP",
            "Flags": ".AP..."
        }
    ]
}

# Convert dictionary to JSON string and then to bytes
body = str.encode(json.dumps(data))

# ---------------------------------------------------------
# 3. SEND REQUEST
# ---------------------------------------------------------

# The header must include the Authorization Bearer token
headers = {
    'Content-Type': 'application/json', 
    'Authorization': ('Bearer ' + api_key), 
    'azureml-model-deployment': 'final-deployment' 
}

req = urllib.request.Request(url, body, headers)

try:
    print("Sending request to Azure Endpoint...")
    response = urllib.request.urlopen(req)
    result = response.read()
    
    # Decode result
    decoded_result = result.decode("utf8")
    print("\n------------------------------------------------")
    print(f"SUCCESS! Prediction received: {decoded_result}")
    print("------------------------------------------------")
    
    if "0" in decoded_result:
        print("Interpretation: Normal Traffic")
    elif "1" in decoded_result:
        print("Interpretation: Attack Detected")
        
except urllib.error.HTTPError as error:
    print(f"The request failed with status code: {error.code}")
    print(error.info())
    print(json.loads(error.read().decode("utf8", 'ignore')))