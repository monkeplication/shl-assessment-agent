# To get the catalog json 
import requests

url = "https://tcp-us-prod-rnd.shl.com/voiceRater/shl-ai-hiring/shl_product_catalog.json"

response = requests.get(url, timeout=30)
response.raise_for_status()

print(response.status_code)
print(response.headers.get("Content-Type"))

with open("data/catalog.json", "wb") as f:
    f.write(response.content)

print("Saved to data/catalog.json")