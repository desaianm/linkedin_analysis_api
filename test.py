import requests
from requests.exceptions import JSONDecodeError

try:
    response = requests.post(
        "https://linkedin-analysis-api.onrender.com",
        json={
            "query": "https://www.linkedin.com/in/artificially-intelligent/"
        }
    )
    data = response.json()
    print(data)
except JSONDecodeError as e:
    print("Error: Unable to decode JSON response. Response content:", response.content)
