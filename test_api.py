import requests

url = "http://127.0.0.1:5000/process"

data = {
    "query": "Explain Artificial Intelligence"
}

try:
    response = requests.post(url, json=data, timeout=300)

    print("Status Code:", response.status_code)

    result = response.json()

    print("\n--- RESEARCH ---")
    print(result.get("research"))

    print("\n--- SUMMARY ---")
    print(result.get("summary"))

    print("\n--- EMAIL ---")
    print(result.get("email"))

except Exception as e:
    print("Error:", e)