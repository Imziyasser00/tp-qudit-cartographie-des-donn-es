import time
import glob
import json
import psycopg2
from pathlib import Path
from prometheus_client import start_http_server, Gauge

RAW_API_DIR = Path("../datalake/raw/api")
RAW_SOURCE2_DIR = Path("../datalake/raw/source2")
AGGREGATED_DIR = Path("../datalake/aggregated")

CONN_PARAMS = {
    "host": "localhost",
    "port": 5432,
    "dbname": "football_international",
    "user": "postgres",
    "password": "2001",
}

raw_api_count = Gauge("pipeline_raw_api_matches", "Nombre de matchs bruts API dans le Data Lake")
raw_source2_count = Gauge("pipeline_raw_source2_lines", "Nombre de lignes brutes Source 2 (dernier import)")
aggregated_count = Gauge("pipeline_aggregated_rows", "Nombre de lignes dans le dernier fichier agrégé")
clean_postgres_count = Gauge("pipeline_clean_postgres_matches", "Nombre de matchs chargés dans PostgreSQL")


def count_raw_api():
    return len(list(RAW_API_DIR.glob("*.json")))


def count_raw_source2():
    runs = sorted(RAW_SOURCE2_DIR.iterdir())
    if not runs:
        return 0
    latest = runs[-1] / "results.csv"
    if not latest.exists():
        return 0
    with open(latest, encoding="utf-8") as f:
        return sum(1 for _ in f) - 1  # -1 pour l'en-tête


def count_aggregated():
    files = sorted(AGGREGATED_DIR.glob("matches_aggregated_*.csv"))
    if not files:
        return 0
    with open(files[-1], encoding="utf-8") as f:
        return sum(1 for _ in f) - 1


def count_postgres():
    conn = psycopg2.connect(**CONN_PARAMS)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM match")
    result = cur.fetchone()[0]
    cur.close()
    conn.close()
    return result


def collect():
    raw_api_count.set(count_raw_api())
    raw_source2_count.set(count_raw_source2())
    aggregated_count.set(count_aggregated())
    clean_postgres_count.set(count_postgres())


if __name__ == "__main__":
    start_http_server(9200)
    print("Exporter démarré sur le port 9200 (/metrics)")
    while True:
        collect()
        time.sleep(30)