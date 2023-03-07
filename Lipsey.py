import requests
import csv
import shutil

url = "https://api.lipseys.com/api/Integration/Authentication/Login"
headers = {"Content-Type": "application/json"}
data = {"Email": "brye@4csgunworks.com", "Password": "65Creedmoor!"}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 200:
    token = response.json()["token"]
else:
    print(response.status_code)

headers = {"Token": token}
response = requests.get("https://api.lipseys.com/api/Integration/Items/PricingQuantityFeed", headers=headers)

if response.status_code == 200:
    data = response.json()
    items = data["data"]["items"]
    
    with open("Lipseys.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["itemNumber", "upc", "mfgModelNumber", "quantity", "allocated", "onSale", "price", "currentPrice", "retailMap"])
        writer.writeheader()
        for item in items:
            writer.writerow(item)

   
else:
    raise Exception(f"Request failed with status code {response.status_code}")

src_path = "./Lipseys.csv"
dst_path = "./Result/"
shutil.copy(src_path, dst_path)
