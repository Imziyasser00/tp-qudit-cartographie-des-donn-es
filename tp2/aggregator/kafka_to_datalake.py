import json
from pathlib import Path
from kafka import KafkaConsumer

TOPIC = "matches_live"
OUTPUT_DIR = Path("../datalake/raw/api")

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="datalake-writer",
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    consumer_timeout_ms=10000,  # s'arrête après 10s sans nouveau message
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

count = 0
for message in consumer:
    match = message.value
    match_id = match.get("id")
    out_file = OUTPUT_DIR / f"match_{match_id}.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(match, f, ensure_ascii=False)
    count += 1

print(f"{count} matchs écrits dans {OUTPUT_DIR}")