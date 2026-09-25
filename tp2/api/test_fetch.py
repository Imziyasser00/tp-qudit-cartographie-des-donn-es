import requests
import os

TOKEN = os.environ.get("FOOTBALL_API_TOKEN", "8cfcb5f3a3474f23aef1b278fbf14d10")

headers = {"X-Auth-Token": TOKEN}
url = "https://api.football-data.org/v4/matches"

params = {
    "dateFrom": "2026-09-20",
    "dateTo": "2026-09-29"
}

r = requests.get(url, headers=headers, params=params)
print("Status:", r.status_code)
data = r.json()
print("Nombre de matchs:", len(data.get("matches", [])))
if data.get("matches"):
    print(data["matches"][0])
else:
    print("Réponse brute:", data)



statuses = set()
has_venue = 0
for m in data["matches"]:
    statuses.add(m["status"])
    if m.get("venue"):
        has_venue += 1

print("Statuts rencontrés:", statuses)
print("Matchs avec venue:", has_venue, "/", len(data["matches"]))