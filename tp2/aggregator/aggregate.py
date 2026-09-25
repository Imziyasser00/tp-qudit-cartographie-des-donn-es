import json
import csv
from datetime import datetime
from pathlib import Path

DATALAKE = Path("../datalake")
RAW_SOURCE2 = DATALAKE / "raw" / "source2"
OUTPUT_DIR = DATALAKE / "aggregated"


def latest_source2_run():
    """Trouve le dossier le plus récent copié par source2/reader.py"""
    runs = sorted(RAW_SOURCE2.iterdir())
    if not runs:
        raise FileNotFoundError("Aucune copie Source 2 trouvée. Lancez source2/reader.py d'abord.")
    return runs[-1]


def load_source2_matches(run_dir):
    """Charge results.csv et le convertit au format commun"""
    rows = []
    with open(run_dir / "results.csv", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append({
                "source": "csv_historique",
                "id_externe": None,
                "date_match": r["date"],
                "equipe_domicile": r["home_team"],
                "equipe_exterieur": r["away_team"],
                "score_domicile": r["home_score"],
                "score_exterieur": r["away_score"],
                "competition": r["tournament"],
                "pays": r["country"],
                "ville": r["city"],
                "statut": "FINISHED",
            })
    return rows


def load_api_matches():
    """Lit les messages Kafka déjà consommés et sauvegardés en JSON brut.
    Pour ce TP, on relit directement depuis un fichier raw/api produit par le producer
    (voir note ci-dessous)."""
    raw_api_dir = DATALAKE / "raw" / "api"
    rows = []
    if not raw_api_dir.exists():
        print("Aucune donnée API brute trouvée dans raw/api/.")
        return rows

    for file in raw_api_dir.glob("*.json"):
        with open(file, encoding="utf-8") as f:
            match = json.load(f)
        rows.append({
            "source": "api_live",
            "id_externe": match.get("id"),
            "date_match": match.get("utcDate", "")[:10],
            "equipe_domicile": match["homeTeam"]["name"],
            "equipe_exterieur": match["awayTeam"]["name"],
            "score_domicile": match["score"]["fullTime"]["home"],
            "score_exterieur": match["score"]["fullTime"]["away"],
            "competition": match["competition"]["name"],
            "pays": match["area"]["name"],
            "ville": None,
            "statut": match.get("status"),
        })
    return rows


def run():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    run_dir = latest_source2_run()
    print(f"Source 2 : lecture depuis {run_dir}")
    s2_rows = load_source2_matches(run_dir)
    print(f"Source 2 : {len(s2_rows)} matchs chargés")

    api_rows = load_api_matches()
    print(f"Source 1 (API) : {len(api_rows)} matchs chargés")

    all_rows = s2_rows + api_rows
    output_file = OUTPUT_DIR / f"matches_aggregated_{timestamp}.csv"

    fieldnames = ["source", "id_externe", "date_match", "equipe_domicile",
                  "equipe_exterieur", "score_domicile", "score_exterieur",
                  "competition", "pays", "ville", "statut"]

    with open(output_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"Agrégation terminée : {len(all_rows)} lignes -> {output_file}")


if __name__ == "__main__":
    run()