import requests
import json

url = "https://www.onemap.gov.sg/api/public/popapi/getAllPlanningarea?year=2019"
headers = {"Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjNmI2ZjlkODk0ODA2OGQ1ZDk4NTk2YTIwODA2ODI3MSIsImlzcyI6Imh0dHA6Ly9pbnRlcm5hbC1hbGItb20tcHJkZXppdC1pdC1uZXctMTYzMzc5OTU0Mi5hcC1zb3V0aGVhc3QtMS5lbGIuYW1hem9uYXdzLmNvbS9hcGkvdjIvdXNlci9wYXNzd29yZCIsImlhdCI6MTc0MTI1MjI2OCwiZXhwIjoxNzQxNTExNDY4LCJuYmYiOjE3NDEyNTIyNjgsImp0aSI6IjduS1FTeEtQSlBMQTBHQ1giLCJ1c2VyX2lkIjo1OTA4LCJmb3JldmVyIjpmYWxzZX0.jqS-0-V-0_3Y1zDZyEPzps6f_-DHzBSRLBDNkXznDFs"}
response = requests.request("GET", url, headers=headers)

data = response.json()

geojson_data = {"type": "FeatureCollection", "features": []}

for result in data["SearchResults"]:
    geojson_feature = {
        "type": "Feature",
        "properties": {"town": result["pln_area_n"]}, 
        "geometry": json.loads(result["geojson"]) 
    }
    geojson_data["features"].append(geojson_feature)

with open("data/singapore_town_boundaries.json", "w") as f:
    json.dump(geojson_data, f)

print("GeoJSON file saved as singapore_town_boundaries.json")
