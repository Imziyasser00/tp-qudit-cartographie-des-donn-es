import json
import os
import time
from datetime import date, timedelta

import requests
from kafka import KafkaProducer

TOKEN = os.environ.get("FOOTBALL_API_TOKEN", "8cfcb5f3a3474f23aef1b278fbf14d10")
KAFKA_BROKER = os.environ.get("KAFKA_BROKER", "localhost:9092")
TOPIC = "matches_live"
POLL_INTERVAL_SECONDS = 60

headers = {"X-Auth-Token": TOKEN}
url = "https://api.football-data.org/v4/matches"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)


def fetch_matches():
    date_to = date.today()
    date_from = date_to - timedelta(days=9)  # limite API : 10 jours max
    params = {"dateFrom": date_from.isoformat(), "dateTo": date_to.isoformat()}

    r = requests.get(url, headers=headers, params=params)
    if r.status_code != 200:
        print("Détail erreur API:", r.status_code, r.text)
    r.raise_for_status()
    return r.json().get("matches", [])


def run():
    print(f"Producer démarré. Envoi vers Kafka topic='{TOPIC}' toutes les {POLL_INTERVAL_SECONDS}s.")
    while True:
        try:
            matches = fetch_matches()
            print(f"{len(matches)} matchs récupérés.")
            for match in matches:
                producer.send(TOPIC, value=match)
            producer.flush()
        except requests.RequestException as e:
            print("Erreur API:", e)

        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    run()