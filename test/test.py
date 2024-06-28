import requests
import json

url = 'http://localhost:5002/get_dd'
data = {
    'url': 'https://www.decolar.com/shop/flights/results/roundtrip/BHZ/SAO/2024-07-23/2024-07-27/1/0/0?from=SB&di=1' #replace with the target URL
    #'proxy': 'proxy12345'  # Replace with your proxy , IF RUNNING LOCALHOST, PROXY IS NOT REQUIRED ! 
}

response = requests.post(url, json=data)

if response.status_code == 200:
    response_json = response.json()
    formatted_response = json.dumps(response_json, indent=4)
    print(formatted_response)
else:
    print(f"Failed to get cf-clearance token: {response.text}")
