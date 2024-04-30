import requests
from requests.exceptions import JSONDecodeError

try:
    response = requests.post(
        "http://0.0.0.0:10001",
        json={
            "query": "https://www.linkedin.com/in/artificially-intelligent/"
        }
    )
    data = response.json()
    print(data)
except JSONDecodeError as e:
    print("Error: Unable to decode JSON response. Response content:", response.content)
